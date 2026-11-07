/** Renderer-only props. The adapter maps the canonical compiled Timeline to these values. */
import type {TimelineVisualEffect} from '../../schemas/index';

export type Box = {x: number; y: number; width: number; height: number};
export type Framing = {crop?: Box; viewport?: Box; fit?: 'cover' | 'contain'; keys?: Array<{frame: number; x?: number; y?: number; scale?: number;transition?:'cut'|'linear'}>; panels?: Array<{assetId?: string; crop?: Box; viewport: Box; sourceStartMs?: number}>};
export type MediaAsset = {id: string; kind: string; path: string; hash?: string; url?: string; technical?: {width?: number; height?: number; durationMs?: number}; sceneSpec?: SceneSpec};
export type GraphicKey = {frame: number; x?: number; y?: number; scale?: number; rotate?: number; opacity?: number};
export type GraphicNode = {id: string; type: string; x?: number; y?: number; width?: number; height?: number; text?: string; assetId?: string; fill?: string; stroke?: string; strokeWidth?: number; fontSize?: number; fontWeight?: number; radius?: number; d?: string; points?: string; opacity?: number; rotate?: number; scale?: number; startFrame?: number; endFrame?: number; keyframes?: GraphicKey[]; children?: GraphicNode[]; align?: string};
export type SceneSpec = {width?: number; height?: number; background?: string; nodes: GraphicNode[]};
export type RenderSpan = {id: string; assetId: string; startFrame: number; endFrame: number; sourceStartMs: number; sourceEndMs?: number; gain?: number; framing?: Framing};
export type RenderWord = {id: string; wordId?:string; spanId?:string; text: string; startFrame: number; endFrame: number; emphasis?: boolean};
export type RenderAuthored = {sceneId:string;version:string;implementationHash:string;parameters:Record<string,unknown>;assetSlots:Record<string,string>;phaseFrames:Record<string,number>;enterFrames:number;exitFrames:number};
export type RenderEvent = {authored?:RenderAuthored;id: string; scene: string; startFrame: number; endFrame: number; assetIds: string[]; params: Record<string, unknown>; steps?: Array<{frame: number; [key: string]: unknown}>; effects?: TimelineVisualEffect[]; zIndex?: number; framing?: Framing};
export type RenderAudio = {id: string; assetId: string; startFrame: number; endFrame: number; sourceStartMs?: number; gain?: number; fadeInFrames?: number; fadeOutFrames?: number; duckGain?: number; loop?: boolean};
export type CaptionFont = {family:string;path:string;hash:string;url?:string};
export type RenderStyle = {accent?: string; background?: string; fontFamily?: string; captionFontSize?: number; captionY?: number; captionMaxWords?: number; captionColor?: string; captionStroke?: string;captionVariant?:'chocolate-r5-word-pulse@1.0.0';captionFont?:CaptionFont};
export type RenderDocument = {designSpace?:{width:number;height:number};width: number; height: number; fps: number; durationInFrames: number; speechDurationInFrames: number; assets: MediaAsset[]; voice: RenderSpan[]; aroll: RenderSpan[]; events: RenderEvent[]; captions: RenderWord[]; sfx: RenderAudio[]; music: RenderAudio[]; style?: RenderStyle};
