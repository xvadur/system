import {EditorialPlanSchema,RuleCheckSchema} from './editorial.ts';
import {ScopedLearningSchema} from './learning.ts';
export * from './editorial.ts';
import {createHash} from 'node:crypto';
import {z} from 'zod';

export const SCHEMA_VERSION = '1.0.0' as const;
export const IdSchema = z.string().min(1).max(200);
export const HashSchema = z.string().regex(/^[a-f0-9]{64}$/, 'Expected SHA-256 hex');
const Ms = z.number().int().nonnegative();
const Revision = z.number().int().positive();
const Details = z.record(z.unknown());
const BaseShape = {schemaVersion: z.literal(SCHEMA_VERSION), clientId: IdSchema, episodeId: IdSchema, revision: Revision, inputHash: HashSchema};
export const BaseSchema = z.object(BaseShape).strict();
const LibraryBase = {...BaseShape, episodeId: IdSchema.optional()};
export const IntervalSchema = z.object({startMs: Ms, endMs: Ms}).strict().refine(x => x.endMs > x.startMs, 'Interval must have positive duration');
export const AnchorSchema = z.discriminatedUnion('kind', [
  z.object({kind: z.literal('word'), spanId: IdSchema, wordId: IdSchema, edge: z.enum(['start', 'end']), offsetMs: z.number().int().default(0)}).strict(),
  z.object({kind: z.literal('boundary'), boundary: z.enum(['clipStart', 'speechEnd', 'clipEnd']), offsetMs: z.number().int().default(0)}).strict(),
]);
export type Anchor = z.infer<typeof AnchorSchema>;

export const WordSchema = z.object({id: IdSchema, segmentId: IdSchema, startMs: Ms, endMs: Ms, text: z.string().min(1), originalText: z.string().min(1), confidence: z.number().min(0).max(1).optional()}).strict().refine(x => x.endMs > x.startMs, 'Word must have positive duration');
export const SegmentSchema = z.object({id: IdSchema, startMs: Ms, endMs: Ms, text: z.string(), wordIds: z.array(IdSchema)}).strict().refine(x => x.endMs > x.startMs, 'Segment must have positive duration');
export const TranscriptSchema = z.object({...BaseShape, sourceId: IdSchema, sourcePath: z.string().optional(), sourceHash: HashSchema.optional(), language: z.string().min(2), durationMs: Ms.positive(), words: z.array(WordSchema).min(1), segments: z.array(SegmentSchema).min(1), asr: z.object({engine: z.string(), model: z.string(), modelRevision: z.string().optional(), config: Details.default({}), correctedFromRevision: Revision.optional()}).strict()}).strict().superRefine((x,ctx) => {
  const ids = new Set<string>(); const segments = new Map(x.segments.map(s => [s.id,s]));
  if (segments.size !== x.segments.length) ctx.addIssue({code:'custom',message:'Duplicate segment id',path:['segments']});
  for (let i=0;i<x.words.length;i++) {const w=x.words[i]!; const s=segments.get(w.segmentId); if(ids.has(w.id)) ctx.addIssue({code:'custom',message:'Duplicate word id',path:['words',i,'id']}); ids.add(w.id); if(w.endMs>x.durationMs || !s || w.startMs<s.startMs || w.endMs>s.endMs || !s.wordIds.includes(w.id)) ctx.addIssue({code:'custom',message:'Word outside source/segment or missing segment reference',path:['words',i]});}
  for(const [i,s] of x.segments.entries()) if(s.endMs>x.durationMs || s.wordIds.some(id=>!ids.has(id))) ctx.addIssue({code:'custom',message:'Invalid segment bounds or word reference',path:['segments',i]});
});
export type Transcript = z.infer<typeof TranscriptSchema>;
export type Word = z.infer<typeof WordSchema>;

export const SourceRecordSchema = z.object({...BaseShape,id:IdSchema,path:z.string(),hash:HashSchema,originUrl:z.string().url().optional(),durationMs:Ms.positive(),width:z.number().int().positive(),height:z.number().int().positive(),fps:z.number().positive(),hasAudio:z.boolean(),importedAt:z.string()}).strict();
export const EpisodeTargetSchema=z.object({clipCount:z.number().int().positive().optional(),minDurationMs:Ms.positive().optional(),maxDurationMs:Ms.positive().optional()}).strict().refine(t=>t.minDurationMs===undefined||t.maxDurationMs===undefined||t.maxDurationMs>=t.minDurationMs,'Episode duration range is reversed');
export const EpisodeSchema = z.object({...BaseShape,id:IdSchema,title:z.string(),source:SourceRecordSchema.optional(),artifacts:z.record(z.string()).default({}),fixture:z.boolean().default(false),target:EpisodeTargetSchema.default({})}).strict();
export type SourceRecord=z.infer<typeof SourceRecordSchema>;
export type Episode=z.infer<typeof EpisodeSchema>;

const ObservationItemSchema=z.object({id:IdSchema,startMs:Ms,endMs:Ms,path:z.string(),hash:HashSchema,width:z.number().positive(),height:z.number().positive(),description:z.string().optional(),observedBy:z.string().optional(),uncertainty:z.string().optional()}).strict().refine(x=>x.endMs>x.startMs,'Observation must have positive duration');
export const SourceObservationSchema=z.object({...BaseShape,sourceId:IdSchema,sourceHash:HashSchema,mode:z.enum(['technical','vision']),frames:z.array(ObservationItemSchema),shots:z.array(IntervalSchema).default([]),coverage:z.array(IntervalSchema).default([]),audioNotes:z.array(z.object({startMs:Ms,endMs:Ms,note:z.string(),origin:z.enum(['measurement','human_listening','audio_model','text_hypothesis']),observer:z.string()}).refine(x=>x.endMs>x.startMs,'Audio observation must have positive duration')).default([])}).strict();
export type SourceObservation=z.infer<typeof SourceObservationSchema>;
export const SemanticMomentSchema=z.object({id:IdSchema,startMs:Ms,endMs:Ms,wordIds:z.array(IdSchema).min(1),text:z.string(),context:z.string(),function:z.string(),entities:z.array(z.string()).default([]),opportunity:z.enum(['portrait','archive','document','comparison','diagram','meme','emoji','text','reaction','aroll']),idea:z.string().min(1),reason:z.string().min(1),uncertainty:z.string().optional()}).strict().refine(x=>x.endMs>x.startMs,'Semantic moment must have positive duration');
export const CandidateSchema=z.object({id:IdSchema,startMs:Ms,endMs:Ms,startWordId:IdSchema,endWordId:IdSchema,title:z.string(),point:z.string(),hook:z.string(),ending:z.string(),context:z.string(),risk:z.string(),ruleCheck:RuleCheckSchema.optional(),momentIds:z.array(IdSchema),overlapIds:z.array(IdSchema).default([])}).strict().refine(x=>x.endMs>x.startMs,'Candidate duration must be positive');
export const EpisodeAnalysisSchema=z.object({...BaseShape,transcriptRevision:Revision,transcriptHash:HashSchema,topics:z.array(z.object({title:z.string(),startMs:Ms,endMs:Ms,summary:z.string()}).refine(x=>x.endMs>x.startMs,'Topic must have positive duration')),entities:z.array(z.string()),summary:z.string(),blocks:z.array(z.object({id:IdSchema,startMs:Ms,endMs:Ms,status:z.enum(['analyzed','missing']),context:z.string().optional()}).refine(x=>x.endMs>x.startMs,'Analysis block must have positive duration')).min(1),moments:z.array(SemanticMomentSchema),candidates:z.array(CandidateSchema),uncertainties:z.array(z.string()).default([]),model:z.string()}).strict();
export type SemanticMoment=z.infer<typeof SemanticMomentSchema>;
export type Candidate=z.infer<typeof CandidateSchema>;
export type EpisodeAnalysis=z.infer<typeof EpisodeAnalysisSchema>;

export const SelectionSpanSchema=z.object({id:IdSchema,startMs:Ms,endMs:Ms,candidateId:IdSchema.optional()}).strict().refine(x=>x.endMs>x.startMs,'Selected interval must have positive duration');
export const SelectionSchema=z.object({...BaseShape,clipId:IdSchema,transcriptRevision:Revision,transcriptHash:HashSchema,spans:z.array(SelectionSpanSchema).min(1),selectedBy:z.enum(['Adam','delegated-ai','fixture']),delegation:z.object({authorizedBy:z.literal('Adam'),agent:z.string().min(1),evidencePath:z.string().min(1),evidenceHash:HashSchema}).strict().optional(),fixture:z.boolean().default(false),reason:z.string().optional()}).strict().superRefine((x,ctx)=>{if(new Set(x.spans.map(s=>s.id)).size!==x.spans.length)ctx.addIssue({code:'custom',message:'Each repeated span needs a unique occurrence id',path:['spans']});if((x.selectedBy==='delegated-ai')!==Boolean(x.delegation))ctx.addIssue({code:'custom',message:'Delegated selection requires explicit Adam authorization evidence, and must retain AI provenance',path:['delegation']});if((x.selectedBy==='fixture')!==x.fixture)ctx.addIssue({code:'custom',message:'Fixture selection must be explicitly marked',path:['fixture']});});
export type Selection=z.infer<typeof SelectionSchema>;
export const PackRefSchema=z.object({id:IdSchema,version:z.string().min(1),hash:HashSchema}).strict();
export const ProductionPackSchema=z.object({schemaVersion:z.literal('production-pack.v1'),clientId:IdSchema,id:IdSchema,version:z.string().min(1),status:z.enum(['calibration','accepted']),designSpace:z.object({width:z.number().positive(),height:z.number().positive()}).strict().optional(),style:z.object({captionVariant:z.literal('chocolate-r5-word-pulse@1.0.0').optional(),captionFont:z.object({family:z.string().min(1),path:z.string().min(1),hash:HashSchema}).strict().optional(),accent:z.string(),background:z.string(),fontFamily:z.string(),captionFontSize:z.number().positive(),captionY:z.number().min(0).max(1),captionMaxWords:z.number().int().positive(),captionColor:z.string(),captionStroke:z.string()}).strict(),zones:z.object({story:z.object({x:z.number(),y:z.number(),width:z.number().positive(),height:z.number().positive()}),captions:z.object({top:z.number(),bottom:z.number()})}),scenes:z.array(z.object({sceneId:IdSchema,version:z.string(),implementationHash:HashSchema})),motion:z.object({enterMs:Ms.positive(),exitMs:Ms.positive(),maxScale:z.number().positive()}),media:z.object({photo:z.enum(['contain','cover']),reaction:z.enum(['contain','cover']),mutedByDefault:z.literal(true)}),camera:z.object({defaultScale:z.number().positive(),maxScale:z.number().positive()}),transitions:z.array(z.enum(['cut','reveal','return'])).min(1),soundPalette:z.array(z.object({role:z.string(),path:z.string(),hash:HashSchema,listening:z.enum(['not_listened','listened']),defaultGain:z.number().min(0).max(1)})),cta:z.object({requiresExplicitTail:z.literal(true),defaultDurationMs:z.literal(0),allowedVariants:z.array(z.string())}),variants:z.array(z.string()),references:z.array(z.object({path:z.string(),hash:HashSchema,note:z.string()})).min(1)}).strict();
export type ProductionPack=z.infer<typeof ProductionPackSchema>;
export const AuthoredBindingSchema=z.object({sceneId:IdSchema,version:z.string(),implementationHash:HashSchema,parameters:Details,assetSlots:z.record(IdSchema),phaseAnchors:z.record(AnchorSchema)}).strict();
export const CompiledAuthoredBindingSchema=z.object({sceneId:IdSchema,version:z.string(),implementationHash:HashSchema,parameters:Details,assetSlots:z.record(IdSchema),phaseFrames:z.record(z.number().int().nonnegative())}).strict();
export type AuthoredBinding=z.infer<typeof AuthoredBindingSchema>;
export const CreativeBriefSchema=z.object({...BaseShape,clipId:IdSchema,productionPack:PackRefSchema.optional(),promise:z.string(),point:z.string(),context:z.string(),tone:z.string(),enrichment:z.string(),style:z.string(),cta:z.string().optional(),lockedRequirements:z.array(z.string()).default([])}).strict();
export type CreativeBrief=z.infer<typeof CreativeBriefSchema>;

export const ProvenanceSchema=z.object({provider:z.string().min(1),sourceUrl:z.string().url().optional(),license:z.string().optional(),attribution:z.string().optional(),acquiredAt:z.string(),parentAssetId:IdSchema.optional(),query:z.string().optional()}).strict();
export const AssetRequestSchema=z.object({id:IdSchema,kind:z.enum(['image','video','audio','graphic','document']),purpose:z.enum(['exact','illustrative','reaction','generated']),description:z.string().min(1),query:z.string().optional(),required:z.boolean().default(true),acceptanceCriteria:z.array(z.string()).min(1),allowedSubstitutions:z.array(z.string()).default([]),sourceUrl:z.string().url().optional(),localPath:z.string().optional(),sceneSpec:z.lazy(()=>SceneSpecSchema).optional()}).strict();
export const AssetCandidateSchema=z.object({id:IdSchema,requestId:IdSchema,provider:z.string(),url:z.string().url(),previewUrl:z.string().url().optional(),title:z.string(),description:z.string(),license:z.string().optional(),attribution:z.string().optional(),durationMs:Ms.optional(),trim:IntervalSchema.optional(),matchReason:z.string(),decision:z.enum(['proposed','selected','rejected']),uncertainty:z.string().optional()}).strict();
export const SceneLayerSchema=z.object({id:IdSchema,type:z.enum(['text','image','rect','circle','line','path','group']),parentId:IdSchema.optional(),text:z.string().optional(),assetRequestId:IdSchema.optional(),x:z.number().default(0),y:z.number().default(0),width:z.number().nonnegative().optional(),height:z.number().nonnegative().optional(),fill:z.string().optional(),stroke:z.string().optional(),strokeWidth:z.number().nonnegative().optional(),fontSize:z.number().positive().optional(),path:z.string().optional(),zIndex:z.number().int().default(0),opacity:z.number().min(0).max(1).default(1),rotation:z.number().default(0),scale:z.number().positive().default(1),revealStep:z.number().int().nonnegative().default(0)}).strict();
export const SceneSpecSchema=z.object({id:IdSchema,version:z.literal('1.0.0'),width:z.number().positive(),height:z.number().positive(),background:z.string().default('transparent'),layers:z.array(SceneLayerSchema).min(1)}).strict().superRefine((x,ctx)=>{const ids=new Set(x.layers.map(l=>l.id));if(ids.size!==x.layers.length)ctx.addIssue({code:'custom',message:'Duplicate scene layer id'});for(const [i,l] of x.layers.entries()){if(l.type==='text'&&!l.text)ctx.addIssue({code:'custom',message:'Text layer needs text',path:['layers',i]});if(l.type==='image'&&!l.assetRequestId)ctx.addIssue({code:'custom',message:'Image layer needs assetRequestId',path:['layers',i]});if(l.type==='path'&&!l.path)ctx.addIssue({code:'custom',message:'Path layer needs path',path:['layers',i]});if(l.parentId&&(!ids.has(l.parentId)||l.parentId===l.id||x.layers.find(p=>p.id===l.parentId)?.type!=='group'))ctx.addIssue({code:'custom',message:'Invalid layer parent',path:['layers',i]});const seen=new Set([l.id]);let parent=l.parentId;while(parent){if(seen.has(parent)){ctx.addIssue({code:'custom',message:'Scene parent cycle',path:['layers',i]});break;}seen.add(parent);parent=x.layers.find(p=>p.id===parent)?.parentId;}}});
export const AssetRecordSchema=z.object({...LibraryBase,fulfillment:z.object({taskId:HashSchema,receiptHash:HashSchema,verificationHash:HashSchema,requestHash:HashSchema}).strict().optional(),id:IdSchema,requestId:IdSchema,kind:z.enum(['image','video','audio','graphic','document']),path:z.string().min(1),hash:HashSchema,provenance:ProvenanceSchema,technical:z.object({checked:z.boolean(),decodeOk:z.boolean(),durationMs:Ms.optional(),width:z.number().positive().optional(),height:z.number().positive().optional(),fps:z.number().positive().optional(),hasAudio:z.boolean().optional()}).strict(),contentReview:z.object({status:z.enum(['checked','unverified','rejected']),reviewedBy:z.string(),reason:z.string(),checkedRanges:z.array(IntervalSchema).default([])}).strict(),status:z.enum(['resolved','blocked','preview_ready']),previewReadiness:z.object({version:z.literal('asset-preview-readiness.v1'),scope:z.literal('this-use'),planHash:HashSchema,requestHash:HashSchema,mediaHash:HashSchema,listening:z.literal('not_listened'),pendingReview:z.array(z.string()).min(1)}).strict().optional(),tags:z.array(z.string()).default([]),sceneSpec:SceneSpecSchema.optional()}).strict().superRefine((x,ctx)=>{if(x.status==='preview_ready'&&(x.kind!=='audio'||!x.technical.checked||!x.technical.decodeOk||!x.technical.hasAudio||!x.technical.durationMs||x.contentReview.status!=='unverified'||!x.previewReadiness||x.previewReadiness.mediaHash!==x.hash||x.previewReadiness.requestHash!==x.inputHash))ctx.addIssue({code:'custom',message:'Preview audio requires real decoded bytes and explicit unlistened this-use readiness'});if(x.status!=='preview_ready'&&x.previewReadiness)ctx.addIssue({code:'custom',message:'Preview readiness cannot globally promote an asset'});if(x.status==='resolved'&&(!x.technical.checked||!x.technical.decodeOk||x.contentReview.status!=='checked'))ctx.addIssue({code:'custom',message:'Resolved asset requires successful technical and content checks'});if(x.status==='resolved'&&x.kind==='graphic'&&!x.sceneSpec)ctx.addIssue({code:'custom',message:'Resolved graphic requires SceneSpec'});if(x.status==='resolved'&&(x.kind==='video'||x.kind==='audio')&&(!x.technical.durationMs||x.technical.durationMs<=0))ctx.addIssue({code:'custom',message:'Resolved temporal media requires positive duration'});});
export type AssetRequest=z.infer<typeof AssetRequestSchema>;
export type AssetCandidate=z.infer<typeof AssetCandidateSchema>;
export type AssetRecord=z.infer<typeof AssetRecordSchema>;
export type SceneSpec=z.infer<typeof SceneSpecSchema>;

export const FramingSchema=z.object({mode:z.enum(['center','crop','split']).default('center'),x:z.number().default(0.5),y:z.number().default(0.5),scale:z.number().positive().default(1),keyframes:z.array(z.object({anchor:AnchorSchema,x:z.number(),y:z.number(),scale:z.number().positive(),transition:z.enum(['cut','linear']).default('linear')})).default([]),override:z.boolean().default(false)}).strict();
export const TimelineFramingSchema=z.object({mode:z.enum(['center','crop','split']),x:z.number(),y:z.number(),scale:z.number().positive(),keyframes:z.array(z.object({frame:z.number().int().nonnegative(),x:z.number(),y:z.number(),scale:z.number().positive(),transition:z.enum(['cut','linear'])})),override:z.boolean()}).strict();
export const EventStepSchema=z.object({id:IdSchema,anchor:AnchorSchema,action:z.enum(['setup','reveal','hold','return','transform']),params:Details.default({})}).strict();

const EffectEasingSchema=z.enum(['linear','ease-in','ease-out','ease-in-out','hold']);
export type EffectEasing=z.infer<typeof EffectEasingSchema>;

// Position is relative to the effect target's width and height. Rotation is in degrees.
const TransformEffectValueSchema=z.object({
  x:z.number().finite().default(0),
  y:z.number().finite().default(0),
  scale:z.number().finite().positive().default(1),
  rotation:z.number().finite().default(0),
}).strict();

const FilterEffectValueSchema=z.object({
  brightness:z.number().finite().nonnegative().default(1),
  contrast:z.number().finite().nonnegative().default(1),
  saturation:z.number().finite().nonnegative().default(1),
  grayscale:z.number().min(0).max(1).default(0),
  blurPx:z.number().finite().nonnegative().default(0),
}).strict();

function visualEffects<Time extends z.ZodRawShape>(time:Time) {
  const keyframes=<Value extends z.ZodTypeAny>(value:Value)=>z.array(z.object({
    ...time,
    value,
    easing:EffectEasingSchema.optional(),
  }).strict()).min(1);
  return z.array(z.discriminatedUnion('kind',[
    z.object({id:IdSchema,kind:z.literal('transform'),keyframes:keyframes(TransformEffectValueSchema)}).strict(),
    z.object({id:IdSchema,kind:z.literal('opacity'),keyframes:keyframes(z.number().min(0).max(1))}).strict(),
    z.object({id:IdSchema,kind:z.literal('filter'),keyframes:keyframes(FilterEffectValueSchema)}).strict(),
  ])).superRefine((effects,ctx)=>{
    const seen=new Set<string>();
    for(const [index,effect] of effects.entries()){
      if(seen.has(effect.id))ctx.addIssue({code:'custom',message:'Duplicate visual effect id',path:[index,'id']});
      seen.add(effect.id);
    }
  });
}

export const PlanVisualEffectsSchema=visualEffects({anchor:AnchorSchema});
const TimelineVisualEffectsSchema=visualEffects({frame:z.number().int().nonnegative()});
export type TimelineVisualEffect=z.infer<typeof TimelineVisualEffectsSchema>[number];

export const PlanEventSchema=z.object({id:IdSchema,momentId:IdSchema.optional(),origin:z.enum(['content','client','technical']),originRef:z.string().optional(),scene:z.enum(['Cutaway','Portrait','Document','Meme','Comparison','Diagram','Graphic','Text','CTA','Authored']),start:AnchorSchema,end:AnchorSchema,authored:AuthoredBindingSchema.optional(),assetRequestIds:z.array(IdSchema).default([]),params:Details.default({}),steps:z.array(EventStepSchema).default([]),effects:PlanVisualEffectsSchema.optional(),required:z.boolean().default(true),zIndex:z.number().int().default(10),reason:z.string().default(''),trim:z.object({startMs:Ms,endMs:Ms}).strict().optional(),shortPolicy:z.enum(['error','loop','hold']).default('error'),muted:z.boolean().default(true)}).strict().superRefine((x,ctx)=>{if((x.scene==='Authored')!==Boolean(x.authored))ctx.addIssue({code:'custom',message:'Authored scene requires exactly one typed binding'});if(x.origin==='content'&&!x.momentId)ctx.addIssue({code:'custom',message:'Content event requires momentId',path:['momentId']});});
export const AudioCueSchema=z.object({id:IdSchema,assetRequestId:IdSchema,start:AnchorSchema,end:AnchorSchema,gain:z.number().min(0).max(4).default(1),fadeInMs:Ms.default(0),fadeOutMs:Ms.default(0),ducking:z.number().min(0).max(1).default(1),trimStartMs:Ms.default(0),loop:z.boolean().default(false)}).strict();
export const EditPlanSchema=z.object({...BaseShape,clipId:IdSchema,editorial:EditorialPlanSchema.optional(),productionPack:PackRefSchema.optional(),sourceSelection:z.object({revision:Revision,hash:HashSchema}).strict(),briefId:IdSchema.optional(),events:z.array(PlanEventSchema),assetRequests:z.array(AssetRequestSchema).default([]),tail:z.object({durationMs:Ms,visual:z.enum(['hold','color','scene']),color:z.string().optional()}).strict().default({durationMs:0,visual:'hold'}),captions:z.object({enabled:z.boolean(),emphasisWordIds:z.array(IdSchema).default([])}).strict().default({enabled:true,emphasisWordIds:[]}),audio:z.object({sfx:z.array(AudioCueSchema).default([]),music:z.array(AudioCueSchema).default([])}).strict().default({sfx:[],music:[]}),framing:FramingSchema.default({}),lockedEventIds:z.array(IdSchema).default([]),lockedFields:z.array(z.enum(['framing','audio'])).default([]),lockedAssetRequestIds:z.array(IdSchema).default([]),momentDecisions:z.array(z.object({momentId:IdSchema,decision:z.enum(['event','aroll','open']),eventId:IdSchema.optional(),reason:z.string()})).default([])}).strict().superRefine((x,ctx)=>{for(const key of ['events','assetRequests'] as const){const arr=x[key];if(new Set(arr.map(e=>e.id)).size!==arr.length)ctx.addIssue({code:'custom',message:`Duplicate ${key} id`,path:[key]});}for(const id of x.lockedEventIds)if(!x.events.some(e=>e.id===id))ctx.addIssue({code:'custom',message:'Unknown locked event',path:['lockedEventIds']});for(const id of x.lockedAssetRequestIds)if(!x.assetRequests.some(r=>r.id===id))ctx.addIssue({code:'custom',message:'Unknown locked material',path:['lockedAssetRequestIds']});});
export type EditPlan=z.infer<typeof EditPlanSchema>;
export type PlanEvent=z.infer<typeof PlanEventSchema>;
export type AudioCue=z.infer<typeof AudioCueSchema>;

export const RecipeRecordSchema=z.object({...LibraryBase,id:IdSchema,title:z.string(),purpose:z.string(),triggers:z.array(z.string()),referenceUrl:z.string().url().optional(),referenceDate:z.string(),rendererVersion:z.string(),parameters:Details,sceneSpec:SceneSpecSchema,limitations:z.array(z.string()).default([])}).strict();
export const UseRecordSchema=z.object({...BaseShape,id:IdSchema,clipId:IdSchema,eventId:IdSchema,assetId:IdSchema.optional(),recipeId:IdSchema.optional(),parameters:Details.default({}),purpose:z.string(),state:z.enum(['used','approved','rejected']),reviewRevision:Revision.optional(),reason:z.string().optional()}).strict();
export type RecipeRecord=z.infer<typeof RecipeRecordSchema>;
export type UseRecord=z.infer<typeof UseRecordSchema>;

const FrameFields={startFrame:z.number().int().nonnegative(),endFrame:z.number().int().positive(),startMs:Ms,endMs:Ms};
export const TimelineSpanSchema=z.object({id:IdSchema,...FrameFields,sourceStartMs:Ms,sourceEndMs:Ms,sourcePath:z.string(),muted:z.boolean()}).strict();
export const TimelineEventSchema=z.object({id:IdSchema,momentId:IdSchema.optional(),origin:z.enum(['content','client','technical']),scene:PlanEventSchema.innerType().shape.scene,...FrameFields,authored:CompiledAuthoredBindingSchema.optional(),assetIds:z.array(IdSchema),params:Details,steps:z.array(z.object({id:IdSchema,frame:z.number().int().nonnegative(),action:z.string(),params:Details})),effects:TimelineVisualEffectsSchema.optional(),required:z.boolean(),zIndex:z.number().int(),trim:z.object({startMs:Ms,endMs:Ms}).optional(),shortPolicy:z.enum(['error','loop','hold']),muted:z.boolean()}).strict().superRefine((event,ctx)=>{
  for(const [effectIndex,effect] of (event.effects??[]).entries()){
    let previous=-1;
    for(const [keyIndex,{frame}] of effect.keyframes.entries()){
      const path=['effects',effectIndex,'keyframes',keyIndex,'frame'];
      if(frame<event.startFrame||frame>event.endFrame)ctx.addIssue({code:'custom',message:'Visual effect keyframe is outside its event',path});
      if(frame<=previous)ctx.addIssue({code:'custom',message:'Visual effect keyframes must be strictly increasing',path});
      previous=frame;
    }
  }
});
export const TimelineCaptionSchema=z.object({id:IdSchema,wordId:IdSchema,spanId:IdSchema,text:z.string(),originalText:z.string(),emphasis:z.boolean(),...FrameFields}).strict();
export const TimelineAudioSchema=z.object({id:IdSchema,assetId:IdSchema,...FrameFields,gain:z.number(),fadeInFrames:z.number().int().nonnegative(),fadeOutFrames:z.number().int().nonnegative(),ducking:z.number(),trimStartMs:Ms,loop:z.boolean()}).strict();
export const TimelineSchema=z.object({...BaseShape,clipId:IdSchema,productionPack:ProductionPackSchema.optional(),fps:z.number().positive(),width:z.number().int().positive(),height:z.number().int().positive(),speechDurationMs:Ms.positive(),durationMs:Ms.positive(),durationInFrames:z.number().int().positive(),sourceSelectionHash:HashSchema,sourceTranscriptHash:HashSchema,sourcePlanHash:HashSchema,assets:z.array(AssetRecordSchema),tail:EditPlanSchema.innerType().shape.tail,framing:TimelineFramingSchema,tracks:z.object({voice:z.array(TimelineSpanSchema),aroll:z.array(TimelineSpanSchema),events:z.array(TimelineEventSchema),captions:z.array(TimelineCaptionSchema),sfx:z.array(TimelineAudioSchema),music:z.array(TimelineAudioSchema)}).strict()}).strict();
export type Timeline=z.infer<typeof TimelineSchema>;
export type TimelineEvent=z.infer<typeof TimelineEventSchema>;
export type TimelineAudio=z.infer<typeof TimelineAudioSchema>;

export const FeedbackRecordSchema=z.object({...BaseShape,id:IdSchema,clipId:IdSchema,eventId:IdSchema.optional(),wordId:IdSchema.optional(),atMs:Ms.optional(),targetRevision:Revision,type:z.enum(['speech','word','crop','event','asset','mix','technical']),severity:z.enum(['info','minor','major','blocking']),author:z.string(),finding:z.string(),requestedChange:z.string(),status:z.enum(['open','applied','verified','rejected']),repairRevision:Revision.optional(),originRef:z.object({kind:z.literal("workplace"),jobId:IdSchema,commentId:IdSchema,versionId:IdSchema,bodyHash:HashSchema}).strict().optional(),critique:z.object({packetHash:HashSchema,masterHash:HashSchema,planHash:HashSchema,expectedTest:z.string().min(1),elementId:IdSchema.optional(),frames:z.array(z.number().int().nonnegative()).min(1)}).strict().optional(),verification:z.string().optional(),verificationBinding:z.object({planHash:HashSchema,timelineHash:HashSchema,masterHash:HashSchema,checkHash:HashSchema}).strict().optional()}).strict();
export const ReviewEvidenceSchema=z.object({id:IdSchema,kind:z.enum(['technical','visual','motion','listening']),method:z.enum(['signal-metrics','sampled-frames','timed-frame-sequence','continuous-video','human-playback','audio-listening']).optional(),status:z.enum(['passed','failed','not_checked','not_listened','listened']),observer:z.string(),ranges:z.array(IntervalSchema),artifactHash:HashSchema,notes:z.string(),fixture:z.boolean().default(false)}).strict().superRefine((x,ctx)=>{if(x.status==='listened'&&(x.kind!=='listening'||!x.observer.trim()||x.ranges.length===0))ctx.addIssue({code:'custom',message:'Listened requires listener and actual ranges'});if(x.kind==='motion'&&x.status==='passed'&&(!['continuous-video','human-playback'].includes(x.method??'')||!x.observer.trim()||!x.ranges.length))ctx.addIssue({code:'custom',message:'Motion pass requires actual continuous playback evidence; timed stills are not continuous motion'});});
export const ReviewRecordSchema=z.object({...BaseShape,id:IdSchema,clipId:IdSchema,protocol:z.literal('p5.v1').optional(),decision:z.enum(['approved','rejected','review_required']),acceptedBy:z.enum(['Adam','fixture']),fixture:z.boolean(),planHash:HashSchema,assetsHash:HashSchema,timelineHash:HashSchema,masterHash:HashSchema,masterPath:z.string(),evidence:z.array(ReviewEvidenceSchema),notes:z.string(),acceptedAt:z.string()}).strict().refine(x=>(x.acceptedBy==='fixture')===x.fixture,'Fixture review must be explicitly marked');
export const RunManifestSchema=z.object({...BaseShape,id:IdSchema,clipId:IdSchema.optional(),phase:z.string(),status:z.enum(['pending','running','succeeded','failed','blocked']),cacheKey:HashSchema,inputs:z.record(HashSchema),outputs:z.record(z.object({path:z.string(),hash:HashSchema})),tool:z.string(),toolVersion:z.string(),model:z.string().optional(),startedAt:z.string(),finishedAt:z.string().optional(),error:z.string().optional(),attempt:z.number().int().nonnegative()}).strict();
export type FeedbackRecord=z.infer<typeof FeedbackRecordSchema>;
export type ReviewEvidence=z.infer<typeof ReviewEvidenceSchema>;
export type ReviewRecord=z.infer<typeof ReviewRecordSchema>;
export type RunManifest=z.infer<typeof RunManifestSchema>;

/** One canonical digest convention for persisted artifact references. */
export function canonicalJson(value:unknown):string {const visit=(v:unknown):unknown=>{if(Array.isArray(v))return v.map(visit);if(v!==null&&typeof v==='object')return Object.fromEntries(Object.entries(v as Record<string,unknown>).filter(([,x])=>x!==undefined).sort(([a],[b])=>a<b?-1:a>b?1:0).map(([k,x])=>[k,visit(x)]));return v;};return JSON.stringify(visit(value));}
export function hashArtifact(value:unknown):string{return createHash('sha256').update(canonicalJson(value)).digest('hex');}

// P1: annotations and legacy evidence are separate from immutable AssetRecord authority.
export const EvidenceRefSchema=z.object({path:z.string().min(1),hash:HashSchema,pointer:z.string(),note:z.string().min(1)}).strict();
export const LibraryAnnotationSchema=z.object({version:z.literal('1.0.0'),clientId:IdSchema,supersedes:z.array(HashSchema).optional(),mediaHash:HashSchema,record:AssetRecordSchema,aliases:z.array(z.string()),entities:z.array(z.string()),action:z.string().min(1),functions:z.array(z.string()),tone:z.array(z.string()),usableRanges:z.array(IntervalSchema),reactionOnsetMs:Ms.optional(),crop:z.enum(['contain','cover']).default('contain'),origins:z.array(EvidenceRefSchema).min(1),observations:z.array(z.object({path:z.string(),hash:HashSchema,atMs:Ms,observer:z.string(),mode:z.literal('sampled-frame')})),limitations:z.array(z.string()),legacyUses:z.array(z.object({id:IdSchema,scope:z.enum(['asset','use','recipe','client']),state:z.enum(['used','accepted','rejected','reference']),reason:z.string(),origin:EvidenceRefSchema})).default([])}).strict();
export const LibraryImportSchema=z.object({version:z.literal('1.0.0'),clientId:IdSchema,entries:z.array(z.object({sourcePath:z.string(),sourceHash:HashSchema,supersedes:z.array(HashSchema).optional(),kind:z.enum(['image','video','audio','document']),description:z.string().min(1),sourceUrl:z.string().url().optional(),license:z.string(),aliases:z.array(z.string()),entities:z.array(z.string()),functions:z.array(z.string()),tone:z.array(z.string()),usableRanges:z.array(IntervalSchema),reactionOnsetMs:Ms.optional(),crop:z.enum(['contain','cover']).default('contain'),origin:EvidenceRefSchema,observations:LibraryAnnotationSchema.shape.observations,limitations:z.array(z.string()),legacyUses:LibraryAnnotationSchema.shape.legacyUses})).min(1)}).strict();
export type LibraryAnnotation=z.infer<typeof LibraryAnnotationSchema>;
export type LibraryImport=z.infer<typeof LibraryImportSchema>;
export type LibraryMatch={id:string;annotationHash:string;annotation:LibraryAnnotation;score:number;reason:string};
export const LibraryContextSchema=z.object({learnings:z.array(z.object({hash:HashSchema,path:z.string(),record:ScopedLearningSchema}).strict()).optional(),version:z.literal('1.0.0'),clientId:IdSchema,query:z.string(),inputHash:HashSchema,recipes:z.array(z.object({id:IdSchema,hash:HashSchema,path:z.string(),recipe:Details})).optional(),matches:z.array(z.object({id:IdSchema,mediaHash:HashSchema,annotationHash:HashSchema,description:z.string(),reason:z.string(),path:z.string(),kind:AssetRequestSchema.shape.kind,usableRanges:z.array(IntervalSchema),previews:LibraryAnnotationSchema.shape.observations,limitations:z.array(z.string()),legacyUses:LibraryAnnotationSchema.shape.legacyUses}))}).strict();
export type LibraryContext=z.infer<typeof LibraryContextSchema>;

export const ProductionRecipeSchema=z.discriminatedUnion('kind',[
 z.object({kind:z.literal('authored'),version:z.literal('1.0.0'),id:IdSchema,clientId:IdSchema,title:z.string(),purpose:z.string(),triggers:z.array(z.string()),scene:z.object({sceneId:IdSchema,version:z.string(),implementationHash:HashSchema}),parameterExample:Details,phaseRoles:z.record(z.string()),origins:z.array(EvidenceRefSchema).min(1),limitations:z.array(z.string())}).strict(),
 z.object({kind:z.literal('dramaturgy'),version:z.literal('1.0.0'),id:IdSchema,clientId:IdSchema,title:z.string(),purpose:z.string(),triggers:z.array(z.string()),steps:z.array(z.string()).min(1),origins:z.array(EvidenceRefSchema).min(1),limitations:z.array(z.string())}).strict(),
]);
export const LibraryRecipeSchema=z.union([ProductionRecipeSchema,RecipeRecordSchema]);
