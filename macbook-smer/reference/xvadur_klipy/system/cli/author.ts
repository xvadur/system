/** Narrow bootstrap for the separately pinned authoring runtime. Keep legacy
 * CLI/workplace imports out: their dependencies can change independently. */
import {context} from '../pipeline/store.ts';
import {prepareAuthoring,verifyAuthoring,runAuthoring,createAuthoringManifest,checkAuthoringManifest,renderAuthoring,checkAuthoringRender} from '../pipeline/authoring.ts';

const help=`XVADUR Remotion Reel — isolated authoring runtime 4.0.529
python3 system/cli/klipy.py autor --epizoda ID --klip ID --akcia AKCIA
priprav [--timeline JSON] [--nazov ID]
stav|spusti [--autor-dir CESTA] [--zadanie TEXT]
manifest --autor-dir CESTA --entry src/Clip.tsx --files src/Clip.tsx,... --revizia N [--treatment TREATMENT.md]
over|render --autor-dir CESTA --manifest JSON [--kvalita draft|master] [--frames OD,DO] [--stills N,N]
kontrola --autor-dir CESTA
Spoločné: --klient fiki; testy --fixture --workspace system/tests/work/NAME.
Ranges are half-open. A render or technical check is not creative acceptance.
`;

async function main(){
 const args=process.argv.slice(3);
 if(args.includes('--help')||!args.length){console.log(help);return;}
 const booleans=new Set(['fixture']),values=new Set(['klient','epizoda','klip','workspace','akcia','timeline','nazov','autor-dir','zadanie','entry','files','revizia','export-name','treatment','manifest','kvalita','frames','stills']);
 const flags:Record<string,string|boolean>={};
 for(let i=0;i<args.length;i++){
  const arg=args[i]!;if(!arg.startsWith('--'))throw new Error(`Neznámy argument ${arg}`);const key=arg.slice(2);
  if(booleans.has(key))flags[key]=true;
  else if(values.has(key)){const value=args[++i];if(!value||value.startsWith('--'))throw new Error(`Chýba --${key}`);flags[key]=value;}
  else throw new Error(`Neznámy prepínač --${key}`);
 }
 const str=(key:string,required=false)=>{const value=flags[key];if(required&&typeof value!=='string')throw new Error(`Chýba --${key}`);return typeof value==='string'?value:undefined;};
 const numbers=(key:string)=>{const value=str(key)?.split(',').map(Number);if(value?.some(n=>!Number.isInteger(n)||n<0))throw new Error(`--${key} musí obsahovať celé nezáporné čísla`);return value;};
 const ctx=await context({clientId:str('klient'),episodeId:str('epizoda',true)!,fixture:!!flags.fixture,workspace:str('workspace')}),clipId=str('klip',true)!,directory=str('autor-dir'),action=str('akcia',true)!;
 let value:unknown;
 if(action==='priprav')value=await prepareAuthoring(ctx,clipId,{timelinePath:str('timeline'),label:str('nazov')});
 else if(action==='stav')value=await verifyAuthoring(ctx,clipId,directory??(await prepareAuthoring(ctx,clipId)).workspace);
 else if(action==='spusti')value=await runAuthoring(ctx,clipId,{directory,instruction:str('zadanie')});
 else if(action==='manifest')value=await createAuthoringManifest(ctx,clipId,{directory,entry:str('entry',true)!,files:str('files',true)!.split(',').filter(Boolean),revision:Number(str('revizia')??1),exportName:str('export-name'),treatmentPath:str('treatment')});
 else if(action==='over')value=await checkAuthoringManifest(ctx,clipId,{directory,manifestPath:str('manifest',true)!});
 else if(action==='render'){
  const frames=numbers('frames'),quality=str('kvalita')??'draft';
  if(frames&&(frames.length!==2||frames[1]!<=frames[0]!))throw new Error('--frames musí byť OD,DO s DO > OD');
  if(quality!=='draft'&&quality!=='master')throw new Error('Kvalita musí byť draft alebo master');
  value=await renderAuthoring(ctx,clipId,{directory,manifestPath:str('manifest',true)!,quality,frameRange:frames as [number,number]|undefined,inspectFrames:numbers('stills')});
 }else if(action==='kontrola')value=await checkAuthoringRender(ctx,clipId,directory);
 else throw new Error('Neznáma autorská akcia');
 console.log(JSON.stringify(value,null,2));
}
main().catch(error=>{console.error(JSON.stringify({status:error.name==='BlockedError'?'blocked':'failed',error:error.message},null,2));process.exitCode=1;});
