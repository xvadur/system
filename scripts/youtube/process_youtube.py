#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
YouTube Video Processor: Stiahne video, extrahuje transkripciu a metadata.

Použitie:
    python scripts/youtube/process_youtube.py <youtube_url> [--audio-only] [--transcript-only]
    
Príklady:
    # Stiahne video + transkripciu + metadata
    python scripts/youtube/process_youtube.py https://www.youtube.com/watch?v=xNcEgqzlPqs
    
    # Len audio + transkripcia
    python scripts/youtube/process_youtube.py https://www.youtube.com/watch?v=xNcEgqzlPqs --audio-only
    
    # Len transkripcia (bez sťahovania videa)
    python scripts/youtube/process_youtube.py https://www.youtube.com/watch?v=xNcEgqzlPqs --transcript-only
"""

import json
import os
import sys
import argparse
import tempfile
import re
from pathlib import Path
from datetime import datetime
from typing import Dict, Optional

# Workspace root (2 levels up from scripts/youtube/)
_workspace_root = Path(__file__).parent.parent.parent

try:
    import yt_dlp
except ImportError:
    print("❌ Chyba: Potrebuješ nainštalovať yt-dlp")
    print("   pip install yt-dlp")
    sys.exit(1)


def extract_video_id(url: str) -> str:
    """
    Extrahuje video ID z YouTube URL.
    
    Podporuje formáty:
    - https://www.youtube.com/watch?v=VIDEO_ID
    - https://youtu.be/VIDEO_ID
    - https://www.youtube.com/embed/VIDEO_ID
    """
    if "watch?v=" in url:
        return url.split("watch?v=")[1].split("&")[0]
    elif "youtu.be/" in url:
        return url.split("youtu.be/")[1].split("?")[0]
    elif "embed/" in url:
        return url.split("embed/")[1].split("?")[0]
    else:
        raise ValueError(f"Nepodporovaný formát URL: {url}")


def get_video_info(url: str) -> Dict:
    """
    Získa základné informácie o videu bez sťahovania.
    
    Returns:
        Dict s metadatami videa (názov, kanál, dĺžka, atď.)
    """
    ydl_opts = {
        'quiet': True,
        'no_warnings': True,
        'skip_download': True,
    }
    
    try:
        with yt_dlp.YoutubeDL(ydl_opts) as ydl:
            info = ydl.extract_info(url, download=False)
            
            return {
                'id': info.get('id'),
                'title': info.get('title'),
                'description': info.get('description', ''),
                'channel': info.get('uploader'),
                'channel_id': info.get('channel_id'),
                'duration': info.get('duration'),  # v sekundách
                'view_count': info.get('view_count'),
                'like_count': info.get('like_count'),
                'upload_date': info.get('upload_date'),  # YYYYMMDD
                'thumbnail': info.get('thumbnail'),
                'url': url,
                'extracted_at': datetime.now().isoformat(),
            }
    except Exception as e:
        print(f"❌ Chyba pri získavaní informácií o videu: {e}")
        raise


def parse_subtitle_file(subtitle_path: Path) -> str:
    """
    Parsuje subtitle súbor (VTT alebo SRT) a vráti čistý text.
    
    Args:
        subtitle_path: Cesta k subtitle súboru
    
    Returns:
        Čistý text transkripcie
    """
    if not subtitle_path.exists():
        return ""
    
    text_lines = []
    
    with open(subtitle_path, 'r', encoding='utf-8') as f:
        content = f.read()
    
    # VTT formát: odstráni časové značky a HTML tagy
    if subtitle_path.suffix == '.vtt':
        # Odstráni VTT hlavičku
        content = re.sub(r'WEBVTT\n.*?\n\n', '', content, flags=re.DOTALL)
        # Odstráni časové značky (napr. "00:00:01.000 --> 00:00:03.000")
        content = re.sub(r'\d{2}:\d{2}:\d{2}\.\d{3} --> \d{2}:\d{2}:\d{2}\.\d{3}\n', '', content)
        # Odstráni HTML tagy
        content = re.sub(r'<[^>]+>', '', content)
        # Odstráni čísla riadkov
        content = re.sub(r'^\d+\n', '', content, flags=re.MULTILINE)
    
    # SRT formát: odstráni časové značky a čísla
    elif subtitle_path.suffix == '.srt':
        # Odstráni čísla riadkov a časové značky
        content = re.sub(r'^\d+\n', '', content, flags=re.MULTILINE)
        content = re.sub(r'\d{2}:\d{2}:\d{2}[,.]\d{3} --> \d{2}:\d{2}:\d{2}[,.]\d{3}\n', '', content)
    
    # Vyčisti riadky a spoj do jedného textu
    for line in content.split('\n'):
        line = line.strip()
        if line and not line.isdigit():
            text_lines.append(line)
    
    return ' '.join(text_lines)


def get_transcript(url: str) -> Optional[str]:
    """
    Pokúsi sa získať transkripciu videa.
    
    Returns:
        Transkripcia ako text, alebo None ak nie je dostupná
    """
    video_id = extract_video_id(url)
    
    # Vytvor dočasný adresár pre titulky
    with tempfile.TemporaryDirectory() as temp_dir:
        temp_path = Path(temp_dir)
        subtitle_file = temp_path / f"{video_id}.%(ext)s"
        
        ydl_opts = {
            'writesubtitles': True,
            'writeautomaticsub': True,  # Automatické titulky
            'subtitleslangs': ['en', 'sk', 'all'],  # Angličtina, slovenčina, alebo akékoľvek
            'skip_download': True,
            'quiet': True,
            'outtmpl': str(subtitle_file),
        }
        
        try:
            with yt_dlp.YoutubeDL(ydl_opts) as ydl:
                info = ydl.extract_info(url, download=False)
                
                # Skús nájsť dostupné titulky
                subtitles = info.get('subtitles', {})
                auto_captions = info.get('automatic_captions', {})
                
                # Priorita: automatické titulky v angličtine > slovenčina > akékoľvek automatické > manuálne
                available_langs = []
                if auto_captions:
                    available_langs.extend(auto_captions.keys())
                if subtitles:
                    available_langs.extend(subtitles.keys())
                
                # Vyber najlepší jazyk
                selected_lang = None
                for lang in ['en', 'sk']:
                    if lang in available_langs:
                        selected_lang = lang
                        break
                
                if not selected_lang and available_langs:
                    selected_lang = available_langs[0]
                
                if selected_lang:
                    # Stiahneme titulky
                    ydl_opts_download = {
                        'writesubtitles': True,
                        'writeautomaticsub': True,
                        'subtitleslangs': [selected_lang], 
                        'skip_download': True,
                        'quiet': True,
                        'outtmpl': str(subtitle_file),
                    }
                    
                    with yt_dlp.YoutubeDL(ydl_opts_download) as ydl_dl:
                        ydl_dl.extract_info(url, download=True)
                        
                        # Nájdeme stiahnutý subtitle súbor
                        # yt-dlp môže uložiť ako .vtt alebo .srt
                        for ext in ['.vtt', '.srt', f'.{selected_lang}.vtt', f'.{selected_lang}.srt']:
                            subtitle_path = temp_path / f"{video_id}{ext}"
                            if subtitle_path.exists():
                                transcript = parse_subtitle_file(subtitle_path)
                                if transcript:
                                    return transcript
                        
                        # Skús nájsť akýkoľvek subtitle súbor
                        for subtitle_path in temp_path.glob(f"{video_id}*"):
                            if subtitle_path.suffix in ['.vtt', '.srt']:
                                transcript = parse_subtitle_file(subtitle_path)
                                if transcript:
                                    return transcript
            
            return None
            
        except Exception as e:
            print(f"⚠️  Transkripcia nie je dostupná: {e}")
            return None


def download_video(url: str, output_dir: Path, audio_only: bool = False) -> Dict:
    """
    Stiahne video alebo audio.
    
    Args:
        url: YouTube URL
        output_dir: Adresár pre uloženie
        audio_only: Ak True, stiahne len audio
    
    Returns:
        Dict s cestami k stiahnutým súborom
    """
    video_id = extract_video_id(url)
    output_dir.mkdir(parents=True, exist_ok=True)
    
    if audio_only:
        output_template = str(output_dir / f"{video_id}.%(ext)s")
        ydl_opts = {
            'format': 'bestaudio/best',
            'outtmpl': output_template,
            'postprocessors': [{
                'key': 'FFmpegExtractAudio',
                'preferredcodec': 'mp3',
                'preferredquality': '192',
            }],
        }
    else:
        output_template = str(output_dir / f"{video_id}.%(ext)s")
        ydl_opts = {
            'format': 'best[height<=720]',  # Max 720p pre menšie súbory
            'outtmpl': output_template,
        }
    
    try:
        with yt_dlp.YoutubeDL(ydl_opts) as ydl:
            info = ydl.extract_info(url, download=True)
            
            # Nájdeme stiahnutý súbor
            filename = ydl.prepare_filename(info)
            if audio_only:
                filename = filename.rsplit('.', 1)[0] + '.mp3'
            
            return {
                'downloaded_file': filename,
                'format': 'audio' if audio_only else 'video',
            }
    except Exception as e:
        print(f"❌ Chyba pri sťahovaní: {e}")
        raise


def save_metadata(metadata: Dict, output_dir: Path) -> Path:
    """
    Uloží metadata do JSON súboru.
    
    Returns:
        Cesta k uloženému súboru
    """
    output_dir.mkdir(parents=True, exist_ok=True)
    video_id = metadata.get('id', 'unknown')
    output_file = output_dir / f"{video_id}_metadata.json"
    
    with open(output_file, 'w', encoding='utf-8') as f:
        json.dump(metadata, f, ensure_ascii=False, indent=2)
    
    return output_file


def process_youtube_video(
    url: str,
    output_dir: Optional[Path] = None,
    audio_only: bool = False,
    transcript_only: bool = False,
    save_metadata_file: bool = True,
) -> Dict:
    """
    Hlavná funkcia na spracovanie YouTube videa.
    
    Args:
        url: YouTube URL
        output_dir: Adresár pre výstup (default: development/data/youtube/)
        audio_only: Stiahnuť len audio
        transcript_only: Získať len transkripciu (bez sťahovania videa)
        save_metadata_file: Uložiť metadata do JSON súboru
    
    Returns:
        Dict s výsledkami spracovania
    """
    if output_dir is None:
        output_dir = _workspace_root / "development" / "data" / "youtube"
    
    print(f"📹 Spracovávam video: {url}")
    
    # 1. Získaj základné informácie
    print("📊 Získavam metadata...")
    metadata = get_video_info(url)
    print(f"   ✅ Názov: {metadata['title']}")
    print(f"   ✅ Kanál: {metadata['channel']}")
    print(f"   ✅ Dĺžka: {metadata['duration']}s")
    
    result = {
        'metadata': metadata,
        'transcript': None,
        'downloaded_file': None,
    }
    
    # 2. Pokús sa získať transkripciu
    if transcript_only or not transcript_only:  # Vždy skús transkripciu
        print("📝 Pokúšam sa získať transkripciu...")
        transcript = get_transcript(url)
        if transcript:
            result['transcript'] = transcript
            print("   ✅ Transkripcia získaná")
        else:
            print("   ⚠️  Transkripcia nie je dostupná")
    
    # 3. Stiahni video/audio (ak nie je transcript_only)
    if not transcript_only:
        print(f"⬇️  Sťahujem {'audio' if audio_only else 'video'}...")
        download_result = download_video(url, output_dir, audio_only=audio_only)
        result['downloaded_file'] = download_result['downloaded_file']
        print(f"   ✅ Uložené: {download_result['downloaded_file']}")
    
    # 4. Ulož metadata
    if save_metadata_file:
        metadata_file = save_metadata(metadata, output_dir)
        result['metadata_file'] = str(metadata_file)
        print(f"   ✅ Metadata uložené: {metadata_file}")
    
    return result


def main():
    """Hlavná funkcia CLI."""
    parser = argparse.ArgumentParser(
        description="Spracuje YouTube video: stiahne, extrahuje transkripciu a metadata"
    )
    parser.add_argument('url', help='YouTube URL')
    parser.add_argument('--audio-only', action='store_true', help='Stiahnuť len audio')
    parser.add_argument('--transcript-only', action='store_true', help='Získať len transkripciu')
    parser.add_argument('--output-dir', type=str, help='Výstupný adresár')
    parser.add_argument('--no-metadata-file', action='store_true', help='Neukladať metadata súbor')
    
    args = parser.parse_args()
    
    output_dir = Path(args.output_dir) if args.output_dir else None
    
    try:
        result = process_youtube_video(
            url=args.url,
            output_dir=output_dir,
            audio_only=args.audio_only,
            transcript_only=args.transcript_only,
            save_metadata_file=not args.no_metadata_file,
        )
        
        print("\n✅ Spracovanie dokončené!")
        print(f"\n📋 Výsledky:")
        print(f"   Metadata: {result.get('metadata_file', 'N/A')}")
        if result.get('downloaded_file'):
            print(f"   Súbor: {result['downloaded_file']}")
        if result.get('transcript'):
            print(f"   Transkripcia: {len(result['transcript'])} znakov")
        
        # Vypíš JSON výsledok (pre ďalšie spracovanie)
        print("\n📄 JSON výsledok:")
        print(json.dumps(result, ensure_ascii=False, indent=2))
        
    except Exception as e:
        print(f"\n❌ Chyba: {e}")
        sys.exit(1)


if __name__ == "__main__":
    main()

