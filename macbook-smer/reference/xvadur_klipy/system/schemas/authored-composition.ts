import {z} from 'zod';

const hash=z.string().regex(/^[a-f0-9]{64}$/);
const projectPath=z.string().min(1).refine(value=>!value.startsWith('/')&&!value.includes('\\')&&value.split('/').every(part=>part!==''&&part!=='.'&&part!=='..'),'Use a normalized project-relative path');

/** A whole-scene implementation, pinned to one existing compiler clock. */
export const AuthoredCompositionManifestSchema=z.object({
  schemaVersion:z.literal('authored-composition.v1'),
  id:z.string().regex(/^[a-zA-Z0-9][a-zA-Z0-9._-]*$/),
  revision:z.number().int().positive(),
  parentManifestHash:hash.optional(),
  timelineHash:hash,
  entryPath:projectPath,
  exportName:z.string().regex(/^(default|[A-Za-z_$][A-Za-z0-9_$]*)$/).default('default'),
  files:z.array(z.object({path:projectPath,hash}).strict()).min(1),
  remotionVersion:z.literal('4.0.529'),
}).strict().superRefine((manifest,ctx)=>{
  if(new Set(manifest.files.map(file=>file.path)).size!==manifest.files.length)ctx.addIssue({code:'custom',message:'Duplicate authored source path',path:['files']});
  if(!manifest.files.some(file=>file.path===manifest.entryPath))ctx.addIssue({code:'custom',message:'Entry must be a pinned source file',path:['entryPath']});
  if(!/\.[cm]?[jt]sx?$/.test(manifest.entryPath))ctx.addIssue({code:'custom',message:'Entry must be a JavaScript/TypeScript component',path:['entryPath']});
});

export type AuthoredCompositionManifest=z.infer<typeof AuthoredCompositionManifestSchema>;
