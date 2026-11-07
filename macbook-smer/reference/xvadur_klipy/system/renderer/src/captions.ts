import type {CaptionFont,RenderWord} from './types';

export const chocolateCaptionVariant='chocolate-r5-word-pulse@1.0.0' as const;
export const chocolatePulse={timesMs:[0,80,200,320],scales:[.88,1.12,.99,1],maximum:1.12} as const;
export function wordPulseScale(ageMs:number):number {
  if(ageMs<0)return 1;
  const {timesMs,scales}=chocolatePulse;
  for(let i=1;i<timesMs.length;i++)if(ageMs<timesMs[i])return scales[i-1]+(scales[i]-scales[i-1])*(ageMs-timesMs[i-1])/(timesMs[i]-timesMs[i-1]);
  return 1;
}
export const activeCaptionWord=(word:RenderWord,frame:number)=>frame>=word.startFrame&&frame<word.endFrame;
export const captionText=(text:string)=>text.toLocaleUpperCase('sk');
export function chocolateCaptionGeometry(width:number,height:number){
  const scale=width/1080;
  return {fontSize:78*scale,top:1450/1920*height,stroke:6*scale,gap:20*scale,margin:55*scale,lineHeight:1.15,shadowY:5*scale,shadowBlur:9*scale,transformOrigin:'50% 65%'};
}
export type CaptionMeasure=(text:string,fontSize:number)=>number;
export type MeasuredCaptionPage={startFrame:number;endFrame:number;words:RenderWord[];fontSize:number;measuredWidth:number;reservedWidth:number;wordWidths:number[];slotWidths:number[]};
/** Group first, shrink only a single word that cannot fit. Every pulse can
 * reach 1.12 without changing a word's fixed layout slot or the next page. */
export function measuredCaptionPages(words:RenderWord[],fps:number,width:number,measure:CaptionMeasure,maxWords=3,maximum=width*78/1080):MeasuredCaptionPage[]{
  const geometry=chocolateCaptionGeometry(width,width*1920/1080),budget=width-geometry.margin*2;
  const extent=(group:RenderWord[],size:number)=>{
    const wordWidths=group.map(word=>measure(captionText(word.text),size)),slotWidths=wordWidths.map(measured=>(measured+geometry.stroke)*chocolatePulse.maximum);
    const measuredWidth=wordWidths.reduce((sum,width)=>sum+width,0)+Math.max(0,group.length-1)*geometry.gap;
    const reservedWidth=slotWidths.reduce((sum,width)=>sum+width,0)+Math.max(0,group.length-1)*geometry.gap;
    return {measuredWidth,reservedWidth,wordWidths,slotWidths};
  };
  const pages:MeasuredCaptionPage[]=[];let current:RenderWord[]=[];
  const close=()=>{
    if(!current.length)return;
    let size=maximum;
    if(current.length===1&&extent(current,size).reservedWidth>budget){const measured=measure(captionText(current[0].text),size);size=Math.min(size,(budget-geometry.stroke*chocolatePulse.maximum)/(measured*chocolatePulse.maximum)*size);}
    const dimensions=extent(current,size);
    if(!Number.isFinite(size)||size<=0||dimensions.reservedWidth>budget+1e-6)throw new Error('Measured caption does not fit the pinned output width');
    pages.push({startFrame:current[0].startFrame,endFrame:current.at(-1)!.endFrame,words:current,fontSize:size,...dimensions});current=[];
  };
  for(const word of words){
    if(!word.text.trim())continue;
    const previous=current.at(-1);
    if(previous&&(word.startFrame-previous.endFrame>fps*.6||current.length>=maxWords||extent([...current,word],maximum).reservedWidth>budget))close();
    current.push(word);if(/[.,!?…:;]$/.test(word.text))close();
  }
  close();
  return pages.map((page,index)=>({...page,endFrame:Math.min(pages[index+1]?.startFrame??page.endFrame+Math.round(fps*.8),page.endFrame+Math.round(fps*.8))}));
}

const fontLoads=new Map<string,Promise<void>>();
/** Called only in Chromium, after node staging verified the declared hash. */
export function loadCaptionFont(font:CaptionFont,url:string):Promise<void>{
  const key=`${font.family}|${font.hash}|${url}`;
  let load=fontLoads.get(key);
  if(!load){load=(async()=>{
    if(!font.url||!/^[a-f0-9]{64}$/.test(font.hash))throw new Error('Caption variant requires a hash-verified staged font');
    const face=await new FontFace(font.family,`url(${JSON.stringify(url)})`,{weight:'900',style:'normal'}).load();
    globalThis.document.fonts.add(face);
    await globalThis.document.fonts.load(`900 78px ${JSON.stringify(font.family)}`,'ĽŠČŤŽÝÁÍÉÚÔÄŇ');
    if(face.status!=='loaded'||!globalThis.document.fonts.check(`900 78px ${JSON.stringify(font.family)}`,'ĽŠČŤŽÝÁÍÉÚÔÄŇ'))throw new Error('Pinned caption font did not load');
  })();fontLoads.set(key,load);}
  return load;
}
export function browserCaptionMeasure(fontFamily:string):CaptionMeasure {
  const canvas=globalThis.document.createElement('canvas'),context=canvas.getContext('2d');
  if(!context)throw new Error('Caption font measurement is unavailable');
  const cache=new Map<string,number>();
  return (text,size)=>{const key=`${size}|${text}`;let measured=cache.get(key);if(measured===undefined){context.font=`900 ${size}px ${JSON.stringify(fontFamily)}`;measured=context.measureText(text).width;if(!Number.isFinite(measured)||measured<=0)throw new Error('Invalid measured caption width');cache.set(key,measured);}return measured;};
}
