#!/usr/bin/env python3
"""
Analyzuje extrahované prompty a vytvorí markdown dokument s popisom každého promptu.
"""

import json
import sys
from pathlib import Path
from datetime import datetime
from typing import List, Dict

workspace_root = Path(__file__).parent.parent
input_file = workspace_root / "xvadur" / "data" / "ai_generated_prompts" / "all_prompts.jsonl"
output_file = workspace_root / "xvadur" / "data" / "ai_generated_prompts" / "PROMPTS_ANALYSIS.md"

print("📝 Analýza Vygenerovaných Promptov\n")
print(f"📁 Input: {input_file}")
print(f"📁 Output: {output_file}\n")


def extract_prompt_summary(prompt_text: str) -> Dict[str, str]:
    """Extrahuje kľúčové informácie z promptu pre popis."""
    summary = {
        "purpose": "",
        "key_elements": [],
        "output_format": "",
        "length": len(prompt_text),
        "word_count": len(prompt_text.split())
    }
    
    prompt_lower = prompt_text.lower()
    
    # Detekcia účelu
    if "analysis" in prompt_lower or "analyze" in prompt_lower:
        summary["purpose"] += "Analýza dát alebo situácie. "
    if "extract" in prompt_lower:
        summary["purpose"] += "Extrakcia informácií. "
    if "create" in prompt_lower or "generate" in prompt_lower:
        summary["purpose"] += "Generovanie obsahu. "
    if "summarize" in prompt_lower or "summary" in prompt_lower:
        summary["purpose"] += "Vytvorenie súhrnu. "
    if "system prompt" in prompt_lower or "you are" in prompt_lower.lower():
        summary["purpose"] += "Definovanie role AI. "
    if "template" in prompt_lower or "šablóna" in prompt_lower:
        summary["purpose"] += "Šablóna pre opakované použitie. "
    if "instructions" in prompt_lower:
        summary["purpose"] += "Poskytnutie inštrukcií. "
    
    # Kľúčové elementy
    if "role" in prompt_lower:
        summary["key_elements"].append("Role")
    if "task" in prompt_lower:
        summary["key_elements"].append("Task")
    if "context" in prompt_lower:
        summary["key_elements"].append("Context")
    if "format" in prompt_lower or "output" in prompt_lower:
        summary["key_elements"].append("Output Format")
    if "structure" in prompt_lower or "structured" in prompt_lower:
        summary["key_elements"].append("Structured Response")
    if "examples" in prompt_lower:
        summary["key_elements"].append("Examples")
    
    # Output format
    if "markdown" in prompt_lower:
        summary["output_format"] = "Markdown"
    elif "json" in prompt_lower:
        summary["output_format"] = "JSON"
    elif "python" in prompt_lower or "code" in prompt_lower:
        summary["output_format"] = "Python/Code"
    else:
        summary["output_format"] = "Text"
    
    if not summary["purpose"]:
        summary["purpose"] = "Rôzne účely (potrebuje manuálnu kontrolu)"
    
    return summary


def analyze_prompt_category(prompt_text: str, category: str) -> str:
    """Analyzuje prompt a vylepšuje kategóriu."""
    prompt_lower = prompt_text.lower()
    
    # System Analysis
    if category == "system_analysis":
        if "mission" in prompt_lower or "briefing" in prompt_lower:
            return "System Analysis - Mission Briefing"
        elif "strategic" in prompt_lower or "strategy" in prompt_lower:
            return "System Analysis - Strategic Analysis"
        elif "phenomenological" in prompt_lower or "psychological" in prompt_lower:
            return "System Analysis - Psychological Analysis"
        else:
            return "System Analysis - General"
    
    # System General
    elif category == "system_general":
        if "you are" in prompt_lower[:200]:
            if "python" in prompt_lower or "script" in prompt_lower:
                return "System General - Code Generation"
            elif "assistant" in prompt_lower or "helper" in prompt_lower:
                return "System General - Assistant Role"
            else:
                return "System General - Role Definition"
        else:
            return "System General - Other"
    
    # System Chat
    elif category == "system_chat":
        return "System Chat - Conversation"
    
    # Template
    elif category == "template":
        return "Template - Reusable Format"
    
    return category


def get_category_description(category: str) -> str:
    """Vráti popis kategórie."""
    descriptions = {
        "system_analysis": "System prompty navrhnuté pre analýzy dát, situácií alebo strategických rozhodnutí.",
        "system_general": "Všeobecné system prompty pre rôzne úlohy a role AI.",
        "system_chat": "System prompty pre konverzačné režimy a chat interakcie.",
        "template": "Šablóny a formáty promptov pre opakované použitie.",
    }
    return descriptions.get(category, "Kategória bez špecifického popisu.")


def main():
    """Hlavná funkcia."""
    
    if not input_file.exists():
        print(f"❌ Súbor neexistuje: {input_file}")
        return
    
    print(f"📖 Načítavam prompty...")
    
    prompts = []
    with open(input_file, 'r', encoding='utf-8') as f:
        for line in f:
            try:
                data = json.loads(line)
                prompts.append(data)
            except Exception:
                continue
    
    print(f"✅ Načítaných {len(prompts)} promptov\n")
    print(f"🔍 Analyzujem prompty...")
    
    # Zoskupíme podľa kategórií
    prompts_by_category = {}
    for prompt_data in prompts:
        category = prompt_data.get("category", "other")
        if category not in prompts_by_category:
            prompts_by_category[category] = []
        prompts_by_category[category].append(prompt_data)
    
    # Vytvoríme markdown dokument
    md_content = f"""# 📋 Analýza Vygenerovaných Promptov

**Vytvorené:** {datetime.now().strftime('%Y-%m-%d %H:%M')}  
**Celkom promptov:** {len(prompts)}

---

## 📊 Prehľad

"""
    
    for category in sorted(prompts_by_category.keys()):
        count = len(prompts_by_category[category])
        md_content += f"- **{category.replace('_', ' ').title()}:** {count} promptov\n"
    
    md_content += "\n---\n\n"
    
    # Pre každú kategóriu
    for category in sorted(prompts_by_category.keys()):
        category_prompts = prompts_by_category[category]
        
        md_content += f"## 📁 {category.replace('_', ' ').title()}\n\n"
        md_content += f"{get_category_description(category)}\n\n"
        md_content += f"**Počet promptov:** {len(category_prompts)}\n\n"
        md_content += "---\n\n"
        
        # Pre každý prompt v kategórii
        for i, prompt_data in enumerate(category_prompts, 1):
            prompt_text = prompt_data.get("prompt", "")
            enhanced_category = analyze_prompt_category(prompt_text, category)
            summary = extract_prompt_summary(prompt_text)
            
            # Prvých 200 znakov pre preview
            preview = prompt_text[:200].replace("\n", " ").strip()
            if len(prompt_text) > 200:
                preview += "..."
            
            md_content += f"### Prompt #{i}: {enhanced_category}\n\n"
            md_content += f"**Kategória:** `{category}`\n\n"
            md_content += f"**Vylepšená kategória:** {enhanced_category}\n\n"
            md_content += f"**Účel:** {summary['purpose']}\n\n"
            
            if summary["key_elements"]:
                md_content += f"**Kľúčové elementy:** {', '.join(summary['key_elements'])}\n\n"
            
            md_content += f"**Formát výstupu:** {summary['output_format']}\n\n"
            md_content += f"**Dĺžka:** {summary['word_count']} slov, {summary['length']} znakov\n\n"
            
            # Metadata
            if prompt_data.get("response_timestamp"):
                md_content += f"**Dátum vytvorenia:** {prompt_data['response_timestamp'][:10]}\n\n"
            
            md_content += f"**Preview:**\n```\n{preview}\n```\n\n"
            
            # Úplný prompt v collapse sekcii
            md_content += "<details>\n"
            md_content += "<summary>📄 Zobraziť celý prompt</summary>\n\n"
            md_content += "```\n"
            md_content += prompt_text
            md_content += "\n```\n\n"
            md_content += "</details>\n\n"
            
            md_content += "---\n\n"
    
    # Zhrnutie
    md_content += f"""## 📈 Štatistiky

- **Celkom promptov:** {len(prompts)}
- **Kategórií:** {len(prompts_by_category)}
- **Priemerná dĺžka:** {sum(len(p.get('prompt', '')) for p in prompts) / len(prompts):.0f} znakov
- **Priemerný počet slov:** {sum(len(p.get('prompt', '').split()) for p in prompts) / len(prompts):.0f} slov

---

## 🔍 Typy Promptov

"""
    
    # Analýza typov
    types = {}
    for prompt_data in prompts:
        prompt_type = prompt_data.get("prompt_type", "unknown")
        types[prompt_type] = types.get(prompt_type, 0) + 1
    
    for prompt_type, count in sorted(types.items()):
        md_content += f"- **{prompt_type.replace('_', ' ').title()}:** {count}\n"
    
    md_content += f"\n---\n\n**Automaticky vygenerované:** {datetime.now().strftime('%Y-%m-%d %H:%M')}\n"
    
    # Uložíme
    with open(output_file, 'w', encoding='utf-8') as f:
        f.write(md_content)
    
    print(f"✅ Markdown vytvorený: {output_file}")
    print(f"\n📊 Štatistiky:")
    print(f"  - Celkom promptov: {len(prompts)}")
    print(f"  - Kategórií: {len(prompts_by_category)}")
    print(f"  - Priemerná dĺžka: {sum(len(p.get('prompt', '')) for p in prompts) / len(prompts):.0f} znakov")


if __name__ == "__main__":
    main()

