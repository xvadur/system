import React from 'react';
import {Easing,useCurrentFrame} from 'remotion';
import type {EffectEasing,TimelineVisualEffect} from '../../schemas/index';

type Keyframe<Value>={frame:number;value:Value;easing?:EffectEasing};

const ease={
  linear:Easing.linear,
  'ease-in':Easing.in(Easing.cubic),
  'ease-out':Easing.out(Easing.cubic),
  'ease-in-out':Easing.inOut(Easing.cubic),
  hold:()=>0,
};

function keyframeSample<Value>(keys:ReadonlyArray<Keyframe<Value>>,frame:number) {
  const index=keys.findIndex(key=>key.frame>frame);
  const left=index===0?keys[0]!:index===-1?keys.at(-1)!:keys[index-1]!;
  const right=index<=0?left:keys[index]!;
  const progress=right===left?0:ease[left.easing??'linear']((frame-left.frame)/(right.frame-left.frame));
  return {from:left.value,to:right.value,progress};
}

function effectStyle(effect:TimelineVisualEffect,frame:number):React.CSSProperties {
  if(effect.kind==='opacity'){
    const {from,to,progress}=keyframeSample(effect.keyframes,frame);
    return {opacity:from+(to-from)*progress};
  }
  if(effect.kind==='transform'){
    const {from,to,progress}=keyframeSample(effect.keyframes,frame);
    const x=(from.x+(to.x-from.x)*progress)*100;
    const y=(from.y+(to.y-from.y)*progress)*100;
    const scale=from.scale+(to.scale-from.scale)*progress;
    const rotation=from.rotation+(to.rotation-from.rotation)*progress;
    return {transform:`translate(${x}%, ${y}%) rotate(${rotation}deg) scale(${scale})`};
  }
  const {from,to,progress}=keyframeSample(effect.keyframes,frame);
  const value=(key:keyof typeof from)=>from[key]+(to[key]-from[key])*progress;
  return {filter:`brightness(${value('brightness')}) contrast(${value('contrast')}) saturate(${value('saturation')}) grayscale(${value('grayscale')}) blur(${value('blurPx')}px)`};
}

/** Apply each operation to the result of the preceding operation in list order. */
export const VisualEffectStack:React.FC<{
  effects:ReadonlyArray<TimelineVisualEffect>;
  children:React.ReactNode;
}>=({effects,children})=>{
  const frame=useCurrentFrame();
  return effects.reduce<React.ReactNode>((content,effect)=>(
    <div key={effect.id} style={{position:'absolute',inset:0,...effectStyle(effect,frame)}}>{content}</div>
  ),children);
};
