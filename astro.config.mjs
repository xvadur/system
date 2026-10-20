import { defineConfig } from 'astro/config';
import react from '@astrojs/react';

export default defineConfig({
  srcDir: './catalog',
  outDir: './catalog-dist',
  output: 'static',
  integrations: [react()],
  trailingSlash: 'always',
});
