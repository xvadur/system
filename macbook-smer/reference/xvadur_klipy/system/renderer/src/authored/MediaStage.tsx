import React from 'react';
import {AbsoluteFill,Img,OffthreadVideo,interpolate,staticFile,useCurrentFrame,useVideoConfig} from 'remotion';
import type {MediaAsset} from '../types';
export type MediaStageProps={parameters:{layout:'object'|'split'|'full'|'pip';motion:'still'|'focus'|'shake';fit:'contain'|'cover';title:string;label:string;rotation:number;sourceStartMs?:number};subject:MediaAsset;phases:Record<string,number>;accent:string;enterFrames:number;exitFrames:number};
/** Derived from the accepted tram's reveal / delayed tremor / return, now parameterized and silent. */
export const MediaStage:React.FC<MediaStageProps>=({parameters:p,subject,phases,accent,enterFrames,exitFrames})=>{
 const f=useCurrentFrame(),{width:w,height:h,fps}=useVideoConfig();
 const enter=interpolate(f,[phases.reveal,phases.reveal+enterFrames],[0,1],{extrapolateLeft:'clamp',extrapolateRight:'clamp'});
 const leave=interpolate(f,[phases.return,phases.return+exitFrames],[1,0],{extrapolateLeft:'clamp',extrapolateRight:'clamp'});
 const active=f>=phases.action,phase=(f-phases.action)*25/fps;
 const shake=active&&p.motion==='shake'?Math.sin(phase*2.4)*w*.009:0;
 const focus=p.motion==='focus'?interpolate(f,[phases.action,phases.return],[1,1.06],{extrapolateLeft:'clamp',extrapolateRight:'clamp'}):1;
 const box=p.layout==='object'?{left:w*.04,top:h*.57,width:w*.92,height:h*.23}:p.layout==='split'?{left:0,top:0,width:w,height:h*.54}:p.layout==='pip'?{left:w*.56,top:h*.12,width:w*.39,height:h*.3}:{left:0,top:0,width:w,height:h};
 const mediaStyle:React.CSSProperties={width:'100%',height:'100%',objectFit:p.fit};
 return <AbsoluteFill style={{opacity:enter*leave,pointerEvents:'none'}}>
  <div style={{position:'absolute',...box,overflow:'hidden',background:p.layout==='object'?'transparent':'#10151b',transform:`translate(${(1-enter)*-w*.08+shake}px,0) rotate(${p.rotation}deg) scale(${focus})`,transformOrigin:'50% 50%'}}>
   {subject.kind==='video'?<OffthreadVideo src={staticFile(subject.url!)} trimBefore={Math.round((p.sourceStartMs??0)*fps/1000)} muted style={mediaStyle}/>:<Img src={staticFile(subject.url!)} style={mediaStyle}/>}
   {p.label?<div style={{position:'absolute',left:w*.035,right:w*.025,bottom:h*.015,color:'#fff',fontSize:w*.024,lineHeight:1.2,textShadow:'0 2px 5px #000',background:'#10151bcc',padding:w*.012}}>{p.label}</div>:null}
  </div>
  {p.title?<div style={{position:'absolute',left:w*.06,right:w*.06,top:p.layout==='split'?h*.565:h*.10,color:accent,fontFamily:'Arial, Helvetica, sans-serif',fontWeight:900,fontSize:w*.078,lineHeight:1.03,textShadow:'0 3px 10px #000'}}>{p.title}</div>:null}
 </AbsoluteFill>;
};
