import React from 'react';
import {MediaStage,type MediaStageProps} from './MediaStage';
// Static imports only. Model plans select a typed version, never an import path or JSX.
export const authoredRegistry:{[key:string]:React.FC<MediaStageProps>}={'media-stage@1.0.0':MediaStage};
