import * as fs from 'node:fs/promises';
import path from 'node:path';
import {randomUUID} from 'node:crypto';
import {z} from 'zod';
import {AssetRecordSchema, CreativeBriefSchema, EditPlanSchema, FeedbackRecordSchema, ReviewEvidenceSchema, ReviewRecordSchema, TimelineSchema, hashArtifact, type AssetRecord, type CreativeBrief, type EditPlan, type FeedbackRecord, type ReviewEvidence, type ReviewRecord, type Timeline} from '../schemas/index.ts';
import {copyImport, ensureInsideRoot, hashFile, runProcess} from './io.ts';
import {probeMedia} from './ingest.ts';
import {runModel, type ModelConfig} from './model.ts';

type Range={startMs:number;endMs:number};
export type TechnicalMetrics={masterHash:string;durationMs:number;expectedDurationMs:number;width:number;height:number;fps:number;decodeOk:boolean;hasAudio:boolean;peakDb:number|null;rmsDb:number|null;integratedLufs:number|null;truePeakDb:number|null;clippingRisk:boolean;silences:Range[];black:Range[]};
const fullRange=(t:Timeline):Range[]=>[{startMs:0,endMs:t.durationMs}];
const lastNumber=(text:string,expression:RegExp):number|null=>{const values=[...text.matchAll(expression)].map(x=>Number(x[1]));const value=values.at(-1);return value===undefined||!Number.isFinite(value)?null:value;};
function feedback(t:Timeline,type:FeedbackRecord['type'],severity:FeedbackRecord['severity'],finding:string,requestedChange:string,atMs?:number,eventId?:string):FeedbackRecord{return FeedbackRecordSchema.parse({schemaVersion:'1.0.0',clientId:t.clientId,episodeId:t.episodeId,revision:t.revision,inputHash:hashArtifact(t),id:`feedback-${randomUUID()}`,clipId:t.clipId,targetRevision:t.revision,type,severity,author:'system-review',finding,requestedChange,status:'open',atMs,eventId});}
function rangesCover(ranges:Range[],durationMs:number):boolean{let edge=0;for(const r of [...ranges].sort((a,b)=>a.startMs-b.startMs)){if(r.startMs>edge)return false;edge=Math.max(edge,r.endMs);}return edge>=durationMs;}

/** Decode and measure the entire actual candidate, without claiming audio listening. */
export async function technicalReview(input:Timeline,masterPath:string,fixture:boolean,options:{previewScale?:number}={}):Promise<{evidence:ReviewEvidence[];feedback:FeedbackRecord[];metrics:TechnicalMetrics}>{
 const t=TimelineSchema.parse(input),master=await ensureInsideRoot(masterPath,{existing:true}),masterHash=await hashFile(master),findings:FeedbackRecord[]=[];
 const scale=options.previewScale??1;if(![0.25,0.5,1].includes(scale))throw new Error('Invalid declared preview scale');
 const info=await probeMedia(master);const expected=t.durationInFrames*1000/t.fps;
 const decoded=await runProcess('ffmpeg',['-v','error','-xerror','-i',master,'-f','null','-'],{timeoutMs:30*60*1000,maxOutputBytes:2*1024*1024});
 const measurements=await runProcess('ffmpeg',['-hide_banner','-nostats','-i',master,'-vf','blackdetect=d=0.2:pix_th=0.10','-af','astats=metadata=0:reset=0,ebur128=peak=true,silencedetect=noise=-45dB:d=0.75','-f','null','-'],{timeoutMs:30*60*1000,maxOutputBytes:8*1024*1024});
 const log=measurements.stderr;
 const silenceStarts=[...log.matchAll(/silence_start:\s*([0-9.]+)/g)].map(m=>Math.round(Number(m[1])*1000));
 const silenceEnds=[...log.matchAll(/silence_end:\s*([0-9.]+)/g)].map(m=>Math.round(Number(m[1])*1000));
 const silences=silenceStarts.map((startMs,i)=>({startMs,endMs:Math.min(info.durationMs,silenceEnds[i]??info.durationMs)})).filter(r=>r.endMs>r.startMs);
 const black=[...log.matchAll(/black_start:([0-9.]+)\s+black_end:([0-9.]+)/g)].map(m=>({startMs:Math.round(Number(m[1])*1000),endMs:Math.round(Number(m[2])*1000)})).filter(r=>r.endMs>r.startMs);
 const peakDb=lastNumber(log,/Peak level dB:\s*(-?[0-9.]+)/g),rmsDb=lastNumber(log,/RMS level dB:\s*(-?[0-9.]+)/g),integratedLufs=lastNumber(log,/I:\s*(-?[0-9.]+)\s+LUFS/g),truePeakDb=lastNumber(log,/Peak:\s*(-?[0-9.]+)\s+dBFS/g);
 const metrics:TechnicalMetrics={masterHash,durationMs:info.durationMs,expectedDurationMs:expected,width:info.width,height:info.height,fps:info.fps,decodeOk:decoded.code===0,hasAudio:info.hasAudio,peakDb,rmsDb,integratedLufs,truePeakDb,clippingRisk:peakDb!==null&&peakDb>=-0.1,silences,black};
 if(!metrics.decodeOk)findings.push(feedback(t,'technical','blocking','Master sa nedekóduje v celom rozsahu.','Opraviť zdroj alebo render a znovu overiť celý nový master.'));
 if(info.width!==Math.round(t.width*scale)||info.height!==Math.round(t.height*scale)||Math.abs(info.fps-t.fps)>0.01)findings.push(feedback(t,'technical','blocking','Rozmery alebo fps kandidáta nezodpovedajú Timeline a deklarovanej mierke náhľadu.','Znovu vyrenderovať s parametrami časovej osi.'));
 if(Math.abs(info.durationMs-expected)>Math.max(80,1000/t.fps+20))findings.push(feedback(t,'technical','blocking',`Trvanie mastera ${info.durationMs} ms nezodpovedá ${Math.round(expected)} ms.`, 'Opraviť rozsah renderu; pracovný úsek nie je celý master.'));
 if(!info.hasAudio||measurements.code!==0)findings.push(feedback(t,'mix','blocking','Chýba zvuková stopa alebo technické zvukové meranie zlyhalo.','Opraviť zvukovú stopu a znovu zmerať celý master.'));
 const silentSpeech=silences.reduce((sum,r)=>sum+Math.max(0,Math.min(r.endMs,t.speechDurationMs)-r.startMs),0);
 if(silentSpeech>t.speechDurationMs*0.95)findings.push(feedback(t,'mix','blocking','Takmer celá plánovaná rečová časť je technicky tichá.','Opraviť chýbajúcu hlasovú stopu a skontrolovať celý nový mix.'));
 if(metrics.clippingRisk)findings.push(feedback(t,'mix','major',`Špička ${peakDb} dBFS môže signalizovať clipping.`, 'Skontrolovať posluchom špičky a podľa potreby znížiť mix; samotná metrika nepreukazuje počuteľné skreslenie.'));
 for(const r of silences.filter(r=>r.endMs-r.startMs>=2000&&r.startMs<t.speechDurationMs))findings.push(feedback(t,'mix','major',`Ticho v rečovej časti ${r.startMs}–${r.endMs} ms.`, 'Overiť, či ide o zamýšľanú pauzu alebo chýbajúcu reč.',r.startMs));
 for(const r of black.filter(r=>r.endMs-r.startMs>=500&&r.startMs<t.speechDurationMs))findings.push(feedback(t,'technical','major',`Čierny obraz ${r.startMs}–${r.endMs} ms.`, 'Pozrieť okno a overiť, či ide o zámer alebo výpadok vrstvy.',r.startMs));
 const evidence:ReviewEvidence[]=[ReviewEvidenceSchema.parse({id:`technical-${randomUUID()}`,kind:'technical',method:'signal-metrics',status:findings.some(f=>f.severity==='blocking')?'failed':'passed',observer:'ffmpeg-full-decode+ffprobe+astats+ebur128+blackdetect+silencedetect',ranges:fullRange(t),artifactHash:masterHash,fixture,notes:JSON.stringify(metrics)}),ReviewEvidenceSchema.parse({id:`listening-${randomUUID()}`,kind:'listening',status:'not_listened',observer:'system-review',ranges:[],artifactHash:masterHash,fixture,notes:'Technické metriky nenahrádzajú posluch. Tento krok zvuk nevypočul.'})];
 evidence.push(ReviewEvidenceSchema.parse({id:`motion-${randomUUID()}`,kind:'motion',status:'not_checked',observer:'system-review',ranges:[],artifactHash:masterHash,fixture,notes:'No verified continuous-video capability is configured. A complete MP4 and sampled stills do not establish motion/rhythm; Adam playback is required.'}));
 if(await hashFile(master)!==masterHash)throw new Error('Master changed while technical review was running');
 return {evidence,feedback:findings,metrics};
}

const VisualSchema=z.object({frames:z.array(z.object({frame:z.number().int().nonnegative(),status:z.enum(['passed','failed']),notes:z.string(),findings:z.array(z.object({type:z.enum(['word','crop','event','asset','technical']),severity:z.enum(['info','minor','major','blocking']),finding:z.string(),requestedChange:z.string(),eventId:z.string().optional()}))}))}).strict();
/** Inspect pixels decoded from the actual master at the requested still frame IDs. */
export async function visualReview(args:{timeline:Timeline;masterPath:string;stills:string[];config:ModelConfig;fixture:boolean;plan?:EditPlan;brief?:CreativeBrief}):Promise<{evidence:ReviewEvidence[];feedback:FeedbackRecord[]}>{
 const t=TimelineSchema.parse(args.timeline),master=await ensureInsideRoot(args.masterPath,{existing:true}),masterHash=await hashFile(master);
 const plan=args.plan?EditPlanSchema.parse(args.plan):undefined,brief=args.brief?CreativeBriefSchema.parse(args.brief):undefined;
 if(plan&&(plan.clientId!==t.clientId||plan.episodeId!==t.episodeId||plan.clipId!==t.clipId||hashArtifact(plan)!==t.sourcePlanHash))throw new Error('Visual review plan does not match the actual Timeline');
 if(brief&&(brief.clientId!==t.clientId||brief.episodeId!==t.episodeId||brief.clipId!==t.clipId))throw new Error('Visual review brief belongs to a different client/episode/clip');
 if(!args.stills.length)throw new Error('Visual review requires actual frame positions');
 const directory=await ensureInsideRoot(path.join(path.dirname(master),`review-${masterHash.slice(0,16)}-${randomUUID()}`));await fs.mkdir(directory,{recursive:true});
 const frames:{frame:number;path:string;hash:string}[]=[];
 for(const still of args.stills){
  await ensureInsideRoot(still,{existing:true});const frame=Number(path.basename(still).match(/frame-(\d+)/)?.[1]);
  if(!Number.isInteger(frame)||frame<0||frame>=t.durationInFrames)throw new Error(`Cannot resolve reviewed still to a full-master frame: ${still}`);
  const target=await ensureInsideRoot(path.join(directory,`frame-${String(frame).padStart(6,'0')}.png`)),temporary=path.join(directory,`.frame-${randomUUID()}.png`);
  const r=await runProcess('ffmpeg',['-v','error','-i',master,'-vf',`select='eq(n,${frame})'`,'-frames:v','1','-threads','1',temporary],{timeoutMs:10*60*1000});
  if(r.code!==0)throw new Error(`Actual master frame extraction failed: ${frame}`);
  try{await copyImport(temporary,target);}finally{await fs.rm(temporary,{force:true});}
  frames.push({frame,path:target,hash:await hashFile(target)});
 }
 const references:{referenceId:string;assetIds:string[];requestIds:string[];path:string;hash:string}[]=[];
 for(const asset of t.assets){
  if(!['image','document'].includes(asset.kind)||!/^\.(png|jpe?g)$/i.test(path.extname(asset.path)))continue;
  const same=references.find(reference=>reference.hash===asset.hash);
  if(same){if(await hashFile(asset.path)!==asset.hash)throw new Error(`Visual reference hash mismatch: ${asset.id}`);same.assetIds.push(asset.id);same.requestIds.push(asset.requestId);continue;}
  if(references.length>=8)continue;
  const file=await ensureInsideRoot(asset.path,{existing:true});if(await hashFile(file)!==asset.hash)throw new Error(`Visual reference hash mismatch: ${asset.id}`);
  references.push({referenceId:`asset-reference-${references.length+1}`,assetIds:[asset.id],requestIds:[asset.requestId],path:file,hash:asset.hash});
 }
 const assetsSummary=t.assets.map(asset=>({id:asset.id,requestId:asset.requestId,kind:asset.kind,contentReviewReason:asset.contentReview.reason,sceneSpec:asset.sceneSpec}));
 const assetRequests=plan?.assetRequests.map(request=>({id:request.id,kind:request.kind,purpose:request.purpose,description:request.description,acceptanceCriteria:request.acceptanceCriteria,allowedSubstitutions:request.allowedSubstitutions}));
 const frameContext=frames.map(({frame})=>({frame,activeEvents:t.tracks.events.filter(event=>event.startFrame<=frame&&frame<event.endFrame).map(event=>({id:event.id,relativeFrame:frame-event.startFrame,stepsAlreadyStarted:event.steps.filter(step=>step.frame<=frame).map(step=>step.id),nextSteps:event.steps.filter(step=>step.frame>frame).map(step=>({id:step.id,frame:step.frame,action:step.action}))}))}));
 const result=await runModel<z.infer<typeof VisualSchema>>({config:{...args.config,profile:'vision',allowedReadPaths:[...frames.map(f=>f.path),...references.map(r=>r.path)]},outputSchema:VisualSchema,promptVersion:'master-visual-review-v3-declared-intent-and-references',inputHash:hashArtifact({masterHash,timeline:hashArtifact(t),plan:plan?hashArtifact(plan):null,brief:brief?hashArtifact(brief):null,frames,references}),prompt:`Prezri všetky master snímky a porovnaj ich s objednaným obsahom a priloženými zdrojovými referenciami. Master snímky: ${JSON.stringify(frames)}. Referenčné asset obrázky: ${JSON.stringify(references)}. Referencie NIE SÚ snímky mastera; slúžia iba na porovnanie a nevytváraj pre ne výstupný frame záznam.
Kontroluj orezanie tváre/obrazu, čitateľnosť a prekrývanie titulkov, správne zobrazenie grafiky a materiálu voči udalostiam. Posudzuj skutočné pixely, textový brief ani plán samy nedokazujú úspešné zobrazenie. Obsahové kritériá určuje konkrétny AssetRequest description/purpose/acceptanceCriteria a explicitný brief.lockedRequirements. Nepridávaj nové obsahové požiadavky iba z názvu scény Portrait: pri objednanom illustrative/generated geometrickom alebo štylizovanom paneli nevyžaduj neobjednanú fotografiu či realistickú tvár. Over, či je prítomný požadovaný konkrétny panel a či zodpovedá referenčnému obrázku. Ak je požadovaná presná fotografia/osoba/udalosť (purpose exact alebo explicitné kritérium), naďalej skontroluj skutočné požadované médium a identitu, nie iba menovku či prázdnu kartu; neistú identitu pomenuj ako neistú. Ilustračný panel nevyhlasuj za dôkaz skutočnej osoby.
Rešpektuj fázy setup/reveal/hold/return a postupné odhaľovanie vrstiev. Event steps majú absolútne frame pozície. SceneSpec layer.revealStep je index do event.steps: 0 znamená viditeľnosť od začiatku eventu, hodnota >0 znamená až príslušný step.frame. Zámerný setup, kde je pred reveal zatiaľ iba podklad alebo text, nie je zlyhanie ani chýbajúci portrét. Posudzuj len to, čo má byť viditeľné v presnej poskytnutej snímke; neodhaduj neskorší reveal z predchádzajúceho setup frame.
Nepredstieraj súvislé prehratie, posluch ani nevidené prechody. Vráť jeden záznam pre každú konkrétnu master snímku; frame ID sú iba ${JSON.stringify(frames.map(f=>f.frame))}. Kontext presných snímok: ${JSON.stringify(frameContext)}. Objednané materiály: ${JSON.stringify(assetRequests??[])}. Brief: ${JSON.stringify(brief?{promise:brief.promise,point:brief.point,context:brief.context,enrichment:brief.enrichment,lockedRequirements:brief.lockedRequirements}:null)}. Timeline a očakávaný obsah: ${JSON.stringify({width:t.width,height:t.height,fps:t.fps,events:t.tracks.events,captions:t.tracks.captions,assets:assetsSummary})}`});
 const checked=new Set<number>();const evidence:ReviewEvidence[]=[],findings:FeedbackRecord[]=[];
 for(const item of result.value.frames){const frame=frames.find(f=>f.frame===item.frame);if(!frame||checked.has(item.frame))throw new Error('Visual model returned unknown or duplicate frame');checked.add(item.frame);
  const atMs=Math.round(item.frame*1000/t.fps),endMs=Math.min(t.durationMs,Math.max(atMs+1,Math.round((item.frame+1)*1000/t.fps)));
  const status=item.status==='failed'||item.findings.some(f=>['major','blocking'].includes(f.severity))?'failed':'passed';
  evidence.push(ReviewEvidenceSchema.parse({id:`visual-${randomUUID()}`,kind:'visual',method:'sampled-frames',status,observer:`${args.config.provider??'claude'}:${result.evidence.actualModel}`,ranges:[{startMs:atMs,endMs}],artifactHash:masterHash,fixture:args.fixture,notes:JSON.stringify({notes:item.notes,stillPath:frame.path,stillHash:frame.hash,referenceAssets:references,modelEvidence:result.evidence})}));
  for(const finding of item.findings){if(finding.eventId&&!t.tracks.events.some(e=>e.id===finding.eventId))throw new Error('Visual finding points to unknown event');findings.push(feedback(t,finding.type,finding.severity,finding.finding,finding.requestedChange,atMs,finding.eventId));}
  if(item.status==='failed'&&!item.findings.length)findings.push(feedback(t,'technical','major',item.notes,'Prezrieť a opraviť konkrétnu zlyhanú snímku.',atMs));
 }
 if(checked.size!==frames.length)throw new Error('Visual model did not inspect every requested frame');
 if(await hashFile(master)!==masterHash)throw new Error('Master changed while visual review was running');
 for(const reference of references)if(await hashFile(reference.path)!==reference.hash)throw new Error('Reference asset changed while visual review was running');
 return {evidence,feedback:findings};
}

/** Called only from an explicit human observation, never from technical metrics. */
export async function humanEvidence(args:{kind:'visual'|'motion'|'listening';status:'passed'|'failed'|'listened'|'not_listened'|'not_checked';observer:string;ranges:Range[];masterPath:string;fixture:boolean;notes:string}):Promise<ReviewEvidence>{
 if(!args.observer.trim()||!args.notes.trim())throw new Error('Human evidence requires an explicit observer and notes');
 if(args.kind==='listening'&&!['listened','not_listened','failed'].includes(args.status))throw new Error('Listening evidence must say listened, not_listened or failed explicitly');
 if(args.kind==='visual'&&args.status==='listened')throw new Error('Visual inspection cannot establish listening');
 const p=await ensureInsideRoot(args.masterPath,{existing:true}),info=await probeMedia(p);
 if(args.ranges.some(r=>r.startMs<0||r.endMs>info.durationMs+50||r.endMs<=r.startMs))throw new Error('Human observation range is outside the actual master');
 if(['passed','failed','listened'].includes(args.status)&&!args.ranges.length)throw new Error('Checked human evidence requires actual observed ranges');
 return ReviewEvidenceSchema.parse({id:`human-${randomUUID()}`,kind:args.kind,method:args.kind==='listening'?'audio-listening':'human-playback',status:args.status,observer:args.observer.trim(),ranges:args.ranges,artifactHash:await hashFile(p),fixture:args.fixture,notes:args.notes});
}

export async function acceptanceBinding(args:{plan:EditPlan;timeline:Timeline;assets:AssetRecord[];masterPath:string}):Promise<{planHash:string;assetsHash:string;timelineHash:string;masterHash:string;inputHash:string;sourceHashes:Record<string,string>}>{
 const plan=EditPlanSchema.parse(args.plan),timeline=TimelineSchema.parse(args.timeline),assets=args.assets.map(a=>AssetRecordSchema.parse(a));
 if(plan.clientId!==timeline.clientId||plan.episodeId!==timeline.episodeId||plan.clipId!==timeline.clipId)throw new Error('Acceptance client/episode/clip mismatch');
 const planHash=hashArtifact(plan),timelineHash=hashArtifact(timeline),assetsHash=hashArtifact(assets),masterHash=await hashFile(args.masterPath);
 if(timeline.sourcePlanHash!==planHash)throw new Error('Acceptance Timeline references a different plan');
 if(hashArtifact(timeline.assets)!==assetsHash)throw new Error('Acceptance asset list differs from Timeline');
 for(const a of assets){const previewUse=a.status==='preview_ready'&&a.kind==='audio'&&a.previewReadiness?.planHash===planHash&&a.previewReadiness.mediaHash===a.hash&&a.previewReadiness.listening==='not_listened';if(a.clientId!==plan.clientId||a.status!=='resolved'&&!previewUse||await hashFile(a.path)!==a.hash)throw new Error(`Acceptance asset bytes changed or unresolved: ${a.id}`);}
 const sourceHashes:Record<string,string>={};
 for(const source of new Set([...timeline.tracks.voice,...timeline.tracks.aroll].map(s=>s.sourcePath)))sourceHashes[source]=await hashFile(source);
 return {planHash,assetsHash,timelineHash,masterHash,inputHash:hashArtifact({planHash,assetsHash,timelineHash,masterHash,sourceHashes}),sourceHashes};
}

/** Rebind accepted records to current file bytes before export; no implicit approval. */
export async function verifyAcceptance(args:{review:ReviewRecord;plan:EditPlan;timeline:Timeline;assets:AssetRecord[];masterPath:string;fixture:boolean}):Promise<Awaited<ReturnType<typeof acceptanceBinding>>>{
 const review=ReviewRecordSchema.parse(args.review),t=TimelineSchema.parse(args.timeline);
 if(review.decision!=='approved')throw new Error('Export requires an approved review');
 if(review.fixture!==args.fixture||(review.acceptedBy==='fixture')!==args.fixture)throw new Error('Fixture acceptance cannot be used as a client approval');
 if(review.clientId!==t.clientId||review.episodeId!==t.episodeId||review.clipId!==t.clipId)throw new Error('Review targets a different client/episode/clip');
 const actual=await acceptanceBinding(args);
 for(const name of ['planHash','assetsHash','timelineHash','masterHash','inputHash']as const)if(review[name]!==actual[name])throw new Error(`Acceptance ${name} mismatch; changed bytes or revision require a new review`);
 if(await ensureInsideRoot(review.masterPath,{existing:true})!==await ensureInsideRoot(args.masterPath,{existing:true}))throw new Error('Acceptance master path mismatch');
 for(const e of review.evidence){if(e.artifactHash!==actual.masterHash||e.fixture!==args.fixture)throw new Error('Review evidence belongs to a different master or fixture scope');if(e.status==='failed')throw new Error('Failed review evidence must be resolved before acceptance');}
 const technical=review.evidence.filter(e=>e.kind==='technical'&&e.status==='passed').flatMap(e=>e.ranges);
 if(!rangesCover(technical,t.durationMs))throw new Error('Acceptance requires technical evidence for the full actual master');
 if(!review.evidence.some(e=>e.kind==='visual'&&e.status==='passed'&&e.ranges.length))throw new Error('Acceptance requires actual visual inspection evidence');
 if(review.protocol==='p5.v1'){
  const played=review.evidence.filter(e=>e.kind==='motion'&&e.status==='passed'&&['human-playback','continuous-video'].includes(e.method??'')).flatMap(e=>e.ranges);
  if(!rangesCover(played,t.durationMs))throw new Error('Acceptance requires continuous playback of the full master; sampled frames do not establish motion or rhythm');
 }
 const listened=review.evidence.filter(e=>e.kind==='listening'&&e.status==='listened').flatMap(e=>e.ranges);
 if(!rangesCover(listened,t.durationMs)){
  const waived=args.fixture&&review.acceptedBy==='fixture'&&review.notes.includes('[fixture-listening-waiver]')&&review.evidence.some(e=>e.kind==='listening'&&e.status==='not_listened');
  if(!waived)throw new Error('Acceptance requires actual listening of the full master; not_listened is not listening');
 }
 return actual;
}
