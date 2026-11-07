export type CachedMedia={path:string;hash:string;filename:string;cacheHit:boolean;sourceHashComputed:boolean;cacheFingerprint:string};
export function streamSha256(file:string):Promise<string>;
export function createMediaCache(projectRoot:string,directory?:string):Promise<{resolve(sourceFile:string,expectedHash?:string):Promise<CachedMedia>;stage(entry:CachedMedia,destination:string):Promise<string>}>;
