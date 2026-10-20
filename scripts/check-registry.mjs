import { readFile, access } from 'node:fs/promises';
import { fileURLToPath } from 'node:url';
import { resolve, dirname } from 'node:path';

const root = resolve(dirname(fileURLToPath(import.meta.url)), '..');
const registry = JSON.parse(await readFile(resolve(root, 'registry.json'), 'utf8'));
const manifest = JSON.parse(await readFile(resolve(root, 'package.json'), 'utf8'));
const exported = await import(resolve(root, 'dist/index.js'));
const names = new Set();
const ids = new Set();
for (const component of registry.components) {
  if (names.has(component.name) || ids.has(component.id)) throw new Error(`Duplicate component: ${component.name}`);
  names.add(component.name); ids.add(component.id);
  if (!/^[a-z][a-z0-9-]+$/.test(component.id)) throw new Error(`Invalid id: ${component.id}`);
  if (!component.example || !component.description || !component.since) throw new Error(`Incomplete record: ${component.name}`);
  if (!/^(preview|stable|deprecated)$/.test(component.status)) throw new Error(`Invalid status: ${component.name}`);
  if (!(component.name in exported)) throw new Error(`Not exported: ${component.name}`);
  if (!component.source.startsWith('src/components/') || component.source.includes('..')) throw new Error('Invalid source path');
  await access(resolve(root, component.source));
}
for (const name of Object.keys(exported)) {
  if (/^[A-Z]/.test(name) && !names.has(name)) throw new Error(`Export missing from registry: ${name}`);
}
for (const path of Object.values(manifest.exports)) {
  for (const file of typeof path === 'string' ? [path] : Object.values(path)) await access(resolve(root, file));
}
console.log(`${names.size} components: exports, source files, metadata and package entry points valid.`);
