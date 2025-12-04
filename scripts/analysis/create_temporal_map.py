#!/usr/bin/env python3
"""
Fáza 2: Temporálna mapa pokračovaní
- Identifikácia story arcs (príbehy projektov v čase)
- Temporálne clustery (súvisiace prompty v rámci 7 dní)
"""

import json
import sys
from pathlib import Path
from datetime import datetime, timedelta
from typing import List, Dict, Set
from collections import defaultdict

# Konfigurácia
INPUT_FILE = Path("data/prompts/prompts_categorized.jsonl")
OUTPUT_FILE = Path("data/prompts/temporal_map.json")
CLUSTER_WINDOW_DAYS = 7  # Okno pre temporálne clustery


def load_categorized_prompts() -> List[Dict]:
    """Načíta kategorizované prompty."""
    prompts = []
    
    if not INPUT_FILE.exists():
        print(f"❌ Súbor {INPUT_FILE} neexistuje!")
        return prompts
    
    try:
        with open(INPUT_FILE, 'r', encoding='utf-8') as f:
            for line in f:
                line = line.strip()
                if not line:
                    continue
                try:
                    data = json.loads(line)
                    # Parsuj dátum
                    date_str = data.get('date', '')
                    if date_str:
                        try:
                            date = datetime.strptime(date_str, "%Y-%m-%d")
                            data['date_obj'] = date
                        except:
                            continue
                    prompts.append(data)
                except json.JSONDecodeError:
                    continue
    except Exception as e:
        print(f"❌ Chyba pri načítaní: {e}")
        return prompts
    
    # Zoraď podľa dátumu
    prompts.sort(key=lambda x: x.get('date_obj', datetime.min))
    
    print(f"✅ Načítaných {len(prompts)} promptov")
    return prompts


def create_story_arcs(prompts: List[Dict]) -> List[Dict]:
    """
    Vytvorí story arcs pre projekty.
    Story arc = sekvencia promptov o tom istom projekte v čase.
    """
    print("\n📖 Vytváram story arcs pre projekty...")
    
    # Zoskupiť prompty podľa projektov
    project_prompts = defaultdict(list)
    
    for prompt in prompts:
        projects = prompt.get('context', {}).get('projects', [])
        if not projects:
            continue
        
        prompt_id = prompt.get('prompt_id')
        date = prompt.get('date_obj')
        category = prompt.get('category')
        subcategory = prompt.get('subcategory')
        
        for project in projects:
            project_prompts[project].append({
                'prompt_id': prompt_id,
                'date': prompt.get('date'),
                'date_obj': date,
                'category': category,
                'subcategory': subcategory,
                'sentiment': prompt.get('sentiment'),
                'word_count': prompt.get('word_count', 0)
            })
    
    # Vytvor story arcs
    story_arcs = []
    
    for project, project_prompts_list in project_prompts.items():
        if len(project_prompts_list) < 2:
            continue  # Skip projekty s menej ako 2 promptmi
        
        # Zoraď podľa dátumu
        project_prompts_list.sort(key=lambda x: x.get('date_obj', datetime.min))
        
        # Vypočítaj trvanie
        first_date = project_prompts_list[0]['date_obj']
        last_date = project_prompts_list[-1]['date_obj']
        duration_days = (last_date - first_date).days + 1
        
        # Zisti dominantnú kategóriu
        categories = [p.get('category') for p in project_prompts_list if p.get('category')]
        from collections import Counter
        dominant_category = Counter(categories).most_common(1)[0][0] if categories else 'unknown'
        
        # Zisti sentiment trend
        sentiments = [p.get('sentiment') for p in project_prompts_list if p.get('sentiment')]
        sentiment_trend = Counter(sentiments).most_common(1)[0][0] if sentiments else 'unknown'
        
        # Vypočítaj celkový word count
        total_words = sum(p.get('word_count', 0) for p in project_prompts_list)
        
        story_arc = {
            'project': project,
            'prompt_ids': [p['prompt_id'] for p in project_prompts_list],
            'prompt_count': len(project_prompts_list),
            'start_date': project_prompts_list[0]['date'],
            'end_date': project_prompts_list[-1]['date'],
            'duration_days': duration_days,
            'dominant_category': dominant_category,
            'sentiment_trend': sentiment_trend,
            'total_words': total_words,
            'avg_words_per_prompt': total_words / len(project_prompts_list) if project_prompts_list else 0
        }
        
        story_arcs.append(story_arc)
    
    # Zoraď podľa počtu promptov (najaktívnejšie projekty prvé)
    story_arcs.sort(key=lambda x: x['prompt_count'], reverse=True)
    
    print(f"✅ Vytvorených {len(story_arcs)} story arcs")
    return story_arcs


def create_temporal_clusters(prompts: List[Dict]) -> List[Dict]:
    """
    Vytvorí temporálne clustery - súvisiace prompty v rámci CLUSTER_WINDOW_DAYS dní.
    Cluster = skupina promptov, ktoré sú časovo blízko a zdieľajú podobné témy.
    """
    print("\n📖 Vytváram temporálne clustery...")
    
    clusters = []
    processed_prompts = set()
    
    for i, prompt in enumerate(prompts):
        prompt_id = prompt.get('prompt_id')
        if prompt_id in processed_prompts:
            continue
        
        # Nájdi všetky prompty v okne CLUSTER_WINDOW_DAYS dní
        prompt_date = prompt.get('date_obj')
        if not prompt_date:
            continue
        
        window_end = prompt_date + timedelta(days=CLUSTER_WINDOW_DAYS)
        
        cluster_prompts = [prompt]
        processed_prompts.add(prompt_id)
        
        # Nájdi súvisiace prompty v okne
        for j in range(i + 1, len(prompts)):
            other_prompt = prompts[j]
            other_id = other_prompt.get('prompt_id')
            other_date = other_prompt.get('date_obj')
            
            if not other_date:
                continue
            
            if other_date > window_end:
                break  # Preskoč okno
            
            if other_id in processed_prompts:
                continue
            
            # Skontroluj, či súvisia (zdieľajú projekty, kategórie alebo koncepty)
            if are_related(prompt, other_prompt):
                cluster_prompts.append(other_prompt)
                processed_prompts.add(other_id)
        
        # Vytvor cluster len ak má aspoň 2 prompty
        if len(cluster_prompts) >= 2:
            # Zoraď podľa dátumu
            cluster_prompts.sort(key=lambda x: x.get('date_obj', datetime.min))
            
            # Zisti dominantné témy
            all_projects = set()
            all_categories = []
            all_concepts = []
            
            for p in cluster_prompts:
                projects = p.get('context', {}).get('projects', [])
                all_projects.update(projects)
                category = p.get('category')
                if category:
                    all_categories.append(category)
                concepts = p.get('concepts', [])
                all_concepts.extend(concepts[:5])  # Top 5 concepts z každého
            
            from collections import Counter
            dominant_category = Counter(all_categories).most_common(1)[0][0] if all_categories else 'unknown'
            top_concepts = [c for c, _ in Counter(all_concepts).most_common(5)]
            
            cluster = {
                'cluster_id': f"cluster_{len(clusters) + 1}",
                'prompt_ids': [p.get('prompt_id') for p in cluster_prompts],
                'prompt_count': len(cluster_prompts),
                'start_date': cluster_prompts[0].get('date'),
                'end_date': cluster_prompts[-1].get('date'),
                'duration_days': (cluster_prompts[-1].get('date_obj') - cluster_prompts[0].get('date_obj')).days + 1,
                'projects': list(all_projects),
                'dominant_category': dominant_category,
                'top_concepts': top_concepts
            }
            
            clusters.append(cluster)
    
    print(f"✅ Vytvorených {len(clusters)} temporálnych clusterov")
    return clusters


def are_related(prompt1: Dict, prompt2: Dict) -> bool:
    """
    Skontroluje, či sú dva prompty súvisiace.
    Súvisia ak zdieľajú:
    - Projekty
    - Kategóriu
    - Alebo významné koncepty (aspoň 2)
    """
    # Projekty
    projects1 = set(prompt1.get('context', {}).get('projects', []))
    projects2 = set(prompt2.get('context', {}).get('projects', []))
    if projects1 & projects2:  # Intersection
        return True
    
    # Kategória
    if prompt1.get('category') == prompt2.get('category') and prompt1.get('category'):
        return True
    
    # Koncepty (aspoň 2 spoločné)
    concepts1 = set(prompt1.get('concepts', [])[:10])  # Top 10
    concepts2 = set(prompt2.get('concepts', [])[:10])
    common_concepts = concepts1 & concepts2
    if len(common_concepts) >= 2:
        return True
    
    return False


def main():
    """Hlavná funkcia."""
    print("="*80)
    print("Fáza 2: Temporálna mapa pokračovaní")
    print("="*80)
    
    # Načítaj prompty
    prompts = load_categorized_prompts()
    
    if not prompts:
        print("❌ Žiadne prompty na spracovanie!")
        return
    
    # Vytvor story arcs
    story_arcs = create_story_arcs(prompts)
    
    # Vytvor temporálne clustery
    temporal_clusters = create_temporal_clusters(prompts)
    
    # Zostav výsledok
    result = {
        'created_at': datetime.now().isoformat(),
        'total_prompts': len(prompts),
        'story_arcs': story_arcs,
        'temporal_clusters': temporal_clusters,
        'statistics': {
            'total_story_arcs': len(story_arcs),
            'total_clusters': len(temporal_clusters),
            'projects_with_arcs': len(set(arc['project'] for arc in story_arcs)),
            'prompts_in_arcs': sum(arc['prompt_count'] for arc in story_arcs),
            'prompts_in_clusters': sum(cluster['prompt_count'] for cluster in temporal_clusters)
        }
    }
    
    # Ulož výsledok
    OUTPUT_FILE.parent.mkdir(parents=True, exist_ok=True)
    with open(OUTPUT_FILE, 'w', encoding='utf-8') as f:
        json.dump(result, f, ensure_ascii=False, indent=2)
    
    print("\n" + "="*80)
    print("✅ VÝSLEDKY")
    print("="*80)
    print(f"📁 Výstup: {OUTPUT_FILE}")
    print()
    print(f"📊 Story arcs: {len(story_arcs)}")
    print(f"   • Projekty s arcami: {result['statistics']['projects_with_arcs']}")
    print(f"   • Prompty v arcach: {result['statistics']['prompts_in_arcs']}")
    print()
    print(f"📊 Temporálne clustery: {len(temporal_clusters)}")
    print(f"   • Prompty v clusteroch: {result['statistics']['prompts_in_clusters']}")
    print()
    print("📊 Top 5 story arcs (podľa počtu promptov):")
    for i, arc in enumerate(story_arcs[:5], 1):
        print(f"   {i}. {arc['project']}: {arc['prompt_count']} promptov, {arc['duration_days']} dní")
    print("="*80)


if __name__ == "__main__":
    main()

