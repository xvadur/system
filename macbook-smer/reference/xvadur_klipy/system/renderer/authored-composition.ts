import fs from 'node:fs/promises';
import path from 'node:path';
import {createHash} from 'node:crypto';
import ts from 'typescript';
import {AuthoredCompositionManifestSchema,type AuthoredCompositionManifest} from '../schemas/authored-composition';
import {hashArtifact,type Timeline} from '../schemas/index';

const sha=(bytes:Uint8Array)=>createHash('sha256').update(bytes).digest('hex');
const code=/\.[cm]?[jt]sx?$/;
const extensions=['','.ts','.tsx','.js','.jsx','.mjs','.cjs','.json','/index.ts','/index.tsx','/index.js','/index.jsx'];
const packageName=(specifier:string)=>specifier.startsWith('@')?specifier.split('/').slice(0,2).join('/'):specifier.split('/')[0];
export type VerifiedAuthoredComposition={manifest:AuthoredCompositionManifest;manifestHash:string;implementationHash:string;files:Array<{path:string;hash:string}>};

async function sourceFile(root:string,relative:string){
  const real=await fs.realpath(path.join(root,relative));
  const rel=path.relative(root,real);
  if(rel.startsWith('..')||path.isAbsolute(rel)||(await fs.stat(real)).isDirectory())throw new Error(`Authored source escapes project or is not a file: ${relative}`);
  return real;
}

/** Validate the complete local import graph. This is provenance validation,
 * not a sandbox for untrusted arbitrary JavaScript. No fixed scene catalog. */
export async function verifyAuthoredComposition(projectRoot:string,input:unknown,timeline:Timeline):Promise<VerifiedAuthoredComposition>{
  const manifest=AuthoredCompositionManifestSchema.parse(input),root=await fs.realpath(projectRoot);
  if(manifest.timelineHash!==hashArtifact(timeline))throw new Error('Authored composition targets another Timeline revision');
  const runtimeRoot=process.env.XVADUR_AUTHORED_RUNTIME_ROOT??path.join(root,'system');
  const runtime=JSON.parse(await fs.readFile(path.join(runtimeRoot,'package.json'),'utf8')) as {dependencies:Record<string,string>};
  if(runtime.dependencies.remotion!==manifest.remotionVersion)throw new Error('Authored composition runtime version changed');
  const pinned=new Map(manifest.files.map(file=>[file.path,file]));
  const local=(owner:string,specifier:string)=>{
    const base=path.posix.normalize(path.posix.join(path.posix.dirname(owner),specifier));
    const match=extensions.map(extension=>base+extension).find(candidate=>pinned.has(candidate));
    if(!match)throw new Error(`Unpinned authored import ${specifier} in ${owner}`);
    return match;
  };
  const imports=new Map<string,string[]>();
  for(const file of manifest.files){
    const bytes=await fs.readFile(await sourceFile(root,file.path));
    if(sha(bytes)!==file.hash)throw new Error(`Authored source hash changed: ${file.path}`);
    if(!code.test(file.path)&&!file.path.endsWith('.json'))throw new Error(`Unsupported authored source type: ${file.path}; stage media through Timeline assets`);
    if(!code.test(file.path)){JSON.parse(bytes.toString('utf8'));continue;}
    const ast=ts.createSourceFile(file.path,bytes.toString('utf8'),ts.ScriptTarget.Latest,true,file.path.endsWith('x')?ts.ScriptKind.TSX:ts.ScriptKind.TS);
    const dependencies:string[]=[];
    const inspect=(specifier:string)=>{
      if(specifier==='@xvadur/authoring')return;
      if(specifier.startsWith('.')){dependencies.push(local(file.path,specifier));return;}
      const name=packageName(specifier);
      if(specifier.startsWith('/')||specifier.startsWith('node:')||!runtime.dependencies[name])throw new Error(`Authored import is not a pinned browser runtime dependency: ${specifier}`);
    };
    const visit=(node:ts.Node)=>{
      if((ts.isImportDeclaration(node)||ts.isExportDeclaration(node))&&node.moduleSpecifier){
        if(!ts.isStringLiteral(node.moduleSpecifier))throw new Error('Authored module import must be literal');
        inspect(node.moduleSpecifier.text);
      }
      if(ts.isCallExpression(node)&&(node.expression.kind===ts.SyntaxKind.ImportKeyword||node.expression.getText(ast)==='require')){
        if(node.arguments.length!==1||!ts.isStringLiteral(node.arguments[0]))throw new Error('Authored dynamic import must have one literal pinned module');
        inspect(node.arguments[0].text);
      }
      ts.forEachChild(node,visit);
    };visit(ast);imports.set(file.path,dependencies);
  }
  const reachable=new Set<string>();
  const walk=(file:string)=>{if(reachable.has(file))return;reachable.add(file);for(const child of imports.get(file)??[])walk(child);};walk(manifest.entryPath);
  for(const file of manifest.files)if(!reachable.has(file.path))throw new Error(`Authored manifest contains an unreachable source: ${file.path}`);
  const files=[...manifest.files].sort((a,b)=>a.path.localeCompare(b.path));
  return {manifest,manifestHash:hashArtifact(manifest),implementationHash:hashArtifact(files),files};
}

/** Freeze the verified code bytes into this render, preserving relative imports. */
export async function stageAuthoredComposition(projectRoot:string,runDir:string,verified:VerifiedAuthoredComposition){
  const sourceRoot=path.join(runDir,'authored-source');
  for(const file of verified.files){
    const bytes=await fs.readFile(await sourceFile(await fs.realpath(projectRoot),file.path));
    if(sha(bytes)!==file.hash)throw new Error(`Authored source changed before staging: ${file.path}`);
    const destination=path.join(sourceRoot,file.path);await fs.mkdir(path.dirname(destination),{recursive:true});await fs.writeFile(destination,bytes,{flag:'wx'});await fs.chmod(destination,0o444);
  }
  const authoredImport='./authored-source/'+verified.manifest.entryPath;
  const entryPoint=path.join(runDir,'authored-entry.tsx');
  const componentId=`Authored-${verified.manifest.id}`;
  const imported=verified.manifest.exportName==='default'?'import Scene':`import {${verified.manifest.exportName} as Scene}`;
  const entry=`import React from 'react';\nimport {Composition,registerRoot} from 'remotion';\nimport {AuthoredCompositionShell} from '@xvadur/authoring';\n${imported} from ${JSON.stringify(authoredImport)};\nconst Clip=({document})=><AuthoredCompositionShell document={document} Scene={Scene}/>;\nconst Root=()=> <Composition id=${JSON.stringify(componentId)} component={Clip} durationInFrames={1} width={1080} height={1920} fps={30} calculateMetadata={({props})=>({durationInFrames:props.document.durationInFrames,width:props.document.width,height:props.document.height,fps:props.document.fps})}/>;\nregisterRoot(Root);\n`;
  await fs.mkdir(sourceRoot,{recursive:true});await fs.writeFile(entryPoint,entry,{flag:'wx'});
  // A local package boundary keeps Webpack's cache inside the writable render
  // workspace even when the CLI's cwd is the read-only project root. This is
  // bundler metadata only; dependencies still come from the pinned runtime.
  await fs.writeFile(path.join(runDir,'package.json'),JSON.stringify({name:'xvadur-authored-render',private:true,version:'1.0.0'}),{flag:'wx'});
  // The staged source lives under the data project, which may run another
  // Remotion version. A nearest dependency boundary prevents its node_modules
  // from winning resolution; nested package dependencies keep normal lookup.
  if(process.env.XVADUR_AUTHORED_RUNTIME_ROOT)await fs.symlink(path.join(process.env.XVADUR_AUTHORED_RUNTIME_ROOT,'node_modules'),path.join(runDir,'node_modules'),'dir');
  const manifestPath=path.join(runDir,'authored-composition.json');await fs.writeFile(manifestPath,JSON.stringify(verified,null,2),{flag:'wx'});
  return {entryPoint,componentId,manifestPath,sourceRoot};
}
