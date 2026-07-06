import fs from 'node:fs';
import path from 'node:path';

const ROOT = path.resolve(process.cwd(), 'data');

const DIRS = {
  dennik: path.join(ROOT, 'dennik'),
  poznamky: path.join(ROOT, 'poznamky'),
  projekty: path.join(ROOT, 'projekty'),
};

// Súbory začínajúce _ sú šablóny/koncepty — nezobrazujú sa.
function mdSubory(dir) {
  if (!fs.existsSync(dir)) return [];
  return fs.readdirSync(dir).filter((f) => f.endsWith('.md') && !f.startsWith('_'));
}

export function dnes() {
  return new Date().toISOString().slice(0, 10);
}

// ---------- frontmatter (kluc: hodnota riadky medzi --- oddeľovačmi) ----------

export function parseFrontmatter(raw) {
  const match = /^---\n([\s\S]*?)\n---\n?([\s\S]*)$/.exec(raw);
  if (!match) return { meta: {}, body: raw.trim() };
  const meta = {};
  for (const line of match[1].split('\n')) {
    const idx = line.indexOf(':');
    if (idx === -1) continue;
    meta[line.slice(0, idx).trim()] = line.slice(idx + 1).trim();
  }
  return { meta, body: match[2].trim() };
}

const cislo = (v) => {
  if (v === undefined || v === null || String(v).trim() === '') return null;
  const n = Number(String(v).replace(',', '.'));
  return Number.isNaN(n) ? null : n;
};

// ---------- denník: data/dennik/RRRR-MM-DD.md ----------

export function readDennik() {
  return mdSubory(DIRS.dennik)
    .map((f) => {
      const raw = fs.readFileSync(path.join(DIRS.dennik, f), 'utf8');
      const { meta, body } = parseFrontmatter(raw);
      return {
        datum: f.replace(/\.md$/, ''),
        kalorie: cislo(meta.kalorie),
        spanok: cislo(meta.spanok),
        meditacia: cislo(meta.meditacia),
        cvicenie: (meta.cvicenie || '').trim(),
        body,
      };
    })
    .sort((a, b) => b.datum.localeCompare(a.datum));
}

// ---------- poznámky: data/poznamky/*.md ----------

export function readPoznamky() {
  return mdSubory(DIRS.poznamky)
    .map((f) => {
      const raw = fs.readFileSync(path.join(DIRS.poznamky, f), 'utf8');
      const { meta, body } = parseFrontmatter(raw);
      return {
        slug: f.replace(/\.md$/, ''),
        nazov: meta.nazov || f.replace(/\.md$/, ''),
        datum: meta.datum || '',
        tagy: (meta.tagy || '').split(',').map((t) => t.trim()).filter(Boolean),
        body,
      };
    })
    .sort((a, b) => b.datum.localeCompare(a.datum));
}

// ---------- projekty: data/projekty/*.md ----------

export function readProjekty() {
  return mdSubory(DIRS.projekty)
    .map((f) => {
      const raw = fs.readFileSync(path.join(DIRS.projekty, f), 'utf8');
      const { meta, body } = parseFrontmatter(raw);
      return {
        slug: f.replace(/\.md$/, ''),
        nazov: meta.nazov || f.replace(/\.md$/, ''),
        status: meta.status || 'aktívny',
        dalsi_krok: meta.dalsi_krok || '',
        body,
      };
    })
    .sort((a, b) => a.nazov.localeCompare(b.nazov));
}
