import fs from 'node:fs/promises';
import path from 'node:path';
import {createRequire} from 'node:module';
import {createHash,randomUUID} from 'node:crypto';
import {execFile} from 'node:child_process';
import {promisify} from 'node:util';
const exec=promisify(execFile),hash=(value:unknown)=>createHash('sha256').update(JSON.stringify(value)).digest('hex');
const PRIMING_SAMPLES=2048;
type Packet={stream_index:number;pts:number;dts:number;duration:number;data_hash:string;side_data_list?:Array<{side_data_type:string;skip_samples?:number}>};
type Stream={index:number;codec_type:string;codec_name:string;profile?:string;sample_rate?:string;time_base:string};
type Probe={streams:Stream[];packets:Packet[]};
export type AuthoredAudioPriming={version:'authored-aac-priming.v1';status:'compensated'|'already_compensated';runtimeVersion:'4.0.529';encoder:'libfdk_aac';sampleRate:number;primingSamples:number;offsetSeconds:number;videoPayloadHash:string;audioPayloadHash:string;videoPacketTimingHash:string;packetPayloadsPreserved:true};

/** Remotion 4.0.529 compresses with libfdk_aac into ADTS, then copies that
 * audio into MP4 without the encoder's 2048-sample priming metadata. This is
 * the same encoder fact handled by Remotion 4.0.541 aac-priming.js. Only new
 * authored outputs from the verified .529 encoder path enter this function.
 * Copying packets with an MP4 edit list fixes timestamps, never source words.
 */
export async function compensateAuthoredAacPriming(file:string,runtimeRoot:string):Promise<AuthoredAudioPriming>{
  const require=createRequire(path.join(runtimeRoot,'package.json'));
  const rendererRoot=path.dirname(require.resolve('@remotion/renderer/package.json'));
  const version=JSON.parse(await fs.readFile(path.join(rendererRoot,'package.json'),'utf8')).version;
  const {mapAudioCodecToFfmpegAudioCodecName}=require(path.join(rendererRoot,'dist/options/audio-codec.js'));
  if(version!=='4.0.529'||mapAudioCodecToFfmpegAudioCodecName('aac')!=='libfdk_aac')throw new Error('AAC priming compensation requires the pinned Remotion 4.0.529 libfdk_aac path');
  if(path.extname(file).toLowerCase()!=='.mp4')throw new Error('Authored AAC priming compensation requires MP4 edit lists');
  const {getExecutablePath}=require(path.join(rendererRoot,'dist/compositor/get-executable-path.js'));
  const binary=(type:string)=>getExecutablePath({type,indent:false,logLevel:'error',binariesDirectory:null});
  const env={...process.env,DYLD_LIBRARY_PATH:path.dirname(binary('ffmpeg'))};
  const probe=async(input:string):Promise<Probe>=>JSON.parse((await exec(binary('ffprobe'),['-v','error','-show_streams','-show_packets','-show_data_hash','sha256','-show_entries','stream=index,codec_type,codec_name,profile,sample_rate,time_base:packet=stream_index,pts,dts,duration,data_hash,side_data_list','-of','json',input],{env,maxBuffer:32*1024*1024})).stdout);
  const before=await probe(file),audio=before.streams.find(s=>s.codec_type==='audio'),video=before.streams.find(s=>s.codec_type==='video');
  // The pinned minimal FFprobe reports FF_PROFILE_AAC_LOW as numeric "1";
  // full FFprobe builds spell the same profile "LC".
  if(before.streams.length!==2||!audio||!video||audio.codec_name!=='aac'||!['LC','1'].includes(audio.profile??''))throw new Error('Expected exactly one video and one AAC-LC stream in authored output');
  const sampleRate=Number(audio.sample_rate);
  if(!Number.isInteger(sampleRate)||sampleRate<=0||audio.time_base!==`1/${sampleRate}`)throw new Error('Authored AAC stream has an unexpected sample clock');
  const packets=(data:Probe,stream:Stream)=>data.packets.filter(p=>p.stream_index===stream.index);
  const aa=packets(before,audio),vv=packets(before,video),first=aa[0];
  if(!first||!vv.length)throw new Error('Authored output has no encoded audio/video packets');
  if([...aa,...vv].some(p=>!/^SHA256:[a-f0-9]{64}$/i.test(p.data_hash??'')))throw new Error('Cannot verify authored encoded packet payload hashes');
  const skip=(p:Packet)=>p.side_data_list?.find(s=>s.side_data_type==='Skip Samples')?.skip_samples??0;
  const payload=(p:Packet[])=>hash(p.map(item=>item.data_hash));
  const timing=(p:Packet[])=>hash(p.map(item=>[item.pts,item.dts,item.duration]));
  const receipt=(status:AuthoredAudioPriming['status']):AuthoredAudioPriming=>({version:'authored-aac-priming.v1',status,runtimeVersion:'4.0.529',encoder:'libfdk_aac',sampleRate,primingSamples:PRIMING_SAMPLES,offsetSeconds:-PRIMING_SAMPLES/sampleRate,videoPayloadHash:payload(vv),audioPayloadHash:payload(aa),videoPacketTimingHash:timing(vv),packetPayloadsPreserved:true});
  if(first.pts===-PRIMING_SAMPLES&&skip(first)===PRIMING_SAMPLES)return receipt('already_compensated');
  if(first.pts!==0||first.dts!==0||skip(first)!==0)throw new Error('Authored AAC already has an unexpected timestamp or priming edit; refusing another shift');
  const temporary=path.join(path.dirname(file),`.aac-priming-${randomUUID()}.mp4`);
  try{
    await exec(binary('ffmpeg'),['-nostdin','-v','error','-n','-i',file,'-itsoffset',(-PRIMING_SAMPLES/sampleRate).toFixed(15),'-i',file,'-map','0:v:0','-map','1:a:0','-c','copy','-use_editlist','1','-movflags','+faststart',temporary],{env,maxBuffer:4*1024*1024});
    const after=await probe(temporary),newAudio=after.streams.find(s=>s.codec_type==='audio')!,newVideo=after.streams.find(s=>s.codec_type==='video')!;
    if(!newAudio||!newVideo||newAudio.time_base!==audio.time_base||newVideo.time_base!==video.time_base)throw new Error('AAC edit-list remux changed stream clocks');
    const nextAudio=packets(after,newAudio),nextVideo=packets(after,newVideo);
    if(payload(aa)!==payload(nextAudio)||payload(vv)!==payload(nextVideo)||timing(vv)!==timing(nextVideo))throw new Error('AAC edit-list remux changed encoded payloads or video timing');
    if(nextAudio[0].pts!==-PRIMING_SAMPLES||skip(nextAudio[0])!==PRIMING_SAMPLES||nextAudio.some((p,i)=>p.pts!==aa[i].pts-PRIMING_SAMPLES||p.dts!==aa[i].dts-PRIMING_SAMPLES))throw new Error('AAC remux did not express the exact priming skip');
    await fs.rename(temporary,file);
    return receipt('compensated');
  }finally{await fs.rm(temporary,{force:true});}
}
