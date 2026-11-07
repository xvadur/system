import {z} from 'zod';
export const TurtleParameters=z.object({layout:z.literal('turtle-coding'),hook:z.string().max(100)}).strict();
export const turtlePhases=['boot','command','draw','afterSchool','timeJump','waiting','obsession','return','outro'] as const;
