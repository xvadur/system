import { mkdtempSync, readFileSync, writeFileSync, mkdirSync, rmSync } from 'node:fs';
import { tmpdir } from 'node:os';
import { join, resolve } from 'node:path';
import { spawnSync } from 'node:child_process';
import assert from 'node:assert/strict';

const root = resolve(import.meta.dirname, '..');
const pkg = JSON.parse(readFileSync(join(root, 'package.json'), 'utf8'));
const fixture = mkdtempSync(join(tmpdir(), 'xvadur-consumer-'));
function run(args, cwd = fixture) {
  const result = spawnSync('npm', args, { cwd, encoding: 'utf8', timeout: 180_000 });
  if (result.status !== 0) throw new Error(`npm ${args.join(' ')} failed\n${result.stdout}\n${result.stderr}`);
  return result.stdout;
}
try {
  const packed = run(['pack', '--json', '--pack-destination', fixture], root);
  const bundle = JSON.parse(packed.slice(packed.indexOf('[')))[0];
  for (const file of ['dist/index.js', 'dist/index.d.ts', 'src/styles/tokens.css', 'src/styles/components.css', 'registry.json']) {
    assert(bundle.files.some(entry => entry.path === file), `Package lacks ${file}`);
  }
  writeFileSync(join(fixture, 'package.json'), JSON.stringify({
    name: 'xvadur-ui-consumer-test', private: true, type: 'module', scripts: { build: 'astro build', check: 'tsc --noEmit' },
    dependencies: {
      '@xvadur/ui': `file:${join(fixture, bundle.filename)}`,
      astro: pkg.devDependencies.astro, '@astrojs/react': pkg.devDependencies['@astrojs/react'],
      react: pkg.devDependencies.react, 'react-dom': pkg.devDependencies['react-dom'],
    },
    devDependencies: { typescript: pkg.devDependencies.typescript, '@types/react': pkg.devDependencies['@types/react'], '@types/react-dom': pkg.devDependencies['@types/react-dom'] },
  }));
  writeFileSync(join(fixture, 'tsconfig.json'), JSON.stringify({ compilerOptions: { strict: true, jsx: 'react-jsx', module: 'NodeNext', moduleResolution: 'NodeNext', skipLibCheck: true, target: 'ES2022', lib: ['ES2022', 'DOM'] }, include: ['src/typecheck.tsx'] }));
  writeFileSync(join(fixture, 'astro.config.mjs'), "import {defineConfig} from 'astro/config'; import react from '@astrojs/react'; export default defineConfig({integrations:[react()]});\n");
  mkdirSync(join(fixture, 'src/pages'), { recursive: true });
  writeFileSync(join(fixture, 'src/typecheck.tsx'), `import { Button, TextField, type ButtonProps } from '@xvadur/ui';
const props: ButtonProps = { variant: 'primary', loading: true };
export const button = <Button {...props}>Uložiť</Button>;
export const field = <TextField label="E-mail" onChange={event => event.currentTarget.value} />;
// @ts-expect-error Unsupported variants must be rejected by the public declarations.
export const invalid = <Button variant="invented">Chyba</Button>;
`);
  writeFileSync(join(fixture, 'src/pages/index.astro'), `---
import { Button, TextField, Tabs } from '@xvadur/ui';
import '@xvadur/ui/tokens.css';
import '@xvadur/ui/styles.css';
---
<html lang="sk"><head><meta charset="utf-8" /></head><body>
<Button>Spotrebiteľský build</Button><TextField label="Testovacie pole" />
<Tabs label="Test" items={[{id:'first',label:'Prvá',content:'Panel'}]} client:load />
</body></html>`);
  run(['install', '--ignore-scripts', '--no-audit', '--no-fund']);
  run(['run', 'check']);
  run(['run', 'build']);
  const html = readFileSync(join(fixture, 'dist/index.html'), 'utf8');
  assert.match(html, /Spotrebiteľský build/);
  assert.match(html, /xv-button/);
  assert.match(html, /Testovacie pole/);
  assert.match(html, /role="tablist"/);
  assert.match(html, /client="load"/);
  assert.match(html, /_astro\/.*\.css/);
  console.log('Packed package installs into a fresh Astro app: SSR, hydration entry, CSS, JS and type entry points verified.');
} finally {
  rmSync(fixture, { recursive: true, force: true });
}
