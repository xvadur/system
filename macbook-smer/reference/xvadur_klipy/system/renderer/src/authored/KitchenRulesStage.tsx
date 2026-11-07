import React from 'react';
import {AbsoluteFill,Img,interpolate,spring,staticFile,useCurrentFrame,useVideoConfig} from 'remotion';
import {KitchenParameters} from '../../../scenes/kitchen-parameters';
import type {JourneyStageProps} from './JourneyStage';

const clamp={extrapolateLeft:'clamp',extrapolateRight:'clamp'} as const;
const rects={chef:[10,110,625,170],meat:[660,65,590,235],breadKnife:[10,410,625,150],fishKnife:[660,410,590,150],onion:[45,600,555,345],steak:[680,650,540,290],bread:[10,945,620,305],fish:[635,935,610,310]} as const;
type Sprite=keyof typeof rects;
const Cutout:React.FC<{name:Sprite;src:string;atlasWidth:number;atlasHeight:number;width:number;style?:React.CSSProperties}>=({name,src,atlasWidth,atlasHeight,width,style})=>{
 const [x,y,w,h]=rects[name],ratio=width/w;
 return <div style={{position:'absolute',width,height:h*ratio,overflow:'hidden',...style}}><Img src={src} style={{position:'absolute',left:-x*ratio,top:-y*ratio,width:atlasWidth*ratio,height:atlasHeight*ratio,maxWidth:'none'}}/></div>;
};

/** One kitchen and the same tools: name, mismatch, return and self-directed payoff. */
export const KitchenRulesStage:React.FC<JourneyStageProps>=({parameters,subject,phases,accent})=>{
 const p=KitchenParameters.parse(parameters),f=useCurrentFrame(),{width:w,height:h,fps}=useVideoConfig(),u=w/1080;
 const src=staticFile(subject.url!),at=(name:string)=>phases[name],age=(name:string)=>f-at(name);
 const enter=spring({frame:f-at('reveal'),fps,config:{damping:19,stiffness:245,mass:.6}});
 const beforeKitchen=f<at('onion')-3,afterReturn=f>=at('return');
 const inPanic=f>=at('panic')&&f<at('panic')+Math.round(1.65*fps);
 const fullCutaway=f>=at('wrongMeat')&&f<Math.min(at('bread'),at('wrongMeat')+Math.round(1.85*fps))||f>=at('wrongFish')&&f<at('order')+Math.round(.65*fps);
 const fade=interpolate(f,[at('return')-4,at('return')],[1,0],clamp);
 const common={src,atlasWidth:p.spriteWidth,atlasHeight:p.spriteHeight};
 const label:React.CSSProperties={fontFamily:'"Arial Black",Arial,sans-serif',fontWeight:900,color:'#fff',WebkitTextStroke:`${4*u}px #101010`,paintOrder:'stroke fill',textShadow:`0 ${4*u}px ${8*u}px #000a`,lineHeight:1.05};
 const knife=spring({frame:Math.max(0,age(f<at('bread')?'onion':'bread')),fps,config:{damping:18,stiffness:250}});
 const wrong=f>=at('wrongMeat')&&f<at('bread')||f>=at('wrongFish');
 const second=f>=at('bread');
 const swapAge=f-(second?at('wrongFish'):at('wrongMeat'));
 const swap=spring({frame:swapAge,fps,config:{damping:17,stiffness:260,mass:.6}});
 const shake=wrong&&swapAge>=0&&swapAge<12?Math.sin(swapAge*2.7)*12*u:0;
 const ordered=f>=at('order');
 const status=ordered?'KAŽDÝ MÁ SVOJE MIESTO':wrong?'NESPRÁVNY NÔŽ':second?'NA CHLIEB':'NA CIBUĽU';
 if(afterReturn)return null;
 return <AbsoluteFill style={{pointerEvents:'none',opacity:fade}}>
  {fullCutaway?<AbsoluteFill style={{background:'radial-gradient(ellipse at 50% 55%,#493423 0%,#1b1510 60%,#0b0a08 100%)'}}/>:null}
  {f<Math.round(2.85*fps)?<div style={{...label,position:'absolute',left:55*u,right:55*u,top:125*u,textAlign:'center',fontSize:65*u,opacity:interpolate(f,[Math.round(2.45*fps),Math.round(2.85*fps)],[1,0],clamp),transform:`translateY(${(1-enter)*-40*u}px) scale(${.94+.06*enter})`}}>OTCOVE NOŽE<br/><span style={{color:accent}}>VLASTNÉ PRAVIDLÁ</span></div>:null}
  {beforeKitchen?<>
   <div style={{position:'absolute',left:90*u,right:90*u,top:1160*u,height:300*u,opacity:enter}}>
    {(['chef','meat','breadKnife','fishKnife'] as Sprite[]).map((name,i)=>{
     const start=at('reveal')+i*Math.round(.17*fps),pr=spring({frame:f-start,fps,config:{damping:16,stiffness:230,mass:.6}});
     const collect=f>=at('collect'),ty=collect?(i%2?15:-15)*u:0;
     return <Cutout key={name} {...common} name={name} width={430*u} style={{left:(i%2)*440*u,top:Math.floor(i/2)*155*u+ty,filter:`drop-shadow(0 ${8*u}px ${6*u}px #0008)`,opacity:f<start?0:1,transform:`translateY(${(1-pr)*55*u}px) rotate(${collect?(i%2?5:-5):0}deg) scale(${.7+.3*pr})`}}/>;
    })}
   </div>
  </>:<>
   <div style={{position:'absolute',left:60*u,right:60*u,top:1120*u,height:300*u,opacity:inPanic?.2:1,transform:`translate(${shake}px,${fullCutaway?-365*u:0}px) scale(${fullCutaway?1.12:1})`}}>
    <div style={{position:'absolute',left:45*u,right:45*u,bottom:5*u,height:205*u,borderRadius:75*u,background:'repeating-linear-gradient(2deg,#c2955b 0px,#c2955b 3px,#b88b52 5px,#c89b60 9px)',boxShadow:`inset 0 ${3*u}px ${5*u}px #fff5,0 ${15*u}px ${20*u}px #0008`,transform:'perspective(900px) rotateX(28deg)'}}/>
    {!ordered?<>
     <Cutout {...common} name={second?'bread':'onion'} width={370*u} style={{left:325*u,bottom:8*u,filter:`drop-shadow(0 ${8*u}px ${5*u}px #0006)`,transform:`scale(${.9+.1*knife})`}}/>
     <Cutout {...common} name={wrong?(second?'fishKnife':'meat'):(second?'breadKnife':'chef')} width={650*u} style={{left:(95+(wrong?(1-swap)*-660:0))*u,top:(second?115:95)*u,filter:`drop-shadow(0 ${10*u}px ${6*u}px #0009)`,transform:`rotate(${wrong?-12:6}deg) scale(${knife})`}}/>
     <div style={{...label,position:'absolute',right:20*u,top:105*u,fontSize:115*u,color:wrong?'#ff4c3d':'#b8f07a',transform:`scale(${wrong?Math.max(.2,swap):knife})`}}>{wrong?'✕':'✓'}</div>
    </>:<>
     {(['chef','meat','breadKnife','fishKnife'] as Sprite[]).map((name,i)=><Cutout key={name} {...common} name={name} width={400*u} style={{left:(i%2)*450*u,top:(Math.floor(i/2)*150+60)*u,opacity:f>=at('problem')?.12:1,transform:`rotate(${i%2?-4:4}deg)`}}/>)}
    </>}
    {f<at('problem')?<div style={{...label,position:'absolute',left:15*u,right:15*u,top:-20*u,fontSize:(ordered?43:54)*u,textAlign:'center',color:wrong&&!ordered?'#ff6553':accent}}>{status}</div>:null}
   </div>
   {f>=at('problem')?<div style={{...label,position:'absolute',left:55*u,right:55*u,top:1090*u,fontSize:75*u,textAlign:'center',color:'#fff',transform:`scale(${1+Math.sin(age('problem')*2.5)*.035})`}}>OBROVSKÝ<br/><span style={{color:'#ff6253'}}>PROBLÉM</span></div>:null}
   {f>=at('problem')&&age('problem')<5?<AbsoluteFill style={{background:'#ff3d23',opacity:interpolate(age('problem'),[0,4],[.2,0],clamp)}}/>:null}
  </>}
 </AbsoluteFill>;
};
