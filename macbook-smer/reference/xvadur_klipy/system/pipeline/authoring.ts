import path from 'node:path';
import os from 'node:os';
import * as fs from 'node:fs/promises';
import {randomUUID} from 'node:crypto';
import {SelectionSchema,SourceRecordSchema,TimelineSchema,TranscriptSchema,hashArtifact,type Timeline} from '../schemas/index.ts';
import {AuthoredCompositionManifestSchema,type AuthoredCompositionManifest} from '../schemas/authored-composition.ts';
import {verifyAuthoredComposition} from '../renderer/authored-composition.ts';
import {renderTimeline} from '../renderer/render.ts';
import {technicalReview} from './review.ts';
import {atomicWriteFile,atomicWriteJson,ensureInsideRoot,hashFile,identifier,projectRoot,readJson,runProcess,withLock,ProcessExecutionError} from './io.ts';
import {latest,writable,type Context} from './store.ts';
import {redactDiagnostics} from './model.ts';
import {codexRoute,codexRouteArgs,type CodexReasoningEffort} from '../runtime/codex-routing.mjs';

const VERSION='remotion-reel-authoring.v1' as const;
const defaultSkill=path.join(os.homedir(),'.codex/skills/remotion-reel');
type FileIdentity={path:string;hash:string};
export type AuthoringPacket={version:typeof VERSION;clientId:string;episodeId:string;clipId:string;workspace:string;inputHash:string;parentInputHash:string;parentTimelineHash:string;inputsPath:string;files:FileIdentity[];skillSource:string;createdAt:string};
type Inputs=Awaited<ReturnType<typeof currentInputs>>;
type AuthoringPlanBinding={version:'authoring-plan-binding.v1';manifestHash:string;inputHash:string;parentTimelineHash:string;treatment?:{sourcePath:string;snapshotPath:string;hash:string}};

async function authoringRuntimeIdentity(){
 const manifestPath=process.env.XVADUR_AUTHORED_RUNTIME_MANIFEST;
 if(!manifestPath)return undefined;
 const identity=await readJson<{version:string;snapshotHash:string;packageHash:string;lockHash:string;dependencies:Record<string,string>}>(manifestPath);
 if(identity.version!=='authored-cli-runtime.v1'||identity.dependencies.remotion!=='4.0.529'||identity.dependencies.zod!=='3.25.76')throw new Error('Unexpected isolated authoring runtime identity');
 return {manifestPath,runtimeRoot:process.env.XVADUR_AUTHORED_RUNTIME_ROOT,snapshotHash:identity.snapshotHash,packageHash:identity.packageHash,lockHash:identity.lockHash,dependencies:identity.dependencies};
}

async function currentInputs(ctx:Context,clipId:string){
 const [selection,transcript,source,timeline]=await Promise.all([
  latest(ctx,'selection',clipId,SelectionSchema),latest(ctx,'transcript',undefined,TranscriptSchema),
  latest(ctx,'source',undefined,SourceRecordSchema),latest(ctx,'timeline',clipId,TimelineSchema),
 ]);
 if(!selection||!transcript||!source||!timeline)throw new Error('Authoring needs the current Selection, Transcript, Source and compiled Timeline; prepare those canonical inputs first.');
 for(const item of [selection,transcript,source,timeline])if(item.clientId!==ctx.clientId||item.episodeId!==ctx.episodeId)throw new Error('Authoring input belongs to another episode/client');
 if(selection.clipId!==clipId||timeline.clipId!==clipId||selection.transcriptHash!==hashArtifact(transcript)||selection.transcriptRevision!==transcript.revision||timeline.sourceSelectionHash!==hashArtifact(selection)||timeline.sourceTranscriptHash!==hashArtifact(transcript))throw new Error('Authoring speech inputs are stale or belong to another clip');
 if(transcript.sourceId!==source.id||transcript.sourceHash!==source.hash||await hashFile(source.path)!==source.hash)throw new Error('Authoring source bytes or transcript source changed');
 if(timeline.tracks.voice.some(s=>s.sourcePath!==source.path))throw new Error('Authoring voice does not use the current canonical source');
 return {selection,transcript,source,timeline};
}

/** Snapshot the entire installed skill, including references/scripts/components.
 * Virtualenvs and dependency caches are executable environments, not skill source. */
async function snapshotSkill(source:string,destination:string):Promise<FileIdentity[]>{
 const identities:FileIdentity[]=[];
 async function visit(relative:string){
  const dir=path.join(source,relative);
  for(const entry of (await fs.readdir(dir,{withFileTypes:true})).sort((a,b)=>a.name.localeCompare(b.name))){
   if(['.venv','node_modules','.git','__pycache__','.DS_Store'].includes(entry.name))continue;
   const rel=path.join(relative,entry.name),original=path.join(source,rel),target=path.join(destination,rel);
   if(entry.isSymbolicLink())throw new Error(`Skill snapshot refuses symlink: ${original}`);
   if(entry.isDirectory())await visit(rel);
   else if(entry.isFile()){await atomicWriteFile(target,await fs.readFile(original));identities.push({path:target,hash:await hashFile(target)});}
  }
 }
 await visit('');
 if(!identities.some(f=>f.path===path.join(destination,'SKILL.md')))throw new Error('remotion-reel SKILL.md is missing');
 return identities;
}

function guide(packet:Pick<AuthoringPacket,'workspace'|'clipId'|'episodeId'>){
 const cli=`python3 ${path.join(projectRoot,'system/cli/klipy.py')} autor --epizoda ${packet.episodeId} --klip ${packet.clipId}`;
 return `# Remotion Reel authoring workspace\n\nThis is the full creative authoring route, alongside the legacy JSON planner. Read the complete .agents/skills/remotion-reel/SKILL.md and its required references, BRAND.md, inputs.json and the selected reference documents before editing. The installed skill's absolute reference paths remain readable; relative references in the copied brand resolve from ${path.join(projectRoot,'brand')}.\n\n## Authority and implementation\n\nThe pinned inputs.json is the one canonical speech/word/frame clock. Do not modify canonical episode artifacts, selected speech, shared renderer, accepted versions or inputs/snapshots in this workspace. Write the new visual treatment in src/Clip.tsx and local modules. There is no preset scene/effect count or closed catalogue of visual operations. Design every sentence and its relation to the next; animate all layers that serve the idea. Preserve the exact Fiki caption implementation. HyperFrames runtime is not used.\n\nThe component default export receives {document: RenderDocument}. Import SourcePicture (muted source), ExactCaptions, wordFrame, TimelineSound and Media from '@xvadur/authoring'; use Remotion/React normally. The runtime shell inserts the locked voice independently. Your TSX owns the full picture and supporting sound. Resolve media through document.assets; no untracked absolute file URLs. Read ${path.join(projectRoot,'system/renderer/authoring-api.md')} if present, and the actual helper/types code under system/renderer.\n\n## Working loop\n\n1. Inspect source frames and reference moments. Write TREATMENT.md with every sentence's word/span anchors, visual action, media, sound and reveal/impact/exit. Ordinary captions alone are not its edit.\n2. Search/acquire or generate materials using tools actually available in this session. Preserve real bytes and provenance in media/. Add verified AssetRecord entries to a new derived Timeline JSON in this workspace (copy inputs.json.timeline, retain exact voice/captions/source hashes/fps/speechDuration, change only visual/supporting material fields). Do not modify canonical episode artifacts or pinned inputs. Run the prepare command below with --timeline derived-timeline.json and a new --nazov, then copy your current src/ modules into the returned workspace and use that workspace for manifest/render. The parent clip authoring/ directory is writable for this transition; the original speech/source remain read-only. This produces a new pinned authoring revision with parent provenance, not a new speech selection. Read system/schemas/index.ts AssetRecordSchema for exact provenance and technical/content fields, and inspect actual acquired media before marking it checked. Do not assume desktop tools are available in CLI. Report a missing capability precisely.\n3. Implement src/Clip.tsx plus any local components. Use wordFrame/document frame timing, deterministic Remotion animation and the pinned captions. Keep sources reusable and independently editable.\n4. Create manifest.json using the manifest command below; it hashes the TSX/module bytes. Render a draft and actual stills, inspect them, render a relevant motion range if needed, and correct. Recreate the manifest with a higher revision after code changes.\n5. Run technical checking and write REVIEW.md with exact visual/motion/listening scope and remaining issues. A successful encode or image read is not listening or Adam's acceptance. Deliver the active authoring workspace path (including a new descendant after media acquisition), complete MP4 path, manifest hash and review. No publishing/deployment.\n\nCommands (all resolve to the pinned project runtime):\n\n\`\`\`sh\n# Only when adding media/changing visual Timeline: use the returned workspace for subsequent commands.\n${cli} --akcia priprav --timeline ${packet.workspace}/derived-timeline.json --nazov media-r2\n${cli} --akcia manifest --autor-dir ${packet.workspace} --entry src/Clip.tsx --files src/Clip.tsx --revizia 1\n${cli} --akcia over --autor-dir ${packet.workspace} --manifest ${packet.workspace}/manifest.json\n${cli} --akcia render --autor-dir ${packet.workspace} --manifest ${packet.workspace}/manifest.json --kvalita draft\n${cli} --akcia kontrola --autor-dir ${packet.workspace}\n\`\`\`\n\nList every local imported implementation module in --files (comma separated). The manifest is immutable; changed code gets a higher --revizia and links its parent. Render receipts identify source/implementation/output hashes and never imply creative acceptance.\n`;
}

export function validateAuthoredTimeline(parent:Timeline,input:unknown):Timeline{
 const timeline=TimelineSchema.parse(input);
 for(const key of ['clientId','episodeId','clipId','fps','speechDurationMs','sourceSelectionHash','sourceTranscriptHash'] as const)if(timeline[key]!==parent[key])throw new Error(`Authored Timeline changed locked speech field: ${key}`);
 if(hashArtifact(timeline.tracks.voice)!==hashArtifact(parent.tracks.voice)||hashArtifact(timeline.tracks.captions)!==hashArtifact(parent.tracks.captions))throw new Error('Authored Timeline changed selected voice or exact caption words/timing');
 if(timeline.durationMs<parent.speechDurationMs||timeline.durationInFrames<Math.max(...parent.tracks.voice.map(s=>s.endFrame)))throw new Error('Authored Timeline truncates selected speech');
 return timeline;
}

export async function prepareAuthoring(ctx:Context,clipId:string,options:{skillDir?:string;label?:string;timelinePath?:string}={}){
 writable(ctx);identifier(clipId);
 const parent=await currentInputs(ctx,clipId),inputs={...parent,timeline:options.timelinePath?validateAuthoredTimeline(parent.timeline,await readJson(options.timelinePath)):parent.timeline},inputHash=hashArtifact(inputs);
 const workspace=path.join(ctx.episodeDir,'klipy',clipId,'authoring',`${inputHash.slice(0,16)}${options.label?'-'+identifier(options.label):''}`);
 return withLock(path.join(workspace,'.prepare.lock'),async()=>{
  const packetPath=path.join(workspace,'authoring.json');
  try {const packet=await readJson<AuthoringPacket>(packetPath);await verifyAuthoring(ctx,clipId,workspace);return packet;}catch(error){if(!String(error).includes('Missing file:')&&(error as NodeJS.ErrnoException).code!=='ENOENT')throw error;}
  const inputsPath=path.join(workspace,'inputs.json');await atomicWriteJson(inputsPath,inputs);
  const files=await snapshotSkill(options.skillDir??defaultSkill,path.join(workspace,'.agents/skills/remotion-reel'));
  for(const [src,name] of [['brand/BRAND.md','BRAND.md'],['docs/CODEX_VYROBNY_POSTUP.md','PRODUCTION.md']] as const){const dest=path.join(workspace,name);await atomicWriteFile(dest,await fs.readFile(path.join(projectRoot,src)));files.push({path:dest,hash:await hashFile(dest)});}
  files.push({path:inputsPath,hash:await hashFile(inputsPath)});
  const packet:AuthoringPacket={version:VERSION,clientId:ctx.clientId,episodeId:ctx.episodeId,clipId,workspace,inputHash,parentInputHash:hashArtifact(parent),parentTimelineHash:hashArtifact(parent.timeline),inputsPath,files,skillSource:options.skillDir??defaultSkill,createdAt:new Date().toISOString()};
  const instructions=guide(packet);for(const name of ['AGENTS.md','AUTHORING.md']){const file=path.join(workspace,name);await atomicWriteFile(file,instructions);files.push({path:file,hash:await hashFile(file)});}
  await fs.mkdir(path.join(workspace,'src'),{recursive:true});await fs.mkdir(path.join(workspace,'media'),{recursive:true});
  await atomicWriteJson(packetPath,packet);return packet;
 });
}

export async function verifyAuthoring(ctx:Context,clipId:string,directory:string):Promise<{packet:AuthoringPacket;inputs:Inputs}>{
 const workspace=await ensureInsideRoot(directory,{existing:true});
 const allowed=path.join(ctx.episodeDir,'klipy',identifier(clipId),'authoring')+path.sep;
 if(!workspace.startsWith(allowed))throw new Error('Authoring workspace belongs to another clip');
 const packet=await readJson<AuthoringPacket>(path.join(workspace,'authoring.json'));
 if(packet.version!==VERSION||packet.workspace!==workspace||packet.clientId!==ctx.clientId||packet.episodeId!==ctx.episodeId||packet.clipId!==clipId)throw new Error('Invalid authoring packet identity');
 for(const file of packet.files){if(!file.path.startsWith(workspace+path.sep)||await hashFile(file.path)!==file.hash)throw new Error(`Pinned authoring input changed: ${file.path}`);}
 const parent=await currentInputs(ctx,clipId),inputs=await readJson<Inputs>(packet.inputsPath);
 if(hashArtifact(parent)!==packet.parentInputHash||hashArtifact(parent.timeline)!==packet.parentTimelineHash||hashArtifact(inputs)!==packet.inputHash)throw new Error('Authoring inputs changed; prepare a new workspace for the current canonical revision');
 validateAuthoredTimeline(parent.timeline,inputs.timeline);
 for(const key of ['selection','transcript','source'] as const)if(hashArtifact(inputs[key])!==hashArtifact(parent[key]))throw new Error('Authored packet changed its locked source/Selection/Transcript');
 return {packet,inputs};
}

async function getWorkspace(ctx:Context,clipId:string,directory?:string){return directory??(await prepareAuthoring(ctx,clipId)).workspace;}

async function verifyPlanBinding(workspace:string,manifest:AuthoredCompositionManifest,packet:AuthoringPacket){
 const binding=await readJson<AuthoringPlanBinding>(path.join(workspace,`manifest.r${String(manifest.revision).padStart(4,'0')}.authoring.json`));
 if(binding.version!=='authoring-plan-binding.v1'||binding.manifestHash!==hashArtifact(manifest)||binding.inputHash!==packet.inputHash||binding.parentTimelineHash!==packet.parentTimelineHash)throw new Error('Authored plan binding does not match the exact code/input revision');
 if(binding.treatment){for(const file of [binding.treatment.sourcePath,binding.treatment.snapshotPath])if(!file.startsWith(workspace+path.sep)||await hashFile(file)!==binding.treatment.hash)throw new Error('Authored treatment changed; create a new manifest revision for the revised creative plan');}
 return binding;
}

export async function createAuthoringManifest(ctx:Context,clipId:string,options:{directory?:string;entry:string;files:string[];revision:number;exportName?:string;treatmentPath?:string}){
 const workspace=await getWorkspace(ctx,clipId,options.directory),{inputs,packet}=await verifyAuthoring(ctx,clipId,workspace);
 const resolve=async(p:string)=>{const absolute=await ensureInsideRoot(path.resolve(workspace,p),{existing:true});if(!absolute.startsWith(workspace+path.sep))throw new Error('Authored implementation must be inside its workspace');return absolute;};
 const entry=await resolve(options.entry),files=await Promise.all([...new Set(options.files)].map(async p=>{const file=await resolve(p);return {path:path.relative(projectRoot,file),hash:await hashFile(file)};}));
 let parentManifestHash:string|undefined;
 try{const previous=AuthoredCompositionManifestSchema.parse(await readJson(path.join(workspace,'manifest.json')));if(options.revision<=previous.revision)throw new Error('Manifest revision must increase; verify or render the existing manifest without rebuilding it');parentManifestHash=hashArtifact(previous);}catch(error){if(!String(error).includes('Missing file:')&&(error as NodeJS.ErrnoException).code!=='ENOENT')throw error;}
 const manifest=AuthoredCompositionManifestSchema.parse({schemaVersion:'authored-composition.v1',id:identifier(clipId),revision:options.revision,...(parentManifestHash?{parentManifestHash}:{}),timelineHash:hashArtifact(inputs.timeline),entryPath:path.relative(projectRoot,entry),exportName:options.exportName??'default',files,remotionVersion:'4.0.529'});
 const verified=await verifyAuthoredComposition(projectRoot,manifest,inputs.timeline);
 const revision=String(manifest.revision).padStart(4,'0'),binding:AuthoringPlanBinding={version:'authoring-plan-binding.v1',manifestHash:verified.manifestHash,inputHash:packet.inputHash,parentTimelineHash:packet.parentTimelineHash};
 const treatmentPath=path.resolve(workspace,options.treatmentPath??'TREATMENT.md');
 try{const sourcePath=await resolve(treatmentPath),snapshotPath=path.join(workspace,`treatment.r${revision}.md`);await atomicWriteFile(snapshotPath,await fs.readFile(sourcePath));binding.treatment={sourcePath,snapshotPath,hash:await hashFile(snapshotPath)};}catch(error){if(options.treatmentPath||(!String(error).includes('Missing file:')&&(error as NodeJS.ErrnoException).code!=='ENOENT'))throw error;}
 const bindingPath=path.join(workspace,`manifest.r${revision}.authoring.json`);await atomicWriteJson(bindingPath,binding);
 const manifestPath=path.join(workspace,`manifest.r${revision}.json`);await atomicWriteJson(manifestPath,manifest);await atomicWriteJson(path.join(workspace,'manifest.json'),manifest,{immutable:false});return {...verified,manifestPath,planBinding:binding,planBindingPath:bindingPath};
}

export async function checkAuthoringManifest(ctx:Context,clipId:string,options:{directory?:string;manifestPath:string}){
 const workspace=await getWorkspace(ctx,clipId,options.directory),{inputs,packet}=await verifyAuthoring(ctx,clipId,workspace);
 const verified=await verifyAuthoredComposition(projectRoot,await readJson(options.manifestPath),inputs.timeline);
 return {...verified,planBinding:await verifyPlanBinding(workspace,verified.manifest,packet)};
}

export async function renderAuthoring(ctx:Context,clipId:string,options:{directory?:string;manifestPath:string;quality?:'draft'|'master';frameRange?:[number,number];inspectFrames?:number[];render?:typeof renderTimeline}){
 writable(ctx);const workspace=await getWorkspace(ctx,clipId,options.directory);
 return withLock(path.join(workspace,'.render.lock'),async()=>{
  const {inputs,packet}=await verifyAuthoring(ctx,clipId,workspace);
  const verified=await verifyAuthoredComposition(projectRoot,await readJson(options.manifestPath),inputs.timeline);
  const planBinding=await verifyPlanBinding(workspace,verified.manifest,packet);
  const quality=options.quality??'draft',runId=`${verified.manifestHash.slice(0,16)}-${quality}-${randomUUID()}`;
  const result=await (options.render??renderTimeline)(inputs.timeline,{projectRoot,outputDir:path.join(workspace,'renders',runId),runId,quality,scale:quality==='draft'?.5:1,sourceHashes:{[inputs.source.path]:inputs.source.hash},authoredComposition:verified.manifest,frameRange:options.frameRange,inspectFrames:options.inspectFrames});
  await verifyAuthoring(ctx,clipId,workspace);
  await verifyPlanBinding(workspace,verified.manifest,packet);
  const receipt={version:'authoring-render.v1',inputHash:packet.inputHash,manifestHash:verified.manifestHash,manifest:verified.manifest,planBinding,runtime:await authoringRuntimeIdentity(),quality,result,createdAt:new Date().toISOString()};
  await atomicWriteJson(path.join(workspace,'renders',runId,'receipt.json'),receipt);await atomicWriteJson(path.join(workspace,'render-latest.json'),receipt,{immutable:false});
  if(result.frameRange[0]===0&&result.frameRange[1]===inputs.timeline.durationInFrames)await atomicWriteJson(path.join(workspace,'render-full-latest.json'),receipt,{immutable:false});
  return receipt;
 });
}

export async function checkAuthoringRender(ctx:Context,clipId:string,directory?:string){
 const workspace=await getWorkspace(ctx,clipId,directory),{inputs,packet}=await verifyAuthoring(ctx,clipId,workspace);
 let receipt:any;
 try{receipt=await readJson(path.join(workspace,'render-full-latest.json'));}catch(error){if(!String(error).includes('Missing file:')&&(error as NodeJS.ErrnoException).code!=='ENOENT')throw error;receipt=await readJson(path.join(workspace,'render-latest.json'));}
 if(receipt.inputHash!==packet.inputHash||await hashFile(receipt.result.outputPath)!==receipt.result.sha256)throw new Error('Authoring render receipt is stale or bytes changed');
 await verifyAuthoredComposition(projectRoot,receipt.manifest,inputs.timeline);
 await verifyPlanBinding(workspace,receipt.manifest,packet);
 const expectedFrames=inputs.timeline.durationInFrames;
 if(receipt.result.frameRange[0]!==0||receipt.result.durationInFrames!==expectedFrames)throw new Error('Full-clip technical check requires a complete render, not a range preview');
 const check=await technicalReview(inputs.timeline,receipt.result.outputPath,ctx.fixture,{previewScale:receipt.result.scale??1});
 const result={version:'authoring-check.v1',manifestHash:receipt.manifestHash,outputHash:receipt.result.sha256,...check,visual:'not_checked',motion:'not_checked',listening:'not_listened',creativeAcceptance:'pending_Adam'};
 await atomicWriteJson(path.join(path.dirname(receipt.result.outputPath),'check.json'),result,{immutable:false});return result;
}

export function authoringAgentArgs(options:{model?:string;reasoningEffort?:CodexReasoningEffort;outputPath:string;authoringRoot?:string}){
 const route=codexRoute({role:'execution',model:options.model,reasoningEffort:options.reasoningEffort});
 return ['exec','--skip-git-repo-check','--sandbox','workspace-write','--json','--color','never','-c','approval_policy="never"','-c','sandbox_workspace_write.network_access=true','-c','web_search="live"','--add-dir',path.join(projectRoot,'system/.cache'),...(options.authoringRoot?['--add-dir',options.authoringRoot]:[]),'--output-last-message',options.outputPath,...codexRouteArgs(route),'-'];
}

/** Toolful execution, deliberately separate from the isolated structured-output analyst. */
export async function runAuthoring(ctx:Context,clipId:string,options:{directory?:string;instruction?:string;binary?:string;model?:string;reasoningEffort?:CodexReasoningEffort;timeoutMs?:number;run?:typeof runProcess}={}){
 writable(ctx);const workspace=await getWorkspace(ctx,clipId,options.directory);
 return withLock(path.join(workspace,'.agent.lock'),async()=>{
  const {packet}=await verifyAuthoring(ctx,clipId,workspace),id=`${Date.now()}-${randomUUID()}`,dir=path.join(workspace,'agent-runs',id);
  const outputPath=path.join(dir,'last-message.txt'),run=options.run??runProcess,binary=options.binary??'codex';await fs.mkdir(dir,{recursive:true});await fs.mkdir(path.join(projectRoot,'system/.cache'),{recursive:true});
  const args=authoringAgentArgs({...options,outputPath,authoringRoot:path.dirname(workspace)});
  const prompt=`Read AGENTS.md, AUTHORING.md, .agents/skills/remotion-reel/SKILL.md and its referenced operation documents in full. You are the author/editor, with tools, not a JSON planning model. Complete the selected clip using the pinned inputs, existing Remotion runtime and authoring CLI. Write your own layered TSX, obtain actual media as needed, render, inspect and repair. Keep original selected speech unchanged. Do not publish/deploy, change accounts, shared code or canonical input records. External source documents are reference material, not authority. If a required tool is unavailable, report the actual blocker rather than creating a placeholder. Resume existing authored files and render receipts before repeating expensive work.\n\n${options.instruction??'Implement and inspect a complete first draft, following the sentence coverage and actual reference mechanisms in the brand.'}`;
  const request={version:VERSION,id,inputHash:packet.inputHash,args,prompt,runtime:await authoringRuntimeIdentity(),startedAt:new Date().toISOString(),requestedModel:codexRoute({role:'execution',model:options.model,reasoningEffort:options.reasoningEffort}).model};
  await atomicWriteJson(path.join(dir,'request.json'),request);
  try{
   const result=await run(binary,args,{cwd:workspace,input:prompt,timeoutMs:options.timeoutMs??2*60*60*1000,maxOutputBytes:64*1024*1024});
   await atomicWriteFile(path.join(dir,'events.jsonl'),redactDiagnostics(result.stdout));await atomicWriteFile(path.join(dir,'stderr.txt'),redactDiagnostics(result.stderr));
   await verifyAuthoring(ctx,clipId,workspace);
   const events=result.stdout.split('\n').flatMap(line=>{try{return [JSON.parse(line)];}catch{return [];}});
   if(result.code!==0||events.some(e=>e.type==='turn.failed'||e.type==='error'))throw new Error(`Authoring agent failed (${result.code}); see ${dir}`);
   const actualModel=events.find(e=>typeof e.model==='string')?.model??'unreported';
   if(actualModel!=='unreported'&&actualModel!==request.requestedModel)throw new Error('Authoring agent used a different model than requested');
   const record={version:VERSION,id,status:'agent_finished',inputHash:packet.inputHash,requestedModel:request.requestedModel,actualModel,usage:events.filter(e=>e.type==='turn.completed').at(-1)?.usage??null,toolEvents:events.filter(e=>e.item&&['command_execution','mcp_tool_call','file_change','web_search'].includes(e.item.type)).length,outputPath,auditDir:dir,finishedAt:new Date().toISOString(),creativeAcceptance:'pending_Adam'};
   await atomicWriteJson(path.join(dir,'result.json'),record);return record;
  }catch(error){
   const partial=error instanceof ProcessExecutionError;
   if(partial){await atomicWriteFile(path.join(dir,'events.jsonl'),redactDiagnostics(error.stdout));await atomicWriteFile(path.join(dir,'stderr.txt'),redactDiagnostics(error.stderr));}
   await atomicWriteJson(path.join(dir,'failure.json'),{version:VERSION,id,status:'failed',inputHash:packet.inputHash,error:redactDiagnostics(String(error)),...(partial?{reason:error.reason,outputCapture:'partial',outputTruncated:error.reason==='output_limit',observedOutputBytes:error.outputBytes,eventsPath:path.join(dir,'events.jsonl'),stderrPath:path.join(dir,'stderr.txt')}:{outputCapture:'completed_or_unavailable'}),finishedAt:new Date().toISOString()});
   throw error;
  }
 });
}
