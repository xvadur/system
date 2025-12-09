import sys
import re
from pathlib import Path

def clean_vtt(vtt_path, output_path):
    print(f"Processing {vtt_path} -> {output_path}")
    
    with open(vtt_path, 'r', encoding='utf-8') as f:
        content = f.read()

    # Remove header
    lines = content.split('\n')
    cleaned_lines = []
    seen_lines = set()
    
    # Regex for timestamp lines (e.g., 00:00:00.000 --> 00:00:02.000)
    timestamp_pattern = re.compile(r'\d{2}:\d{2}:\d{2}\.\d{3} --> \d{2}:\d{2}:\d{2}\.\d{3}')
    
    # Regex for tags like <c> or <00:00:00.000>
    tag_pattern = re.compile(r'<[^>]+>')

    last_line = ""

    for line in lines:
        line = line.strip()
        
        # Skip empty lines, WEBVTT header, timestamps
        if not line or line == 'WEBVTT' or timestamp_pattern.match(line):
            continue
            
        # Remove tags
        line = tag_pattern.sub('', line)
        
        # Skip duplicates (VTT often repeats lines for karaoke effect)
        # We only keep if it's different from the immediate last line added
        if line != last_line:
            cleaned_lines.append(line)
            last_line = line

    # Join and save
    full_text = ' '.join(cleaned_lines)
    
    # Post-processing cleanup (fix double spaces etc)
    full_text = re.sub(r'\s+', ' ', full_text).strip()

    with open(output_path, 'w', encoding='utf-8') as f:
        f.write(full_text)
    
    print(f"Saved {len(full_text)} chars to {output_path}")

if __name__ == "__main__":
    if len(sys.argv) < 3:
        print("Usage: python vtt_to_txt.py <input_vtt> <output_txt>")
        sys.exit(1)
        
    clean_vtt(sys.argv[1], sys.argv[2])

