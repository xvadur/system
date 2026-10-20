import test from 'node:test';
import assert from 'node:assert/strict';
import { mkdtempSync, mkdirSync, copyFileSync, writeFileSync, readFileSync, rmSync } from 'node:fs';
import { tmpdir } from 'node:os';
import { join } from 'node:path';
import { spawnSync } from 'node:child_process';

function fixture() {
  const dir = mkdtempSync(join(tmpdir(), 'xvadur-version-'));
  mkdirSync(join(dir, 'scripts'));
  copyFileSync(new URL('../scripts/version.mjs', import.meta.url), join(dir, 'scripts/version.mjs'));
  writeFileSync(join(dir, 'package.json'), JSON.stringify({ name: '@xvadur/ui', version: '0.1.0' }));
  writeFileSync(join(dir, 'package-lock.json'), JSON.stringify({ name: '@xvadur/ui', version: '0.1.0', packages: { '': { version: '0.1.0' }, 'node_modules/dependency': { version: '0.1.0' } } }));
  writeFileSync(join(dir, 'CHANGELOG.md'), '# Changelog\n\n## [0.1.0] - 2026-10-20\n\n- Prvá verzia.\n');
  return dir;
}

test('release command prepares a coherent version without rewriting dependency versions', () => {
  const dir = fixture();
  try {
    const result = spawnSync(process.execPath, [join(dir, 'scripts/version.mjs'), 'minor', 'Pridaný komponent'], { encoding: 'utf8' });
    assert.equal(result.status, 0, result.stderr);
    assert.equal(JSON.parse(readFileSync(join(dir, 'package.json'))).version, '0.2.0');
    const lock = JSON.parse(readFileSync(join(dir, 'package-lock.json')));
    assert.equal(lock.version, '0.2.0');
    assert.equal(lock.packages[''].version, '0.2.0');
    assert.equal(lock.packages['node_modules/dependency'].version, '0.1.0');
    assert.match(readFileSync(join(dir, 'CHANGELOG.md'), 'utf8'), /## \[0\.2\.0\][\s\S]+Pridaný komponent[\s\S]+## \[0\.1\.0\]/);
  } finally { rmSync(dir, { recursive: true, force: true }); }
});

test('dry run and invalid release input leave all release files unchanged', () => {
  const dir = fixture();
  try {
    const files = ['package.json', 'package-lock.json', 'CHANGELOG.md'];
    const before = files.map(file => readFileSync(join(dir, file), 'utf8'));
    assert.equal(spawnSync(process.execPath, [join(dir, 'scripts/version.mjs'), 'patch', 'Oprava fokusu', '--dry-run']).status, 0);
    assert.equal(spawnSync(process.execPath, [join(dir, 'scripts/version.mjs'), 'invalid', 'Oprava fokusu']).status, 1);
    assert.deepEqual(files.map(file => readFileSync(join(dir, file), 'utf8')), before);
  } finally { rmSync(dir, { recursive: true, force: true }); }
});
