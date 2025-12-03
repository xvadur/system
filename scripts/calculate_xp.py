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


def calculate_xp(log_path: str = 'xvadur/logs/XVADUR_LOG.md',
                 prompts_path: str = 'xvadur/data/prompts_log.jsonl') -> Dict:
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


def update_xp_file(xp_file_path: str, xp_data: Dict) -> None:
    """
    Aktualizuje XVADUR_XP.md s novými hodnotami
    """
    xp_file_path = Path(xp_file_path)
    
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

*História sa bude automaticky generovať pri každom /savegame*

---

**Automaticky vypočítané z:**
- `xvadur/logs/XVADUR_LOG.md` (práca)
- `xvadur/data/prompts_log.jsonl` (aktivita)
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
    update_xp_file('xvadur/logs/XVADUR_XP.md', xp_data)
    print("\n✅ XP súbor aktualizovaný")

