/**
 * Chrome's network Blob reader can reject a large raw 4K frame when available
 * disk falls below its Blob storage admission threshold. Reading the identical
 * response bytes into memory first keeps this short-lived frame off that path.
 * This only applies inside an authored render to the local Remotion frame proxy.
 */
export function installAuthoredFrameTransport():void{
  if(typeof window==='undefined'||typeof window.fetch!=='function')return;
  const marker=Symbol.for('xvadur.authored-frame-transport.v1');
  const state=window as unknown as Record<symbol,boolean>;
  if(state[marker])return;
  const original=window.fetch.bind(window);
  window.fetch=async(input:RequestInfo|URL,init?:RequestInit):Promise<Response>=>{
    const response=await original(input,init);
    const raw=typeof input==='string'?input:input instanceof URL?input.href:input.url;
    const url=new URL(raw,window.location.href);
    if(['localhost','127.0.0.1','[::1]'].includes(url.hostname)&&url.pathname==='/proxy'&&url.searchParams.has('src')&&url.searchParams.has('time')){
      Object.defineProperty(response,'blob',{configurable:true,value:async()=>new Blob([await response.arrayBuffer()],{type:response.headers.get('content-type')??''})});
    }
    return response;
  };
  state[marker]=true;
}
