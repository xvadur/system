import path from 'node:path';
import {readFile} from 'node:fs/promises';
import ts from 'typescript';
import manifest from './authored-manifest.json';
import journeyManifest from './journey-manifest.json';
import kitchenManifest from './kitchen-manifest.json';
import turtleManifest from './turtle-manifest.json';
import profileWhackManifest from './profile-whack-manifest.json';
import phonePaperManifest from './phone-paper-manifest.json';
import {hashArtifact} from '../schemas/index.ts';
import {hashFile,projectRoot} from '../pipeline/io.ts';
export function validateSceneImports(source:string,extraAllowed:string[]=[]){
 const ast=ts.createSourceFile('scene.tsx',source,ts.ScriptTarget.Latest,true,ts.ScriptKind.TSX);
 const allowed=new Set(['react','remotion','../types','./MediaStage',...extraAllowed]);
 const visit=(node:ts.Node)=>{
  if(ts.isImportDeclaration(node)&&(!ts.isStringLiteral(node.moduleSpecifier)||!allowed.has(node.moduleSpecifier.text)))throw new Error('Forbidden authored import');
  if(ts.isCallExpression(node)&&(/^(eval|Function|fetch|require)$/.test(node.expression.getText(ast))||node.expression.kind===ts.SyntaxKind.ImportKeyword))throw new Error('Forbidden authored dynamic execution');
  ts.forEachChild(node,visit);
 };visit(ast);
}
export async function verifyAuthoredImplementation(bindings?:Array<{sceneId:string;version:string;implementationHash:string}>){
 if(bindings){
  for(const b of bindings){
   if(b.sceneId==='media-stage'){if(b.version!==manifest.version||b.implementationHash!==manifest.implementationHash)throw new Error('Unknown authored version');await verifyAuthoredImplementation();}
   else if(b.sceneId==='journey-stage'){
    if(b.version!==journeyManifest.version||b.implementationHash!==journeyManifest.implementationHash)throw new Error('Unknown authored version');
    for(const f of journeyManifest.files){if(await hashFile(path.join(projectRoot,f.path))!==f.hash)throw new Error(`Authored implementation changed: ${f.path}`);if(f.path.endsWith('.tsx'))validateSceneImports(await readFile(path.join(projectRoot,f.path),'utf8'),['../../../scenes/journey-parameters']);}
    if(hashArtifact(journeyManifest.files)!==journeyManifest.implementationHash)throw new Error('Authored manifest hash mismatch');
   }else if(b.sceneId==='kitchen-rules-stage'){
    if(b.version!==kitchenManifest.version||b.implementationHash!==kitchenManifest.implementationHash)throw new Error('Unknown authored version');
    for(const f of kitchenManifest.files){if(await hashFile(path.join(projectRoot,f.path))!==f.hash)throw new Error(`Authored implementation changed: ${f.path}`);if(f.path.endsWith('.tsx'))validateSceneImports(await readFile(path.join(projectRoot,f.path),'utf8'),['../../../scenes/kitchen-parameters','./JourneyStage']);}
    if(hashArtifact(kitchenManifest.files)!==kitchenManifest.implementationHash)throw new Error('Authored manifest hash mismatch');
   }else if(b.sceneId==='turtle-coding-stage'){
    if(b.version!==turtleManifest.version||b.implementationHash!==turtleManifest.implementationHash)throw new Error('Unknown authored version');
    for(const f of turtleManifest.files){if(await hashFile(path.join(projectRoot,f.path))!==f.hash)throw new Error(`Authored implementation changed: ${f.path}`);if(f.path.endsWith('.tsx'))validateSceneImports(await readFile(path.join(projectRoot,f.path),'utf8'),['./JourneyStage']);}
    if(hashArtifact(turtleManifest.files)!==turtleManifest.implementationHash)throw new Error('Authored manifest hash mismatch');
   }else if(b.sceneId==='phone-paper-stage'){
    if(b.version!==phonePaperManifest.version||b.implementationHash!==phonePaperManifest.implementationHash)throw new Error('Unknown authored version');
    for(const f of phonePaperManifest.files){if(await hashFile(path.join(projectRoot,f.path))!==f.hash)throw new Error(`Authored implementation changed: ${f.path}`);if(f.path.endsWith('.tsx'))validateSceneImports(await readFile(path.join(projectRoot,f.path),'utf8'),['./JourneyStage']);}
    if(hashArtifact(phonePaperManifest.files)!==phonePaperManifest.implementationHash)throw new Error('Authored manifest hash mismatch');
   }else if(b.sceneId==='profile-whack-stage'){
    if(b.version!==profileWhackManifest.version||b.implementationHash!==profileWhackManifest.implementationHash)throw new Error('Unknown authored version');
    for(const f of profileWhackManifest.files){if(await hashFile(path.join(projectRoot,f.path))!==f.hash)throw new Error(`Authored implementation changed: ${f.path}`);if(f.path.endsWith('.tsx'))validateSceneImports(await readFile(path.join(projectRoot,f.path),'utf8'),['./JourneyStage']);}
    if(hashArtifact(profileWhackManifest.files)!==profileWhackManifest.implementationHash)throw new Error('Authored manifest hash mismatch');
   }else throw new Error(`Unknown authored scene ${b.sceneId}`);
  }
  return hashArtifact(bindings);
 }
 const files=[];
 for(const file of manifest.files){const p=path.join(projectRoot,file.path);const hash=await hashFile(p);if(hash!==file.hash)throw new Error(`Authored implementation changed: ${file.path}`);if(file.path.includes('/authored/'))validateSceneImports(await readFile(p,'utf8'));files.push({path:file.path,hash});}
 if(!files.length||hashArtifact(files)!==manifest.implementationHash)throw new Error('Authored manifest hash mismatch');
 return manifest.implementationHash;
}
export async function verifyRegisteredSceneManifest(value:unknown){
 const v=value as typeof journeyManifest;
 const expected=v?.sceneId===phonePaperManifest.sceneId?phonePaperManifest:v?.sceneId===profileWhackManifest.sceneId?profileWhackManifest:v?.sceneId===turtleManifest.sceneId?turtleManifest:v?.sceneId===kitchenManifest.sceneId?kitchenManifest:journeyManifest;
 if(v?.sceneId!==expected.sceneId||hashArtifact(v)!==hashArtifact(expected))throw new Error('Scene result is not the exact registered manifest');
 await verifyAuthoredImplementation([{sceneId:v.sceneId,version:v.version,implementationHash:v.implementationHash}]);return v;
}
