import {z} from 'zod';
export const PhonePaperParameters=z.object({layout:z.literal('phone-paper'),hook:z.string().max(100)}).strict();
export const phonePaperPhases=['boot','foreignVideo','comment','ownStory','opinion','cleanMeaning','audience','return'] as const;
