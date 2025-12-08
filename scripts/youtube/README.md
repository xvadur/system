# YouTube Video Processor

Skript na spracovanie YouTube videí: stiahnutie, transkripcia, metadata.

## Inštalácia

```bash
pip install yt-dlp
```

Alebo cez `requirements.txt`:
```bash
pip install -r requirements.txt
```

## Použitie

### Základné použitie

```bash
# Stiahne video + transkripciu + metadata
python scripts/youtube/process_youtube.py https://www.youtube.com/watch?v=xNcEgqzlPqs
```

### Len audio

```bash
# Stiahne len audio (MP3) + transkripciu + metadata
python scripts/youtube/process_youtube.py https://www.youtube.com/watch?v=xNcEgqzlPqs --audio-only
```

### Len transkripcia

```bash
# Získa len transkripciu (bez sťahovania videa)
python scripts/youtube/process_youtube.py https://www.youtube.com/watch?v=xNcEgqzlPqs --transcript-only
```

### Vlastný výstupný adresár

```bash
python scripts/youtube/process_youtube.py <url> --output-dir /path/to/output
```

## Výstup

Skript vytvorí:

1. **Metadata súbor:** `{video_id}_metadata.json`
   - Názov, kanál, dĺžka, zobrazenia, atď.

2. **Video/Audio súbor:** `{video_id}.{ext}`
   - Video (default) alebo audio (s `--audio-only`)

3. **Transkripcia:** Vrátená v JSON výstupe (ak je dostupná)

## Príklad výstupu

```json
{
  "metadata": {
    "id": "xNcEgqzlPqs",
    "title": "The Memory Problem Breaking Every Al Agent-And How to Fix It",
    "channel": "AI News & Strategy Daily | Nate B Jones",
    "duration": 188,
    "view_count": 392,
    ...
  },
  "transcript": "Full transcript text here...",
  "downloaded_file": "/path/to/video.mp4",
  "metadata_file": "/path/to/metadata.json"
}
```

## Integrácia s RAG systémom

Výstup môže byť ďalej spracovaný a pridaný do RAG indexu:

```python
from scripts.youtube.process_youtube import process_youtube_video

result = process_youtube_video("https://www.youtube.com/watch?v=xNcEgqzlPqs")

# Použiť transkripciu pre RAG
if result['transcript']:
    # Pridať do RAG indexu
    pass
```

## Podporované formáty URL

- `https://www.youtube.com/watch?v=VIDEO_ID`
- `https://youtu.be/VIDEO_ID`
- `https://www.youtube.com/embed/VIDEO_ID`

## Poznámky

- Transkripcia je dostupná len ak video má titulky (automatické alebo manuálne)
- Video sa sťahuje v maximálnej kvalite 720p (pre menšie súbory)
- Audio sa konvertuje do MP3 (192 kbps)

