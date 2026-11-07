import fs from 'node:fs/promises';
import os from 'node:os';
import path from 'node:path';

// Exact catalog slugs, verified against Codex 0.166.0-alpha.6 and the official
// models/configuration reference on 2026-11-04. Never rewrite an unavailable
// requested model to another model or silently fall back to the CLI default.
export const CODEX_ROUTES=Object.freeze({
  execution:Object.freeze({model:'gpt-6.1-sol',reasoningEffort:'ultra'}),
  concept:Object.freeze({model:'gpt-6-astra',reasoningEffort:'ultra'}),
});
export function codexRoute({role='execution',model,reasoningEffort}={}) {
  if(!Object.hasOwn(CODEX_ROUTES,role))throw new Error('Unknown Codex task role');
  const route={role,model:model??CODEX_ROUTES[role].model,reasoningEffort:reasoningEffort??CODEX_ROUTES[role].reasoningEffort};
  if(typeof route.model!=='string'||!/^gpt-[a-z0-9.-]+$/.test(route.model))throw new Error('Codex requires an exact model catalog slug');
  if(!['low','medium','high','xhigh','max','ultra'].includes(route.reasoningEffort))throw new Error('Unsupported Codex reasoning effort');
  return route;
}
export function codexRouteArgs(route) {
  const checked=codexRoute(route);
  return ['--model',checked.model,'-c',`model_reasoning_effort=${JSON.stringify(checked.reasoningEffort)}`,
    ...(checked.reasoningEffort==='ultra'?['--enable','multi_agent','-c','agents.max_threads=3']:[])];
}
export function validateCodexCatalog(route,catalog) {
  const selected=catalog?.models?.find(entry=>entry.slug===route.model);
  if(!selected)throw new Error(`Requested Codex model is absent from the local catalog: ${route.model}`);
  if(!selected.supported_reasoning_levels?.some(level=>level.effort===route.reasoningEffort))throw new Error(`Requested reasoning effort is not advertised for ${route.model}: ${route.reasoningEffort}`);
  return {model:selected.slug,reasoningEfforts:selected.supported_reasoning_levels.map(level=>level.effort)};
}
/** Read-only prerequisite check. Auth content is reduced to a boolean and never
 * returned or persisted. A catalog entry is not proof of a successful turn.
 */
export async function inspectCodexRuntime({binary='codex',run,cwd,catalogPath=path.join(process.env.CODEX_HOME??path.join(os.homedir(),'.codex'),'models_cache.json'),routes=[codexRoute({role:'execution'}),codexRoute({role:'concept'})]}) {
  const version=await run(binary,['--version'],{cwd,timeoutMs:15000,maxOutputBytes:65536});
  if(version.code!==0)throw new Error('Configured Codex CLI is unavailable');
  const authentication=await run(binary,['login','status'],{cwd,timeoutMs:15000,maxOutputBytes:65536});
  if(authentication.code!==0)throw new Error('Codex CLI authentication is unavailable');
  const catalog=JSON.parse(await fs.readFile(catalogPath,'utf8'));
  return {cliVersion:version.stdout.trim(),authenticated:true,catalogSource:'local-model-cache',catalogFetchedAt:catalog.fetched_at??null,
    routes:routes.map(route=>({...route,...validateCodexCatalog(route,catalog)})),modelTurnVerified:false};
}
