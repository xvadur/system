#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Extrahuje len user zmienky o konkrétnej téme z konverzácií.
"""

import json
import sys
from pathlib import Path
from typing import List, Dict

def extract_user_mentions(
    query_words: List[str],
    conversations_file: Path,
    output_path: Path
) -> None:
    """
    Extrahuje user texty, ktoré obsahujú relevantné slová.
    """
    results = []
    
    print(f"📖 Načítavam konverzácie z: {conversations_file}")
    
    with open(conversations_file, 'r', encoding='utf-8') as f:
        for line_num, line in enumerate(f, 1):
            try:
                data = json.loads(line)
                
                # Rôzne formáty - skús rôzne kľúče
                user_text = ""
                if 'user' in data:
                    user_text = data.get('user', '').strip()
                elif 'user_prompt' in data:
                    user_prompt = data.get('user_prompt', {})
                    if isinstance(user_prompt, dict):
                        user_text = user_prompt.get('extracted_text', user_prompt.get('text', '')).strip()
                    else:
                        user_text = str(user_prompt).strip()
                elif 'prompt' in data:
                    user_text = data.get('prompt', '').strip()
                
                if not user_text:
                    continue
                
                # Skontroluj, či obsahuje relevantné slová
                user_lower = user_text.lower()
                if any(word.lower() in user_lower for word in query_words):
                    results.append({
                        'text': user_text,
                        'date': data.get('date', 'N/A'),
                        'timestamp': data.get('timestamp', 'N/A'),
                        'line': line_num
                    })
            except Exception as e:
                print(f"⚠️  Chyba na riadku {line_num}: {e}")
                continue
    
    print(f"✅ Nájdených {len(results)} relevantných user textov")
    
    # Vytvor markdown
    md_lines = []
    md_lines.append(f"# User zmienky o: {", ".join(query_words)}\n")
    md_lines.append(f"**Súbor:** `{conversations_file.name}`\n")
    md_lines.append(f"**Počet výsledkov:** {len(results)}\n")
    md_lines.append("---\n\n")
    
    for idx, result in enumerate(results, 1):
        md_lines.append(f"## Zmienka #{idx}\n")
        md_lines.append(f"**Dátum:** {result['date']}  \n")
        md_lines.append(f"**Timestamp:** {result['timestamp']}  \n")
        md_lines.append(f"**Riadok:** {result['line']}\n\n")
        md_lines.append("**Text:**\n")
        md_lines.append(f"{result['text']}\n\n")
        md_lines.append("---\n\n")
    
    # Ulož
    output_path.parent.mkdir(parents=True, exist_ok=True)
    with open(output_path, 'w', encoding='utf-8') as f:
        f.write(''.join(md_lines))
    
    print(f"✅ Markdown uložený: {output_path}")


if __name__ == "__main__":
    if len(sys.argv) < 3:
        print("Použitie: python3 extract_user_mentions.py <conversations_file> <output_file> [query_words...]")
        print("Príklad: python3 extract_user_mentions.py conversations.jsonl output.md kresťanstvo biblia")
        sys.exit(1)
    
    conversations_file = Path(sys.argv[1])
    output_file = Path(sys.argv[2])
    query_words = sys.argv[3:] if len(sys.argv) > 3 else ['kresťanstvo', 'biblia', 'kresťan', 'vier', 'nábožen']
    
    extract_user_mentions(query_words, conversations_file, output_file)
