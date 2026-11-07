import {z} from 'zod';
export const KitchenParameters=z.object({layout:z.literal('kitchen'),hook:z.string().max(100),spriteWidth:z.number().positive(),spriteHeight:z.number().positive()}).strict();
export const kitchenPhases=['reveal','collect','onion','wrongMeat','bread','wrongFish','order','panic','problem','return','punch'] as const;
