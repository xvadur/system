export type RenderResources={ready:boolean;reasons:string[];freeDiskBytes:number;freeMemoryBytes:number;minFreeDiskBytes:number;minFreeMemoryBytes:number};
export function assessRenderResources(input:{freeDiskBytes:number;freeMemoryBytes:number;minFreeDiskBytes?:number;minFreeMemoryBytes?:number}):RenderResources;
export function availableMemory():Promise<{bytes:number;method:string}>;
export function withHeavyRender<T>(root:string,operation:()=>Promise<T>,options?:{timeoutMs?:number;minFreeDiskBytes?:number;minFreeMemoryBytes?:number}):Promise<T>;
