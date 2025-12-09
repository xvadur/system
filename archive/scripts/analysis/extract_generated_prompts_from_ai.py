#!/usr/bin/env python3
"""
Extrakcia promptov, ktoré AI vygenerovalo pre užívateľa z AI odpovedí.
Identifikuje rôzne typy promptov: system prompts, user prompts, šablóny, atď.
"""

import json
import re
import sys
from pathlib import Path
from datetime import datetime
from typing import List, Dict, Set
from collections import defaultdict

workspace_root = Path(__file__).parent.parent
input_file = workspace_root / "xvadur" / "data" / "kortex_guaranteed" / "ai_responses_guaranteed.jsonl"
output_dir = workspace_root / "xvadur" / "data" / "ai_generated_prompts"

output_dir.mkdir(parents=True, exist_ok=True)

print("🔍 Extrakcia Vygenerovaných Promptov z AI Odpovedí\n")
print(f"📁 Input: {input_file}")
print(f"📁 Output: {output_dir}\n")


# Vzorce pre detekciu promptov
PROMPT_PATTERNS = [
    # System prompts
    (r"(?i)(?:^|\n)(?:You are|System:|System Prompt:|System Instructions?:|ROLE|You are to assume the role|Your mission is)",
     "system_prompt"),
    
    # Markers pre prompt bloky
    (r"(?i)(?:\[PROMPT START\]|\[PROMPT_END\]|# \[PROMPT START\]|# PROMPT START|PROMPT START|PROMPT END)",
     "prompt_marker"),
    
    # Explicitné prompt headers
    (r"(?i)(?:^|\n)(?:Prompt:|Prompt Template:|Prompt Engineering:|Generated Prompt:|Here is (?:the|a) prompt)",
     "explicit_prompt"),
    
    # Code blocks s promptom
    (r"```(?:prompt|system|template|markdown)?\s*\n(?:You are|System:|# System|## System|ROLE)",
     "code_block_prompt"),
    
    # Štruktúrované prompty s sekciami
    (r"(?i)(?:^|\n)(?:##?\s*(?:ROLE|OBJECTIVE|CONTEXT|INSTRUCTIONS|CONSTRAINTS|OUTPUT FORMAT)|###?\s*(?:Role|Objective|Context|Instructions))",
     "structured_prompt"),
    
    # Prompt matice / templates
    (r"(?i)(?:Prompt-Matice|Prompt Matice|prompt matice|Template:|Šablóna:|Prompt Template)",
     "prompt_template"),
    
    # Instructions v promptoch
    (r"(?i)(?:^|\n)(?:Instructions?:|Your task is|Your goal is|Primary Directive|REQUIRED OUTPUT FORMAT)",
     "prompt_instructions"),
]


def detect_prompt_type(text: str) -> List[Dict[str, any]]:
    """Detekuje typ promptu a vráti informácie o ňom."""
    detected = []
    
    for pattern, prompt_type in PROMPT_PATTERNS:
        matches = re.finditer(pattern, text, re.MULTILINE)
        for match in matches:
            detected.append({
                "type": prompt_type,
                "start": match.start(),
                "end": match.end(),
                "match_text": match.group(),
            })
    
    return detected


def extract_code_blocks(text: str) -> List[Dict[str, any]]:
    """Extrahuje code blocks, ktoré môžu obsahovať prompty."""
    code_blocks = []
    
    # Markdown code blocks
    pattern = r"```(?:prompt|system|template|markdown|text)?\s*\n(.*?)```"
    for match in re.finditer(pattern, text, re.DOTALL):
        code_blocks.append({
            "type": "code_block",
            "language": match.group(1) if match.groups() else None,
            "content": match.group(0),
            "start": match.start(),
            "end": match.end(),
        })
    
    return code_blocks


def extract_prompt_content(text: str, detections: List[Dict], code_blocks: List[Dict]) -> List[str]:
    """Extrahuje skutočný obsah promptov na základe detekcií."""
    extracted_prompts = []
    
    # Najprv extrahuj code blocks, ktoré vyzerajú ako prompty
    for code_block in code_blocks:
        content = code_block["content"]
        # Odstráň markdown wrapper
        content = re.sub(r"```\w*\n", "", content)
        content = re.sub(r"```$", "", content).strip()
        
        # Skontroluj, či to vyzerá ako prompt
        if re.search(r"(?i)(?:You are|System:|ROLE|Your task|Instructions)", content):
            extracted_prompts.append({
                "prompt": content,
                "source": "code_block",
                "type": "code_block_prompt"
            })
    
    # Potom extrahuj prompty na základe detekcií
    for detection in detections:
        start = detection["start"]
        
        # Skús extrahovať prompt od detekcie až po koniec odseku/sekcie
        # Hľadáme koniec promptu (prázdny riadok, nová sekcia, atď.)
        text_after = text[start:]
        
        # Ak je to system prompt, extrahuj do konca odseku alebo do nasledujúcej sekcie
        if detection["type"] == "system_prompt":
            # Extrahuj do konca odstavca alebo do max 2000 znakov
            match = re.search(r"(.{0,2000}?)(?:\n\n|\n##|$)", text_after, re.DOTALL)
            if match:
                prompt_content = match.group(1).strip()
                if len(prompt_content) > 50:  # Minimálna dĺžka
                    extracted_prompts.append({
                        "prompt": prompt_content,
                        "source": "text_extraction",
                        "type": "system_prompt"
                    })
        
        # Ak je to prompt marker, extrahuj obsah medzi markerami
        elif detection["type"] == "prompt_marker":
            # Hľadaj koniec promptu
            end_marker = re.search(r"\[PROMPT (?:END|_END)\]", text_after, re.IGNORECASE)
            if end_marker:
                prompt_content = text_after[:end_marker.start()].strip()
                # Odstráň začiatočný marker
                prompt_content = re.sub(r"(?i)^.*?\[PROMPT START\]\s*", "", prompt_content)
                if len(prompt_content) > 50:
                    extracted_prompts.append({
                        "prompt": prompt_content,
                        "source": "marker_extraction",
                        "type": "prompt_marker"
                    })
    
    return extracted_prompts


def is_likely_prompt(text: str) -> bool:
    """Skontroluje, či text vyzerá ako prompt."""
    prompt_indicators = [
        r"(?i)You are",
        r"(?i)System:",
        r"(?i)Your task is",
        r"(?i)Instructions?:",
        r"(?i)ROLE",
        r"(?i)Your goal is",
        r"(?i)Primary Directive",
        r"(?i)Output Format",
        r"(?i)Constraints?:",
    ]
    
    for indicator in prompt_indicators:
        if re.search(indicator, text):
            return True
    
    return False


def clean_prompt(prompt: str) -> str:
    """Vyčistí prompt od nepotrebných znakov."""
    # Odstráň príliš veľa prázdnych riadkov
    prompt = re.sub(r"\n{3,}", "\n\n", prompt)
    
    # Odstráň začiatočné/koncové prázdne znaky
    prompt = prompt.strip()
    
    return prompt


def load_ai_responses() -> List[Dict]:
    """Načíta AI odpovede."""
    responses = []
    
    if not input_file.exists():
        print(f"⚠️  Súbor neexistuje: {input_file}")
        return responses
    
    print(f"📖 Načítavam AI odpovede...")
    
    with open(input_file, 'r', encoding='utf-8') as f:
        for line_num, line in enumerate(f, 1):
            try:
                data = json.loads(line)
                
                text = data.get("extracted_text", "")
                if not text:
                    continue
                
                timestamp = data.get("date_created", "")
                uuid = data.get("uuid", "")
                session = data.get("session", "")
                
                responses.append({
                    "uuid": uuid,
                    "session": session,
                    "timestamp": timestamp,
                    "text": text,
                    "text_length": len(text),
                    "word_count": data.get("word_count", len(text.split())),
                })
            except Exception:
                continue
    
    print(f"✅ Načítaných {len(responses)} AI odpovedí")
    return responses


def extract_prompts_from_response(response: Dict) -> List[Dict]:
    """Extrahuje prompty z jednej AI odpovede."""
    text = response["text"]
    extracted = []
    
    # Detekuj prompty
    detections = detect_prompt_type(text)
    
    # Extrahuj code blocks
    code_blocks = extract_code_blocks(text)
    
    # Extrahuj obsah promptov
    prompt_contents = extract_prompt_content(text, detections, code_blocks)
    
    # Pre každý extrahovaný prompt
    for prompt_data in prompt_contents:
        prompt_text = prompt_data["prompt"]
        
        # Vyčisti prompt
        prompt_text = clean_prompt(prompt_text)
        
        # Skontroluj, či to naozaj vyzerá ako prompt
        if not is_likely_prompt(prompt_text):
            continue
        
        # Minimálna dĺžka
        if len(prompt_text) < 50:
            continue
        
        extracted.append({
            "prompt": prompt_text,
            "prompt_type": prompt_data.get("type", "unknown"),
            "source": prompt_data.get("source", "unknown"),
            "response_uuid": response["uuid"],
            "response_session": response["session"],
            "response_timestamp": response["timestamp"],
            "word_count": len(prompt_text.split()),
            "char_count": len(prompt_text),
        })
    
    return extracted


def categorize_prompt(prompt_text: str) -> str:
    """Kategorizuje prompt podľa obsahu."""
    text_lower = prompt_text.lower()
    
    if re.search(r"(?i)(?:system|you are|role|mission)", prompt_text):
        if re.search(r"(?i)(?:synthes|analyz|extract|generate)", prompt_text):
            return "system_analysis"
        elif re.search(r"(?i)(?:chat|conversation|dialogue)", prompt_text):
            return "system_chat"
        else:
            return "system_general"
    
    elif re.search(r"(?i)(?:template|šablóna|matice)", prompt_text):
        return "template"
    
    elif re.search(r"(?i)(?:instructions|task|goal|objective)", prompt_text):
        return "instructions"
    
    elif re.search(r"(?i)(?:format|output|structure)", prompt_text):
        return "format_spec"
    
    else:
        return "other"


def main():
    """Hlavná funkcia."""
    
    # Načítaj AI odpovede
    responses = load_ai_responses()
    
    if not responses:
        print("❌ Žiadne AI odpovede na spracovanie")
        return
    
    print(f"\n🔍 Extrahujem prompty z {len(responses)} AI odpovedí...\n")
    
    all_prompts = []
    prompt_count_by_type = defaultdict(int)
    
    for i, response in enumerate(responses, 1):
        if i % 100 == 0:
            print(f"  Spracovaných {i}/{len(responses)} odpovedí...")
        
        extracted = extract_prompts_from_response(response)
        
        for prompt_data in extracted:
            # Kategorizuj prompt
            category = categorize_prompt(prompt_data["prompt"])
            prompt_data["category"] = category
            prompt_count_by_type[category] += 1
            
            all_prompts.append(prompt_data)
    
    print(f"\n✅ Extrahovaných {len(all_prompts)} promptov\n")
    
    # Zobraziť štatistiky
    print("📊 Štatistiky podľa kategórií:")
    for category, count in sorted(prompt_count_by_type.items()):
        print(f"  - {category}: {count}")
    
    # Ulož všetky prompty
    all_prompts_file = output_dir / "all_prompts.jsonl"
    with open(all_prompts_file, 'w', encoding='utf-8') as f:
        for prompt_data in all_prompts:
            f.write(json.dumps(prompt_data, ensure_ascii=False) + "\n")
    
    print(f"\n💾 Uložené všetky prompty: {all_prompts_file}")
    
    # Zoskup podľa kategórií
    prompts_by_category = defaultdict(list)
    for prompt_data in all_prompts:
        prompts_by_category[prompt_data["category"]].append(prompt_data)
    
    # Ulož podľa kategórií
    category_dir = output_dir / "by_category"
    category_dir.mkdir(exist_ok=True)
    
    for category, category_prompts in prompts_by_category.items():
        category_file = category_dir / f"{category}.jsonl"
        with open(category_file, 'w', encoding='utf-8') as f:
            for prompt_data in category_prompts:
                f.write(json.dumps(prompt_data, ensure_ascii=False) + "\n")
        
        print(f"  ✅ {category}: {len(category_prompts)} promptov → {category_file.name}")
    
    # Vytvor README
    readme_content = f"""# 🤖 Prompty Vygenerované AI

**Vytvorené:** {datetime.now().strftime('%Y-%m-%d %H:%M')}  
**Zdroj:** `xvadur/data/dataset/responses.jsonl`

---

## 📊 Prehľad

- **Celkom extrahovaných promptov:** {len(all_prompts)}
- **Zdrojových AI odpovedí:** {len(responses)}
- **Priemer promptov na odpoveď:** {len(all_prompts) / len(responses):.2f}

---

## 📁 Kategórie

"""
    
    for category, count in sorted(prompt_count_by_type.items()):
        readme_content += f"- **{category}:** {count} promptov\n"
    
    readme_content += f"""
---

## 📂 Súbory

- `all_prompts.jsonl` - Všetky extrahované prompty
- `by_category/` - Prompty zoskupené podľa kategórií
  - `system_analysis.jsonl` - System prompty pre analýzy
  - `system_chat.jsonl` - System prompty pre konverzácie
  - `system_general.jsonl` - Ostatné system prompty
  - `template.jsonl` - Prompt šablóny
  - `instructions.jsonl` - Inštrukčné prompty
  - `format_spec.jsonl` - Formátové špecifikácie
  - `other.jsonl` - Ostatné prompty

---

## 🔍 Ako to Funguje

Skript identifikuje prompty pomocou viacerých vzorcov:
- System prompts ("You are", "System:", "ROLE")
- Prompt markery ("[PROMPT START]", "[PROMPT END]")
- Code blocks s promptmi
- Štruktúrované prompty (sekcie: ROLE, OBJECTIVE, CONTEXT, atď.)
- Prompt templates a šablóny

---

**Automaticky vygenerované:** {datetime.now().strftime('%Y-%m-%d %H:%M')}
"""
    
    readme_file = output_dir / "README.md"
    with open(readme_file, 'w', encoding='utf-8') as f:
        f.write(readme_content)
    
    print(f"\n💾 README vytvorený: {readme_file}")
    print(f"\n🎉 Extrakcia dokončená!")
    print(f"📁 Výsledky: {output_dir}")


if __name__ == "__main__":
    main()

