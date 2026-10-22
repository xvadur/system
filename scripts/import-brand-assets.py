"""One-time import of the existing local studies into the standalone brand book.

The resulting catalog/data and public/brand files are committed: a fresh clone
needs neither the private originals nor the old Python servers.
"""
from pathlib import Path
import base64
import hashlib
import json
import re
import shutil

ROOT = Path(__file__).resolve().parent.parent
STUDIES = ROOT / 'design/interview'
PUBLIC = ROOT / 'public/brand'
DATA = ROOT / 'catalog/data'
PUBLIC.mkdir(parents=True, exist_ok=True)
DATA.mkdir(parents=True, exist_ok=True)
(PUBLIC / 'fonts').mkdir(exist_ok=True)
(PUBLIC / 'licenses').mkdir(exist_ok=True)
(PUBLIC / 'photos').mkdir(exist_ok=True)

pairs = {}
faces = set()
for round_number, folder in enumerate(['', 'round-2', 'round-3', 'round-4'], 1):
    source = STUDIES / 'fonty' / folder
    for pair in json.loads((source / 'pairs.json').read_text()):
        original_round = (int(pair['id']) - 1) // 12 + 1
        pairs[pair['id']] = {**pair, 'round': original_round}
    css = (source / 'fonts-embedded.css').read_text()
    for face in re.findall(r'@font-face\s*\{[^}]+\}', css):
        def replace_font(match):
            binary = base64.b64decode(match.group(1))
            name = hashlib.sha256(binary).hexdigest()[:20] + '.woff2'
            (PUBLIC / 'fonts' / name).write_bytes(binary)
            return "url('/brand/fonts/" + name + "')"
        face = re.sub(r"url\(['\"]?data:font/woff2;base64,([^)'\"]+)['\"]?\)", replace_font, face)
        faces.add(face)
    for license_file in (source / 'assets').glob('*.txt'):
        (PUBLIC / 'licenses' / license_file.name).write_text('\n'.join(line.rstrip() for line in license_file.read_text().splitlines()) + '\n')

(PUBLIC / 'fonts.css').write_text('\n'.join(sorted(faces)) + '\n')
(DATA / 'font-pairs.json').write_text(json.dumps(sorted(pairs.values(), key=lambda p: p['id']), ensure_ascii=False, indent=2) + '\n')
favorites = json.loads((STUDIES / 'fonty/round-4/current-selection.json').read_text())
(DATA / 'font-favorites.json').write_text(json.dumps([p['id'] for p in favorites['pairs']], indent=2) + '\n')

manifest = json.loads((STUDIES / 'fotky/manifest.json').read_text())
images = []
for image in manifest['images']:
    name = image['id'] + '.webp'
    shutil.copy2(STUDIES / 'fotky' / image['thumbnail'], PUBLIC / 'photos' / name)
    images.append({**image, 'thumbnail': '/brand/photos/' + name})
(DATA / 'photos.json').write_text(json.dumps(images, ensure_ascii=False, indent=2) + '\n')
selection = json.loads((STUDIES / 'fotky/selection.json').read_text())
(DATA / 'photo-favorites.json').write_text(json.dumps(selection['selected'], indent=2) + '\n')
print(f'Imported {len(pairs)} font pairs, {len(faces)} font faces, {len(images)} photos.')
