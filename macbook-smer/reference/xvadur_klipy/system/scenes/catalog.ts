import {z} from 'zod';
import manifest from './authored-manifest.json';
export const MediaStageParameters=z.object({layout:z.enum(['object','split','full','pip']),motion:z.enum(['still','focus','shake']),fit:z.enum(['contain','cover']),title:z.string().max(70),label:z.string().max(100),rotation:z.number().min(-8).max(8),sourceStartMs:z.number().int().nonnegative().default(0)}).strict();
export const sceneCatalog={
 'media-stage':{version:'1.0.0',parameters:MediaStageParameters,slots:['subject'],phases:['reveal','action','return'],allowedKinds:['image','video','document'],implementationHash:manifest.implementationHash},
} as const;
export function validateAuthored(binding:{sceneId:string;version:string;implementationHash:string;parameters:Record<string,unknown>;assetSlots:Record<string,string>;phaseAnchors?:Record<string,unknown>;phaseFrames?:Record<string,number>}){
 if(binding.sceneId!=='media-stage')throw new Error(`Unknown authored scene ${binding.sceneId}`);
 const spec=sceneCatalog[binding.sceneId];
 if(binding.version!==spec.version||binding.implementationHash!==spec.implementationHash)throw new Error('Unknown authored version or implementation hash');
 const parameters=spec.parameters.parse(binding.parameters);
 for(const [keys,expected,label] of [[Object.keys(binding.assetSlots),spec.slots,'slot'],[Object.keys(binding.phaseAnchors??binding.phaseFrames??{}),spec.phases,'phase']] as const){if(keys.length!==expected.length||expected.some(k=>!keys.includes(k)))throw new Error(`Missing or unknown authored ${label}`);}
 return {spec,parameters};
}
