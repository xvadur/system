import {validateAuthored} from '../scenes/registry';
import {bundle} from '@remotion/bundler';
import {openBrowser,renderMedia,renderStill,selectComposition} from '@remotion/renderer';
import {createHash} from 'node:crypto';
import {execFile} from 'node:child_process';
import {promisify} from 'node:util';
import fs from 'node:fs/promises';
import path from 'node:path';
import {fileURLToPath} from 'node:url';
import {connect,createServer} from 'node:net';
import {SceneSpecSchema,TimelineSchema,hashArtifact,type Timeline} from '../schemas/index';
import {verifyAuthoredImplementation} from '../scenes/verify';
import {toRenderDocument} from './adapter';
import type {MediaAsset,RenderStyle} from './src/types';
import {createMediaCache,streamSha256,type CachedMedia} from '../runtime/media-cache.mjs';
import {withHeavyRender} from '../runtime/resource-gates.mjs';
import type {AuthoredCompositionManifest} from '../schemas/authored-composition';
import {stageAuthoredComposition,verifyAuthoredComposition} from './authored-composition';
import {compensateAuthoredAacPriming,type AuthoredAudioPriming} from './audio-priming';
const exec=promisify(execFile);
const sha=(b:Uint8Array|string)=>createHash('sha256').update(b).digest('hex');
const digest=streamSha256;

// Remotion 4.0.529 resolves public render calls before its asynchronous server
// cleanup completes. Never reuse one of those ports in this process.
const usedRendererPorts=new Set<number>();
async function bounded<T>(operation:Promise<T>,timeoutMs:number,message:string):Promise<T>{
  let timer:ReturnType<typeof setTimeout>|undefined;
  try{return await Promise.race([operation,new Promise<never>((_,reject)=>{timer=setTimeout(()=>reject(new Error(message)),timeoutMs);})]);}
  finally{if(timer)clearTimeout(timer);}
}
async function freshRendererPort():Promise<number>{
  for(let attempt=0;attempt<64;attempt++){
    const port=await new Promise<number>((resolve,reject)=>{const server=createServer();server.once('error',reject);server.listen(0,()=>{const address=server.address();if(!address||typeof address==='string'){server.close();reject(new Error('Cannot reserve renderer port'));return;}server.close(error=>error?reject(error):resolve(address.port));});});
    if(!usedRendererPorts.has(port)){usedRendererPorts.add(port);return port;}
  }
  throw new Error('Cannot allocate a fresh renderer port');
}
function portOpen(port:number,host:string):Promise<boolean>{
  return new Promise(resolve=>{const socket=connect({port,host});let settled=false;const finish=(open:boolean)=>{if(settled)return;settled=true;socket.destroy();resolve(open);};socket.once('connect',()=>finish(true));socket.once('error',()=>finish(false));socket.setTimeout(200,()=>finish(false));});
}
async function waitForPortClose(port:number):Promise<void>{
  const deadline=Date.now()+10000;
  while((await Promise.all([portOpen(port,'127.0.0.1'),portOpen(port,'::1')])).some(Boolean)){
    if(Date.now()>=deadline)throw new Error(`Remotion server on render-owned port ${port} did not close`);
    await new Promise(resolve=>setTimeout(resolve,25));
  }
}

export interface MasterContentAcceptance {packageHash:string;bundleHash:string;timelineHash:string;actor:'Adam';watched:true;listened:true;mediaHashes:string[]}
export type RenderOptions={projectRoot:string;outputDir:string;runId:string;frameRange?:[number,number];quality?:'draft'|'master';scale?:number;sourceHashes?:Record<string,string>;browserExecutable?:string;clientStyle?:RenderStyle;inspectFrames?:number[];timeoutMs?:number;frozenBundleHash?:string;masterAcceptance?:MasterContentAcceptance;authoredComposition?:AuthoredCompositionManifest};
type SourceDerivative={sourcePath:string;sourceHash:string;path:string;hash:string;startMs:number;endMs:number;ffmpegVersion:string;encoding:string[]};
export type RenderResult={path:string;outputPath:string;propsPath:string;metadataPath:string;sha256:string;frameRange:[number,number];durationInFrames:number;fps:number;width:number;height:number;scale?:number;assets:Array<{id:string;path:string;hash:string}>;sourceDerivatives?:SourceDerivative[];stills:string[];audioPriming?:AuthoredAudioPriming;implementationSnapshot?:{version:'renderer-source-snapshot.v1';implementationHash:string;files:Array<{path:string;hash:string}>};authoredComposition?:{id:string;revision:number;manifestHash:string;implementationHash:string;manifestPath:string;entryPath:string};technical:{decodeOk:boolean;durationMs:number;hasAudio:boolean}};
export function renderGeometry(t:Pick<Timeline,'width'|'height'>,options:Pick<RenderOptions,'quality'|'scale'>){
  const scale=options.scale??1;
  if(![0.25,0.5,1].includes(scale)||options.quality==='master'&&scale!==1)throw new Error('Master requires full resolution; preview scale must be 0.25, 0.5 or 1');
  return {scale,width:Math.round(t.width*scale),height:Math.round(t.height*scale)};
}
/** A package acceptance applies to this exact use/mix. It never changes the
 * library audio's unverified/not_listened record into a global approval. */
export function assertRenderAssetReadiness(t:Timeline,options:Pick<RenderOptions,'quality'|'masterAcceptance'|'frozenBundleHash'|'sourceHashes'>){
 const pending=t.assets.filter(asset=>asset.status==='preview_ready');
 for(const asset of pending)if(asset.kind!=='audio'||!asset.technical.checked||!asset.technical.decodeOk||asset.previewReadiness?.planHash!==t.sourcePlanHash||asset.previewReadiness.mediaHash!==asset.hash||asset.contentReview.status!=='unverified')throw new Error('Preview-only audio is stale or not technically ready');
 if(options.quality==='master'&&pending.length){
  const accepted=options.masterAcceptance;
  if(!accepted||!options.frozenBundleHash||accepted.bundleHash!==options.frozenBundleHash||accepted.timelineHash!==hashArtifact(t)||accepted.actor!=='Adam'||accepted.watched!==true||accepted.listened!==true||!/^[a-f0-9]{64}$/.test(accepted.packageHash)||pending.some(asset=>!accepted.mediaHashes.includes(asset.hash))||Object.values(options.sourceHashes??{}).some(hash=>!accepted.mediaHashes.includes(hash)))throw new Error('Unlistened audio master requires the matching D1 accepted package and unchanged frozen bundle');
 }
}

/** Use an installed browser only. Remotion must never start an implicit browser download. */
export async function resolveBrowserExecutable(configured?:string):Promise<string>{
  const explicit=configured??process.env.CHROME_PATH;
  const candidates=explicit?[explicit]:[
    '/Applications/Google Chrome.app/Contents/MacOS/Google Chrome',
    '/Applications/Chromium.app/Contents/MacOS/Chromium',
    '/Applications/Google Chrome Canary.app/Contents/MacOS/Google Chrome Canary',
    '/usr/bin/google-chrome','/usr/bin/chromium','/usr/bin/chromium-browser',
    ...(process.env.PROGRAMFILES?[path.join(process.env.PROGRAMFILES,'Google','Chrome','Application','chrome.exe')]:[]),
  ];
  for(const candidate of candidates){try{const stat=await fs.stat(candidate);if(!stat.isFile())continue;await fs.access(candidate,fs.constants.X_OK);return candidate;}catch{}}
  throw new Error(explicit?'Configured Chromium browser is unavailable or not executable. Check CHROME_PATH.':'No installed Chromium browser found. Set CHROME_PATH to a local executable; automatic browser downloads are disabled.');
}

async function inside(root:string,candidate:string):Promise<string>{
  const absolute=path.resolve(root,candidate),rel=path.relative(root,absolute);
  if(rel.startsWith('..')||path.isAbsolute(rel))throw new Error(`Renderer path escapes project root: ${candidate}`);
  let existing=absolute;while(true){try{const real=await fs.realpath(existing);const outside=path.relative(root,real);if(outside.startsWith('..')||path.isAbsolute(outside))throw new Error(`Renderer symlink escapes root: ${candidate}`);break;}catch(error){if((error as NodeJS.ErrnoException).code!=='ENOENT')throw error;const parent=path.dirname(existing);if(parent===existing)throw error;existing=parent;}}
  return absolute;
}
async function mediaMetadata(file:string) {
  const {stdout}=await exec('ffprobe',['-v','error','-show_streams','-show_format','-of','json',file]);
  type Stream={codec_type:string;codec_name?:string;profile?:string;pix_fmt?:string;color_transfer?:string;start_time?:string;duration?:string;width?:number;height?:number;avg_frame_rate?:string};
  const metadata=JSON.parse(stdout) as {streams?:Stream[];format?:{duration?:string;start_time?:string}};
  const video=metadata.streams?.find(stream=>stream.codec_type==='video');
  const audio=metadata.streams?.find(stream=>stream.codec_type==='audio');
  const [numerator,denominator]=(video?.avg_frame_rate??'0/1').split('/').map(Number);
  const technical={width:video?.width,height:video?.height,durationMs:Math.round(Number(metadata.format?.duration??video?.duration??0)*1000),hasAudio:!!audio,fps:denominator?numerator/denominator:undefined};
  const zeroBased=[video?.start_time,audio?.start_time,metadata.format?.start_time].every(start=>Math.abs(Number(start??0))<=0.001);
  return {video,zeroBased,technical};
}
export async function probeMedia(file:string){return (await mediaMetadata(file)).technical;}

// Main 10 SDR originals can fail in Remotion's frame proxy. Render only the
// selected source windows. Whole-second origins stay on the source and output
// frame grids used here, so the transport offset does not shift a word or cut.
const compatibilityEncoding=['-map','0:v:0','-map','0:a:0?','-c:v','libx264','-preset','veryfast','-crf','16','-maxrate','32M','-bufsize','32M','-threads','4','-pix_fmt','yuv420p','-fps_mode','passthrough','-c:a','aac','-b:a','256k','-movflags','+faststart'];
async function sourceWindow(root:string,sourcePath:string,source:{path:string;hash:string},startMs:number,endMs:number,ffmpegVersion:string,technical:Awaited<ReturnType<typeof probeMedia>>):Promise<SourceDerivative>{
  const key=sha(JSON.stringify({version:1,sourceHash:source.hash,startMs,endMs,ffmpegVersion,encoding:compatibilityEncoding}));
  const directory=await inside(root,'system/.cache/media/source-windows');
  await fs.mkdir(directory,{recursive:true});
  const output=await inside(root,path.join(directory,`${key}.mp4`));
  const receipt=await inside(root,path.join(directory,`${key}.json`));
  const temporary=await inside(root,path.join(directory,`${key}.pending.mp4`));
  const pendingReceipt=await inside(root,path.join(directory,`${key}.pending.json`));
  const result=(hash:string):SourceDerivative=>({sourcePath,sourceHash:source.hash,path:output,hash,startMs,endMs,ffmpegVersion,encoding:compatibilityEncoding});
  try {
    const cached=JSON.parse(await fs.readFile(receipt,'utf8')) as {key:string;hash:string};
    if(cached?.key===key&&/^[a-f0-9]{64}$/.test(cached.hash)&&await digest(output)===cached.hash)return result(cached.hash);
  } catch(error) {
    if((error as NodeJS.ErrnoException).code!=='ENOENT'&&!(error instanceof SyntaxError))throw error;
  }

  // The caller holds the shared heavy-render slot, including during recovery.
  // Reserve enough for the bounded window and its staging copies.
  const disk=await fs.statfs(directory);
  if(disk.bavail*disk.bsize<1024**3+15_000*(endMs-startMs))throw new Error('Insufficient disk space for the selected source compatibility window');
  await fs.rm(temporary,{force:true});
  await fs.rm(pendingReceipt,{force:true});
  try {
    await exec('ffmpeg',['-nostdin','-hide_banner','-loglevel','error','-ss',(startMs/1000).toFixed(3),'-i',source.path,'-t',((endMs-startMs)/1000).toFixed(3),...compatibilityEncoding,temporary],{timeout:600_000});
    const normalized=await mediaMetadata(temporary);
    if(normalized.video?.codec_name!=='h264'||normalized.video.pix_fmt!=='yuv420p')throw new Error('Source compatibility window is not 8-bit H.264');
    if(normalized.technical.width!==technical.width||normalized.technical.height!==technical.height||normalized.technical.hasAudio!==technical.hasAudio)throw new Error('Source compatibility window geometry or streams changed');
    if(!normalized.zeroBased||Math.abs(normalized.technical.durationMs-(endMs-startMs))>100)throw new Error('Source compatibility window does not match the selected duration and origin');
    const hash=await digest(temporary);
    await fs.chmod(temporary,0o444);
    await fs.rename(temporary,output);
    await fs.writeFile(pendingReceipt,JSON.stringify({key,hash})+'\n',{flag:'wx'});
    await fs.rename(pendingReceipt,receipt);
    return result(hash);
  } finally {
    await fs.rm(temporary,{force:true});
    await fs.rm(pendingReceipt,{force:true});
  }
}

/** Internal ranges are half-open. The renderer's frameRange is inclusive. */
export async function renderTimeline(input:Timeline,options:RenderOptions):Promise<RenderResult>{
  return withHeavyRender(options.projectRoot,()=>renderTimelineInSlot(input,options));
}
async function renderTimelineInSlot(input:Timeline,options:RenderOptions):Promise<RenderResult>{
  const t=TimelineSchema.parse(input);
  assertRenderAssetReadiness(t,options);
  const geometry=renderGeometry(t,options);
  for(const e of t.tracks.events){
    if((e.scene==='Authored')!==Boolean(e.authored))throw new Error('Invalid authored scene binding');
    if(e.authored){validateAuthored(e.authored);if(!t.productionPack?.scenes.some(s=>s.sceneId===e.authored!.sceneId&&s.version===e.authored!.version&&s.implementationHash===e.authored!.implementationHash))throw new Error('Authored scene outside pinned pack');}
  }
  if(t.tracks.events.some(e=>e.authored))await verifyAuthoredImplementation(t.tracks.events.flatMap(e=>e.authored?[e.authored]:[]));const root=await fs.realpath(options.projectRoot);
  // Immutable author CLI snapshots read real media from root, while all
  // implementation and dependency reads stay within the selected runtime.
  const implementationRoot=options.authoredComposition&&process.env.XVADUR_AUTHORED_RUNTIME_ROOT?await fs.realpath(fileURLToPath(new URL('../../',import.meta.url))):root;
  const dependencyRoot=options.authoredComposition&&process.env.XVADUR_AUTHORED_RUNTIME_ROOT?await fs.realpath(process.env.XVADUR_AUTHORED_RUNTIME_ROOT):path.join(root,'system');
  const authored=options.authoredComposition?await verifyAuthoredComposition(root,options.authoredComposition,t):undefined;
  const sourceFiles:string[]=['system/renderer/render.ts','system/renderer/adapter.ts','system/renderer/authored-composition.ts','system/renderer/audio-priming.ts','system/schemas/authored-composition.ts','system/schemas/index.ts','system/package.json','system/package-lock.json'];
  const scan=async(directory:string)=>{for(const entry of await fs.readdir(path.join(implementationRoot,directory),{withFileTypes:true})){const file=path.posix.join(directory,entry.name);if(entry.isDirectory())await scan(file);else if(/\.(?:tsx?|json)$/.test(entry.name))sourceFiles.push(file);}};
  await scan('system/renderer/src');
  const implementationFiles=await Promise.all([...new Set(sourceFiles)].sort().map(async file=>({path:file,hash:await digest(await inside(implementationRoot,file))})));
  const implementationSnapshot={version:'renderer-source-snapshot.v1' as const,implementationHash:hashArtifact(implementationFiles),files:implementationFiles};
  const range=options.frameRange??[0,t.durationInFrames];if(!Number.isInteger(range[0])||!Number.isInteger(range[1])||range[0]<0||range[1]>t.durationInFrames||range[1]<=range[0])throw new Error('Invalid half-open preview frame range');
  for(const frame of options.inspectFrames??[])if(!Number.isInteger(frame)||frame<range[0]||frame>=range[1])throw new Error('Inspect frame outside render range');
  const browserExecutable=await resolveBrowserExecutable(options.browserExecutable);
  if(!/^[a-zA-Z0-9][a-zA-Z0-9._-]*$/.test(options.runId))throw new Error('Invalid render runId');
  const outputDir=await inside(root,options.outputDir);await fs.mkdir(outputDir,{recursive:true});
  const runDir=await inside(root,path.join(outputDir,options.runId));await fs.mkdir(runDir,{recursive:false});
  const publicDir=path.join(runDir,'public');await fs.mkdir(publicDir);
  const mediaCache=await createMediaCache(root);
  const staged:Array<{id:string;path:string;hash:string}>=[];const assets:MediaAsset[]=[];
  const stage=async(id:string,source:string,cached:CachedMedia)=>{
    await mediaCache.stage(cached,path.join(publicDir,cached.filename));
    staged.push({id,path:source,hash:cached.hash});return {url:cached.filename,hash:cached.hash};
  };
  const copy=async(id:string,file:string,expected?:string)=>{
    const source=await inside(root,file);
    return stage(id,source,await mediaCache.resolve(source,expected));
  };
  for(const a of t.assets){
    if(a.status!=='preview_ready'&&(a.status!=='resolved'||!a.technical.checked||!a.technical.decodeOk||a.contentReview.status!=='checked'))throw new Error(`Unresolved or unchecked asset ${a.id}`);
    const copied=await copy(a.id,a.path,a.hash);
    if(a.kind==='graphic'){
      const savedFile=JSON.parse(await fs.readFile(path.join(publicDir,copied.url),'utf8'));
      const saved=SceneSpecSchema.parse(savedFile.scene??savedFile);
      if(JSON.stringify(saved)!==JSON.stringify(a.sceneSpec))throw new Error(`Graphic SceneSpec differs from verified asset bytes: ${a.id}`);
    }
    assets.push({...a,...copied,sceneSpec:undefined});
  }
  type SourceSpan=Timeline['tracks']['voice'][number];
  const spansBySource=new Map<string,SourceSpan[]>();
  for(const span of [...t.tracks.voice,...t.tracks.aroll]){
    const spans=spansBySource.get(span.sourcePath)??[];
    spans.push(span);
    spansBySource.set(span.sourcePath,spans);
  }
  const sourceIds=new Map<string,string>();
  const derivatives=new Map<string,SourceDerivative>();
  const remappedSpans=new Map<SourceSpan,SourceSpan>();
  const stageSource=async(file:string,cached:CachedMedia,technical:Awaited<ReturnType<typeof probeMedia>>)=>{
    if(sourceIds.has(file))return;
    const id=`source-${sha(file).slice(0,16)}`;
    const copied=await stage(id,file,cached);
    sourceIds.set(file,id);
    assets.push({id,kind:'video',path:file,...copied,technical});
  };
  for(const [file,spans] of spansBySource){
    const pinnedHash=options.sourceHashes?.[file];
    if(options.sourceHashes&&!pinnedHash)throw new Error('Missing pinned source hash for Timeline source');
    const cached=await mediaCache.resolve(await inside(root,file),pinnedHash);
    const {video,zeroBased,technical}=await mediaMetadata(cached.path);
    if(video?.codec_name!=='hevc'||video.profile!=='Main 10'||video.pix_fmt!=='yuv420p10le'){
      await stageSource(file,cached,technical);
      continue;
    }
    if(options.frozenBundleHash||options.masterAcceptance)throw new Error('Frozen render requires a pinned HEVC source compatibility derivative');
    if(!Number.isInteger(t.fps)||!Number.isInteger(technical.fps)||!zeroBased||['smpte2084','arib-std-b67'].includes(video.color_transfer??''))throw new Error('HEVC source compatibility requires SDR, zero-based streams and integer frame rates');
    const ffmpegVersion=(await exec('ffmpeg',['-version'])).stdout.split('\n')[0];
    for(const span of spans){
      if(span.sourceEndMs>technical.durationMs||span.sourceEndMs<=span.sourceStartMs)throw new Error('Source span is outside the verified HEVC media duration');
      const startMs=Math.max(0,Math.floor((span.sourceStartMs-250)/1000)*1000);
      const endMs=Math.min(technical.durationMs,Math.ceil((span.sourceEndMs+250)/1000)*1000);
      const key=JSON.stringify([file,startMs,endMs]);
      let derivative=derivatives.get(key);
      if(!derivative){
        derivative=await sourceWindow(root,file,cached,startMs,endMs,ffmpegVersion,technical);
        derivatives.set(key,derivative);
        const media=await mediaCache.resolve(derivative.path,derivative.hash);
        await stageSource(derivative.path,media,await probeMedia(media.path));
      }
      remappedSpans.set(span,{...span,sourcePath:derivative.path,sourceStartMs:span.sourceStartMs-startMs,sourceEndMs:span.sourceEndMs-startMs});
    }
  }
  const remap=(span:SourceSpan)=>remappedSpans.get(span)??span;
  const renderTimelineInput={...t,tracks:{...t.tracks,voice:t.tracks.voice.map(remap),aroll:t.tracks.aroll.map(remap)}};
  const document=toRenderDocument(renderTimelineInput,assets,sourceIds,options.clientStyle);
  const packStyle=t.productionPack?.style as (Record<string,unknown>|undefined);
  const font=packStyle?.captionFont as {family?:unknown;path?:unknown;hash?:unknown}|undefined;
  if(packStyle?.captionVariant&&!font)throw new Error('Caption variant requires its exact pinned font');
  if(font){
    if(typeof font.family!=='string'||!font.family.trim()||typeof font.path!=='string'||typeof font.hash!=='string'||!/^[a-f0-9]{64}$/.test(font.hash)||!/^\.(ttf|otf|woff2?)$/i.test(path.extname(font.path)))throw new Error('Pinned caption font descriptor is invalid');
    const stagedFont=await copy(`caption-font-${font.hash.slice(0,20)}`,font.path,font.hash);
    document.style=document.style??{};
    Object.assign(document.style,{captionFont:{family:font.family,url:stagedFont.url,hash:font.hash}});
  }
  const propsPath=path.join(runDir,'props.json');await fs.writeFile(propsPath,JSON.stringify({document},null,2));
  const authoredStage=authored?await stageAuthoredComposition(root,runDir,authored):undefined;
  const entryPoint=authoredStage?.entryPoint??fileURLToPath(new URL('./src/index.ts',import.meta.url));
  // Only this render's independent immutable clones are linked by the transient
  // bundle. Neither the bundle nor its public directory points at originals.
  const serveUrl=await bundle({entryPoint,publicDir,outDir:path.join(runDir,'bundle'),enableCaching:true,symlinkPublicDir:true,...(authoredStage?{rootDir:runDir,webpackOverride:(config:any)=>({...config,resolve:{...config.resolve,alias:{...config.resolve?.alias,'@xvadur/authoring':path.join(implementationRoot,'system/renderer/src/authoring.tsx')},modules:[...(config.resolve?.modules??['node_modules']),path.join(dependencyRoot,'node_modules')]}})}:{})});
  const inputProps={document};
  const browser=await openBrowser('chrome',{browserExecutable});
  const lifecycle:{browserId:string;browserClosed:boolean;ports:Array<{stage:string;port:number}>;cleanupErrors:string[];error?:string}={browserId:browser.id,browserClosed:false,ports:[],cleanupErrors:[]};
  const call=async<T>(stage:string,run:(port:number)=>Promise<T>):Promise<T>=>{
    const port=await freshRendererPort();lifecycle.ports.push({stage,port});let originalError:unknown;
    try{return await run(port);}catch(error){originalError=error;throw error;}
    finally{
      // Every page belongs exclusively to this render's browser. Public Remotion
      // helpers may still be finishing their non-awaited page/server cleanup.
      try{await bounded((async()=>{await Promise.allSettled((await browser.pages()).map(page=>page.close()));})(),10000,`Renderer page cleanup timed out after ${stage}`);await waitForPortClose(port);}
      catch(error){lifecycle.cleanupErrors.push((error as Error).message);if(!originalError)throw error;}
    }
  };
  try {
  const composition=await call('select',port=>selectComposition({serveUrl,id:authoredStage?.componentId??'XVADUR',inputProps,browserExecutable,puppeteerInstance:browser,port,timeoutInMilliseconds:options.timeoutMs??60000}));
  const outputPath=path.join(runDir,options.frameRange?'preview.mp4':'master.mp4');
  await call('media',port=>renderMedia({serveUrl,composition,inputProps,puppeteerInstance:browser,port,outputLocation:outputPath,codec:'h264',audioCodec:'aac',pixelFormat:'yuv420p',frameRange:[range[0],range[1]-1],crf:options.quality==='master'?18:28,x264Preset:'veryfast',concurrency:1,scale:geometry.scale,browserExecutable,timeoutInMilliseconds:options.timeoutMs??60000,overwrite:false,enforceAudioTrack:true}));
  const audioPriming=authored?await compensateAuthoredAacPriming(outputPath,dependencyRoot):undefined;
  const technical=await probeMedia(outputPath);await exec('ffmpeg',['-v','error','-i',outputPath,'-f','null','-'],{maxBuffer:8*1024*1024});
  if(technical.width!==geometry.width||technical.height!==geometry.height||Math.abs((technical.fps??0)-t.fps)>.001)throw new Error('Rendered dimensions or fps differ from Timeline and declared preview scale');
  const expectedMs=(range[1]-range[0])*1000/t.fps;if(Math.abs(technical.durationMs-expectedMs)>1000/t.fps+80)throw new Error(`Rendered duration mismatch ${technical.durationMs} vs ${expectedMs}`);
  const stills:string[]=[];
  for(const frame of options.inspectFrames??[]){if(frame<range[0]||frame>=range[1])throw new Error('Inspect frame outside render range');const file=path.join(runDir,`frame-${String(frame).padStart(6,'0')}.png`);await call(`still-${frame}`,port=>renderStill({serveUrl,composition,inputProps,puppeteerInstance:browser,port,output:file,frame,browserExecutable,imageFormat:'png',timeoutInMilliseconds:options.timeoutMs??60000}));stills.push(file);}
  const metadataPath=path.join(runDir,'render.json');
  for(const file of implementationFiles)if(await digest(path.join(implementationRoot,file.path))!==file.hash)throw new Error('Renderer source changed during the exact render');
  if(authored)await verifyAuthoredComposition(root,authored.manifest,t);
  const authoredReceipt=authored&&authoredStage?{id:authored.manifest.id,revision:authored.manifest.revision,manifestHash:authored.manifestHash,implementationHash:authored.implementationHash,manifestPath:authoredStage.manifestPath,entryPath:authored.manifest.entryPath}:undefined;
  const result:RenderResult={path:outputPath,outputPath,propsPath,metadataPath,sha256:await digest(outputPath),frameRange:range,durationInFrames:range[1]-range[0],fps:t.fps,...geometry,assets:staged,...(derivatives.size?{sourceDerivatives:[...derivatives.values()]}:{}),stills,implementationSnapshot,...(audioPriming?{audioPriming}:{}),...(authoredReceipt?{authoredComposition:authoredReceipt}:{}),technical:{decodeOk:true,durationMs:technical.durationMs,hasAudio:technical.hasAudio}};
  await fs.writeFile(metadataPath,JSON.stringify({...result,remotionVersion:'4.0.529',...(authored?{isolatedRuntime:{implementationRoot,dependencyRoot,packageHash:await digest(path.join(dependencyRoot,'package.json')),lockHash:await digest(path.join(dependencyRoot,'package-lock.json'))}}:{}),quality:options.quality??'draft',sourceTimelineHash:sha(JSON.stringify(t)),review:{listening:'not_listened',visual:'not_checked'}},null,2));
  return result;
  } catch(error){lifecycle.error=(error as Error).message;throw error;}
  finally {
    try{await bounded(browser.close({silent:true}),10000,'Renderer browser cleanup timed out');lifecycle.browserClosed=true;}
    catch(error){browser.disconnect();lifecycle.cleanupErrors.push((error as Error).message);if(!lifecycle.error)throw error;}
    finally{await fs.writeFile(path.join(runDir,'runtime.json'),JSON.stringify(lifecycle,null,2));}
  }
}
