import React,{useMemo} from 'react';
import {AbsoluteFill,Freeze,Img,Loop,OffthreadVideo,Sequence,interpolate,staticFile,useCurrentFrame,useVideoConfig} from 'remotion';
import {AudioCue,Captions,Voice} from './TimelineComposition';
import type {Box,Framing,MediaAsset,RenderDocument,RenderSpan} from './types';
import {installAuthoredFrameTransport} from './frame-transport';
installAuthoredFrameTransport();
export type {Box,Framing,MediaAsset,RenderDocument,RenderSpan,RenderWord} from './types';
export type AuthoredSceneProps={document:RenderDocument};

/** Source word IDs remain authoritative; repeated occurrences require spanId. */
export function wordFrame(document:RenderDocument,wordId:string,edge:'start'|'end'='start',spanId?:string):number{
  const words=document.captions.filter(word=>(word.id===wordId||word.wordId===wordId)&&(!spanId||word.spanId===spanId));
  if(words.length!==1)throw new Error(`Expected one word occurrence for ${wordId}${spanId?` in ${spanId}`:''}, found ${words.length}`);
  return edge==='start'?words[0].startFrame:words[0].endFrame;
}

/** All visual assets are staged by the production renderer before code runs. */
export function mediaAsset(document:RenderDocument,id:string):MediaAsset{
  const asset=document.assets.find(item=>item.id===id);
  if(!asset?.url)throw new Error(`Missing staged authored asset ${id}`);
  return asset;
}

export type AuthoredMediaProps={asset:MediaAsset;sourceStartMs?:number;sourceEndMs?:number;framing?:Framing;transparent?:boolean;muted?:boolean;gain?:number;loop?:boolean;hold?:boolean;style?:React.CSSProperties};
/** Optional primitive, not a prescribed layout. Its transparent container permits
 * mattes, masks, custom foreground/background ordering and ordinary CSS effects. */
export const Media:React.FC<AuthoredMediaProps>=({asset,sourceStartMs=0,sourceEndMs,framing,transparent=false,muted=true,gain=1,loop=false,hold=false,style:extra})=>{
  const {width,height,fps}=useVideoConfig(),frame=useCurrentFrame();
  if(!asset.url)throw new Error(`Unstaged authored media ${asset.id}`);
  const viewport:Box=framing?.viewport??{x:0,y:0,width,height};
  const sw=asset.technical?.width??width,sh=asset.technical?.height??height;
  const crop=framing?.crop??{x:0,y:0,width:sw,height:sh};
  const ratio=framing?.fit==='contain'?Math.min(viewport.width/crop.width,viewport.height/crop.height):Math.max(viewport.width/crop.width,viewport.height/crop.height);
  const value=(property:'x'|'y'|'scale',fallback:number)=>{
    const keys=(framing?.keys??[]).filter(key=>key[property]!==undefined).sort((a,b)=>a.frame-b.frame);
    const next=keys.findIndex(key=>key.frame>frame);if(next>0&&keys[next].transition==='cut')return keys[next-1][property]!;
    return keys.length>1?interpolate(frame,keys.map(key=>key.frame),keys.map(key=>key[property]!),{extrapolateLeft:'clamp',extrapolateRight:'clamp'}):keys[0]?.[property]??fallback;
  };
  const style:React.CSSProperties={position:'absolute',width:sw*ratio,height:sh*ratio,left:(viewport.width-crop.width*ratio)/2-crop.x*ratio,top:(viewport.height-crop.height*ratio)/2-crop.y*ratio,transform:`translate(${value('x',0)}px,${value('y',0)}px) scale(${value('scale',1)})`,transformOrigin:'50% 40%',...extra};
  const available=Math.max(1,Math.round(((sourceEndMs??asset.technical?.durationMs??sourceStartMs+1000)-sourceStartMs)*fps/1000));
  const video=<OffthreadVideo src={staticFile(asset.url)} trimBefore={Math.round(sourceStartMs*fps/1000)} trimAfter={sourceEndMs===undefined?undefined:Math.round(sourceEndMs*fps/1000)} transparent={transparent} muted={muted} volume={gain} style={style}/>;
  return <div style={{position:'absolute',left:viewport.x,top:viewport.y,width:viewport.width,height:viewport.height,overflow:'hidden'}}>{asset.kind==='video'?(loop?<Loop durationInFrames={available}>{video}</Loop>:hold&&frame>=available?<Freeze frame={available-1}>{video}</Freeze>:video):<Img src={staticFile(asset.url)} style={style}/>}</div>;
};

/** Original selected picture, always silent; the shell owns its one voice track. */
export const SourcePicture:React.FC<{document:RenderDocument;framing?:Framing|((span:RenderSpan)=>Framing);style?:React.CSSProperties}>=({document,framing,style})=><AbsoluteFill style={style}>
  {document.aroll.map(span=><Sequence key={span.id} from={span.startFrame} durationInFrames={span.endFrame-span.startFrame}><Media asset={mediaAsset(document,span.assetId)} sourceStartMs={span.sourceStartMs} sourceEndMs={span.sourceEndMs} framing={typeof framing==='function'?framing(span):framing??span.framing} muted/></Sequence>)}
</AbsoluteFill>;

/** The existing pinned caption implementation, with scene-owned visibility and
 * position. Call once, or conditionally per beat; never transcribe again. */
export const ExactCaptions:React.FC<{document:RenderDocument;top?:number;hidden?:boolean}>=({document,top,hidden=false})=>hidden?null:<Captions document={top===undefined?document:{...document,style:{...document.style,captionY:top}}}/>;

/** Optional reuse of the canonical SFX/music mix. The shell does NOT add this
 * automatically; authored code may use it once or design its own sound layers. */
export const TimelineSound:React.FC<{document:RenderDocument}>=({document})=><>{[...document.sfx,...document.music].map(cue=><Sequence key={cue.id} from={cue.startFrame} durationInFrames={cue.endFrame-cue.startFrame}><AudioCue cue={cue} asset={mediaAsset(document,cue.assetId)} voice={document.voice}/></Sequence>)}</>;

export function freezeAuthoredDocument(document:RenderDocument):RenderDocument{
  const cloned=structuredClone(document);
  const freeze=(value:unknown)=>{if(value&&typeof value==='object'&&!Object.isFrozen(value)){for(const child of Object.values(value))freeze(child);Object.freeze(value);}};freeze(cloned);return cloned;
}

/** Every visual belongs to Scene. Only original speech is outside its control.
 * No canonical A-roll, caption or SFX layer is silently duplicated underneath. */
export const AuthoredCompositionShell:React.FC<{document:RenderDocument;Scene:React.ComponentType<AuthoredSceneProps>}>=({document,Scene})=>{
  const locked=useMemo(()=>freezeAuthoredDocument(document),[document]);
  return <AbsoluteFill style={{background:locked.style?.background??'#101820',overflow:'hidden'}}>
    <Scene document={locked}/>
    {locked.voice.map(span=><Sequence key={`locked-voice-${span.id}`} from={span.startFrame} durationInFrames={span.endFrame-span.startFrame}><Voice span={span} asset={mediaAsset(locked,span.assetId)}/></Sequence>)}
  </AbsoluteFill>;
};
