import fs from 'node:fs';
import path from 'node:path';

const ROOT = path.resolve(process.cwd(), 'data');

const DIRS = {
  dennik: path.join(ROOT, 'dennik'),
  poznamky: path.join(ROOT, 'poznamky'),
  projekty: path.join(ROOT, 'projekty'),
};

function ensureDir(dir) {
  fs.mkdirSync(dir, { recursive: true });
}

export function dnes() {
  return new Date().toISOString().slice(0, 10);
}

export function slugify(text) {
  return text
    .normalize('NFD')
    .replace(/[̀-ͯ]/g, '')
    .toLowerCase()
    .replace(/[^a-z0-9]+/g, '-')
    .replace(/^-+|-+$/g, '')
    .slice(0, 60) || 'zaznam';
}

// ---------- frontmatter (title: value riadky medzi --- oddeľovačmi) ----------

export function parseFrontmatter(raw) {
  const match = /^---\n([\s\S]*?)\n---\n?([\s\S]*)$/.exec(raw);
  if (!match) return { meta: {}, body: raw };
  const meta = {};
  for (const line of match[1].split('\n')) {
    const idx = line.indexOf(':');
    if (idx === -1) continue;
    meta[line.slice(0, idx).trim()] = line.slice(idx + 1).trim();
  }
  return { meta, body: match[2].trim() };
}

export function serializeFrontmatter(meta, body) {
  const lines = Object.entries(meta)
    .filter(([, v]) => v !== undefined && v !== null && String(v).trim() !== '')
    .map(([k, v]) => `${k}: ${String(v).replace(/\n/g, ' ')}`);
  return `---\n${lines.join('\n')}\n---\n\n${body.trim()}\n`;
}

// ---------- denník ----------

export function readDennik() {
  ensureDir(DIRS.dennik);
  return fs
    .readdirSync(DIRS.dennik)
    .filter((f) => f.endsWith('.json'))
    .map((f) => JSON.parse(fs.readFileSync(path.join(DIRS.dennik, f), 'utf8')))
    .sort((a, b) => b.datum.localeCompare(a.datum));
}

export function readDennikDen(datum) {
  const file = path.join(DIRS.dennik, `${datum}.json`);
  if (!fs.existsSync(file)) return null;
  return JSON.parse(fs.readFileSync(file, 'utf8'));
}

export function writeDennikDen(zaznam) {
  ensureDir(DIRS.dennik);
  const file = path.join(DIRS.dennik, `${zaznam.datum}.json`);
  fs.writeFileSync(file, JSON.stringify(zaznam, null, 2) + '\n');
}

// ---------- poznámky ----------

export function readPoznamky() {
  ensureDir(DIRS.poznamky);
  return fs
    .readdirSync(DIRS.poznamky)
    .filter((f) => f.endsWith('.md'))
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

export function readPoznamka(slug) {
  return readPoznamky().find((p) => p.slug === slug) ?? null;
}

export function writePoznamka({ nazov, tagy, body }) {
  ensureDir(DIRS.poznamky);
  const datum = dnes();
  let slug = slugify(nazov);
  let file = path.join(DIRS.poznamky, `${slug}.md`);
  let i = 2;
  while (fs.existsSync(file)) {
    file = path.join(DIRS.poznamky, `${slug}-${i}.md`);
    i += 1;
  }
  fs.writeFileSync(file, serializeFrontmatter({ nazov, datum, tagy }, body));
}

// ---------- projekty ----------

export function readProjekty() {
  ensureDir(DIRS.projekty);
  return fs
    .readdirSync(DIRS.projekty)
    .filter((f) => f.endsWith('.md'))
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

export function writeProjektDalsiKrok(slug, dalsi_krok) {
  const file = path.join(DIRS.projekty, `${slug}.md`);
  if (!fs.existsSync(file)) return;
  const { meta, body } = parseFrontmatter(fs.readFileSync(file, 'utf8'));
  meta.dalsi_krok = dalsi_krok;
  fs.writeFileSync(file, serializeFrontmatter(meta, body));
}

// ---------- work log ----------

const WORKLOG = path.join(ROOT, 'worklog.json');

export function readWorklog() {
  if (!fs.existsSync(WORKLOG)) return [];
  return JSON.parse(fs.readFileSync(WORKLOG, 'utf8')).sort((a, b) =>
    b.datum.localeCompare(a.datum)
  );
}

export function appendWorklog(zaznam) {
  ensureDir(ROOT);
  const log = fs.existsSync(WORKLOG) ? JSON.parse(fs.readFileSync(WORKLOG, 'utf8')) : [];
  log.push(zaznam);
  fs.writeFileSync(WORKLOG, JSON.stringify(log, null, 2) + '\n');
}
