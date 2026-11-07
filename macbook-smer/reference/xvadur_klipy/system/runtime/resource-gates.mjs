import fs from 'node:fs/promises';
import os from 'node:os';
import path from 'node:path';
import {randomUUID} from 'node:crypto';
import {execFile} from 'node:child_process';
import {promisify} from 'node:util';
import {AsyncLocalStorage} from 'node:async_hooks';
const heavyScope=new AsyncLocalStorage();

/** macOS keeps reclaimable inactive pages outside os.freemem(). Linux exposes
 * MemAvailable directly. A low count of completely unused pages alone must not
 * block every render on an otherwise healthy Mac.
 */
export async function availableMemory() {
  if(process.platform==='darwin')try{
    const {stdout}=await promisify(execFile)('/usr/bin/vm_stat',[],{timeout:5000,maxBuffer:65536});
    const pageSize=Number(stdout.match(/page size of (\d+) bytes/)?.[1]??4096);
    const pages=['free','inactive','speculative'].map(name=>Number(stdout.match(new RegExp(`Pages ${name}:\\s*(\\d+)`))?.[1]??0));
    if(pages.some(Boolean))return {bytes:pages.reduce((a,b)=>a+b,0)*pageSize,method:'vm_stat-free+inactive+speculative'};
  }catch{/* Conservative fallback below. */}
  if(process.platform==='linux')try{const text=await fs.readFile('/proc/meminfo','utf8'),kb=Number(text.match(/^MemAvailable:\s*(\d+) kB/m)?.[1]);if(kb>0)return {bytes:kb*1024,method:'linux-MemAvailable'};}catch{/* Conservative fallback below. */}
  return {bytes:os.freemem(),method:'os-freemem'};
}

export function assessRenderResources({freeDiskBytes,freeMemoryBytes,minFreeDiskBytes=1024**3,minFreeMemoryBytes=256*1024**2}) {
  const reasons=[];
  if(!Number.isFinite(freeDiskBytes)||freeDiskBytes<minFreeDiskBytes)reasons.push('insufficient_free_disk');
  if(!Number.isFinite(freeMemoryBytes)||freeMemoryBytes<minFreeMemoryBytes)reasons.push('insufficient_free_memory');
  return {ready:reasons.length===0,reasons,freeDiskBytes,freeMemoryBytes,minFreeDiskBytes,minFreeMemoryBytes};
}
const delay=ms=>new Promise(resolve=>setTimeout(resolve,ms));
const alive=pid=>{try{process.kill(pid,0);return true;}catch(error){return error.code==='EPERM';}};
/** Uses the existing renders/0.lock namespace: canonical and authored workers
 * share exactly one local heavy-render slot. This is not a second job registry.
 */
export async function withHeavyRender(root,operation,{timeoutMs=30*60*1000,minFreeDiskBytes,minFreeMemoryBytes}={}) {
  const realRoot=await fs.realpath(root);
  if(heavyScope.getStore()===realRoot)return operation();
  const directory=path.join(realRoot,'system/.cache/semaphores/renders');
  let ancestor=directory;
  for(;;)try{const real=await fs.realpath(ancestor);if(real!==realRoot&&!real.startsWith(realRoot+path.sep))throw new Error('Render lock directory escapes project root');break;}catch(error){if(error.code!=='ENOENT')throw error;ancestor=path.dirname(ancestor);}
  await fs.mkdir(directory,{recursive:true});
  const realDirectory=await fs.realpath(directory);
  if(!realDirectory.startsWith(realRoot+path.sep))throw new Error('Render lock directory escapes project root');
  const lock=path.join(directory,'0.lock'),token=randomUUID(),deadline=Date.now()+timeoutMs;
  for(;;){
    try{const file=await fs.open(lock,'wx',0o600);try{await file.writeFile(JSON.stringify({pid:process.pid,token,createdAt:new Date().toISOString()}));}finally{await file.close();}break;}
    catch(error){
      if(error.code!=='EEXIST')throw error;
      try{const owner=JSON.parse(await fs.readFile(lock,'utf8'));if(Number.isInteger(owner.pid)&&!alive(owner.pid))await fs.rm(lock,{force:true});}
      catch(error){if(error.code!=='ENOENT'){const stat=await fs.stat(lock).catch(()=>null);if(stat&&Date.now()-stat.mtimeMs>30000)await fs.rm(lock,{force:true});}}
      if(Date.now()>=deadline)throw new Error('Heavy render slot timeout');await delay(100);
    }
  }
  try{
    const disk=await fs.statfs(realRoot),memory=await availableMemory(),resources={...assessRenderResources({freeDiskBytes:disk.bavail*disk.bsize,freeMemoryBytes:memory.bytes,minFreeDiskBytes,minFreeMemoryBytes}),memoryMethod:memory.method};
    if(!resources.ready){const error=new Error(`Render waiting for resources: ${resources.reasons.join(', ')}`);error.code='RESOURCE_PRESSURE';error.resources=resources;throw error;}
    return await heavyScope.run(realRoot,operation);
  }finally{try{const owner=JSON.parse(await fs.readFile(lock,'utf8'));if(owner.token===token)await fs.rm(lock,{force:true});}catch{/* Removed only by the owning process. */}}
}
