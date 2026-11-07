import fs from 'node:fs/promises';
import {constants, createReadStream} from 'node:fs';
import {createHash, randomUUID} from 'node:crypto';
import path from 'node:path';

/** File bytes are streamed, including multi-GB episode originals. */
export async function streamSha256(file) {
  const digest = createHash('sha256');
  for await (const bytes of createReadStream(file)) digest.update(bytes);
  return digest.digest('hex');
}
const fingerprint = (s) => [s.dev,s.ino,s.size,s.mtimeNs,s.ctimeNs,s.mode].map(String).join(':');
const hashText = (text) => createHash('sha256').update(text).digest('hex');
const within = (root,file) => file===root || file.startsWith(root+path.sep);
async function regular(file) {
  const stat = await fs.lstat(file,{bigint:true});
  if (!stat.isFile() || stat.isSymbolicLink()) throw new Error('Media cache requires a regular file');
  return {fingerprint:fingerprint(stat),size:stat.size,ino:stat.ino,dev:stat.dev};
}
async function contained(root,file) {
  const absolute=path.resolve(root,file);
  if(!within(root,absolute))throw new Error('Media cache path escapes project root');
  let ancestor=absolute;
  for(;;)try {
    if(!within(root,await fs.realpath(ancestor)))throw new Error('Media cache symlink escapes project root');
    return absolute;
  }catch(error){if(error.code!=='ENOENT')throw error;ancestor=path.dirname(ancestor);}
}

/** An optimization over canonical manifests, never an authority for acceptance.
 * Receipts bind source and cache inode/size/nanosecond mtime+ctime. Any change
 * forces streaming verification. Media is always an independent CoW clone or
 * copy; no hardlink or symlink ever points at the original.
 */
export async function createMediaCache(projectRoot, directory='system/.cache/media') {
  const root=await fs.realpath(projectRoot),cache=await contained(root,directory);
  await fs.mkdir(cache,{recursive:true});
  await contained(root,cache);
  const objects=path.join(cache,'objects'),receipts=path.join(cache,'receipts');
  for(const dir of [objects,receipts]){await contained(root,dir);await fs.mkdir(dir,{recursive:true});}
  async function resolve(sourceFile,expectedHash) {
    if(expectedHash&&!/^[a-f0-9]{64}$/.test(expectedHash))throw new Error('Invalid expected media hash');
    const source=await contained(root,sourceFile),real=await fs.realpath(source);
    const initial=await regular(real),receiptFile=path.join(receipts,hashText(real)+'.json');
    let receipt;
    try{receipt=JSON.parse(await fs.readFile(await contained(root,receiptFile),'utf8'));}catch(error){if(error.code!=='ENOENT'&&!(error instanceof SyntaxError))throw error;}
    const extension=/^\.[a-z0-9]{1,10}$/i.test(path.extname(real))?path.extname(real).toLowerCase():'.bin';
    const reusable=receipt?.version===1 && /^[a-f0-9]{64}$/.test(receipt.hash) && receipt.source===real && receipt.sourceFingerprint===initial.fingerprint && (!expectedHash||receipt.hash===expectedHash);
    let digest=reusable?receipt.hash:await streamSha256(real);
    if(expectedHash&&digest!==expectedHash)throw new Error('Media source hash mismatch');
    const filename=digest+extension,object=await contained(root,path.join(objects,filename));
    let cached=await regular(object).catch(error=>{if(error.code==='ENOENT')return undefined;throw error;});
    const cacheHit=Boolean(reusable&&cached&&receipt.cacheFingerprint===cached.fingerprint);
    if(cached&&!cacheHit&&await streamSha256(object)!==digest)throw new Error('Immutable media cache bytes changed');
    if(!cached){
      const temporary=path.join(objects,'.pending-'+randomUUID());
      try{
        await fs.copyFile(real,temporary,constants.COPYFILE_EXCL|constants.COPYFILE_FICLONE);
        if(await streamSha256(temporary)!==digest)throw new Error('Media source changed while caching');
        await fs.chmod(temporary,0o444);
        try{await fs.link(temporary,object);}catch(error){if(error.code!=='EEXIST')throw error;if(await streamSha256(object)!==digest)throw new Error('Immutable media cache collision');}
      }finally{await fs.rm(temporary,{force:true});}
      cached=await regular(object);
    }
    if((await regular(real)).fingerprint!==initial.fingerprint)throw new Error('Media source changed while caching');
    const temporary=receiptFile+'.'+randomUUID()+'.tmp';
    try{
      await fs.writeFile(temporary,JSON.stringify({version:1,source:real,sourceFingerprint:initial.fingerprint,cacheFingerprint:cached.fingerprint,hash:digest})+'\n',{flag:'wx',mode:0o600});
      await fs.rename(temporary,receiptFile);
    }finally{await fs.rm(temporary,{force:true});}
    return {path:object,hash:digest,filename,cacheHit,sourceHashComputed:!reusable,cacheFingerprint:cached.fingerprint};
  }
  async function stage(entry,destination) {
    const source=await contained(root,entry.path),target=await contained(root,destination),before=await regular(source);
    if(before.fingerprint!==entry.cacheFingerprint)throw new Error('Media cache changed between verification and staging');
    await fs.mkdir(path.dirname(target),{recursive:true});await contained(root,path.dirname(target));
    try{await fs.copyFile(source,target,constants.COPYFILE_EXCL|constants.COPYFILE_FICLONE);}
    catch(error){if(error.code!=='EEXIST')throw error;if(await streamSha256(target)!==entry.hash)throw new Error('Immutable staging collision');}
    if((await regular(source)).fingerprint!==before.fingerprint)throw new Error('Media cache changed while staging');
    const staged=await regular(target);
    if(staged.size!==before.size||(staged.ino===before.ino&&staged.dev===before.dev))throw new Error('Media staging must be an independent clone');
    await fs.chmod(target,0o444);
    return target;
  }
  return {resolve,stage};
}
