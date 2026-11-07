import path from 'node:path';
import * as fs from 'node:fs/promises';
import {randomUUID} from 'node:crypto';
import type {ZodTypeAny} from 'zod';
import {hashArtifact,RunManifestSchema,type RunManifest} from '../schemas/index.ts';
import {atomicWriteJson,ensureInsideRoot,hashFile,identifier,projectRoot,readJson,withLock} from './io.ts';

export interface Context {clientId:string;episodeId:string;episodeDir:string;libraryDir:string;fixture:boolean;workspace:string}
export async function context(options:{clientId?:string;episodeId:string;workspace?:string;fixture?:boolean}):Promise<Context>{
  const clientId=identifier(options.clientId??'fiki'),episodeId=identifier(options.episodeId);
  if(clientId!=='fiki')throw new Error('Only the Fiki client is supported');
  const workspace=await ensureInsideRoot(options.workspace??projectRoot);
  const fixture=options.fixture??false;
  if(workspace!==projectRoot&&!workspace.startsWith(path.join(projectRoot,'system/tests/work')+path.sep))throw new Error('Alternate workspace must be under system/tests/work');
  if(fixture&&workspace===projectRoot)throw new Error('Fixture decisions require an isolated test workspace');
  return {clientId,episodeId,workspace,fixture,episodeDir:path.join(workspace,clientId,'epizody',episodeId),libraryDir:path.join(workspace,clientId,'kniznica')};
}
export function writable(ctx:Context):void {
  // Deliberate hard boundary until the separate, jointly run M9 test is authorized.
  if(ctx.episodeId==='105')throw new Error('Episode 105 is reserved for the joint M9 test; no processing is enabled');
}
export function base(ctx:Context,revision:number,input:unknown){return {schemaVersion:'1.0.0' as const,clientId:ctx.clientId,episodeId:ctx.episodeId,revision,inputHash:hashArtifact(input)};}
export function artifactDir(ctx:Context,kind:string,clipId?:string):string{return path.join(ctx.episodeDir,...(clipId?['klipy',identifier(clipId)]:[]),'artefakty',identifier(kind));}
export async function latest<T>(ctx:Context,kind:string,clipId?:string,schema?:{parse:(v:unknown)=>T}):Promise<T|undefined>{
  const dir=artifactDir(ctx,kind,clipId);
  let pointer:{path:string;hash:string};
  try{pointer=await readJson(path.join(dir,'latest.json'));}catch(e){if((e as NodeJS.ErrnoException).code==='ENOENT'||String(e).includes('Missing file:'))return undefined;throw e;}
  const target=await ensureInsideRoot(pointer.path,{existing:true});
  if(path.dirname(target)!==dir||await hashFile(target)!==pointer.hash)throw new Error(`Corrupt ${kind} revision pointer`);
  const value=await readJson<T>(target);return schema?schema.parse(value):value;
}
export async function nextRevision(ctx:Context,kind:string,clipId?:string):Promise<number>{
  const dir=artifactDir(ctx,kind,clipId);let names:string[]=[];try{names=await fs.readdir(dir);}catch(e){if((e as NodeJS.ErrnoException).code!=='ENOENT')throw e;}
  return 1+Math.max(0,...names.map(n=>/^r(\d+)\.json$/.exec(n)).filter(Boolean).map(m=>Number(m![1])));
}
export async function saveRevision<T extends {revision:number}>(ctx:Context,kind:string,value:T,clipId?:string,options:{expectedHash?:string|null}={}):Promise<T>{
  writable(ctx);const dir=artifactDir(ctx,kind,clipId);
  return withLock(path.join(dir,'.write.lock'),async()=>{
    const file=path.join(dir,`r${String(value.revision).padStart(4,'0')}.json`);
    const existing=await latest<T>(ctx,kind,clipId);
    if('expectedHash' in options&&(existing?hashArtifact(existing):null)!==options.expectedHash)throw new Error(`Concurrent ${kind} revision changed; recovery requires the recorded parent`);
    if(existing&&existing.revision>value.revision)throw new Error(`Stale ${kind} revision ${value.revision}`);
    await atomicWriteJson(file,value);
    await atomicWriteJson(path.join(dir,'latest.json'),{path:file,hash:await hashFile(file),revision:value.revision},{immutable:false});
    return value;
  });
}
export async function implementationHash(files:string[]):Promise<string>{return hashArtifact(await Promise.all(files.map(async p=>[p,await hashFile(path.join(projectRoot,p))])));}
export class BlockedError extends Error {constructor(message:string){super(message);this.name='BlockedError';}}
export interface PhaseResult<T>{value:T;cached:boolean;manifest:RunManifest}
/** Cache entries are evidence-backed receipts: every declared output is rehashed on a hit. */
export async function phase<T>(ctx:Context,options:{name:string;clipId?:string;inputs:Record<string,string>;implementation:string[];config?:unknown;attempts?:number;force?:boolean;tool?:string;toolVersion?:string;schema?:ZodTypeAny;canReuse?:(value:T)=>Promise<boolean>;run:(id:string)=>Promise<{value:T;files?:string[];model?:string}>}):Promise<PhaseResult<T>>{
  writable(ctx);const name=identifier(options.name),clipId=options.clipId;
  const impl=await implementationHash(['system/schemas/index.ts','system/pipeline/store.ts',...options.implementation]);
  const inputs={...options.inputs,implementation:impl,config:hashArtifact(options.config??{})};
  const key=hashArtifact({name,inputs}),dir=path.join(ctx.episodeDir,'behy',...(clipId?[identifier(clipId)]:[]),name),cache=path.join(dir,`${key}.cache.json`);
  return withLock(path.join(dir,`${key}.lock`),async()=>{
    if(!options.force){
      let receipt:{manifest:RunManifest;value:T}|undefined;
      try{receipt=await readJson(cache);}catch(e){if(!String(e).includes('Missing file:')&&(e as NodeJS.ErrnoException).code!=='ENOENT')throw e;}
      if(receipt){
        const m=RunManifestSchema.parse(receipt.manifest);let intact=m.status==='succeeded';
        for(const out of Object.values(m.outputs)){try{if(await hashFile(out.path)!==out.hash)intact=false;}catch{intact=false;}}
        if(intact){const value=options.schema?options.schema.parse(receipt.value) as T:receipt.value;if(!options.canReuse||await options.canReuse(value))return {value,cached:true,manifest:m};}
      }
    }
    await fs.mkdir(dir,{recursive:true});
    for(const n of await fs.readdir(dir))if(n.startsWith(key)&&n.endsWith('.manifest.json')){
      const p=path.join(dir,n),old=await readJson<RunManifest>(p);
      if(old.status==='running')await atomicWriteJson(p,{...old,status:'failed',error:'Interrupted owner; recovered under phase lock',finishedAt:new Date().toISOString()},{immutable:false});
    }
    for(let attempt=1;attempt<=(options.attempts??1);attempt++){
      const id=`${key}-${randomUUID()}`,manifestPath=path.join(dir,`${id}.manifest.json`);
      let manifest=RunManifestSchema.parse({...base(ctx,1,inputs),id,clipId,phase:name,status:'running',cacheKey:key,inputs,outputs:{},tool:options.tool??'xvadur-klipy',toolVersion:options.toolVersion??'1.0.0',startedAt:new Date().toISOString(),attempt});
      await atomicWriteJson(manifestPath,manifest);
      try{
        const result=await options.run(id),value=options.schema?options.schema.parse(result.value) as T:result.value;
        const payload=path.join(dir,`${id}.result.json`);await atomicWriteJson(payload,value);
        const files=[payload,...(result.files??[])];const outputs=Object.fromEntries(await Promise.all(files.map(async(p,i)=>[String(i),{path:await ensureInsideRoot(p,{existing:true}),hash:await hashFile(p)}])));
        manifest=RunManifestSchema.parse({...manifest,status:'succeeded',outputs,model:result.model,finishedAt:new Date().toISOString()});
        await atomicWriteJson(manifestPath,manifest,{immutable:false});await atomicWriteJson(cache,{manifest,value},{immutable:false});
        return {value,cached:false,manifest};
      }catch(e){
        manifest=RunManifestSchema.parse({...manifest,status:e instanceof BlockedError?'blocked':'failed',error:(e as Error).message,finishedAt:new Date().toISOString()});
        await atomicWriteJson(manifestPath,manifest,{immutable:false});
        if(attempt===(options.attempts??1)||e instanceof BlockedError||/403|401|oauth|credential|not logged/i.test((e as Error).message))throw e;
      }
    }
    throw new Error('Unreachable phase retry state');
  },{timeoutMs:3600000});
}
export async function listClipIds(ctx:Context):Promise<string[]>{try{return (await fs.readdir(path.join(ctx.episodeDir,'klipy'),{withFileTypes:true})).filter(x=>x.isDirectory()).map(x=>identifier(x.name)).sort();}catch(e){if((e as NodeJS.ErrnoException).code==='ENOENT')return [];throw e;}}
