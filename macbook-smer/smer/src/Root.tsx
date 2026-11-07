import React from 'react';
import {AbsoluteFill, Composition} from 'remotion';

// A setup card only. It contains no Smer footage and establishes no creative style.
const WorkspaceReady: React.FC = () => (
  <AbsoluteFill style={{backgroundColor: '#161616', color: '#fff', padding: 96, justifyContent: 'center', fontFamily: 'sans-serif'}}>
    <div style={{fontSize: 28, color: '#b5b5b5', marginBottom: 24}}>XVADUR / SMER</div>
    <div style={{fontSize: 64, fontWeight: 700, lineHeight: 1.15}}>Pracovisko pripravené</div>
    <div style={{fontSize: 30, lineHeight: 1.5, marginTop: 32}}>Kontext a skilly sú prenesené. Ďalší krok je načítať zdrojový materiál a vybranú pasáž.</div>
  </AbsoluteFill>
);

export const Root: React.FC = () => (
  <Composition id="WorkspaceReady" component={WorkspaceReady} width={1080} height={1920} fps={30} durationInFrames={90} />
);
