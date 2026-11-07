import {z} from 'zod';
const Text=z.string().trim().min(1),Hash=z.string().regex(/^[a-f0-9]{64}$/);
export const LearningInputSchema=z.object({feedbackId:Text,scope:z.enum(['use','asset','recipe','client']),subjectId:Text.optional(),lesson:Text,tags:z.array(Text).min(1),confidence:z.enum(['observed','hypothesis']),evidence:z.array(z.object({path:Text,hash:Hash}).strict()).min(1)}).strict();
export const ScopedLearningSchema=z.object({version:z.literal('scoped-learning.v1'),clientId:Text,scope:z.object({kind:LearningInputSchema.shape.scope,subjectId:Text}).strict(),lesson:Text,tags:z.array(Text),confidence:LearningInputSchema.shape.confidence,application:z.literal('context_only'),source:z.object({episodeId:Text,clipId:Text,feedbackId:Text,feedbackHash:Hash,feedbackPath:Text,feedbackFileHash:Hash,planHash:Hash,masterHash:Hash}).strict(),evidence:LearningInputSchema.shape.evidence}).strict();
export type ScopedLearning=z.infer<typeof ScopedLearningSchema>;
