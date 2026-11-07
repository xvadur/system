export type CodexTaskRole='execution'|'concept';
export type CodexReasoningEffort='low'|'medium'|'high'|'xhigh'|'max'|'ultra';
export type CodexRoute={role:CodexTaskRole;model:string;reasoningEffort:CodexReasoningEffort};
export const CODEX_ROUTES:Readonly<Record<CodexTaskRole,Readonly<{model:string;reasoningEffort:CodexReasoningEffort}>>>;
export function codexRoute(options?:{role?:CodexTaskRole;model?:string;reasoningEffort?:CodexReasoningEffort}):CodexRoute;
export function codexRouteArgs(route:CodexRoute):string[];
export function validateCodexCatalog(route:CodexRoute,catalog:unknown):{model:string;reasoningEfforts:string[]};
export function inspectCodexRuntime(options:{binary?:string;run:(binary:string,args:string[],options:{cwd?:string;timeoutMs:number;maxOutputBytes:number})=>Promise<{code:number;stdout:string;stderr:string}>;cwd?:string;catalogPath?:string;routes?:CodexRoute[]}):Promise<{cliVersion:string;authenticated:boolean;catalogSource:string;catalogFetchedAt:string|null;routes:Array<CodexRoute&{reasoningEfforts:string[]}>;modelTurnVerified:boolean}>;
