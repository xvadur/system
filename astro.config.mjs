import { defineConfig } from 'astro/config';
import node from '@astrojs/node';

// Server mód: stránky čítajú a formuláre zapisujú živé dáta zo súborov v data/.
// Pri deploji na Cloudflare stačí vymeniť adaptér za @astrojs/cloudflare.
export default defineConfig({
  output: 'server',
  site: 'https://xvadur.com',
  adapter: node({ mode: 'standalone' }),
  security: {
    // Bez tohto Astro nedôveruje Host hlavičke, Astro.url stratí port
    // a CSRF kontrola (checkOrigin) zablokuje aj vlastné formuláre.
    allowedDomains: [
      { hostname: 'localhost' },
      { hostname: '127.0.0.1' },
      { hostname: 'xvadur.com', protocol: 'https' },
      { hostname: '**.xvadur.com', protocol: 'https' },
    ],
  },
});
