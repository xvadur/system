import { defineConfig } from 'astro/config';

// Čisto statický read-only control panel. Zápis sa deje úpravou
// súborov v data/ (Codex, editor, ...), appka ich len zobrazuje.
export default defineConfig({
  output: 'static',
  site: 'https://xvadur.com',
});
