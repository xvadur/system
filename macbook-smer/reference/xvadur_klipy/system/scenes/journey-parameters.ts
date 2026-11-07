import {z} from 'zod';
export const JourneyParameters=z.object({fromLabel:z.string().min(1).max(36),toLabel:z.string().min(1).max(36),beforeLabel:z.string().max(52),afterLabel:z.string().max(52),subjectScale:z.number().min(.6).max(1.3),direction:z.enum(['left-to-right','right-to-left']),background:z.enum(['night','paper'])}).strict();
export type JourneyParametersValue=z.infer<typeof JourneyParameters>;
