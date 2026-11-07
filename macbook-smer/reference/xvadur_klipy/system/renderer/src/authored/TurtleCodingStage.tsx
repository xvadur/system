import React from 'react';
import {AbsoluteFill, Img, interpolate, staticFile, useCurrentFrame, useVideoConfig} from 'remotion';
import type {JourneyStageProps} from './JourneyStage';

const clamp = {extrapolateLeft: 'clamp', extrapolateRight: 'clamp'} as const;
const points = [[225,245],[400,245],[400,70],[225,70],[225,245]];
const lengths = points.slice(1).map((p,i)=>Math.hypot(p[0]-points[i][0],p[1]-points[i][1]));
const total = lengths.reduce((a,b)=>a+b,0);
const path = points.map((p,i)=>`${i?'L':'M'} ${p[0]} ${p[1]}`).join(' ');
const commands = ['OPAKUJ 4 [','  DOPREDU 175','  VĽAVO 90',']'];
const loopCommands = ['OPAKUJ STÁLE [','  DOPREDU 15','  VĽAVO 10',']'];
const radius=15/(2*Math.sin(Math.PI/36));
const circle=Array.from({length:37},(_,i)=>[312+radius*Math.cos(i*Math.PI/18),155-radius*Math.sin(i*Math.PI/18)]);
const circlePath=circle.map((p,i)=>`${i?'L':'M'} ${p[0]} ${p[1]}`).join(' ');
const circleLengths=circle.slice(1).map((p,i)=>Math.hypot(p[0]-circle[i][0],p[1]-circle[i][1]));
const circleLength=circleLengths.reduce((a,b)=>a+b,0);
const pointOn=(pts:number[][],lens:number[],distance:number)=>{
 let index=0;
 while(index<lens.length-1&&distance>lens[index]){distance-=lens[index];index++;}
 const fraction=Math.min(1,Math.max(0,distance/lens[index]));
 return {x:pts[index][0]+(pts[index+1][0]-pts[index][0])*fraction,y:pts[index][1]+(pts[index+1][1]-pts[index][1])*fraction,angle:Math.atan2(pts[index+1][1]-pts[index][1],pts[index+1][0]-pts[index][0])*180/Math.PI};
};

/** All phases are event-local frames. The drawing and turtle share one progress value. */
export const TurtleCodingStage:React.FC<JourneyStageProps> = ({parameters,subject,phases})=>{
 const p=parameters as {layout:'turtle-coding';hook:string};
 const frame=useCurrentFrame(),{width,height,fps}=useVideoConfig(),u=width/1080;
 const at=(name:string)=>phases[name];
 const outro=at('outro')??Infinity,isOutro=frame>=outro;
 const full=isOutro||frame>=at('afterSchool')&&frame<Math.min(at('timeJump'),at('afterSchool')+2*fps);
 const opacity=isOutro?1:interpolate(frame,[at('boot'),at('boot')+6],[0,1],clamp)*interpolate(frame,[at('return')-5,at('return')],[1,0],clamp);
 const drawing=frame>=at('draw');
 const obsessive=frame>=at('obsession');
 // After the first square the program keeps running, including the whole mother/družina passage and outro.
 const squareEnd=at('draw')+2.5*fps,circleStart=squareEnd+.45*fps,lapFrames=4*fps;
 const looping=frame>=circleStart;
 const progress=drawing?interpolate(frame,[at('draw'),squareEnd],[0,1],clamp):0;
 const lapAge=Math.max(0,frame-circleStart),circleVisible=Math.min(1,lapAge/lapFrames);
 let position=pointOn(points,lengths,progress*total);
 if(frame>=squareEnd&&!looping){const mix=interpolate(frame,[squareEnd,circleStart],[0,1],clamp);position={x:225+(circle[0][0]-225)*mix,y:245+(circle[0][1]-245)*mix,angle:Math.atan2(circle[0][1]-245,circle[0][0]-225)*180/Math.PI};}
 if(looping)position=pointOn(circle,circleLengths,(lapAge%lapFrames)/lapFrames*circleLength);
 const {x,y,angle}=position;
 const instructions=looping?loopCommands:commands;
 const monitorWidth=(full?1020:600)*u;
 const monitorTop=(full?610:1100)*u;
 const elapsed=interpolate(frame,[at('timeJump'),at('waiting')],[0,4],clamp);
 const activeCommand=looping?1:progress>=1?3:drawing?1:0;
 const typed=Math.max(0,Math.floor((frame-(looping?circleStart:at('command')))/(fps*.045)));
 if(frame<at('boot')||frame>=at('return')&&frame<outro||!subject.url)return null;
 return <AbsoluteFill style={{pointerEvents:'none',opacity}}>
  {full?<AbsoluteFill style={{background:'radial-gradient(ellipse at 30% 30%,#d1aa70 0%,#806346 52%,#2b241e 100%)'}}>
   <div style={{position:'absolute',left:60*u,top:240*u,width:350*u,height:470*u,background:'#f6d68b',border:`22px solid #7c6145`,boxShadow:`0 0 ${100*u}px #ffcf7755`}}>
    <div style={{position:'absolute',left:'47%',width:'6%',height:'100%',background:'#7c6145'}}/><div style={{position:'absolute',top:'48%',height:'5%',width:'100%',background:'#7c6145'}}/>
   </div>
   {/* Empty chair silhouettes imply the class has left, without depicting a new person. */}
   {[0,1,2].map(i=><div key={i} style={{position:'absolute',left:(90+i*320)*u,top:820*u,width:200*u,height:240*u,borderRadius:'35% 35% 8% 8%',background:'#493b2b',boxShadow:`0 ${120*u}px 0 -${75*u}px #322a22`,opacity:.5}}/>)}
   <div style={{position:'absolute',top:1400*u,left:0,width,height:height-1400*u,background:'linear-gradient(#94633e,#412e20)',borderTop:`14px solid #bd8d57`}}/>
   <div style={{position:'absolute',right:85*u,top:320*u,width:220*u,height:220*u,borderRadius:'50%',border:`12px solid #694c31`,background:'#e5d6b5'}}>
    {[0,1,2,3].map(i=><div key={i} style={{position:'absolute',left:'48%',top:'5%',height:'9%',width:'4%',background:'#604d34',transformOrigin:'50% 500%',transform:`rotate(${i*90}deg)`}}/>)}
    <div style={{position:'absolute',left:'49%',top:'22%',width:'5%',height:'29%',background:'#57452f',transformOrigin:'50% 100%',transform:`rotate(${(frame-at('afterSchool'))/fps*160}deg)`}}/>
   </div>
  </AbsoluteFill>:null}
  <div aria-label={p.hook} style={{position:'absolute',width:monitorWidth,height:monitorWidth,left:(width-monitorWidth)/2,top:monitorTop,filter:`drop-shadow(0 ${15*u}px ${14*u}px #0007)`}}>
   <Img src={staticFile(subject.url)} style={{width:'100%',height:'100%'}}/>
   <div style={{position:'absolute',left:'18%',top:'11.9%',width:'62.5%',height:'44.9%',borderRadius:'6%',overflow:'hidden',background:'#031b10',color:'#9dfa9b',boxShadow:'inset 0 0 24px #000'}}>
    <svg viewBox="0 0 500 360" style={{width:'100%',height:'100%'}}>
     <defs><pattern id="turtle-grid" width="25" height="25" patternUnits="userSpaceOnUse"><path d="M25 0H0V25" fill="none" stroke="#62ba6a" strokeWidth=".7" opacity=".17"/></pattern></defs>
     <rect width="500" height="360" fill="url(#turtle-grid)"/>
     <text x="18" y="30" fill="#b6ffb4" fontFamily="monospace" fontSize="21">{frame<at('command')?'PRIPRAVENÝ':obsessive?'EŠTE RAZ!':'KORYTNAČKA'}</text>
     <path d="M16 44H484" stroke="#83d48b" opacity=".5"/>
     {frame>=at('command')?instructions.map((command,i)=><text key={command+i} x="16" y={83+i*39} fontFamily="monospace" fontSize="16" fill={i===activeCommand?'#e5ffa3':'#69b879'} opacity={i>activeCommand?.38:1}>{i===activeCommand?'›':' '} {command.slice(0,Math.max(0,typed-i*8))}</text>):<text x="18" y="85" fontSize="23" fontFamily="monospace" fill="#a5ffa9">{Math.floor(frame/(fps*.45))%2?'_':''}</text>}
     {drawing?<path d={path} pathLength={1} stroke="#b0ff8d" strokeWidth="5" opacity={looping?.38:1} fill="none" strokeDasharray={`${progress} 1`} strokeLinecap="round"/>:null}
     {looping?<path d={circlePath} pathLength={1} stroke="#b0ff8d" strokeWidth="5" fill="none" strokeDasharray={`${circleVisible} 1`} strokeLinecap="round"/>:null}
     <g transform={`translate(${x} ${y}) rotate(${angle})`}>
      <ellipse cx="0" cy="0" rx="17" ry="13" fill="#80c94c" stroke="#c1ff9c" strokeWidth="2"/>
      <path d="M-7 -11L-8 11M5 -11L5 11M-16 0H15" stroke="#376b32" strokeWidth="2"/>
      <circle cx="21" cy="0" r="8" fill="#bbef91"/><circle cx="24" cy="-3" r="1.8" fill="#082015"/>
      {[-1,1].map(side=><g key={side}><ellipse cx="-10" cy={side*15} rx="6" ry="3" fill="#9ee47a"/><ellipse cx="10" cy={side*15} rx="6" ry="3" fill="#9ee47a"/></g>)}
     </g>
     <text x="18" y="338" fill="#a5d5a0" fontSize="19" fontFamily="monospace">{frame>=at('timeJump')?`+${Math.floor(elapsed)} h`:frame>=at('afterSchool')?'PO ŠKOLE':'› SPUSTIŤ'}{frame>=at('waiting')?'  •  STÁLE PROGRAMUJEM':''}</text>
    </svg>
    <div style={{position:'absolute',inset:0,background:'repeating-linear-gradient(0deg,transparent 0px,transparent 3px,#0003 4px)',opacity:.5}}/>
   </div>
  </div>
 </AbsoluteFill>;
};
