import {SceneSpecSchema,type Timeline,type TimelineVisualEffect,type SceneSpec as CanonicalSceneSpec} from '../schemas/index';
import type {Framing,GraphicKey,GraphicNode,MediaAsset,RenderDocument,RenderEvent,RenderStyle,SceneSpec} from './src/types';
import {scaleOutputParameters,type DesignSpace} from './design-space';

type CompiledStep=Timeline['tracks']['events'][number]['steps'][number];
const numeric=(v:unknown,fallback:number)=>typeof v==='number'&&Number.isFinite(v)?v:fallback;

function graphic(spec:CanonicalSceneSpec,event:Timeline['tracks']['events'][number],assets:MediaAsset[],fps:number):SceneSpec {
  const layers=new Map(spec.layers.map(layer=>[layer.id,layer]));
  for(const layer of spec.layers){const visited=new Set<string>([layer.id]);let parent=layer.parentId;while(parent){if(visited.has(parent))throw new Error(`SceneSpec ${spec.id}: cyclic layer parent`);visited.add(parent);parent=layers.get(parent)?.parentId;}}
  const nodes=(parentId?:string):GraphicNode[]=>spec.layers.filter(l=>l.parentId===parentId).sort((a,b)=>a.zIndex-b.zIndex).map(layer=>{
    const step=event.steps[layer.revealStep];
    if(layer.revealStep>0&&!step)throw new Error(`SceneSpec ${spec.id}/${layer.id}: missing reveal step ${layer.revealStep}`);
    const reveal=layer.revealStep===0?0:Math.max(0,step!.frame-event.startFrame);
    const keys:GraphicKey[]=[{frame:0,x:layer.x,y:layer.y,scale:layer.scale,rotate:layer.rotation,opacity:layer.opacity}];
    for(const transformation of event.steps.filter((s:CompiledStep)=>s.action==='transform'&&s.params.layerId===layer.id)){
      const frame=transformation.frame-event.startFrame,duration=numeric(transformation.params.durationFrames,Math.max(1,Math.round(fps*.2)));
      const last=keys.at(-1)!;
      keys.push({...last,frame:Math.max(last.frame,frame)});
      keys.push({frame:frame+duration,x:numeric(transformation.params.x,last.x??layer.x),y:numeric(transformation.params.y,last.y??layer.y),scale:numeric(transformation.params.scale,last.scale??layer.scale),rotate:numeric(transformation.params.rotation,last.rotate??layer.rotation),opacity:numeric(transformation.params.opacity,last.opacity??layer.opacity)});
    }
    return {id:layer.id,type:layer.type==='line'?'path':layer.type,x:layer.x,y:layer.y,width:layer.width,height:layer.height,text:layer.text,assetId:assets.find(a=>(a as MediaAsset&{requestId?:string}).requestId===layer.assetRequestId)?.id,fill:layer.fill,stroke:layer.stroke,strokeWidth:layer.strokeWidth,fontSize:layer.fontSize,d:layer.path??(layer.type==='line'?`M0 0 L${layer.width??100} ${layer.height??0}`:undefined),opacity:layer.opacity,rotate:layer.rotation,scale:layer.scale,startFrame:reveal,keyframes:keys,children:layer.type==='group'?nodes(layer.id):undefined};
  });
  return {width:spec.width,height:spec.height,background:spec.background,nodes:nodes()};
}

function framing(t:Timeline,asset:MediaAsset,startFrame:number):Framing {
  const f=t.framing,sw=asset.technical?.width??t.width,sh=asset.technical?.height??t.height;
  const aspect=t.width/t.height;
  const visibleW=Math.min(sw,sh*aspect)/f.scale,visibleH=visibleW/aspect;
  const center=(requested:number,visible:number,source:number)=>visible>=source?source/2:Math.min(source-visible/2,Math.max(visible/2,requested));
  const centerX=center(f.x*sw,visibleW,sw);
  const centerY=center(f.y*sh,visibleH,sh);
  const ratio=t.width/visibleW;
  const cameraKeys=f.keyframes[0]?.frame===0?f.keyframes:[{frame:0,x:f.x,y:f.y,scale:f.scale,transition:'linear' as const},...f.keyframes];
  const base:Framing={crop:{x:centerX-visibleW/2,y:centerY-visibleH/2,width:visibleW,height:visibleH},keys:cameraKeys.map(k=>{const w=Math.min(sw,sh*aspect)/k.scale,h=w/aspect;return {frame:k.frame-startFrame,x:(centerX-center(k.x*sw,w,sw))*ratio,y:(centerY-center(k.y*sh,h,sh))*ratio,scale:k.scale/f.scale,transition:k.transition};})};
  if(f.mode==='split')base.panels=[{crop:{x:0,y:0,width:sw/2,height:sh},viewport:{x:0,y:0,width:t.width,height:t.height/2}},{crop:{x:sw/2,y:0,width:sw/2,height:sh},viewport:{x:0,y:t.height/2,width:t.width,height:t.height/2}}];
  return base;
}

function localEffect(effect:TimelineVisualEffect,startFrame:number,blurScale:number):TimelineVisualEffect {
  const local=<Key extends {frame:number}>(key:Key):Key=>({...key,frame:key.frame-startFrame});
  if(effect.kind==='transform')return {...effect,keyframes:effect.keyframes.map(local)};
  if(effect.kind==='opacity')return {...effect,keyframes:effect.keyframes.map(local)};
  return {...effect,keyframes:effect.keyframes.map(key=>({
    ...local(key),value:{...key.value,blurPx:key.value.blurPx*blurScale},
  }))};
}

/** Pure mapping; node-only staging has already replaced all local paths with static URLs. */
export function toRenderDocument(t:Timeline,assets:MediaAsset[],sourceIds:Map<string,string>,style?:RenderStyle):RenderDocument {
  const designSpace=(t.productionPack as (NonNullable<Timeline['productionPack']>&{designSpace?:DesignSpace})|undefined)?.designSpace;
  if(t.productionPack){
    const p=t.productionPack;const pinned={...p.style,captionFontSize:p.style.captionFontSize*t.width,captionY:p.style.captionY*t.height};
    if(style&&Object.entries(style).some(([k,v])=>(pinned as Record<string,unknown>)[k]!==v))throw new Error('Render style cannot override pinned ProductionPack');
    style=pinned;
  }
  const byId=new Map(assets.map(a=>[a.id,a]));
  const span=(s:Timeline['tracks']['voice'][number])=>{
    const assetId=sourceIds.get(s.sourcePath);if(!assetId)throw new Error(`Unstaged source ${s.sourcePath}`);
    return {id:s.id,assetId,startFrame:s.startFrame,endFrame:s.endFrame,sourceStartMs:s.sourceStartMs,sourceEndMs:s.sourceEndMs,framing:framing(t,byId.get(assetId)!,s.startFrame)};
  };
  const events:RenderEvent[]=t.tracks.events.map(e=>{
    const spec=e.params.sceneSpec?SceneSpecSchema.parse(e.params.sceneSpec):t.assets.find(a=>e.assetIds.includes(a.id)&&a.sceneSpec)?.sceneSpec;
    const sceneSpec=spec?graphic(spec,e,assets,t.fps):undefined;
    const params=scaleOutputParameters(e.params,{width:t.width,height:t.height},designSpace,e.scene);
    const effects=e.effects?.map(effect=>localEffect(effect,e.startFrame,designSpace?t.width/designSpace.width:1));
    return {id:e.id,scene:e.scene,...(e.authored?{authored:{...e.authored,phaseFrames:Object.fromEntries(Object.entries(e.authored.phaseFrames).map(([k,v])=>[k,v-e.startFrame])),enterFrames:Math.max(1,Math.round(t.productionPack!.motion.enterMs*t.fps/1000)),exitFrames:Math.max(1,Math.round(t.productionPack!.motion.exitMs*t.fps/1000))}}:{}),startFrame:e.startFrame,endFrame:e.endFrame,assetIds:e.assetIds,zIndex:e.zIndex,params:{...params,trim:e.trim,shortPolicy:e.shortPolicy,muted:e.muted,...(sceneSpec?{sceneSpec}:{})},steps:e.steps.map(step=>({...step,frame:step.frame-e.startFrame})),...(effects?{effects}:{})};
  });
  const speechDurationInFrames=Math.round(t.speechDurationMs*t.fps/1000);
  if(t.tail.durationMs>0&&t.tail.visual==='color')events.unshift({id:'technical-tail-background',scene:'Text',startFrame:speechDurationInFrames,endFrame:t.durationInFrames,assetIds:[],params:{background:t.tail.color??'#101820',text:''},zIndex:0});
  const audio=(cue:Timeline['tracks']['sfx'][number])=>({id:cue.id,assetId:cue.assetId,startFrame:cue.startFrame,endFrame:cue.endFrame,sourceStartMs:cue.trimStartMs,gain:cue.gain,fadeInFrames:cue.fadeInFrames,fadeOutFrames:cue.fadeOutFrames,duckGain:cue.ducking,loop:cue.loop});
  return {...(designSpace?{designSpace}:{}),width:t.width,height:t.height,fps:t.fps,durationInFrames:t.durationInFrames,speechDurationInFrames,assets,voice:t.tracks.voice.map(span),aroll:t.tracks.aroll.map(span),events:events.sort((a,b)=>(a.zIndex??10)-(b.zIndex??10)),captions:t.tracks.captions.map(w=>({...w,id:w.id})),sfx:t.tracks.sfx.map(audio),music:t.tracks.music.map(audio),style};
}
