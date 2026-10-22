import test from 'node:test';
import assert from 'node:assert/strict';
import { readFileSync, existsSync } from 'node:fs';
import { fileURLToPath } from 'node:url';
const root = new URL('../', import.meta.url);
const json = path => JSON.parse(readFileSync(new URL(path, root), 'utf8'));

test('a fresh clone contains every photo preview and all 48 font pairs', () => {
  const photos = json('catalog/data/photos.json');
  const pairs = json('catalog/data/font-pairs.json');
  assert.equal(photos.length, 54);
  assert.equal(pairs.length, 48);
  assert.equal(new Set(photos.map(photo => photo.id)).size, 54);
  assert.equal(new Set(pairs.map(pair => pair.id)).size, 48);
  for (const photo of photos) {
    assert.ok(photo.thumbnail.startsWith('/brand/photos/'));
    assert.ok(existsSync(new URL(`public${photo.thumbnail}`, root)), photo.id);
    assert.ok(photo.width > 0 && photo.height > 0);
    assert.ok(!JSON.stringify(photo).includes('/Users/'));
  }
});

test('the migrated font shortlist retains the nine observed favorites', () => {
  assert.deepEqual(json('catalog/data/font-favorites.json'), ['03', '14', '24', '33', '36', '37', '39', '46', '47']);
  const valid = new Set(json('catalog/data/photos.json').map(photo => photo.id));
  for (const id of json('catalog/data/photo-favorites.json')) assert.ok(valid.has(id));
});

test('font styles resolve to committed binary assets instead of local servers', () => {
  const css = readFileSync(new URL('public/brand/fonts.css', root), 'utf8');
  const assets = [...css.matchAll(/url\('([^']+)'\)/g)];
  assert.ok(assets.length > 0);
  assert.ok(!css.includes('base64,'));
  for (const [, path] of assets) {
    const bytes = readFileSync(new URL(`public${path}`, root));
    assert.equal(bytes.subarray(0, 4).toString(), 'wOF2', fileURLToPath(new URL(`public${path}`, root)));
  }
});
