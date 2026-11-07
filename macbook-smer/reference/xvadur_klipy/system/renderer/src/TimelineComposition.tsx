import React,{useEffect,useMemo,useState} from 'react';
import {AbsoluteFill,Freeze,Html5Audio,Sequence,cancelRender,continueRender,delayRender,interpolate,spring,staticFile,useCurrentFrame,useVideoConfig} from 'remotion';
import {ArollMedia} from './media';
import {EventScene} from './scenes';
import {VisualEffectStack} from './visual-effects';
import type {Box,MediaAsset,RenderAudio,RenderDocument,RenderSpan,RenderWord} from './types';
import {activeCaptionWord,browserCaptionMeasure,captionText,chocolateCaptionGeometry,chocolateCaptionVariant,loadCaptionFont,measuredCaptionPages,wordPulseScale} from './captions';

/** Ported punctuation/pause grouping from the old strany(), now in compiled frames. */
export function captionPages(words:RenderWord[],fps:number,max=3):Array<{startFrame:number;endFrame:number;words:RenderWord[]}>{
  const pages:Array<{startFrame:number;endFrame:number;words:RenderWord[]}>=[];let current:RenderWord[]=[];
  const close=()=>{if(current.length)pages.push({startFrame:current[0].startFrame,endFrame:current.at(-1)!.endFrame,words:current});current=[];};
  for(const word of words){if(!word.text.trim())continue;const prev=current.at(-1);if(prev&&(word.startFrame-prev.endFrame>fps*.6||current.length>=max))close();current.push(word);if(/[.,!?…:;]$/.test(word.text))close();}close();
  return pages.map((page,i)=>({...page,endFrame:Math.min(pages[i+1]?.startFrame??page.endFrame+Math.round(fps*.8),page.endFrame+Math.round(fps*.8))}));
}

/** Conservative uppercase width estimate retained from the verified original caption port. */
export function captionFontSize(words:Pick<RenderWord,'text'>[],width:number,maximum=width*.078):number{
  const characters=words.map(w=>w.text).join(' ').length;
  return Math.min(maximum,width*.88/Math.max(1,characters*.72));
}

const LegacyCaptions:React.FC<{document:RenderDocument}>=({document})=>{
  const frame=useCurrentFrame(),{width,height,fps}=useVideoConfig();
  const pages=useMemo(()=>captionPages(document.captions,fps,document.style?.captionMaxWords??3),[document.captions,document.style?.captionMaxWords,fps]);
  const page=pages.find(p=>frame>=p.startFrame&&frame<p.endFrame);if(!page||frame>=document.speechDurationInFrames)return null;
  const enter=spring({frame:frame-page.startFrame,fps,config:{damping:14,stiffness:180}});
  const size=captionFontSize(page.words,width,document.style?.captionFontSize);
  return <div style={{position:'absolute',top:document.style?.captionY??height*.76,left:width*.06,right:width*.06,textAlign:'center',fontFamily:document.style?.fontFamily??'Arial, sans-serif',fontWeight:900,fontSize:size,lineHeight:1.1,textTransform:'uppercase',transform:`scale(${interpolate(enter,[0,1],[.9,1])})`,zIndex:500}}>
    {page.words.map((word,i)=><span key={word.id} style={{color:word.emphasis||(frame>=word.startFrame&&frame<(page.words[i+1]?.startFrame??page.endFrame))?document.style?.accent??'#F2B45F':document.style?.captionColor??'#fff',WebkitTextStroke:`${width*.007}px ${document.style?.captionStroke??'#080a0c'}`,paintOrder:'stroke fill',textShadow:'0 2px 6px #000',marginRight:i<page.words.length-1?'.24em':0}}>{word.text}</span>)}
  </div>;
};

const ChocolateCaptions:React.FC<{document:RenderDocument}>=({document})=>{
  const frame=useCurrentFrame(),{width,height,fps}=useVideoConfig(),font=document.style?.captionFont;
  if(!font?.url)throw new Error('Chocolate caption variant requires its pinned staged font');
  const [handle]=useState(()=>delayRender('Loading exact caption font'));
  const [ready,setReady]=useState(false);
  useEffect(()=>{let active=true,released=false;const release=()=>{if(!released){released=true;continueRender(handle);}};
    loadCaptionFont(font,staticFile(font.url!)).then(()=>{if(active){setReady(true);release();}}).catch(error=>{if(active)cancelRender(error);});
    return()=>{active=false;release();};
  },[font.family,font.hash,font.url,handle]);
  const pages=useMemo(()=>ready?measuredCaptionPages(document.captions,fps,width,browserCaptionMeasure(font.family),document.style?.captionMaxWords??3,document.style?.captionFontSize):[],[ready,document.captions,document.style?.captionMaxWords,document.style?.captionFontSize,font.family,fps,width]);
  const page=pages.find(p=>frame>=p.startFrame&&frame<p.endFrame);if(!page||frame>=document.speechDurationInFrames)return null;
  const geometry=chocolateCaptionGeometry(width,height);
  return <div data-caption-variant={chocolateCaptionVariant} data-reserved-width={page.reservedWidth} style={{position:'absolute',left:geometry.margin,right:geometry.margin,top:document.style?.captionY??geometry.top,display:'flex',justifyContent:'center',alignItems:'center',gap:geometry.gap,fontFamily:JSON.stringify(font.family),fontWeight:900,fontSize:page.fontSize,lineHeight:geometry.lineHeight,whiteSpace:'nowrap',textShadow:`0 ${geometry.shadowY}px ${geometry.shadowBlur}px #000a`,WebkitTextStroke:`${geometry.stroke}px ${document.style?.captionStroke??'#101010'}`,paintOrder:'stroke fill',zIndex:500}}>
    {page.words.map((word,index)=><span key={word.id} data-word-slot={word.id} style={{display:'inline-flex',justifyContent:'center',alignItems:'center',flexShrink:0,width:page.slotWidths[index]}}><span data-word-id={word.id} style={{display:'inline-block',flexShrink:0,width:page.wordWidths[index],color:activeCaptionWord(word,frame)?'#FFE45C':'#fff',transform:`scale(${wordPulseScale((frame-word.startFrame)/fps*1000)})`,transformOrigin:geometry.transformOrigin}}>{captionText(word.text)}</span></span>)}
  </div>;
};
export const Captions:React.FC<{document:RenderDocument}>=({document})=>document.style?.captionVariant===chocolateCaptionVariant?<ChocolateCaptions key={`${document.style.captionFont?.hash}:${document.style.captionFont?.url}`} document={document}/>:<LegacyCaptions document={document}/>;

function OutputEvent({event,document,assets}:{event:RenderDocument['events'][number];document:RenderDocument;assets:Map<string,MediaAsset>}){
  const scene=<EventScene event={event} assets={assets} accent={document.style?.accent??'#F2B45F'}/>;
  const box=document.designSpace&&event.scene!=='Authored'&&event.params.sceneSpec?event.params.box as Box|undefined:undefined;
  const content=box?<div style={{position:'absolute',left:box.x,top:box.y,width:box.width,height:box.height,overflow:'hidden'}}>{scene}</div>:scene;
  return event.effects?.length?<VisualEffectStack effects={event.effects}>{content}</VisualEffectStack>:content;
}

export const Voice:React.FC<{span:RenderSpan;asset:MediaAsset}>=({span,asset})=>{
  const {fps}=useVideoConfig();const duration=span.endFrame-span.startFrame;
  return <Html5Audio src={staticFile(asset.url!)} trimBefore={Math.round(span.sourceStartMs*fps/1000)} trimAfter={span.sourceEndMs===undefined?undefined:Math.round(span.sourceEndMs*fps/1000)} volume={(frame)=>Math.min(1,Math.max(0,(frame+1)/2),Math.max(0,(duration-frame)/2))*(span.gain??1)}/>;
};
export const AudioCue:React.FC<{cue:RenderAudio;asset:MediaAsset;voice:RenderSpan[]}>=({cue,asset,voice})=>{
  const local=useCurrentFrame(),{fps}=useVideoConfig();const global=cue.startFrame+local,duration=cue.endFrame-cue.startFrame;
  const fade=Math.min(cue.fadeInFrames?Math.max(0,local/cue.fadeInFrames):1,cue.fadeOutFrames?Math.max(0,(duration-1-local)/cue.fadeOutFrames):1,1);
  const ramp=fps*.15;let speech=0;
  for(const span of voice){const enter=Math.min(1,Math.max(0,(global-span.startFrame+ramp)/ramp));const exit=Math.min(1,Math.max(0,(span.endFrame+ramp-global)/ramp));speech=Math.max(speech,Math.min(enter,exit));}
  const gain=(cue.gain??1)*fade*(1-speech*(1-(cue.duckGain??1)));
  return <Html5Audio src={staticFile(asset.url!)} trimBefore={Math.round((cue.sourceStartMs??0)*fps/1000)} loop={cue.loop} volume={gain}/>;
};

export const TimelineComposition:React.FC<{document:RenderDocument}>=({document})=>{
  const frame=useCurrentFrame();
  const split=document.events.find(e=>e.authored?.parameters.layout==='split'&&frame>=e.startFrame&&frame<Math.min(e.endFrame,e.startFrame+e.authored.phaseFrames.return+e.authored.exitFrames));
  const splitOpacity=split?.authored?Math.min(interpolate(frame-split.startFrame,[split.authored.phaseFrames.reveal,split.authored.phaseFrames.reveal+split.authored.enterFrames],[0,1],{extrapolateLeft:'clamp',extrapolateRight:'clamp'}),interpolate(frame-split.startFrame,[split.authored.phaseFrames.return,split.authored.phaseFrames.return+split.authored.exitFrames],[1,0],{extrapolateLeft:'clamp',extrapolateRight:'clamp'})):0;
  const assets=useMemo(()=>new Map(document.assets.map(a=>[a.id,a])),[document.assets]);
  const asset=(id:string)=>{const a=assets.get(id);if(!a?.url)throw new Error(`Timeline references unstaged asset ${id}`);return a;};
  const last=document.aroll.at(-1);
  return <AbsoluteFill style={{background:document.style?.background??'#101820',fontFamily:document.style?.fontFamily??'Arial, sans-serif',overflow:'hidden'}}>
    {document.aroll.map(span=><Sequence key={span.id} from={span.startFrame} durationInFrames={span.endFrame-span.startFrame}><ArollMedia asset={asset(span.assetId)} sourceStartMs={span.sourceStartMs} sourceEndMs={span.sourceEndMs} framing={span.framing} assets={assets}/>{split?<AbsoluteFill style={{opacity:splitOpacity}}><ArollMedia asset={asset(span.assetId)} sourceStartMs={span.sourceStartMs} sourceEndMs={span.sourceEndMs} framing={{viewport:{x:0,y:document.height*.54,width:document.width,height:document.height*.46},fit:'cover'}} assets={assets}/></AbsoluteFill>:null}</Sequence>)}
    {document.durationInFrames>document.speechDurationInFrames&&last?<Sequence from={document.speechDurationInFrames} durationInFrames={document.durationInFrames-document.speechDurationInFrames}><Freeze frame={last.endFrame-last.startFrame-1}><ArollMedia asset={asset(last.assetId)} sourceStartMs={last.sourceStartMs} sourceEndMs={last.sourceEndMs} framing={last.framing} assets={assets}/></Freeze></Sequence>:null}
    {document.events.map(event=><Sequence key={event.id} from={event.startFrame} durationInFrames={event.endFrame-event.startFrame} style={{zIndex:event.zIndex??10}}><OutputEvent event={event} document={document} assets={assets}/></Sequence>)}
    <Captions document={document}/>
    {document.voice.map(span=><Sequence key={`voice-${span.id}`} from={span.startFrame} durationInFrames={span.endFrame-span.startFrame}><Voice span={span} asset={asset(span.assetId)}/></Sequence>)}
    {[...document.sfx,...document.music].map(cue=><Sequence key={`audio-${cue.id}`} from={cue.startFrame} durationInFrames={cue.endFrame-cue.startFrame}><AudioCue cue={cue} asset={asset(cue.assetId)} voice={document.voice}/></Sequence>)}
  </AbsoluteFill>;
};
