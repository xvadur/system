#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Xvadur Visualizations: Generovanie ASCII grafov a vizualizácií pre xvadur log.

TODO: Add support for color output in terminals
TODO: Implement interactive mode for real-time updates
FIXME: Handle very long metric names in dashboard

Tento skript generuje:
- Progress bary
- Metriky dashboard
- Timeline vizualizácie
- Knowledge graph (ASCII)
"""

from typing import Dict, List
from datetime import datetime


def generate_progress_bar(current: float, total: float, width: int = 20) -> str:
    """
    Generuje ASCII progress bar.
    
    Args:
        current: Aktuálna hodnota
        total: Celková hodnota
        width: Šírka progress baru (počet znakov)
    
    Returns:
        ASCII progress bar string
    """
    if total == 0:
        return "[" + "░" * width + "] 0 / 0 (0%)"
    
    percentage = min(100, (current / total) * 100)
    filled = int((current / total) * width)
    empty = width - filled
    
    bar = "█" * filled + "░" * empty
    return f"[{bar}] {current:.2f} / {total:.2f} ({percentage:.1f}%)"


def generate_meter(value: float, max_value: float, width: int = 10) -> str:
    """
    Generuje ASCII meter.
    
    Args:
        value: Aktuálna hodnota
        max_value: Maximálna hodnota
        width: Šírka metra
    
    Returns:
        ASCII meter string
    """
    if max_value == 0:
        return "[" + "░" * width + "] 0.0"
    
    filled = int((value / max_value) * width)
    empty = width - filled
    
    bar = "█" * filled + "░" * empty
    return f"[{bar}] {value:.1f}/{max_value:.1f}"


def generate_status_dashboard(session_id: str, date: str, duration: str, xp_current: float, xp_total: float, level: int, streak: int = 0) -> str:
    """
    Generuje status dashboard podobný ako v XVADUR_XP.md.
    
    Args:
        session_id: ID session
        date: Dátum
        duration: Trvanie session
        xp_current: Aktuálne XP
        xp_total: Celkové XP pre level
        level: Aktuálny level
        streak: Streak dní
    
    Returns:
        Status dashboard string
    """
    xp_percentage = (xp_current / xp_total * 100) if xp_total > 0 else 0
    xp_progress = int((xp_current / xp_total) * 10) if xp_total > 0 else 0
    xp_bar = "█" * xp_progress + "░" * (10 - xp_progress)
    
    streak_progress = min(30, streak)
    streak_bar = "█" * streak_progress + "░" * (30 - streak_progress)
    
    dashboard = f"""╔═══════════════════════════════════════════════════════════════╗
║                    XVADUR SESSION STATUS                      ║
╠═══════════════════════════════════════════════════════════════╣
║  Session ID:     [{session_id}]                          ║
║  Dátum:          [{date}]                                 ║
║  Trvanie:        [{duration}]                                    ║
║  Status:         [🟢 Active]                                   ║
╠═══════════════════════════════════════════════════════════════╣
║  XP Progress:    [{xp_bar}] {xp_current:.2f} / {xp_total:.1f} XP ({xp_percentage:.1f}%)         ║
║  Level:          [{level}] → [{level + 1}] (potrebuje {xp_total - xp_current:.2f} XP)               ║
║  Streak:         [{streak} dní] ████████████████████░░░░░░░░░░░░░░░░░░  ║
╚═══════════════════════════════════════════════════════════════╝"""
    
    return dashboard


def generate_xp_breakdown(xp_breakdown: Dict) -> str:
    """
    Generuje XP breakdown podobný ako v XVADUR_XP.md.
    
    Args:
        xp_breakdown: Dict s XP hodnotami pre jednotlivé kategórie
    
    Returns:
        XP breakdown string
    """
    total_xp = sum(xp_breakdown.values())
    
    lines = []
    lines.append("╔═══════════════════════════════════════════════════════════════╗")
    lines.append("║  💎 XP BREAKDOWN                                               ║")
    lines.append("╠═══════════════════════════════════════════════════════════════╣")
    
    for category, xp_value in xp_breakdown.items():
        if total_xp > 0:
            percentage = (xp_value / total_xp) * 100
            progress = int((xp_value / total_xp) * 10)
            bar = "█" * progress + "░" * (10 - progress)
            lines.append(f"║  {category:<25} {bar} {xp_value:.2f} XP ({percentage:.1f}%)        ║")
        else:
            lines.append(f"║  {category:<25} ░░░░░░░░░░ 0.00 XP (0.0%)        ║")
    
    lines.append("╠═══════════════════════════════════════════════════════════════╣")
    lines.append(f"║  ⭐ TOTAL XP:               ███░░░░░░░░ {total_xp:.2f} XP                ║")
    lines.append("╚═══════════════════════════════════════════════════════════════╝")
    
    return "\n".join(lines)


def generate_metrics_dashboard(metrics: Dict) -> str:
    """
    Generuje ASCII tabuľku s metrikami.
    
    Args:
        metrics: Dict s metrikami
    
    Returns:
        ASCII tabuľka string
    """
    lines = []
    lines.append("┌─────────────────────────────────────────────────────────────────┐")
    lines.append("│  📊 METRIKY DASHBOARD                                           │")
    lines.append("├─────────────────────┬──────────────┬───────────────────────────┤")
    lines.append("│ Metrika             │ Hodnota      │ Visual Progress           │")
    lines.append("├─────────────────────┼──────────────┼───────────────────────────┤")
    
    # Word Count
    word_count = metrics.get("word_count", 0)
    word_progress = min(20, int((word_count / 500) * 20))
    word_bar = "█" * word_progress + "░" * (20 - word_progress)
    word_percentage = (word_count / 500 * 100) if word_count > 0 else 0
    lines.append(f"│ 📝 Word Count       │ {word_count:<12} │ {word_bar} {word_percentage:.0f}%  │")
    
    # Prompt Count
    prompt_count = metrics.get("prompt_count", 0)
    prompt_progress = min(20, int((prompt_count / 10) * 20))
    prompt_bar = "█" * prompt_progress + "░" * (20 - prompt_progress)
    prompt_percentage = (prompt_count / 10 * 100) if prompt_count > 0 else 0
    lines.append(f"│ 💬 Prompt Count     │ {prompt_count:<12} │ {prompt_bar} {prompt_percentage:.0f}%  │")
    
    # Complexity
    complexity = metrics.get("complexity", 0)
    complexity_progress = min(20, int((complexity / 10) * 20))
    complexity_bar = "█" * complexity_progress + "░" * (20 - complexity_progress)
    complexity_percentage = (complexity / 10 * 100) if complexity > 0 else 0
    lines.append(f"│ 🧩 Complexity       │ {complexity:.1f}/10{'':<8} │ {complexity_bar} {complexity_percentage:.0f}%  │")
    
    # Temporal References
    temp_refs = metrics.get("temporal_references", 0)
    temp_progress = min(20, int((temp_refs / 5) * 20))
    temp_bar = "█" * temp_progress + "░" * (20 - temp_progress)
    temp_percentage = (temp_refs / 5 * 100) if temp_refs > 0 else 0
    lines.append(f"│ ⏰ Temporal Refs     │ {temp_refs:<12} │ {temp_bar} {temp_percentage:.0f}%  │")
    
    # Recursive Depth
    rec_depth = metrics.get("recursive_depth", 0)
    rec_progress = min(20, int((rec_depth / 3) * 20))
    rec_bar = "█" * rec_progress + "░" * (20 - rec_progress)
    rec_percentage = (rec_depth / 3 * 100) if rec_depth > 0 else 0
    lines.append(f"│ 🔄 Recursive Depth   │ {rec_depth:<12} │ {rec_bar} {rec_percentage:.0f}%  │")
    
    # Sentiment
    sentiment = metrics.get("sentiment", "neutral")
    sentiment_map = {"positive": 8, "neutral": 5, "negative": 2}
    sentiment_value = sentiment_map.get(sentiment.lower(), 5)
    sentiment_progress = min(20, int((sentiment_value / 10) * 20))
    sentiment_bar = "█" * sentiment_progress + "░" * (20 - sentiment_progress)
    sentiment_percentage = (sentiment_value / 10 * 100) if sentiment_value > 0 else 0
    lines.append(f"│ 😊 Sentiment         │ {sentiment:<12} │ {sentiment_bar} {sentiment_percentage:.0f}%  │")
    
    # RAG Queries
    rag_queries = metrics.get("rag_queries", 0)
    rag_progress = min(20, int((rag_queries / 5) * 20))
    rag_bar = "█" * rag_progress + "░" * (20 - rag_progress)
    rag_percentage = (rag_queries / 5 * 100) if rag_queries > 0 else 0
    lines.append(f"│ 🔍 RAG Queries       │ {rag_queries:<12} │ {rag_bar} {rag_percentage:.0f}%  │")
    
    # XP Earned
    xp_earned = metrics.get("xp_earned", 0.0)
    xp_progress = min(20, int((xp_earned / 10.0) * 20))
    xp_bar = "█" * xp_progress + "░" * (20 - xp_progress)
    xp_percentage = (xp_earned / 10.0 * 100) if xp_earned > 0 else 0
    lines.append(f"│ ⭐ XP Earned         │ {xp_earned:<12.2f} │ {xp_bar} {xp_percentage:.0f}%  │")
    
    lines.append("└─────────────────────┴──────────────┴───────────────────────────┘")
    
    return "\n".join(lines)


def generate_timeline(start_time: str, end_time: str, events: List[Dict] = None) -> str:
    """
    Generuje ASCII timeline vizualizáciu.
    
    Args:
        start_time: Čas začiatku (HH:MM)
        end_time: Čas konca (HH:MM)
        events: Zoznam eventov s časom a popisom
    
    Returns:
        ASCII timeline string
    """
    timeline = f"Session Timeline:\n"
    timeline += f"[{start_time}] ─"
    
    if events:
        for i, event in enumerate(events):
            event_time = event.get("time", "")
            event_label = event.get("label", "")
            if i == 0:
                timeline += f"───● {event_label} ───"
            else:
                timeline += f"───● {event_label} ───"
    else:
        timeline += "────────●────────"
    
    timeline += f" [{end_time}]"
    
    return timeline


def generate_knowledge_graph(backlinks: List[str], current_doc: str = "XVADUR Session") -> str:
    """
    Generuje ASCII knowledge graph.
    
    Args:
        backlinks: Zoznam backlinkov v formáte [[DocumentName]]
        current_doc: Názov aktuálneho dokumentu
    
    Returns:
        ASCII knowledge graph string
    """
    import re
    
    graph = f"{current_doc}\n"
    graph += "    │\n"
    
    for i, link in enumerate(backlinks):
        # Extrahovať názov dokumentu z [[DocumentName]]
        match = re.search(r'\[\[([^\]]+)\]\]', link)
        if match:
            doc_name = match.group(1)
            
            if i == len(backlinks) - 1:
                graph += f"    └── {link}\n"
            else:
                graph += f"    ├── {link}\n"
    
    return graph


def generate_activity_heatmap(hourly_data: Dict[int, int]) -> str:
    """
    Generuje ASCII heatmap pre hourly activity.
    
    Args:
        hourly_data: Dict s hodinami (0-23) a hodnotami
    
    Returns:
        ASCII heatmap string
    """
    heatmap = "Hourly Activity (24h):\n"
    
    for hour in range(0, 24, 6):  # Každé 6 hodín
        value = hourly_data.get(hour, 0)
        max_value = max(hourly_data.values()) if hourly_data else 1
        bar_length = int((value / max_value) * 10) if max_value > 0 else 0
        bar = "█" * bar_length + "░" * (10 - bar_length)
        heatmap += f"{hour:02d}: {bar}\n"
    
    return heatmap


if __name__ == "__main__":
    # Testovanie
    print("=" * 60)
    print("STATUS DASHBOARD:")
    print("=" * 60)
    print(generate_status_dashboard("2025-12-01_08:15", "2025-12-01", "1h 15min", 1.54, 10.0, 1, 3))
    
    print("\n" + "=" * 60)
    print("METRICS DASHBOARD:")
    print("=" * 60)
    print(generate_metrics_dashboard({
        "word_count": 250,
        "prompt_count": 6,
        "complexity": 8.0,
        "temporal_references": 2,
        "recursive_depth": 1,
        "sentiment": "neutral",
        "rag_queries": 1,
        "xp_earned": 1.54
    }))
    
    print("\n" + "=" * 60)
    print("XP BREAKDOWN:")
    print("=" * 60)
    print(generate_xp_breakdown({
        "Introspektívna Hĺbka": 0.20,
        "Prompt Count Bonus": 0.24,
        "Complexity Bonus": 0.30,
        "Temporal References": 0.60,
        "RAG Queries": 0.20
    }))
    
    print("\n" + "=" * 60)
    print("PROGRESS BAR:")
    print("=" * 60)
    print(generate_progress_bar(1.54, 10.0))
    
    print("\n" + "=" * 60)
    print("TIMELINE:")
    print("=" * 60)
    print(generate_timeline("08:00", "09:30", [
        {"time": "08:15", "label": "Start"},
        {"time": "08:45", "label": "Main"},
        {"time": "09:15", "label": "Reflection"}
    ]))
    
    print("\n" + "=" * 60)
    print("KNOWLEDGE GRAPH:")
    print("=" * 60)
    print(generate_knowledge_graph([
        "[[CHECKPOINT_LATEST]]",
        "[[CHRONOLOGICAL_MAP_2025]]",
        "[[Recepcia]]"
    ]))

