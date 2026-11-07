import React from 'react';
import {AbsoluteFill,Img,interpolate,spring,staticFile,useCurrentFrame,useVideoConfig} from 'remotion';
import type {JourneyStageProps} from './JourneyStage';

const clamp={extrapolateLeft:'clamp',extrapolateRight:'clamp'} as const;
/** One tangible paper travels from a foreign video's comment slot to the speaker's own space. */
export const PhonePaperStage:React.FC<JourneyStageProps>=({parameters,subject,phases})=>{
 const frame=useCurrentFrame(),{width,fps}=useVideoConfig(),u=width/1080;
 const at=(name:string)=>phases[name];
 if(frame<at('boot')||frame>=at('return')||frame>=at('cleanMeaning')&&frame<at('audience')||!subject.url)return null;
 const enter=interpolate(frame,[at('boot'),at('boot')+5],[0,1],clamp),leave=interpolate(frame,[at('return')-3,at('return')],[1,0],clamp);
 const paperIn=interpolate(frame,[at('foreignVideo'),at('foreignVideo')+5],[0,1],clamp);
 const insert=interpolate(frame,[at('comment'),at('comment')+.55*fps],[0,1],clamp);
 const travel=spring({frame:frame-at('ownStory'),fps,durationInFrames:Math.round(.48*fps),config:{damping:20,stiffness:230,mass:.6}});
 const attached=frame>=at('ownStory'),audience=frame>=at('audience');
 const boardIn=interpolate(frame,[at('ownStory'),at('ownStory')+6],[0,1],clamp);
 const x=120+(620-120)*travel,y=180+65*insert+(170-245)*travel;
 const paperWidth=88+72*travel,paperHeight=76+104*travel;
 const angle=(1-travel)*(-6+Math.sin(frame/fps*2.8)*2)+travel*2;
 const writing=interpolate(frame,[at('opinion'),at('opinion')+.42*fps],[0,1],clamp);
 const pin=spring({frame:frame-at('ownStory')-Math.round(.38*fps),fps,config:{damping:12,stiffness:290,mass:.4}});
 const playhead=(frame%(fps*2.6))/(fps*2.6);
 return <AbsoluteFill style={{pointerEvents:'none'}}>
  <div aria-label={String(parameters.hook)} style={{position:'absolute',left:80*u,top:1120*u,width:920*u,height:310*u,overflow:'hidden',opacity:enter*leave}}>
   <Img src={staticFile(subject.url)} style={{position:'absolute',left:32*u,top:5*u,width:176*u,height:300*u,objectFit:'contain',filter:`drop-shadow(0 ${6*u}px ${5*u}px #0008)`}}/>
   <svg viewBox="0 0 920 310" width="100%" height="100%" style={{position:'absolute',inset:0,overflow:'hidden',fontFamily:'Arial Black,Arial,sans-serif',fontWeight:900}}>
    <defs>
     <linearGradient id="paper-board-wood" x2="0" y2="1"><stop stopColor="#cda568"/><stop offset=".5" stopColor="#80603b"/><stop offset="1" stopColor="#513c27"/></linearGradient>
     <linearGradient id="travel-paper" x2=".2" y2="1"><stop stopColor="#fff0c6"/><stop offset="1" stopColor="#d4b783"/></linearGradient>
     <pattern id="physical-cork-grain" width="41" height="37" patternUnits="userSpaceOnUse"><rect width="41" height="37" fill="#997b52"/>{Array.from({length:14},(_,i)=><ellipse key={i} cx={(i*17+3)%41} cy={(i*11+4)%37} rx={i%3+1} ry={i%2+1} fill={i%2?'#59452f':'#e0bf85'} opacity={i%2?.25:.3}/>)}</pattern>
     <filter id="paper-object-shadow" x="-40%" y="-40%" width="180%" height="200%"><feDropShadow dx="0" dy="5" stdDeviation="4" floodColor="#000" floodOpacity=".6"/></filter>
     <clipPath id="foreign-paper-slot"><rect x="0" y="0" width="330" height="248"/></clipPath>
    </defs>
    {/* A deliberately abstract video surface, with no impersonated account or analytics UI. */}
    <rect x="58" y="36" width="123" height="112" rx="9" fill="#26383f"/>
    <path d="M108 65L108 112L144 88Z" fill="#f0deb3" opacity={.75+Math.sin(frame/fps*3)*.13}/>
    <rect x="67" y="134" width="105" height="4" rx="2" fill="#53626a"/>
    <rect x="67" y="134" width={Math.max(2,105*playhead)} height="4" rx="2" fill="#ffe45c"/>
    <text x="120" y="163" textAnchor="middle" fontSize="12" fill="#eee6d2">CUDZIE VIDEO</text>
    <g opacity={boardIn} filter="url(#paper-object-shadow)">
     <rect x="350" y="19" width="546" height="281" rx="9" fill="url(#paper-board-wood)"/>
     <rect x="364" y="32" width="518" height="254" rx="4" fill="url(#physical-cork-grain)" stroke="#5c4227" strokeWidth="3"/>
     {[0,1,2,3,4,5,6].map(i=><path key={i} d={`M371 ${46+i*34}Q620 ${30+i*34} 875 ${49+i*34}`} stroke="#5d4931" opacity=".16" fill="none" strokeWidth="2"/>)}
     <text x="623" y="58" textAnchor="middle" fontSize="20" fill="#fff2d3">{attached?'VLASTNÁ REAKCIA':'VLASTNÝ PRIESTOR'}</text>
    </g>
    <g clipPath={!attached&&frame>=at('comment')?'url(#foreign-paper-slot)':undefined} opacity={paperIn}>
     <g transform={`translate(${x} ${y}) rotate(${angle})`} filter="url(#paper-object-shadow)">
      <path d={`M${-paperWidth/2} ${-paperHeight/2}H${paperWidth/2-14}L${paperWidth/2} ${-paperHeight/2+14}V${paperHeight/2}H${-paperWidth/2}Z`} fill="url(#travel-paper)" stroke="#a58653" strokeWidth="1.5"/>
      <path d={`M${paperWidth/2-14} ${-paperHeight/2}V${-paperHeight/2+14}H${paperWidth/2}`} fill="#bca06b"/>
      <text x="0" y="15" textAnchor="middle" fontSize={44+10*travel} fill="#533b29" opacity={1-writing}>!</text>
      {[0,1,2,3].filter(i=>writing*4>i).map(i=><path key={i} d={`M${-paperWidth*.34} ${-paperHeight*.2+i*28}q${paperWidth*.15} ${i%2?8:-5} ${paperWidth*.29} 0t${paperWidth*(i===3?.11:.3)} 0`} pathLength="1" stroke="#40372a" strokeWidth="4" strokeLinecap="round" fill="none" strokeDasharray={`${Math.max(0,Math.min(1,writing*4-i))} 1`}/>)}
     </g>
    </g>
    {frame>=at('comment')?<g><rect x="60" y="246" width="119" height="7" rx="3" fill="#080b0d"/><text x="120" y="280" textAnchor="middle" fontSize="15" fill="#f7e8c5" stroke="#171717" strokeWidth="3" paintOrder="stroke fill">KOMENTÁR</text></g>:null}
    {attached?<g transform={`translate(620 ${83-(1-pin)*28}) scale(${Math.max(0,pin)})`}><path d="M0 0L-2 29" stroke="#b7b7ae" strokeWidth="3"/><ellipse cy="0" rx="13" ry="9" fill="#772c23"/><ellipse cy="-3" rx="12" ry="8" fill="#f37354"/></g>:null}
    {audience?[0,1,2,3,4,5,6].map(i=>{const pop=spring({frame:frame-at('audience')-i,fps,config:{damping:17,stiffness:230}});return <g key={i} transform={`translate(${403+i*73} ${283+(1-pop)*36})`} opacity={Math.max(0,Math.min(1,pop))}><circle cy="-10" r="11" fill={i%2?'#dbd0b3':'#eadbb7'}/><path d="M-19 22Q-20 1 0 1Q20 1 19 22Z" fill={i%2?'#75644e':'#9e8868'}/></g>;}):null}
   </svg>
  </div>
 </AbsoluteFill>;
};
