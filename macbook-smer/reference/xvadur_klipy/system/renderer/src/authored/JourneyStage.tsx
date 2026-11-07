import React from 'react';
import {AbsoluteFill,Easing,Img,interpolate,staticFile,useCurrentFrame,useVideoConfig} from 'remotion';
import type {MediaStageProps} from './MediaStage';
import {JourneyParameters} from '../../../scenes/journey-parameters';

export type JourneyStageProps=Omit<MediaStageProps,'parameters'>&{parameters:Record<string,unknown>};
/** A held announcement, an anchored journey, then arrival. One compiler clock. */
export const JourneyStage:React.FC<JourneyStageProps>=({parameters,subject,phases,accent,enterFrames,exitFrames})=>{
 const p=JourneyParameters.parse(parameters),frame=useCurrentFrame(),{width:w,height:h}=useVideoConfig();
 const enter=interpolate(frame,[phases.reveal,phases.reveal+enterFrames],[0,1],{extrapolateLeft:'clamp',extrapolateRight:'clamp'});
 const leave=interpolate(frame,[phases.return,phases.return+exitFrames],[1,0],{extrapolateLeft:'clamp',extrapolateRight:'clamp'});
 const travel=interpolate(frame,[phases.action,Math.max(phases.action+1,phases.arrive)],[0,1],{extrapolateLeft:'clamp',extrapolateRight:'clamp',easing:Easing.inOut(Easing.cubic)});
 const x=(p.direction==='left-to-right'?travel:1-travel),arrived=frame>=phases.arrive,dark=p.background==='night';
 return <AbsoluteFill style={{opacity:enter*leave,pointerEvents:'none'}}>
  <div style={{position:'absolute',left:w*.035,right:w*.035,top:h*.10,height:h*.49,borderRadius:w*.035,overflow:'hidden',background:dark?'#122331':'#eee8dc',color:dark?'#f8f3e8':'#182832',fontFamily:'Arial, Helvetica, sans-serif',boxShadow:'0 10px 35px #0005'}}>
   <div style={{position:'absolute',left:w*.05,right:w*.05,top:h*.026,fontSize:w*.052,fontWeight:800,lineHeight:1.12}}>{arrived?p.afterLabel:p.beforeLabel}</div>
   <svg viewBox="0 0 1000 200" style={{position:'absolute',left:'8%',bottom:'18%',width:'84%',height:'22%',overflow:'visible'}}>
    <path d="M 40 116 C 280 116 720 116 960 116" stroke={dark?'#52616b':'#b2aca1'} strokeWidth="8" fill="none"/>
    <path d="M 40 133 L 960 133" stroke={dark?'#52616b':'#b2aca1'} strokeWidth="4" fill="none"/>
    <path d={p.direction==='left-to-right'?'M 40 116 L 960 116':'M 960 116 L 40 116'} pathLength="1" stroke={accent} strokeWidth="9" strokeDasharray={`${travel} 1`} fill="none"/>
    {[40,960].map(v=><g key={v}><circle cx={v} cy="116" r="23" fill={dark?'#122331':'#eee8dc'} stroke={accent} strokeWidth="7"/><circle cx={v} cy="116" r="7" fill={accent}/></g>)}
   </svg>
   <Img src={staticFile(subject.url!)} style={{position:'absolute',width:w*.47*p.subjectScale,height:h*.24*p.subjectScale,objectFit:'contain',left:w*(.015+.40*x),bottom:h*.105,filter:'drop-shadow(0 12px 9px #0004)',transform:`translateY(${(1-enter)*h*.02}px)`}}/>
   <div style={{position:'absolute',left:w*.05,right:w*.05,bottom:h*.025,display:'flex',justifyContent:'space-between',gap:w*.08,fontSize:w*.037,fontWeight:700,lineHeight:1.12}}><span style={{maxWidth:'44%'}}>{p.fromLabel}</span><span style={{maxWidth:'44%',textAlign:'right',color:arrived?accent:undefined}}>{p.toLabel}</span></div>
  </div>
 </AbsoluteFill>;
};
