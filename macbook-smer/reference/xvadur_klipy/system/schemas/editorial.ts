import {z} from 'zod';

// Kept independent of index.ts so the canonical EditPlan can embed this contract.
const Id=z.string().min(1),Hash=z.string().regex(/^[a-f0-9]{64}$/);
export const editorialAxes=['image','meme','broll','authored_graphics','imagegen','framing','captions','sound','transition','duration','aroll'] as const;
const WordRef=z.object({spanId:Id,wordId:Id}).strict();
const ArcPart=z.object({text:Id,anchors:z.array(WordRef).min(1)}).strict();
export const EditorialPlanSchema=z.object({
  version:z.literal('editorial.v1'),libraryContextHash:Hash,analysisHash:Hash,
  arc:z.object({promise:ArcPart,setup:ArcPart,payoff:ArcPart,ending:ArcPart}).strict(),
  context:z.object({sourceMeaning:Id,selectionMeaning:Id,verdict:z.enum(['preserved','review_required']),reason:Id,risks:z.array(Id)}).strict(),
  decisions:z.array(z.object({
    momentId:Id,spanId:Id,wordIds:z.array(Id).min(1),function:Id,purpose:Id,
    treatment:z.enum(['event','aroll','open']),eventIds:z.array(Id),requestIds:z.array(Id),needIds:z.array(Id),
    axes:z.array(z.object({axis:z.enum(editorialAxes),decision:z.enum(['use','not_use','open']),reason:Id,refs:z.array(Id),needIds:z.array(Id)}).strict()),
    alternatives:z.array(z.object({mediaHash:Hash,annotationHash:Hash,decision:z.enum(['candidate','rejected']),reason:Id,requestId:Id.optional()}).strict()),
    expectedResult:Id,test:Id,
  }).strict()),
  openNeeds:z.array(z.object({id:Id,kind:z.enum(['obtain-media','generate-image','implement-scene','review-required']),description:Id,required:z.boolean(),acceptanceCriteria:z.array(Id).min(1),assetRequestId:Id.optional(),eventId:Id.optional()}).strict()),
}).strict();
export type EditorialPlan=z.infer<typeof EditorialPlanSchema>;

export const SourceEditorialContextSchema=z.object({
  version:z.literal('source-editorial.v1'),revision:z.number().int().positive(),clientId:Id,episodeId:Id,
  sourceId:Id,sourceHash:Hash,sourceNames:z.array(Id).min(1),access:z.enum(['public','paid','unknown']),
  paidLimitScope:z.enum(['clip','batch']).optional(),evidence:Id,recordedBy:z.enum(['Adam','fixture']),
}).strict();
export type SourceEditorialContext=z.infer<typeof SourceEditorialContextSchema>;

export const RuleCheckSchema=z.object({
  version:z.literal('rule-check.v1'),rulesHash:Hash,dictionaryHash:Hash,sourceHash:Hash,sourceContextHash:Hash.optional(),
  inputHash:Hash,status:z.enum(['allowed','blocked','review_required']),
  findings:z.array(z.object({code:Id,status:z.enum(['blocked','review_required']),reason:Id}).strict()),
  limits:z.object({paidMaximumMs:z.number().positive(),selectedMs:z.number().nonnegative(),sourceUnionMs:z.number().nonnegative()}),
  exceptionNotes:z.array(Id),scope:z.literal('deterministic_rules_only'),
}).strict();
export type RuleCheck=z.infer<typeof RuleCheckSchema>;
