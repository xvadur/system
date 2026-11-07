import {sceneCatalog as legacyCatalog,validateAuthored as validateLegacy} from './catalog';
import {JourneyParameters} from './journey-parameters';
import journeyManifest from './journey-manifest.json';
import kitchenManifest from './kitchen-manifest.json';
import {KitchenParameters,kitchenPhases} from './kitchen-parameters';
import turtleManifest from './turtle-manifest.json';
import {TurtleParameters,turtlePhases} from './turtle-parameters';
import profileWhackManifest from './profile-whack-manifest.json';
import {ProfileWhackParameters,profileWhackPhases} from './profile-whack-parameters';
import phonePaperManifest from './phone-paper-manifest.json';
import {PhonePaperParameters,phonePaperPhases} from './phone-paper-parameters';
// Append-only scene families. The frozen P2 catalog and its hashes stay intact.
export const sceneCatalog={...legacyCatalog,'journey-stage':{version:'1.0.0',parameters:JourneyParameters,slots:['subject'],phases:['reveal','action','arrive','return'],allowedKinds:['image','document'],implementationHash:journeyManifest.implementationHash},'kitchen-rules-stage':{version:'1.0.0',parameters:KitchenParameters,slots:['subject'],phases:[...kitchenPhases],allowedKinds:['image'],implementationHash:kitchenManifest.implementationHash},'turtle-coding-stage':{version:'1.0.0',parameters:TurtleParameters,slots:['subject'],phases:[...turtlePhases],allowedKinds:['image'],implementationHash:turtleManifest.implementationHash},'profile-whack-stage':{version:'1.0.0',parameters:ProfileWhackParameters,slots:['subject'],phases:[...profileWhackPhases],allowedKinds:['image'],implementationHash:profileWhackManifest.implementationHash},'phone-paper-stage':{version:'1.0.0',parameters:PhonePaperParameters,slots:['subject'],phases:[...phonePaperPhases],allowedKinds:['image'],implementationHash:phonePaperManifest.implementationHash}};
export function validateAuthored(binding:Parameters<typeof validateLegacy>[0]){
 if(binding.sceneId!=='journey-stage'&&binding.sceneId!=='kitchen-rules-stage'&&binding.sceneId!=='turtle-coding-stage'&&binding.sceneId!=='profile-whack-stage'&&binding.sceneId!=='phone-paper-stage')return validateLegacy(binding);
 const spec=sceneCatalog[binding.sceneId];
 if(binding.version!==spec.version||binding.implementationHash!==spec.implementationHash)throw new Error('Unknown authored version or implementation hash');
 const parameters=spec.parameters.parse(binding.parameters);
 for(const [keys,expected,label]of [[Object.keys(binding.assetSlots),spec.slots,'slot'],[Object.keys(binding.phaseAnchors??binding.phaseFrames??{}),spec.phases,'phase']]as const)if(keys.length!==expected.length||expected.some(k=>!keys.includes(k)))throw new Error(`Missing or unknown authored ${label}`);
 return {spec,parameters};
}
