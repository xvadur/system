import React from 'react';
import {AbsoluteFill, interpolate, spring, useCurrentFrame, useVideoConfig} from 'remotion';
import {authoredRegistry} from './authored/extended-registry';
import {validateAuthored} from '../../scenes/registry';
import {GraphicScene} from './graphics';
import {FramedMedia} from './media';
import type {Box,Framing,MediaAsset,RenderEvent,SceneSpec} from './types';

const string=(value:unknown,fallback=''):string=>typeof value==='string'?value:fallback;
const number=(value:unknown,fallback:number):number=>typeof value==='number'&&Number.isFinite(value)?value:fallback;
type Step={frame:number;action?:unknown;params?:unknown;text?:unknown};
const stepText=(step:Step|undefined,fallback:string)=>string(step?.text,string((step?.params as Record<string,unknown>|undefined)?.text,fallback));

/** Scene clocks are local to the event; props always retain the compiled absolute clock. */
export const EventScene:React.FC<{event:RenderEvent;assets:Map<string,MediaAsset>;accent:string}> = ({event,assets,accent}) => {
  const frame=useCurrentFrame(),{width,height,fps}=useVideoConfig();
  if(event.scene==='Authored'){
    if(!event.authored)throw new Error('Missing authored render binding');
    const b=event.authored,{parameters}=validateAuthored(b),Component=authoredRegistry[`${b.sceneId}@${b.version}`];
    const subject=assets.get(b.assetSlots.subject);
    if(!Component||!subject?.url)throw new Error('Missing authored implementation or staged slot');
    return <Component parameters={parameters} subject={subject} phases={b.phaseFrames} accent={accent} enterFrames={b.enterFrames} exitFrames={b.exitFrames}/>;
  }
  const p=event.params;
  const chosen=event.assetIds.map(id=>assets.get(id)).filter((a):a is MediaAsset=>Boolean(a));
  const steps=event.steps??[];
  const activeStep=[...steps].filter(s=>s.frame<=frame).at(-1);
  const returnAt=steps.find(s=>s.action==='return')?.frame;
  const endOpacity=returnAt===undefined?1:interpolate(frame,[returnAt,Math.max(returnAt+1,Math.min(event.endFrame-event.startFrame,returnAt+Math.max(1,Math.round(fps*.15))))],[1,0],{extrapolateLeft:'clamp',extrapolateRight:'clamp'});
  const generated=chosen.find(a=>a.sceneSpec);
  const spec=(p.sceneSpec??generated?.sceneSpec) as SceneSpec|undefined;
  if(spec){if(!Array.isArray(spec.nodes))throw new Error(`Scene ${event.id}: SceneSpec must pass through the canonical adapter`);return <AbsoluteFill style={{opacity:endOpacity}}><GraphicScene spec={spec} assets={assets}/></AbsoluteFill>;}
  const enter=spring({frame,fps,config:{damping:200}});
  const inset=width*.06;
  const caption=string(p.text,string(p.title));
  const currentText=stepText(activeStep,caption);
  const box=p.box as Box|undefined;
  const viewport=box??{x:0,y:0,width,height};
  const mediaFraming:Framing={...(p.framing as Framing|undefined),...(p.crop?{crop:p.crop as Box}:{})};
  const textStyle:React.CSSProperties={fontSize:width*.064,fontWeight:900,lineHeight:1.1,textAlign:'center',color:'#fff',textShadow:'0 3px 10px #000',overflowWrap:'anywhere',whiteSpace:'pre-line'};
  if(event.scene==='Graphic') throw new Error(`Graphic ${event.id} has no SceneSpec`);
  if(event.scene==='Cutaway'&&Array.isArray(p.panels))return <AbsoluteFill style={{opacity:endOpacity}}>{(p.panels as Array<{assetId?:string;assetRequestId?:string;assetIndex?:number;sourceStartMs?:number;sourceEndMs?:number;crop?:Box;viewport:Box;muted?:boolean;gain?:number}>).map((panel,i)=>{
    const media=assets.get(panel.assetId??'')??chosen.find(a=>(a as MediaAsset&{requestId?:string}).requestId===panel.assetRequestId)??chosen[panel.assetIndex??i];if(!media)throw new Error(`Missing reaction panel asset in ${event.id}`);
    return <FramedMedia key={i} asset={media} sourceStartMs={panel.sourceStartMs??0} sourceEndMs={panel.sourceEndMs} framing={{crop:panel.crop,viewport:panel.viewport}} muted={panel.muted??p.muted!==false} gain={panel.gain??1}/>;
  })}</AbsoluteFill>;
  if(event.scene==='Diagram') {
    const nodes=(p.nodes??[]) as Array<{id?:string;text?:string;x?:number;y?:number;width?:number;height?:number;revealStep?:number}>;
    const edges=(p.edges??[]) as Array<{from:string;to:string;label?:string}>;
    if(!nodes.length) throw new Error(`Diagram ${event.id} has no nodes or SceneSpec`);
    const reveal=(node:typeof nodes[number],i:number)=>steps[node.revealStep??i]?.frame??0;
    const geometry=(node:typeof nodes[number],i:number)=>({x:node.x??inset,y:node.y??height*(.2+i*.18),w:node.width??width*.88,h:node.height??height*.12});
    return <svg width="100%" height="100%" viewBox={`0 0 ${width} ${height}`} style={{position:'absolute',inset:0,opacity:endOpacity,background:string(p.background,'#101820')}}>
      <defs><marker id={`arrow-${event.id}`} viewBox="0 0 10 10" refX="9" refY="5" markerWidth="6" markerHeight="6" orient="auto-start-reverse"><path d="M0 0 L10 5 L0 10 Z" fill={accent}/></marker></defs>
      {edges.map((edge,i)=>{const ai=nodes.findIndex(n=>n.id===edge.from),bi=nodes.findIndex(n=>n.id===edge.to);if(ai<0||bi<0)throw new Error(`Unknown diagram edge ${edge.from} → ${edge.to}`);const a=nodes[ai],b=nodes[bi];if(frame<Math.max(reveal(a,ai),reveal(b,bi)))return null;const ag=geometry(a,ai),bg=geometry(b,bi),ax=ag.x+ag.w/2,ay=ag.y+ag.h,bx=bg.x+bg.w/2,by=bg.y;return <g key={i}><path d={`M${ax} ${ay} L${bx} ${by}`} stroke={accent} strokeWidth={width*.009} markerEnd={`url(#arrow-${event.id})`} fill="none"/>{edge.label?<text x={(ax+bx)/2+width*.02} y={(ay+by)/2} fill="#fff" fontSize={width*.035}>{edge.label}</text>:null}</g>;})}
      {nodes.map((node,i)=>{if(frame<reveal(node,i))return null;const g=geometry(node,i);return <g key={node.id??i} transform={`translate(${g.x} ${g.y})`}><rect width={g.w} height={g.h} rx={width*.02} fill="#172d3a" stroke={accent}/><text x={g.w/2} y={g.h*.6} textAnchor="middle" fill="#fff" fontWeight={800} fontSize={Math.min(width*.048,g.w/Math.max(1,(node.text?.length??0)*.6))}>{node.text}</text></g>;})}
    </svg>;
  }
  if(event.scene==='Comparison') {
    const labels=p.labels as string[]|undefined;
    if(chosen.length<2&&(!labels||labels.length<2))throw new Error(`Comparison ${event.id} needs two concrete sides`);
    return <AbsoluteFill style={{background:string(p.background,'#101820'),opacity:endOpacity}}>
      {[0,1].map(i=>{const at=steps[i]?.frame??0;if(frame<at)return null;const asset=chosen[i];return <React.Fragment key={i}>{asset?<FramedMedia asset={asset} framing={{viewport:{x:i*width/2,y:height*.2,width:width/2,height:height*.42},fit:'contain'}} muted/>:null}<div style={{...textStyle,position:'absolute',top:height*.64,left:i*width/2,width:width/2,padding:inset/2,boxSizing:'border-box'}}>{labels?.[i]}</div></React.Fragment>;})}
      <div style={{...textStyle,position:'absolute',left:inset,right:inset,top:height*.08,color:accent}}>{caption}</div>
    </AbsoluteFill>;
  }
  if(event.scene==='CTA'||event.scene==='Text') return <AbsoluteFill style={{background:string(p.background,event.scene==='CTA'?'#101820':'transparent'),justifyContent:'center',alignItems:'center',padding:inset,boxSizing:'border-box',opacity:enter*endOpacity}}><div style={{...textStyle,fontSize:number(p.fontSize,width*.085),transform:`translateY(${(1-enter)*height*.025}px)`}}>{currentText}</div>{p.subtitle?<div style={{...textStyle,fontSize:width*.052,color:accent,marginTop:height*.025}}>{string(p.subtitle)}</div>:null}</AbsoluteFill>;
  if(!chosen[0]) throw new Error(`${event.scene} ${event.id}: missing asset`);
  const primary=chosen[0];
  const portrait=event.scene==='Portrait',document=event.scene==='Document',meme=event.scene==='Meme';
  const revealFrame=meme?(steps.find(s=>s.action==='reveal')?.frame??0):0;
  const revealed=frame>=revealFrame;
  const mediaViewport=box??(portrait?{x:width*.2,y:height*.16,width:width*.6,height:height*.46}:document?{x:inset,y:height*.12,width:width-inset*2,height:height*.58}:viewport);
  const trim=p.trim as {startMs:number;endMs:number}|undefined;
  return <AbsoluteFill style={{opacity:endOpacity,background:string(p.background,portrait||document||meme&&revealed?'#101820':'transparent')}}>
    {revealed?<FramedMedia asset={primary} sourceStartMs={trim?.startMs??number(p.sourceStartMs,0)} sourceEndMs={trim?.endMs} framing={{...mediaFraming,viewport:mediaViewport,fit:portrait||document||meme?'contain':mediaFraming.fit??'cover'}} muted={p.muted!==false} gain={number(p.gain,1)} loop={p.shortPolicy==='loop'} hold={p.shortPolicy==='hold'}/>:null}
    {document&&p.highlight?<div style={{position:'absolute',left:(p.highlight as Box).x,top:(p.highlight as Box).y,width:(p.highlight as Box).width,height:(p.highlight as Box).height,background:'rgba(255,214,0,.25)',border:`2px solid ${accent}`}}/>:null}
    {(caption||currentText)?<div style={{...textStyle,position:'absolute',left:inset,right:inset,top:meme?height*.06:portrait?height*.65:height*.06,color:portrait?accent:'#fff',background:meme?'rgba(0,0,0,.72)':'transparent',padding:width*.025,transform:`scale(${interpolate(enter,[0,1],[.95,1])})`}}>{meme&&!revealed?stepText(steps.find(s=>s.action==='setup'),string(p.setupText,caption)):currentText}</div>:null}
    {p.bottomText&&revealed?<div style={{...textStyle,position:'absolute',left:inset,right:inset,bottom:height*.1}}>{string(p.bottomText)}</div>:null}
  </AbsoluteFill>;
};
