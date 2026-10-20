#!/usr/bin/env node
import { readFile, writeFile } from 'node:fs/promises';
import { fileURLToPath } from 'node:url';
import path from 'node:path';

const root = fileURLToPath(new URL('../', import.meta.url));
const usage = 'Použitie: npm run version:next -- patch|minor|major "Popis zmeny" [--dry-run]';

function parseArguments(args) {
  const positionals = [];
  let dryRun = false;
  let explicitMessage;
  for (let index = 0; index < args.length; index += 1) {
    const argument = args[index];
    if (argument === '--dry-run') {
      if (dryRun) throw new Error('Voľbu --dry-run uveď iba raz.');
      dryRun = true;
    } else if (argument === '--message') {
      if (explicitMessage !== undefined || !args[index + 1] || args[index + 1].startsWith('--')) {
        throw new Error('Voľba --message vyžaduje jeden popis zmeny.');
      }
      explicitMessage = args[++index];
    } else if (argument.startsWith('--')) {
      throw new Error(`Neznáma voľba: ${argument}`);
    } else {
      positionals.push(argument);
    }
  }

  const [kind, positionalMessage] = positionals;
  if (!['patch', 'minor', 'major'].includes(kind)) throw new Error(usage);
  if (positionals.length > 2 || (positionalMessage !== undefined && explicitMessage !== undefined)) {
    throw new Error('Uveď jeden popis zmeny v úvodzovkách alebo cez --message.');
  }
  const message = (explicitMessage ?? positionalMessage ?? '').trim();
  if (message.length < 3 || message.length > 240 || /[\r\n\u0000-\u001f\u007f]/u.test(message)) {
    throw new Error('Popis musí mať 3–240 znakov na jednom riadku.');
  }
  return { kind, message, dryRun };
}

function nextVersion(current, kind) {
  const match = /^(0|[1-9]\d*)\.(0|[1-9]\d*)\.(0|[1-9]\d*)$/u.exec(current);
  if (!match) throw new Error(`Nepodporovaná verzia ${JSON.stringify(current)}. Očakávaný tvar je X.Y.Z.`);
  const parts = match.slice(1).map(Number);
  if (parts.some((part) => !Number.isSafeInteger(part))) throw new Error('Číslo verzie je príliš veľké.');
  const index = { major: 0, minor: 1, patch: 2 }[kind];
  parts[index] += 1;
  if (!Number.isSafeInteger(parts[index])) throw new Error('Nové číslo verzie je príliš veľké.');
  for (let reset = index + 1; reset < parts.length; reset += 1) parts[reset] = 0;
  return parts.join('.');
}

try {
  const { kind, message, dryRun } = parseArguments(process.argv.slice(2));
  const packagePath = path.join(root, 'package.json');
  const lockPath = path.join(root, 'package-lock.json');
  const changelogPath = path.join(root, 'CHANGELOG.md');
  const [packageSource, lockSource, changelogSource] = await Promise.all([
    readFile(packagePath, 'utf8'),
    readFile(lockPath, 'utf8'),
    readFile(changelogPath, 'utf8'),
  ]);
  const manifest = JSON.parse(packageSource);
  const lockfile = JSON.parse(lockSource);
  const current = manifest.version;
  const next = nextVersion(current, kind);

  if (!manifest.name || lockfile.name !== manifest.name) throw new Error('Manifest a lockfile musia mať rovnaké meno balíka.');
  if (lockfile.version !== current) throw new Error('Koreňová verzia v package-lock.json sa nezhoduje s package.json.');
  if (!lockfile.packages?.[''] || lockfile.packages[''].version !== current) {
    throw new Error('Koreňový balík v package-lock.json chýba alebo má inú verziu. Spusti npm install a skontroluj lockfile.');
  }
  if (!/^# Changelog\s*$/mu.test(changelogSource)) throw new Error('CHANGELOG.md musí obsahovať nadpis # Changelog.');
  if (changelogSource.includes(`## [${next}]`)) throw new Error(`CHANGELOG.md už obsahuje verziu ${next}.`);

  const date = new Intl.DateTimeFormat('en-CA', {
    timeZone: 'Europe/Bratislava', year: 'numeric', month: '2-digit', day: '2-digit',
  }).format(new Date());
  const entry = `## [${next}] - ${date}\n\n- ${message}\n\n`;
  const firstRelease = /^## \[/mu.exec(changelogSource);
  const insertAt = firstRelease?.index ?? changelogSource.trimEnd().length;
  const prefix = changelogSource.slice(0, insertAt).trimEnd();
  const suffix = changelogSource.slice(insertAt);
  const nextChangelog = `${prefix}\n\n${entry}${suffix}`.trimEnd() + '\n';

  manifest.version = next;
  lockfile.version = next;
  lockfile.packages[''].version = next;

  if (!dryRun) {
    // All inputs are validated before changing any of the release files.
    await writeFile(packagePath, `${JSON.stringify(manifest, null, 2)}\n`);
    await writeFile(lockPath, `${JSON.stringify(lockfile, null, 2)}\n`);
    await writeFile(changelogPath, nextChangelog);
  }
  console.log(`${dryRun ? 'Náhľad' : 'Pripravené'}: ${manifest.name} ${current} → ${next}`);
  console.log(entry.trimEnd());
  console.log(dryRun ? 'Súbory zostali nezmenené.' : 'Upravené: package.json, package-lock.json, CHANGELOG.md. Git operácie sa nevykonali.');
} catch (error) {
  console.error(error instanceof Error ? error.message : String(error));
  process.exitCode = 1;
}
