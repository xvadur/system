import React from 'react';
import {AbsoluteFill, Freeze, Img, Loop, OffthreadVideo, interpolate, staticFile, useCurrentFrame, useVideoConfig} from 'remotion';
import type {Box,Framing,MediaAsset} from './types';

export const FramedMedia: React.FC<{asset:MediaAsset;sourceStartMs?:number;sourceEndMs?:number;framing?:Framing;muted?:boolean;gain?:number;loop?:boolean;hold?:boolean}> = ({asset,sourceStartMs=0,sourceEndMs,framing,muted=true,gain=1,loop=false,hold=false}) => {
  const {width,height,fps}=useVideoConfig();
  const frame=useCurrentFrame();
  if (!asset.url) throw new Error(`Unstaged media: ${asset.id}`);
  const viewport:Box=framing?.viewport??{x:0,y:0,width,height};
  const sw=asset.technical?.width??width,sh=asset.technical?.height??height;
  const crop=framing?.crop??{x:0,y:0,width:sw,height:sh};
  const fit=framing?.fit??'cover';
  const ratio=fit==='contain'?Math.min(viewport.width/crop.width,viewport.height/crop.height):Math.max(viewport.width/crop.width,viewport.height/crop.height);
  const keys=framing?.keys??[];
  const value=(prop:'x'|'y'|'scale',fallback:number)=>{
    const rows=keys.filter(k=>k[prop]!==undefined).sort((a,b)=>a.frame-b.frame);
    const after=rows.findIndex(k=>k.frame>frame);if(after>0&&rows[after].transition==='cut')return rows[after-1][prop]!;
    return rows.length>1?interpolate(frame,rows.map(k=>k.frame),rows.map(k=>k[prop]!),{extrapolateLeft:'clamp',extrapolateRight:'clamp'}):rows[0]?.[prop]??fallback;
  };
  const style:React.CSSProperties={position:'absolute',width:sw*ratio,height:sh*ratio,left:(viewport.width-crop.width*ratio)/2-crop.x*ratio,top:(viewport.height-crop.height*ratio)/2-crop.y*ratio,transform:`translate(${value('x',0)}px,${value('y',0)}px) scale(${value('scale',1)})`,transformOrigin:'50% 40%'};
  const available=Math.max(1,Math.round(((sourceEndMs??asset.technical?.durationMs??sourceStartMs+1000)-sourceStartMs)*fps/1000));
  const video=<OffthreadVideo src={staticFile(asset.url)} trimBefore={Math.round(sourceStartMs*fps/1000)} trimAfter={sourceEndMs===undefined?undefined:Math.round(sourceEndMs*fps/1000)} muted={muted} volume={gain} style={style}/>;
  const media=asset.kind==='video'?(loop?<Loop durationInFrames={available}>{video}</Loop>:hold&&frame>=available?<Freeze frame={available-1}>{video}</Freeze>:video):<Img src={staticFile(asset.url)} style={style}/>;
  return <div style={{position:'absolute',left:viewport.x,top:viewport.y,width:viewport.width,height:viewport.height,overflow:'hidden',background:'#090c10'}}>
    {media}
  </div>;
};

export const ArollMedia:React.FC<{asset:MediaAsset;sourceStartMs:number;sourceEndMs?:number;framing?:Framing;assets:Map<string,MediaAsset>}> = ({asset,sourceStartMs,sourceEndMs,framing,assets}) => <AbsoluteFill>
  <FramedMedia asset={asset} sourceStartMs={sourceStartMs} sourceEndMs={sourceEndMs} framing={framing} muted/>
  {(framing?.panels??[]).map((panel,i)=><FramedMedia key={i} asset={panel.assetId?assets.get(panel.assetId)??asset:asset} sourceStartMs={panel.sourceStartMs??sourceStartMs} sourceEndMs={sourceEndMs} framing={{crop:panel.crop,viewport:panel.viewport}} muted/>)}
</AbsoluteFill>;
