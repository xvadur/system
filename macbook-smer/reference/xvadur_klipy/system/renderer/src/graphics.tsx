import React from 'react';
import {Img, interpolate, staticFile, useCurrentFrame} from 'remotion';
import type {GraphicKey, GraphicNode, MediaAsset, SceneSpec} from './types';

const sample = (keys: GraphicKey[], property: 'x' | 'y' | 'scale' | 'rotate' | 'opacity', frame: number, fallback: number): number => {
  const usable = [...new Map(keys.filter(k => k[property] !== undefined).map(k=>[k.frame,k])).values()].sort((a,b) => a.frame-b.frame);
  if (!usable.length) return fallback;
  if (usable.length === 1) return usable[0][property]!;
  return interpolate(frame, usable.map(k=>k.frame), usable.map(k=>k[property]!), {extrapolateLeft:'clamp',extrapolateRight:'clamp'});
};

/** Declarative scene language: no eval, fetched code, CSS animations or arbitrary HTML. */
const Node: React.FC<{node: GraphicNode; frame: number; assets: Map<string,MediaAsset>}> = ({node,frame,assets}) => {
  if (frame < (node.startFrame ?? 0) || frame >= (node.endFrame ?? Infinity)) return null;
  const keys=node.keyframes??[];
  const x=sample(keys,'x',frame,node.x??0), y=sample(keys,'y',frame,node.y??0);
  const scale=sample(keys,'scale',frame,node.scale??1), rotate=sample(keys,'rotate',frame,node.rotate??0);
  const opacity=sample(keys,'opacity',frame,node.opacity??1);
  const common={opacity,transform:`translate(${x} ${y}) rotate(${rotate}) scale(${scale})`};
  if (node.type==='group') return <g {...common}>{(node.children??[]).map(n=><Node key={n.id} node={n} frame={frame} assets={assets}/>)}</g>;
  if (node.type==='text') return <g {...common}><text x={0} y={node.fontSize??42} fill={node.fill??'#fff'} fontSize={node.fontSize??42} fontWeight={node.fontWeight??800} textAnchor={node.align==='center'?'middle':node.align==='right'?'end':'start'}>{(node.text??'').split('\n').map((line,i)=><tspan key={i} x={0} dy={i===0?0:(node.fontSize??42)*1.2}>{line}</tspan>)}</text></g>;
  if (node.type==='image') {
    const asset=assets.get(node.assetId??'');
    if (!asset?.url) throw new Error(`SceneSpec ${node.id}: missing local image asset ${node.assetId}`);
    return <g {...common}><foreignObject width={node.width??200} height={node.height??200}><Img src={staticFile(asset.url)} style={{width:'100%',height:'100%',objectFit:'contain'}}/></foreignObject></g>;
  }
  if (node.type==='path') return <g {...common}><path d={node.d??''} fill={node.fill??'none'} stroke={node.stroke??'#fff'} strokeWidth={node.strokeWidth??4}/></g>;
  if (node.type==='ellipse'||node.type==='circle') return <g {...common}><ellipse cx={(node.width??100)/2} cy={(node.height??node.width??100)/2} rx={(node.width??100)/2} ry={(node.height??node.width??100)/2} fill={node.fill??'#F2B45F'} stroke={node.stroke} strokeWidth={node.strokeWidth}/></g>;
  if (node.type==='rect'||node.type==='shape') return <g {...common}><rect width={node.width??100} height={node.height??100} rx={node.radius??0} fill={node.fill??'#F2B45F'} stroke={node.stroke} strokeWidth={node.strokeWidth}/></g>;
  throw new Error(`Unsupported SceneSpec node type: ${node.type}`);
};

export const GraphicScene: React.FC<{spec: SceneSpec; assets: Map<string,MediaAsset>}> = ({spec,assets}) => {
  const frame=useCurrentFrame();
  const width=spec.width??1080,height=spec.height??1920;
  return <svg width="100%" height="100%" viewBox={`0 0 ${width} ${height}`} style={{position:'absolute',inset:0,background:spec.background,fontFamily:'Arial, sans-serif'}}>{spec.nodes.map(n=><Node key={n.id} node={n} frame={frame} assets={assets}/>)}</svg>;
};
