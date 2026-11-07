import {z} from 'zod';
export const ProfileWhackParameters=z.object({layout:z.literal('profile-whack'),hook:z.string().max(100)}).strict();
export const profileWhackPhases=['boot','block','pop','nothing','quiet','views','estimate','platforms','perPlatform','hundred','subtotal','total','return'] as const;
