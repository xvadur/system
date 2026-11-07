import {constants, createReadStream} from 'node:fs';
import * as fs from 'node:fs/promises';
import path from 'node:path';
import {fileURLToPath} from 'node:url';
import {createHash, randomUUID} from 'node:crypto';
import {spawn} from 'node:child_process';
import {withHeavyRender} from '../runtime/resource-gates.mjs';

// The isolated authoring code snapshot has its own module/dependency root,
// while all canonical artifacts still belong to the explicit data workspace.
export const projectRoot = path.resolve(process.env.XVADUR_PROJECT_ROOT??fileURLToPath(new URL('../../', import.meta.url)));
const inside = (root:string,p:string) => p===root || p.startsWith(root+path.sep);

/** Both the lexical path and every existing ancestor must stay in the new root. */
export async function ensureInsideRoot(input:string, options:{existing?:boolean}={}):Promise<string> {
  if(input.includes('\0')) throw new Error('NUL in path');
  const absolute=path.resolve(projectRoot,input);
  if(!inside(projectRoot,absolute)) throw new Error(`Path is outside project root: ${absolute}`);
  const realRoot=await fs.realpath(projectRoot);
  let ancestor=absolute;
  for(;;){
    try {
      const real=await fs.realpath(ancestor);
      if(!inside(realRoot,real)) throw new Error(`Real path escapes project root: ${absolute}`);
      break;
    } catch(error) {
      if((error as NodeJS.ErrnoException).code!=='ENOENT') throw error;
      if(options.existing && ancestor===absolute) throw new Error(`Missing file: ${absolute}`);
      const parent=path.dirname(ancestor);
      if(parent===ancestor) throw new Error(`Cannot validate path: ${absolute}`);
      ancestor=parent;
    }
  }
  return absolute;
}

export async function hashFile(input:string):Promise<string> {
  const p=await ensureInsideRoot(input,{existing:true});
  const h=createHash('sha256');
  for await(const chunk of createReadStream(p)) h.update(chunk);
  return h.digest('hex');
}

export async function atomicWriteFile(input:string,data:string|Uint8Array,options:{immutable?:boolean}={}):Promise<void> {
  const p=await ensureInsideRoot(input);
  await fs.mkdir(path.dirname(p),{recursive:true});
  await ensureInsideRoot(path.dirname(p),{existing:true});
  const temp=await ensureInsideRoot(path.join(path.dirname(p),`.${path.basename(p)}.${process.pid}.${randomUUID()}.tmp`));
  const bytes=typeof data==='string'?Buffer.from(data):Buffer.from(data);
  let handle:fs.FileHandle|undefined;
  try {
    handle=await fs.open(temp,constants.O_CREAT|constants.O_EXCL|constants.O_WRONLY,0o600);
    await handle.writeFile(bytes); await handle.sync(); await handle.close(); handle=undefined;
    await ensureInsideRoot(p);
    if(options.immutable ?? true){
      try {await fs.link(temp,p);} catch(error){
        if((error as NodeJS.ErrnoException).code!=='EEXIST')throw error;
        const current=await fs.readFile(await ensureInsideRoot(p,{existing:true}));
        if(!current.equals(bytes))throw new Error(`Immutable artifact already exists: ${p}`);
      }
    } else await fs.rename(temp,p);
  } finally {await handle?.close();await fs.rm(temp,{force:true});}
}
export async function atomicWriteJson(input:string,value:unknown,options:{immutable?:boolean}={}):Promise<void> {
  // Serialize completely before touching any destination.
  const serialized=JSON.stringify(value,null,2);
  if(serialized===undefined) throw new Error('Cannot persist undefined JSON');
  await atomicWriteFile(input,serialized+'\n',options);
}
export async function readJson<T=unknown>(input:string):Promise<T> {
  return JSON.parse(await fs.readFile(await ensureInsideRoot(input,{existing:true}),'utf8')) as T;
}

export async function copyImport(source:string,destination:string):Promise<string> {
  const src=await fs.realpath(path.resolve(source));
  const info=await fs.stat(src);
  if(!info.isFile())throw new Error('Import source must be a regular file');
  const dest=await ensureInsideRoot(destination);
  await fs.mkdir(path.dirname(dest),{recursive:true});
  await ensureInsideRoot(path.dirname(dest),{existing:true});
  const tmp=path.join(path.dirname(dest),`.import.${randomUUID()}.tmp`);
  try{
    await fs.copyFile(src,tmp,constants.COPYFILE_EXCL|constants.COPYFILE_FICLONE);
    const h=await hashFile(tmp);
    try {await fs.link(tmp,dest);}catch(error){
      if((error as NodeJS.ErrnoException).code!=='EEXIST')throw error;
      if(await hashFile(dest)!==h)throw new Error(`Import destination already has different content: ${dest}`);
    }
    return h;
  }finally{await fs.rm(tmp,{force:true});}
}

const delay=(ms:number)=>new Promise<void>(resolve=>setTimeout(resolve,ms));
function alive(pid:number):boolean {try{process.kill(pid,0);return true;}catch(e){return (e as NodeJS.ErrnoException).code==='EPERM';}}
async function acquireLock(p:string):Promise<string|undefined>{
  await fs.mkdir(path.dirname(p),{recursive:true});await ensureInsideRoot(path.dirname(p),{existing:true});
  const token=randomUUID();
  try{
    const f=await fs.open(p,'wx',0o600);
    await f.writeFile(JSON.stringify({pid:process.pid,token,createdAt:new Date().toISOString()}));await f.close();return token;
  }catch(error){
    if((error as NodeJS.ErrnoException).code!=='EEXIST')throw error;
    // Only recover an abandoned owner's lock. Elapsed time alone never steals a live job.
    try {const owner=await readJson<{pid:number}>(p);if(Number.isInteger(owner.pid)&&!alive(owner.pid))await fs.rm(p,{force:true});}
    catch{const stat=await fs.stat(p).catch(()=>null);if(stat&&Date.now()-stat.mtimeMs>30000)await fs.rm(p,{force:true});}
    return undefined;
  }
}
async function releaseLock(p:string,token:string){try{const owner=await readJson<{token:string}>(p);if(owner.token===token)await fs.rm(p,{force:true});}catch{/* Already removed by its owner. */}}
export async function withLock<T>(input:string,fn:()=>Promise<T>,options:{timeoutMs?:number}={}):Promise<T>{
  const p=await ensureInsideRoot(input);const deadline=Date.now()+(options.timeoutMs??120000);let token:string|undefined;
  while(!(token=await acquireLock(p))){if(Date.now()>deadline)throw new Error(`Lock timeout: ${p}`);await delay(50);}
  try{return await fn();}finally{await releaseLock(p,token);}
}
export async function withSemaphore<T>(name:string,limit:number,fn:()=>Promise<T>):Promise<T>{
  if(!/^[a-z0-9-]+$/i.test(name)||!Number.isInteger(limit)||limit<1)throw new Error('Invalid semaphore');
  const dir=await ensureInsideRoot(`system/.cache/semaphores/${name}`);await fs.mkdir(dir,{recursive:true});
  const deadline=Date.now()+30*60*1000;
  for(;;){
    for(let i=0;i<limit;i++){
      const p=path.join(dir,`${i}.lock`),token=await acquireLock(p);
      if(token){try{return await fn();}finally{await releaseLock(p,token);}}
    }
    if(Date.now()>deadline)throw new Error(`Semaphore timeout: ${name}`);await delay(100);
  }
}

export type ProcessOptions={cwd?:string,input?:string,timeoutMs?:number,maxOutputBytes?:number,env?:NodeJS.ProcessEnv};
/** Failure still carries the bounded output already received, so a caller can
 * persist an interrupted tool audit rather than losing hours of work evidence. */
export class ProcessExecutionError extends Error {
  constructor(message:string,readonly reason:'timeout'|'output_limit'|'spawn',readonly stdout:string,readonly stderr:string,readonly outputBytes:number,options?:ErrorOptions){super(message,options);this.name='ProcessExecutionError';}
}
export async function runProcess(binary:string,args:string[],options:ProcessOptions={}):Promise<{stdout:string,stderr:string,code:number}>{
  return path.basename(binary)==='ffmpeg'?withHeavyRender(projectRoot,()=>runProcessRaw(binary,args,options)):runProcessRaw(binary,args,options);
}
async function runProcessRaw(binary:string,args:string[],options:ProcessOptions):Promise<{stdout:string,stderr:string,code:number}>{
  const cwd=await ensureInsideRoot(options.cwd??projectRoot,{existing:true});
  return new Promise((resolve,reject)=>{
    const child=spawn(binary,args,{cwd,env:{...process.env,...options.env},stdio:['pipe','pipe','pipe'],shell:false});
    let stdout='',stderr='',bytes=0,settled=false;
    const finishError=(error:Error,reason:ProcessExecutionError['reason'])=>{if(settled)return;settled=true;child.kill('SIGTERM');clearTimeout(timer);reject(new ProcessExecutionError(error.message,reason,stdout,stderr,bytes,{cause:error}));};
    const timer=setTimeout(()=>finishError(new Error(`Process timeout after ${options.timeoutMs??120000}ms: ${path.basename(binary)}`),'timeout'),options.timeoutMs??120000);
    const take=(kind:'stdout'|'stderr',data:Buffer)=>{
      if(settled)return;
      const limit=options.maxOutputBytes??16*1024*1024,retained=data.subarray(0,Math.max(0,limit-bytes));bytes+=data.length;
      if(kind==='stdout')stdout+=retained.toString();else stderr+=retained.toString();
      if(bytes>limit)finishError(new Error(`Process output limit exceeded: ${path.basename(binary)}`),'output_limit');
    };
    child.stdout.on('data',d=>take('stdout',d));child.stderr.on('data',d=>take('stderr',d));
    child.on('error',error=>finishError(error,'spawn'));
    child.on('close',code=>{clearTimeout(timer);if(!settled){settled=true;resolve({stdout,stderr,code:code??-1});}});
    child.stdin.on('error',()=>{});child.stdin.end(options.input??'');
  });
}

export function identifier(value:string):string{
  if(!/^[A-Za-z0-9][A-Za-z0-9_.-]{0,99}$/.test(value)||value.includes('..'))throw new Error(`Invalid identifier: ${value}`);
  return value;
}
