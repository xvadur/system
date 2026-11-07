import React from 'react';
import {AbsoluteFill, Img, interpolate, staticFile, useCurrentFrame, useVideoConfig} from 'remotion';
import type {JourneyStageProps} from './JourneyStage';

const clamp = {extrapolateLeft:'clamp',extrapolateRight:'clamp'} as const;
const platforms = [{name:'YT',color:'#ff453a'},{name:'TT',color:'#6ce6e6'},{name:'FB',color:'#63a0ff'},{name:'IG',color:'#f099d2'}];

/** Event-local word phases; the parent owns all GIF occlusion. No second event clock. */
export const ProfileWhackStage:React.FC<JourneyStageProps> = ({parameters,subject,phases}) => {
 const p=parameters as {layout:'profile-whack';hook:string};
 const frame=useCurrentFrame(),{width,fps}=useVideoConfig(),u=width/1080;
 const at=(name:string)=>phases[name];
 const quiet=frame>=at('quiet'), counting=frame>=at('platforms');
 const period=Math.max(1,Math.round(.82*fps));
 const playOrigin=frame>=at('pop')?at('pop'):frame>=at('block')?at('block'):at('boot');
 const cycle=Math.floor(Math.max(0,frame-playOrigin)/period)+(frame>=at('pop')?2:frame>=at('block')?1:0);
 const tick=Math.max(0,frame-playOrigin)%period/period;
 const active=[0,2,1,3][cycle%4];
 const rise=quiet?0:interpolate(tick,[0,.18,.52,.68,1],[0,1,1,0,0],clamp);
 const hit=!quiet&&tick>=.50&&tick<.76;
 const hammerAngle=interpolate(tick,[0,.38,.56,.68,1],[-28,-28,34,-16,-28],clamp);
 const opacity=interpolate(frame,[at('boot'),at('boot')+4],[0,1],clamp)*interpolate(frame,[at('return')-4,at('return')],[1,0],clamp);
 const total=frame>=at('total'), subtotal=frame>=at('subtotal'), hundred=frame>=at('hundred'), per=frame>=at('perPlatform');
 // Only a number already spoken may appear. The 50–100M views claim stays in speech/captions.
 const number=total?'320–400':subtotal?'320…':hundred?'80–100':per?'80…':counting?'4':'';
 const label=total||subtotal?'PROFILOV SPOLU':per?'NA PLATFORME':counting?'PLATFORMY':'';
 if(!subject.url||frame<at('boot')||frame>=at('return'))return null;
 return <AbsoluteFill style={{pointerEvents:'none',opacity}}>
  {/* This hard clip contains heads, hammer, shadows and all motion below the mouth. */}
  <div aria-label={p.hook} style={{position:'absolute',left:80*u,top:1120*u,width:920*u,height:310*u,overflow:'hidden'}}>
   <div style={{position:'absolute',inset:0,width:920,height:310,transform:`scale(${u})`,transformOrigin:'top left'}}>
    <svg viewBox="0 0 920 310" style={{position:'absolute',inset:0,width:920,height:310}}>
     <defs><linearGradient id="whack-wood" x2="0" y2="1"><stop stopColor="#b88750"/><stop offset="1" stopColor="#684327"/></linearGradient></defs>
     <path d="M18 172L902 172L920 267L0 267Z" fill="url(#whack-wood)" stroke="#d4ad72" strokeWidth="3"/>
     <path d="M0 267H920V305H0Z" fill="#422b1c" stroke="#a27549" strokeWidth="3"/>
     {[192,220,250].map(y=><path key={y} d={`M15 ${y}H905`} stroke="#51331d" opacity=".18" strokeWidth="2"/>)}
     {platforms.map((platform,i)=><g key={platform.name}>
      <ellipse cx={130+i*220} cy="204" rx="88" ry="35" fill="#3d281e" stroke="#d6ae71" strokeWidth="5"/>
      <ellipse cx={130+i*220} cy="201" rx="74" ry="25" fill="#150f0d"/>
     </g>)}
    </svg>
    {platforms.map((platform,i)=>{
     const visible=quiet||i===active;
     const headRise=rise;
     return <React.Fragment key={platform.name}>
      <div style={{position:'absolute',left:44+i*220,top:22,width:172,height:188,overflow:'hidden'}}>
       <Img src={staticFile(subject.url!)} style={{position:'absolute',width:quiet?50:148,height:quiet?62:188,objectFit:'contain',left:quiet?61:12,top:quiet?125:188-(visible?headRise*178:0),filter:'drop-shadow(0 4px 2px #0008)',transform:`rotate(${visible&&!quiet?Math.sin(tick*Math.PI)*6:0}deg)`}}/>
      </div>
      <div style={{position:'absolute',left:62+i*220,top:244,width:136,height:43,borderRadius:12,background:'#241d18',border:`2px solid ${platform.color}`,color:platform.color,textAlign:'center',fontFamily:'Arial Black, Arial, sans-serif',fontSize:29,lineHeight:'40px'}}>{platform.name}</div>
      {hit&&i===active?<div style={{position:'absolute',left:84+i*220,top:164,fontFamily:'Arial Black',fontSize:48,color:'#ff6755',textShadow:'2px 3px #2b0c08',transform:'rotate(-12deg)'}}>×</div>:null}
     </React.Fragment>;
    })}
    {!quiet?<div style={{position:'absolute',left:130+active*220,top:35,width:110,height:155,transform:`rotate(${hammerAngle}deg)`,transformOrigin:'70% 90%'}}>
     <div style={{position:'absolute',left:58,top:38,width:21,height:113,borderRadius:8,background:'linear-gradient(90deg,#8d5b30,#d4a164,#83502d)',border:'2px solid #301e13'}}/>
     <div style={{position:'absolute',left:8,top:12,width:106,height:49,borderRadius:18,background:'linear-gradient(#f4b85b,#b0662b)',border:'4px solid #4d2d16',boxShadow:'inset 0 -8px #7c412755'}}/>
    </div>:null}
    {number?<div style={{position:'absolute',left:225,top:5,width:470,height:145,textAlign:'center',fontFamily:'Arial Black, Arial, sans-serif',color:'#fff',textShadow:'0 3px 3px #000,2px 0 #000,-2px 0 #000'}}>
     <div style={{fontSize:22,color:'#e8d9c5',letterSpacing:3}}>ODHAD</div>
     <div style={{fontSize:65,lineHeight:'71px',color:'#ffe45c'}}>{number}</div>
     <div style={{fontSize:23,lineHeight:'28px'}}>{label}</div>
    </div>:null}
   </div>
  </div>
 </AbsoluteFill>;
};
