#!/usr/bin/env python3
"""
Lokálna chronologická syntéza príbehu (bez OpenAI API).
Vytvorí syntetizovaný naratív z kategorizovaných promptov pomocou lokálnej analýzy.
"""

import json
from pathlib import Path
from datetime import datetime
from typing import List, Dict
from collections import Counter, defaultdict

# Konfigurácia
CATEGORIZED_FILE = Path("data/prompts/prompts_categorized.jsonl")
TEMPORAL_MAP_FILE = Path("data/prompts/temporal_map.json")
OUTPUT_DIR = Path("data/prompts/synthesis")
OUTPUT_DIR.mkdir(parents=True, exist_ok=True)


def load_data() -> tuple:
    """Načíta kategorizované prompty a temporálnu mapu."""
    prompts = []
    with open(CATEGORIZED_FILE, 'r', encoding='utf-8') as f:
        for line in f:
            if line.strip():
                try:
                    data = json.loads(line)
                    date_str = data.get('date', '')
                    if date_str:
                        try:
                            data['date_obj'] = datetime.strptime(date_str, "%Y-%m-%d")
                        except:
                            continue
                    prompts.append(data)
                except:
                    continue
    
    prompts.sort(key=lambda x: x.get('date_obj', datetime.min))
    
    temporal_map = {}
    if TEMPORAL_MAP_FILE.exists():
        with open(TEMPORAL_MAP_FILE, 'r', encoding='utf-8') as f:
            temporal_map = json.load(f)
    
    return prompts, temporal_map


def synthesize_by_period_local(prompts: List[Dict]) -> Dict:
    """Lokálna syntéza podľa časových období."""
    print(f"\n📅 Syntetizujem podľa časových období (lokálne)...")
    
    periods = defaultdict(list)
    for prompt in prompts:
        date_obj = prompt.get('date_obj')
        if not date_obj:
            continue
        period_key = date_obj.strftime("%Y-%m")
        periods[period_key].append(prompt)
    
    syntheses = {}
    
    for period, period_prompts in sorted(periods.items()):
        print(f"   Syntetizujem {period} ({len(period_prompts)} promptov)...")
        
        # Analýza dát
        categories = Counter(p.get('category') for p in period_prompts if p.get('category'))
        subcategories = Counter(p.get('subcategory') for p in period_prompts if p.get('subcategory'))
        sentiments = Counter(p.get('sentiment') for p in period_prompts if p.get('sentiment'))
        
        all_projects = []
        all_concepts = []
        all_emotions = []
        
        for p in period_prompts:
            projects = p.get('context', {}).get('projects', [])
            all_projects.extend(projects)
            concepts = p.get('concepts', [])
            all_concepts.extend(concepts[:5])
            emotions = p.get('context', {}).get('emotions', [])
            all_emotions.extend(emotions)
        
        top_projects = Counter(all_projects).most_common(5)
        top_concepts = Counter(all_concepts).most_common(10)
        top_emotions = Counter(all_emotions).most_common(5)
        
        total_words = sum(p.get('word_count', 0) for p in period_prompts)
        avg_words = total_words / len(period_prompts) if period_prompts else 0
        
        # Vytvor syntézu
        synthesis = f"""# {period} - Syntéza

## 📊 Základné Štatistiky
- **Počet promptov:** {len(period_prompts)}
- **Celkový počet slov:** {total_words:,}
- **Priemerný počet slov na prompt:** {avg_words:.0f}

## 🎯 Hlavné Kategórie
"""
        for cat, count in categories.most_common():
            percentage = (count / len(period_prompts)) * 100
            synthesis += f"- **{cat}**: {count} promptov ({percentage:.1f}%)\n"
        
        synthesis += f"\n## 📝 Subkategórie\n"
        for subcat, count in subcategories.most_common(5):
            synthesis += f"- **{subcat}**: {count} promptov\n"
        
        synthesis += f"\n## 💼 Projekty\n"
        if top_projects:
            for project, count in top_projects:
                synthesis += f"- **{project}**: {count} zmienok\n"
        else:
            synthesis += "- Žiadne špecifické projekty\n"
        
        synthesis += f"\n## 💭 Top Koncepty\n"
        for concept, count in top_concepts:
            synthesis += f"- {concept} ({count}x)\n"
        
        synthesis += f"\n## 😊 Emocionálny Tón\n"
        for emotion, count in top_emotions:
            synthesis += f"- **{emotion}**: {count} zmienok\n"
        
        synthesis += f"\n## 📈 Sentiment Rozdelenie\n"
        for sentiment, count in sentiments.most_common():
            percentage = (count / len(period_prompts)) * 100
            synthesis += f"- **{sentiment}**: {count} ({percentage:.1f}%)\n"
        
        # Kľúčové momenty (prompty s najvyšším word count alebo významnými zmenami)
        key_prompts = sorted(period_prompts, key=lambda x: x.get('word_count', 0), reverse=True)[:5]
        synthesis += f"\n## 🔑 Kľúčové Prompty (najdlhšie)\n"
        for p in key_prompts:
            date = p.get('date', '')
            word_count = p.get('word_count', 0)
            category = p.get('category', '')
            text_preview = p.get('text', '')[:150].replace('\n', ' ')
            synthesis += f"- **{date}** ({word_count} slov, {category}): {text_preview}...\n"
        
        syntheses[period] = synthesis
    
    return syntheses


def synthesize_story_arcs_local(temporal_map: Dict, prompts: List[Dict]) -> Dict:
    """Lokálna syntéza story arcs."""
    print(f"\n📖 Syntetizujem story arcs (lokálne)...")
    
    story_arcs = temporal_map.get('story_arcs', [])
    syntheses = {}
    prompts_by_id = {p.get('prompt_id'): p for p in prompts}
    
    for arc in story_arcs[:10]:
        project = arc['project']
        print(f"   Syntetizujem {project} ({arc['prompt_count']} promptov)...")
        
        # Zbieraj dáta z promptov
        arc_prompts = [prompts_by_id.get(pid) for pid in arc['prompt_ids'] if prompts_by_id.get(pid)]
        
        categories = Counter(p.get('category') for p in arc_prompts if p.get('category'))
        sentiments = Counter(p.get('sentiment') for p in arc_prompts if p.get('sentiment'))
        total_words = sum(p.get('word_count', 0) for p in arc_prompts)
        
        synthesis = f"""# {project} - Story Arc

## 📊 Prehľad
- **Počet promptov:** {arc['prompt_count']}
- **Trvanie:** {arc['duration_days']} dní
- **Obdobie:** {arc['start_date']} - {arc['end_date']}
- **Celkový počet slov:** {total_words:,}
- **Priemer slov na prompt:** {arc.get('avg_words_per_prompt', 0):.0f}

## 🎯 Dominantná Kategória
- **{arc.get('dominant_category', 'unknown')}**: {categories.get(arc.get('dominant_category', ''), 0)} promptov

## 📈 Sentiment Trend
- **{arc.get('sentiment_trend', 'unknown')}**: {sentiments.get(arc.get('sentiment_trend', ''), 0)} promptov

## 📝 Rozdelenie Kategórií
"""
        for cat, count in categories.most_common():
            synthesis += f"- **{cat}**: {count} promptov\n"
        
        synthesis += f"\n## 📅 Chronologický Prehľad Promptov\n"
        for i, pid in enumerate(arc['prompt_ids'][:10], 1):  # Top 10
            prompt = prompts_by_id.get(pid)
            if prompt:
                date = prompt.get('date', '')
                category = prompt.get('category', '')
                word_count = prompt.get('word_count', 0)
                synthesis += f"{i}. **{date}** ({category}, {word_count} slov)\n"
        
        if len(arc['prompt_ids']) > 10:
            synthesis += f"\n... a ďalších {len(arc['prompt_ids']) - 10} promptov\n"
        
        syntheses[project] = synthesis
    
    return syntheses


def synthesize_transformations_local(prompts: List[Dict]) -> str:
    """Lokálna syntéza transformačných momentov."""
    print(f"\n🔄 Syntetizujem transformačné momenty (lokálne)...")
    
    changes = []
    for i in range(1, len(prompts)):
        prev = prompts[i-1]
        curr = prompts[i]
        
        if prev.get('sentiment') != curr.get('sentiment'):
            changes.append({
                'date': curr.get('date', ''),
                'type': 'sentiment_change',
                'from': prev.get('sentiment'),
                'to': curr.get('sentiment'),
                'prompt_id': curr.get('prompt_id')
            })
        
        if prev.get('category') != curr.get('category'):
            changes.append({
                'date': curr.get('date', ''),
                'type': 'category_change',
                'from': prev.get('category'),
                'to': curr.get('category'),
                'prompt_id': curr.get('prompt_id')
            })
    
    synthesis = """# Transformačné Momenty

## 📊 Prehľad
"""
    synthesis += f"- **Celkom transformácií:** {len(changes)}\n"
    synthesis += f"- **Zmeny sentimentu:** {len([c for c in changes if c['type'] == 'sentiment_change'])}\n"
    synthesis += f"- **Zmeny kategórie:** {len([c for c in changes if c['type'] == 'category_change'])}\n"
    
    synthesis += "\n## 🔄 Zmeny Sentimentu\n"
    sentiment_changes = [c for c in changes if c['type'] == 'sentiment_change']
    for change in sentiment_changes[:20]:
        synthesis += f"- **{change['date']}**: {change['from']} → {change['to']}\n"
    
    synthesis += "\n## 🎯 Zmeny Kategórií\n"
    category_changes = [c for c in changes if c['type'] == 'category_change']
    for change in category_changes[:20]:
        synthesis += f"- **{change['date']}**: {change['from']} → {change['to']}\n"
    
    return synthesis


def main():
    """Hlavná funkcia."""
    print("="*80)
    print("Lokálna chronologická syntéza príbehu (bez API)")
    print("="*80)
    
    # Načítaj dáta
    print("\n📖 Načítavam dáta...")
    prompts, temporal_map = load_data()
    print(f"✅ Načítaných {len(prompts)} promptov")
    
    # Syntéza podľa období
    period_syntheses = synthesize_by_period_local(prompts)
    
    # Syntéza story arcs
    story_arc_syntheses = {}
    if temporal_map:
        story_arc_syntheses = synthesize_story_arcs_local(temporal_map, prompts)
    
    # Syntéza transformácií
    transformation_synthesis = synthesize_transformations_local(prompts)
    
    # Ulož výsledky
    print("\n💾 Ukladám výsledky...")
    
    periods_file = OUTPUT_DIR / "synthesis_by_periods_local.md"
    with open(periods_file, 'w', encoding='utf-8') as f:
        f.write("# Chronologická Syntéza podľa Období (Lokálna Analýza)\n\n")
        for period, synthesis in sorted(period_syntheses.items()):
            f.write(f"{synthesis}\n\n---\n\n")
    print(f"✅ Uložené: {periods_file}")
    
    arcs_file = OUTPUT_DIR / "synthesis_story_arcs_local.md"
    with open(arcs_file, 'w', encoding='utf-8') as f:
        f.write("# Syntéza Story Arcs (Lokálna Analýza)\n\n")
        for project, synthesis in story_arc_syntheses.items():
            f.write(f"{synthesis}\n\n---\n\n")
    print(f"✅ Uložené: {arcs_file}")
    
    trans_file = OUTPUT_DIR / "synthesis_transformations_local.md"
    with open(trans_file, 'w', encoding='utf-8') as f:
        f.write(transformation_synthesis)
    print(f"✅ Uložené: {trans_file}")
    
    print("\n" + "="*80)
    print("✅ DOKONČENÉ")
    print("="*80)
    print(f"📁 Výstupné súbory v: {OUTPUT_DIR}/")
    print("="*80)


if __name__ == "__main__":
    main()

