import * as fs from 'node:fs/promises';
import path from 'node:path';
import {createHash,randomUUID} from 'node:crypto';
import {createReadStream} from 'node:fs';
import {SourceRecordSchema,TranscriptSchema,SourceObservationSchema,hashArtifact,type SourceRecord,type Transcript,type SourceObservation} from '../schemas/index.ts';
import {projectRoot,ensureInsideRoot,runProcess,copyImport,hashFile,readJson} from './io.ts';

export async function probeMedia(input:string){
 const p=await fs.realpath(input);
 const r=await runProcess('ffprobe',['-v','error','-show_streams','-show_format','-of','json',p]);
 if(r.code!==0)throw new Error(`ffprobe failed: ${r.stderr.slice(-600)}`);
 const v=JSON.parse(r.stdout),video=v.streams?.find((s:any)=>s.codec_type==='video');
 const durationMs=Math.round(Number(v.format?.duration??video?.duration)*1000);
 if(!Number.isFinite(durationMs)||durationMs<=0)throw new Error('Media has no positive duration');
 const [n,d]=String(video?.avg_frame_rate??'0/1').split('/').map(Number);
 return {durationMs,width:Number(video?.width??0),height:Number(video?.height??0),fps:n/(d||1),hasAudio:Boolean(v.streams?.some((s:any)=>s.codec_type==='audio')),streams:v.streams??[],format:v.format};
}

export async function ingestSource(opts:{source:string,clientId:string,episodeId:string,episodeDir:string,revision:number,bannedVideoIds?:string[]}):Promise<SourceRecord>{
 let local=opts.source;let originUrl:string|undefined;
 const dir=await ensureInsideRoot(path.join(opts.episodeDir,'zdroje'));await fs.mkdir(dir,{recursive:true});
 if(/^https?:\/\//i.test(opts.source)){
  const url=new URL(opts.source);if(url.protocol!=='https:')throw new Error('Remote media requires HTTPS');
  const videoId=url.hostname==='youtu.be'?url.pathname.slice(1):url.searchParams.get('v');
  if(videoId&&opts.bannedVideoIds?.includes(videoId))throw new Error('Source video is excluded by client rules');
  originUrl=url.href;const tmp=await ensureInsideRoot(path.join(opts.episodeDir,'cache',`download-${randomUUID()}`));await fs.mkdir(tmp,{recursive:true});
  const r=await runProcess('yt-dlp',['--no-playlist','--no-progress','--restrict-filenames','-f','bv*+ba/b','--merge-output-format','mp4','-o',path.join(tmp,'source.%(ext)s'),url.href],{timeoutMs:30*60*1000});
  if(r.code!==0)throw new Error(`Source download failed: ${r.stderr.slice(-500)}`);
  const entries=(await fs.readdir(tmp)).filter(x=>!x.endsWith('.part')&&!x.endsWith('.json'));
  if(entries.length!==1)throw new Error('Downloader did not return exactly one media file');local=path.join(tmp,entries[0]!);
 }
 const src=await fs.realpath(path.resolve(local));const h=createHash('sha256');for await(const b of createReadStream(src))h.update(b);const hash=h.digest('hex');
 const ext=path.extname(src).toLowerCase();if(!/^\.[a-z0-9]{1,8}$/.test(ext))throw new Error('Source extension is invalid');
 const dest=path.join(dir,hash+ext);await copyImport(src,dest);
 const info=await probeMedia(dest);if(!info.width||!info.height||!info.fps)throw new Error('Episode source must contain video');
 const decode=await runProcess('ffmpeg',['-v','error','-i',dest,'-t','1','-f','null','-']);if(decode.code!==0)throw new Error('Source decode failed');
 const {streams:_streams,format:_format,...technical}=info;
 return SourceRecordSchema.parse({schemaVersion:'1.0.0',clientId:opts.clientId,episodeId:opts.episodeId,revision:opts.revision,inputHash:hashArtifact({hash,originUrl}),id:`source-${hash.slice(0,16)}`,path:dest,hash,originUrl,...technical,importedAt:new Date().toISOString()});
}

export async function transcribeSource(opts:{source:SourceRecord,revision:number,outputDir:string,python:string,modelPath:string,language?:string,corrections?:Record<string,string>}):Promise<Transcript>{
 SourceRecordSchema.parse(opts.source);
 if(!opts.source.hasAudio)throw new Error('Local ASR requires an audio stream');
 const python=await ensureInsideRoot(opts.python,{existing:true});
 let model:string;
 try{model=await ensureInsideRoot(opts.modelPath,{existing:true});}catch{throw new Error('Local ASR model is missing; run system/bootstrap.py --download-model');}
 const manifest=await readJson<{model:string,revision:string,files:{file:string,size:number,sha256:string}[]}>(path.join(projectRoot,'system/models/manifest.json'));
 for(const f of manifest.files){
  if(path.basename(f.file)!==f.file)throw new Error('Invalid local model manifest filename');
  const p=await ensureInsideRoot(path.join(model,f.file));const stat=await fs.lstat(p).catch(()=>null);
  if(!stat?.isFile()||stat.isSymbolicLink()||stat.size!==f.size||await hashFile(p)!==f.sha256)throw new Error(`Local ASR model is missing or failed integrity check: ${f.file}`);
 }
 const out=await ensureInsideRoot(path.join(opts.outputDir,`asr-${randomUUID()}.json`));await fs.mkdir(path.dirname(out),{recursive:true});
 const result=await runProcess(python,[path.join(projectRoot,'system/python/transcribe.py'),opts.source.path,'--model',model,'--language',opts.language??'sk','--output',out],{timeoutMs:30*60*1000,maxOutputBytes:2*1024*1024,env:{HF_HUB_OFFLINE:'1',HF_HOME:path.join(projectRoot,'system/.cache/huggingface'),NUMBA_CACHE_DIR:path.join(projectRoot,'system/.cache/numba'),TORCH_HOME:path.join(projectRoot,'system/.cache/torch'),XDG_CACHE_HOME:path.join(projectRoot,'system/.cache')}});
 if(result.code!==0)throw new Error(`Local ASR failed (${result.code}): ${result.stderr.slice(-800)}`);
 const raw=await readJson<any>(out),words:Transcript['words']=[],segments:Transcript['segments']=[];let wi=0;
 for(const [i,s] of (raw.segments??[]).entries()){
  const segmentId=`t${opts.revision}-s${i}`,ids:string[]=[];
  for(const w of s.words??[]){
   const originalText=String(w.word??'').trim();const startMs=Math.max(0,Math.round(w.start*1000)),endMs=Math.min(opts.source.durationMs,Math.round(w.end*1000));
   if(!originalText||!Number.isFinite(startMs)||!Number.isFinite(endMs)||endMs<=startMs)continue;
   const id=`t${opts.revision}-w${wi++}`;ids.push(id);words.push({id,segmentId,startMs,endMs,text:opts.corrections?.[originalText]??originalText,originalText,confidence:typeof w.probability==='number'?Math.max(0,Math.min(1,w.probability)):undefined});
  }
  if(ids.length){const subset=words.filter(w=>w.segmentId===segmentId);segments.push({id:segmentId,startMs:Math.min(Math.round(s.start*1000),subset[0]!.startMs),endMs:Math.min(opts.source.durationMs,Math.max(Math.round(s.end*1000),subset.at(-1)!.endMs)),text:String(s.text??''),wordIds:ids});}
 }
 if(!words.length)throw new Error('ASR returned no timed words; no transcript was fabricated');
 return TranscriptSchema.parse({schemaVersion:'1.0.0',clientId:opts.source.clientId,episodeId:opts.source.episodeId,revision:opts.revision,inputHash:hashArtifact({source:opts.source.hash,model:manifest,language:opts.language??'sk',corrections:opts.corrections??{}}),sourceId:opts.source.id,sourcePath:opts.source.path,sourceHash:opts.source.hash,language:raw.language??opts.language??'sk',durationMs:opts.source.durationMs,segments,words,asr:{engine:'mlx-whisper',model:manifest.model,modelRevision:manifest.revision,config:{temperature:0,wordTimestamps:true,rawPath:out,corrections:opts.corrections??{}}}});
}

/** Editorial corrections retain original ASR text and alignment; no new ASR call. */
export function correctTranscript(original:Transcript,changes:Record<string,string>,revision:number):Transcript{
 const input=TranscriptSchema.parse(original);
 if(revision<=input.revision)throw new Error('Transcript correction requires a new revision');
 const ids=new Set(input.words.map(w=>w.id));
 for(const [id,text]of Object.entries(changes))if(!ids.has(id)||!text.trim())throw new Error(`Invalid transcript word correction: ${id}`);
 return TranscriptSchema.parse({...input,revision,inputHash:hashArtifact({previous:hashArtifact(input),changes}),words:input.words.map(w=>({...w,text:changes[w.id]?.trim()??w.text})),asr:{...input.asr,correctedFromRevision:input.revision,config:{...input.asr.config,wordCorrections:changes}}});
}

export async function indexSource(opts:{source:SourceRecord,revision:number,outputDir:string,intervalMs?:number,windows?:{startMs:number,endMs:number,intervalMs?:number}[],baseObservation?:SourceObservation}):Promise<SourceObservation>{
 const out=await ensureInsideRoot(opts.outputDir);await fs.mkdir(out,{recursive:true});const interval=opts.intervalMs??5000;
 if(interval<500)throw new Error('Observation interval must be at least 500ms');
 const base=opts.baseObservation?SourceObservationSchema.parse(opts.baseObservation):undefined;
 if(base&&(base.clientId!==opts.source.clientId||base.episodeId!==opts.source.episodeId||base.sourceId!==opts.source.id||base.sourceHash!==opts.source.hash))throw new Error('Base observation belongs to a different source');
 let cuts:number[];
 if(base?.shots.length){cuts=base.shots.slice(1).map(s=>s.startMs);}
 else{
  const scene=await runProcess('ffmpeg',['-hide_banner','-i',opts.source.path,'-vf',"select='gt(scene,0.3)',showinfo",'-an','-f','null','-'],{timeoutMs:10*60*1000,maxOutputBytes:8*1024*1024});
  if(scene.code!==0)throw new Error('Scene detection failed');
  cuts=[...new Set([...scene.stderr.matchAll(/pts_time:([0-9.]+)/g)].map(x=>Math.round(Number(x[1])*1000)))].filter(t=>t>0&&t<opts.source.durationMs);
 }
 const dense:number[]=[];
 for(const w of opts.windows??[]){const step=w.intervalMs??500;if(!Number.isInteger(w.startMs)||!Number.isInteger(w.endMs)||w.startMs<0||w.endMs>opts.source.durationMs||w.endMs<=w.startMs||step<100)throw new Error('Invalid targeted observation window');for(let t=w.startMs;t<w.endMs;t+=step)dense.push(t);}
 const times=[...new Set([0,...cuts,...dense,...(base?base.frames.map(f=>f.startMs):Array.from({length:Math.ceil(opts.source.durationMs/interval)},(_,i)=>i*interval))])].filter(t=>t<opts.source.durationMs).sort((a,b)=>a-b);
 const frames:SourceObservation['frames']=[];
 for(const [i,t] of times.entries()){
  const known=base?.frames.find(f=>f.startMs===t);
  if(known){if(await hashFile(known.path)!==known.hash)throw new Error(`Base observation frame bytes changed: ${known.id}`);const {description:_description,observedBy:_observer,uncertainty:_uncertainty,...technical}=known;frames.push({...technical,id:`frame-${t}`});continue;}
  const p=path.join(out,`frame-${String(t).padStart(9,'0')}.jpg`);
  const r=await runProcess('ffmpeg',['-v','error','-ss',String(t/1000),'-i',opts.source.path,'-frames:v','1','-vf','scale=640:-2','-q:v','3','-y',p]);if(r.code!==0)throw new Error(`Frame extraction failed at ${t}ms`);
  const windowEnds=(opts.windows??[]).filter(w=>w.startMs<=t&&t<w.endMs).map(w=>Math.min(w.endMs,t+(w.intervalMs??500)));
  frames.push({id:`frame-${t}`,startMs:t,endMs:Math.min(opts.source.durationMs,t+interval,times[i+1]??opts.source.durationMs,...windowEnds),path:p,hash:await hashFile(p),width:640,height:Math.round(opts.source.height/opts.source.width*640/2)*2});
 }
 const boundaries=[...new Set([0,...cuts,opts.source.durationMs])].sort((a,b)=>a-b);
 const shots=boundaries.slice(0,-1).map((t,i)=>({startMs:t,endMs:boundaries[i+1]!})).filter(x=>x.endMs>x.startMs);
 return SourceObservationSchema.parse({schemaVersion:'1.0.0',clientId:opts.source.clientId,episodeId:opts.source.episodeId,revision:opts.revision,inputHash:hashArtifact({source:opts.source.hash,interval,windows:opts.windows??[],base:base?hashArtifact(base):undefined,detector:'ffmpeg-scene-0.3-v1'}),sourceId:opts.source.id,sourceHash:opts.source.hash,mode:'technical',frames,shots,coverage:[],audioNotes:base?.audioNotes??[]});
}
