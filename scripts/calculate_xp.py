"""
Automatický výpočet XP z logu a promptov
Volá sa pri každom /savegame
"""

import re
import json
from pathlib import Path
from datetime import datetime, timedelta
from collections import defaultdict
from typing import Dict, List, Set, Tuple


# XP hodnoty (potvrdené)
XP_PER_LOG_ENTRY = 0.5
XP_PER_FILE_CHANGE = 0.1
XP_PER_TASK = 0.5
XP_PER_PROMPT = 0.1
XP_PER_1000_WORDS = 0.5
XP_PER_STREAK_DAY = 0.2
XP_PER_SESSION = 1.0

# Level systém (exponenciálny)
LEVEL_THRESHOLDS = [10, 25, 50, 100, 200]  # Level 1-5
# Level 6+ = predchádzajúci × 2


def parse_log_entries(log_path: Path) -> Dict:
    """
    Parsuje log markdown a počíta:
    - Počet záznamov
    - Počet unikátnych zmien súborov
    - Počet dokončených úloh
    """
    if not log_path.exists():
        return {
            'entries': 0,
            'files': set(),
            'tasks': 0
        }
    
    content = log_path.read_text(encoding='utf-8')
    
    # Počet záznamov: detekcia patternu ## [YYYY-MM-DD HH:MM]
    entry_pattern = r'^## \[(\d{4}-\d{2}-\d{2} \d{2}:\d{2})\]'
    entries = len(re.findall(entry_pattern, content, re.MULTILINE))
    
    # Zmeny súborov: detekcia v sekcii "Zmeny v súboroch"
    files = set()
    file_pattern = r'- `([^`]+)`'
    file_matches = re.findall(file_pattern, content)
    for file_match in file_matches:
        # Odstrániť popis za pomlčkou (ak existuje)
        file_path = file_match.split(' - ')[0].strip()
        if file_path:
            files.add(file_path)
    
    # Dokončené úlohy: detekcia v sekcii "Vykonané:"
    tasks = 0
    # Počítať všetky bullet points v sekcii "Vykonané:"
    vykonane_section = re.findall(r'\*\*Vykonané:\*\*(.*?)(?=\*\*Zmeny|\*\*Status|---|$)', content, re.DOTALL)
    for section in vykonane_section:
        # Počítať riadky začínajúce s "-"
        task_lines = [line for line in section.split('\n') if line.strip().startswith('-')]
        tasks += len(task_lines)
    
    return {
        'entries': entries,
        'files': files,
        'tasks': tasks
    }


def parse_prompts(prompts_path: Path) -> Dict:
    """
    Parsuje JSONL promptov a počíta:
    - Počet promptov
    - Celkový word count
    """
    if not prompts_path.exists():
        return {
            'count': 0,
            'total_words': 0,
            'dates': []
        }
    
    prompts = []
    dates = []
    
    with open(prompts_path, 'r', encoding='utf-8') as f:
        for line in f:
            line = line.strip()
            if not line:
                continue
            try:
                prompt_data = json.loads(line)
                prompts.append(prompt_data)
                
                # Extrahovať dátum z timestamp
                timestamp = prompt_data.get('timestamp', '')
                if timestamp:
                    # Parsovať dátum (podporovať rôzne formáty)
                    try:
                        if '+' in timestamp or timestamp.endswith('Z'):
                            # ISO format s timezone
                            dt = datetime.fromisoformat(timestamp.replace('Z', '+00:00'))
                        else:
                            dt = datetime.fromisoformat(timestamp)
                        dates.append(dt.date())
                    except:
                        pass
            except json.JSONDecodeError:
                continue
    
    # Počítať slová v content
    total_words = 0
    for prompt in prompts:
        content = prompt.get('content', '')
        if content:
            # Jednoduchý word count (rozdelenie podľa medzier)
            words = len(content.split())
            total_words += words
    
    return {
        'count': len(prompts),
        'total_words': total_words,
        'dates': dates
    }


def calculate_streak(prompt_dates: List) -> int:
    """
    Počíta streak dní (počet dní v rade s aktivitou)
    """
    if not prompt_dates:
        return 0
    
    # Zoradiť dátumy a odstrániť duplikáty
    unique_dates = sorted(set(prompt_dates))
    
    if not unique_dates:
        return 0
    
    # Počítať streak od najnovšieho dátumu smerom dozadu
    streak = 1
    current_date = unique_dates[-1]
    
    for i in range(len(unique_dates) - 2, -1, -1):
        prev_date = unique_dates[i]
        expected_date = current_date - timedelta(days=1)
        
        if prev_date == expected_date:
            streak += 1
            current_date = prev_date
        else:
            break
    
    return streak


def calculate_level(total_xp: float) -> Tuple[int, float, float]:
    """
    Počíta level z XP podľa exponenciálneho systému
    Vracia: (current_level, next_level_xp, xp_needed)
    """
    if total_xp < LEVEL_THRESHOLDS[0]:
        return (1, LEVEL_THRESHOLDS[0], LEVEL_THRESHOLDS[0] - total_xp)
    
    # Skontrolovať základné levely
    for i, threshold in enumerate(LEVEL_THRESHOLDS):
        if total_xp < threshold:
            return (i + 1, threshold, threshold - total_xp)
    
    # Level 6+ (exponenciálny)
    current_level = len(LEVEL_THRESHOLDS) + 1
    next_level_xp = LEVEL_THRESHOLDS[-1]
    
    while next_level_xp <= total_xp:
        next_level_xp *= 2
        current_level += 1
    
    return (current_level - 1, next_level_xp, next_level_xp - total_xp)


def calculate_xp(log_path: str = 'development/logs/XVADUR_LOG.md',
                 prompts_path: str = 'development/data/prompts_log.jsonl') -> Dict:
    """
    Hlavná funkcia pre výpočet XP
    Vracia dict s breakdown a celkovým XP
    """
    log_path = Path(log_path)
    prompts_path = Path(prompts_path)
    
    # Parsovať log
    log_data = parse_log_entries(log_path)
    
    # Parsovať prompty
    prompts_data = parse_prompts(prompts_path)
    
    # Počítať XP z práce (log)
    xp_from_entries = log_data['entries'] * XP_PER_LOG_ENTRY
    xp_from_files = len(log_data['files']) * XP_PER_FILE_CHANGE
    xp_from_tasks = log_data['tasks'] * XP_PER_TASK
    
    # Počítať XP z aktivity (prompty)
    xp_from_prompts = prompts_data['count'] * XP_PER_PROMPT
    xp_from_words = (prompts_data['total_words'] / 1000) * XP_PER_1000_WORDS
    
    # Počítať streak
    streak_days = calculate_streak(prompts_data['dates'])
    xp_from_streak = streak_days * XP_PER_STREAK_DAY
    
    # Počítať sessions (z log entries - každý dátum = session)
    unique_dates = set()
    if log_path.exists():
        content = log_path.read_text(encoding='utf-8')
        date_pattern = r'^## \[(\d{4}-\d{2}-\d{2})'
        dates = re.findall(date_pattern, content, re.MULTILINE)
        unique_dates = set(dates)
    
    xp_from_sessions = len(unique_dates) * XP_PER_SESSION
    
    # Celkové XP
    total_xp = (
        xp_from_entries +
        xp_from_files +
        xp_from_tasks +
        xp_from_prompts +
        xp_from_words +
        xp_from_streak +
        xp_from_sessions
    )
    
    # Počítať level
    current_level, next_level_xp, xp_needed = calculate_level(total_xp)
    
    return {
        'total_xp': round(total_xp, 2),
        'current_level': current_level,
        'next_level_xp': next_level_xp,
        'xp_needed': round(xp_needed, 2),
        'streak_days': streak_days,
        'breakdown': {
            'from_work': {
                'entries': {
                    'count': log_data['entries'],
                    'xp': round(xp_from_entries, 2)
                },
                'files': {
                    'count': len(log_data['files']),
                    'xp': round(xp_from_files, 2)
                },
                'tasks': {
                    'count': log_data['tasks'],
                    'xp': round(xp_from_tasks, 2)
                },
                'total': round(xp_from_entries + xp_from_files + xp_from_tasks, 2)
            },
            'from_activity': {
                'prompts': {
                    'count': prompts_data['count'],
                    'xp': round(xp_from_prompts, 2)
                },
                'words': {
                    'count': prompts_data['total_words'],
                    'xp': round(xp_from_words, 2)
                },
                'total': round(xp_from_prompts + xp_from_words, 2)
            },
            'bonuses': {
                'streak': {
                    'days': streak_days,
                    'xp': round(xp_from_streak, 2)
                },
                'sessions': {
                    'count': len(unique_dates),
                    'xp': round(xp_from_sessions, 2)
                },
                'total': round(xp_from_streak + xp_from_sessions, 2)
            }
        }
    }


def save_xp_history(xp_data: Dict, history_path: str = 'development/data/xp_history.jsonl') -> None:
    """
    Uloží aktuálny výpočet XP do histórie
    """
    history_path = Path(history_path)
    history_path.parent.mkdir(parents=True, exist_ok=True)
    
    # Vytvoriť záznam
    record = {
        'timestamp': datetime.now().isoformat(),
        'total_xp': xp_data['total_xp'],
        'level': xp_data['current_level'],
        'next_level_xp': xp_data['next_level_xp'],
        'xp_needed': xp_data['xp_needed'],
        'streak_days': xp_data['streak_days'],
        'breakdown': xp_data['breakdown']
    }
    
    # Pridať do JSONL súboru
    with open(history_path, 'a', encoding='utf-8') as f:
        f.write(json.dumps(record) + '\n')


def load_xp_history(history_path: str = 'development/data/xp_history.jsonl', limit: int = 30) -> List[Dict]:
    """
    Načíta históriu XP (posledných N záznamov)
    """
    history_path = Path(history_path)
    
    if not history_path.exists():
        return []
    
    records = []
    with open(history_path, 'r', encoding='utf-8') as f:
        for line in f:
            line = line.strip()
            if not line:
                continue
            try:
                record = json.loads(line)
                records.append(record)
            except json.JSONDecodeError:
                continue
    
    # Vrátiť posledných N záznamov
    return records[-limit:]


def generate_xp_graph(history: List[Dict], max_width: int = 40) -> str:
    """
    Generuje ASCII graf z histórie XP
    """
    if not history:
        return "```\n(Žiadna história - graf sa zobrazí po prvom /savegame)\n```"
    
    # Zoradiť podľa dátumu
    sorted_history = sorted(history, key=lambda x: x.get('timestamp', ''))
    
    # Nájsť min a max XP pre škálovanie
    xp_values = [record['total_xp'] for record in sorted_history]
    if not xp_values:
        return "```\n(Žiadne dáta)\n```"
    
    min_xp = min(xp_values)
    max_xp = max(xp_values)
    xp_range = max_xp - min_xp if max_xp > min_xp else max_xp if max_xp > 0 else 1
    
    # Generovať graf
    graph_lines = ["```"]
    graph_lines.append("## 📈 XP Progress Graph")
    graph_lines.append("")
    
    # Progress bar pre aktuálny level
    if sorted_history:
        latest = sorted_history[-1]
        current_xp = latest['total_xp']
        next_level = latest['next_level_xp']
        level = latest['level']
        
        # Progress bar
        percentage = (current_xp / next_level * 100) if next_level > 0 else 0
        filled = int((current_xp / next_level) * max_width) if next_level > 0 else 0
        empty = max_width - filled
        bar = "█" * filled + "░" * empty
        
        graph_lines.append(f"**Level {level} Progress:**")
        graph_lines.append(f"[{bar}] {current_xp:.2f} / {next_level} XP ({percentage:.1f}%)")
        graph_lines.append("")
    
    # Časová os (posledných 15 záznamov)
    graph_lines.append("**XP Timeline (posledných 15 záznamov):**")
    graph_lines.append("")
    
    # Zobraziť len posledných 15 záznamov
    recent_history = sorted_history[-15:]
    
    for record in recent_history:
        timestamp_str = record.get('timestamp', '')
        try:
            dt = datetime.fromisoformat(timestamp_str)
            date_str = dt.strftime('%m-%d %H:%M')
        except:
            date_str = timestamp_str[:10] if len(timestamp_str) > 10 else timestamp_str
        
        xp = record['total_xp']
        level = record.get('level', 1)
        
        # Normalizovať XP na 0-1 rozsah pre graf (relatívne k max_xp)
        normalized = (xp / max_xp) if max_xp > 0 else 0
        bar_width = int(normalized * max_width)
        bar = "█" * bar_width + "░" * (max_width - bar_width)
        
        graph_lines.append(f"{date_str}  {bar}  {xp:.2f} XP (L{level})")
    
    # Trend
    if len(sorted_history) >= 2:
        first_xp = sorted_history[0]['total_xp']
        last_xp = sorted_history[-1]['total_xp']
        change = last_xp - first_xp
        
        if change > 0:
            trend = f"↗️ +{change:.2f} XP"
        elif change < 0:
            trend = f"↘️ {change:.2f} XP"
        else:
            trend = "➡️ 0 XP"
        
        first_date = sorted_history[0].get('timestamp', '')[:10]
        last_date = sorted_history[-1].get('timestamp', '')[:10]
        
        graph_lines.append("")
        graph_lines.append(f"**Trend:** {trend} (od {first_date} do {last_date})")
        graph_lines.append(f"**Záznamov v histórii:** {len(sorted_history)}")
    
    graph_lines.append("```")
    
    return "\n".join(graph_lines)


def update_xp_file(xp_file_path: str, xp_data: Dict) -> None:
    """
    Aktualizuje XVADUR_XP.md s novými hodnotami a grafom
    """
    xp_file_path = Path(xp_file_path)
    
    # Uložiť do histórie
    save_xp_history(xp_data)
    
    # Načítať históriu pre graf
    history = load_xp_history()
    
    # Generovať graf
    graph = generate_xp_graph(history)
    
    breakdown = xp_data['breakdown']
    timestamp = datetime.now().strftime('%Y-%m-%d %H:%M')
    
    content = f"""# 🎮 XVADUR XP TRACKING

**Status:** Aktívny  
**Posledná aktualizácia:** {timestamp}

---

## 📊 Aktuálny Status

- **Celkové XP:** {xp_data['total_xp']}
- **Level:** {xp_data['current_level']}
- **Next Level:** {xp_data['next_level_xp']} XP (potrebuje ešte {xp_data['xp_needed']} XP)
- **Streak:** {xp_data['streak_days']} dní

---

{graph}

---

## 💎 XP Breakdown

### Z Práce (Log)
- **Záznamy:** {breakdown['from_work']['entries']['count']} × {XP_PER_LOG_ENTRY} = {breakdown['from_work']['entries']['xp']} XP
- **Zmeny súborov:** {breakdown['from_work']['files']['count']} × {XP_PER_FILE_CHANGE} = {breakdown['from_work']['files']['xp']} XP
- **Dokončené úlohy:** {breakdown['from_work']['tasks']['count']} × {XP_PER_TASK} = {breakdown['from_work']['tasks']['xp']} XP
- **Subtotal:** {breakdown['from_work']['total']} XP

### Z Aktivity (Prompty)
- **Prompty:** {breakdown['from_activity']['prompts']['count']} × {XP_PER_PROMPT} = {breakdown['from_activity']['prompts']['xp']} XP
- **Word count:** {breakdown['from_activity']['words']['count']:,} slov × ({XP_PER_1000_WORDS} / 1000) = {breakdown['from_activity']['words']['xp']} XP
- **Subtotal:** {breakdown['from_activity']['total']} XP

### Bonusy
- **Streak:** {breakdown['bonuses']['streak']['days']} dní × {XP_PER_STREAK_DAY} = {breakdown['bonuses']['streak']['xp']} XP
- **Sessions:** {breakdown['bonuses']['sessions']['count']} × {XP_PER_SESSION} = {breakdown['bonuses']['sessions']['xp']} XP
- **Subtotal:** {breakdown['bonuses']['total']} XP

**⭐ TOTAL:** {xp_data['total_xp']} XP

---

## 📈 História

*História sa automaticky ukladá do `development/data/xp_history.jsonl`*

---

**Automaticky vypočítané z:**
- `development/logs/XVADUR_LOG.md` (práca)
- `development/data/prompts_log.jsonl` (aktivita)
"""
    
    xp_file_path.write_text(content, encoding='utf-8')


if __name__ == '__main__':
    # Testovanie
    xp_data = calculate_xp()
    print(f"Total XP: {xp_data['total_xp']}")
    print(f"Level: {xp_data['current_level']}")
    print(f"Next Level: {xp_data['next_level_xp']} XP (potrebuje {xp_data['xp_needed']} XP)")
    print(f"Streak: {xp_data['streak_days']} dní")
    print("\nBreakdown:")
    print(json.dumps(xp_data['breakdown'], indent=2))
    
    # Aktualizovať súbor
    update_xp_file('development/logs/XVADUR_XP.md', xp_data)
    print("\n✅ XP súbor aktualizovaný")

