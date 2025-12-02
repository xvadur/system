#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Xvadur Backlinking System: Automatické vytváranie Obsidian linkov [[...]] pre xvadur režim.

TODO: Add support for custom entity extraction patterns
TODO: Implement fuzzy matching for document names
FIXME: Handle special characters in document names better

Tento skript:
1. Extrahuje entity z obsahu (ľudia, projekty, koncepty, dátumy)
2. Nájde relevantné dokumenty v Obsidian vaultu
3. Vytvorí backlinky v formáte [[DocumentName]]
4. Mapuje knowledge graph vzťahov

Kľúčové koncepty (heuristika):
- Extrahované z RAG analýzy datasetu (664 promptov)
- Analýza vykonaná: 2025-12-01
- 10 hlavných kategórií: Technické termíny, Osobné koncepty, Projekty,
  Filozofické koncepty, Organizačné koncepty
"""

import json
import sys
import re
from pathlib import Path
from typing import List, Dict

# Konfigurácia
# TODO: Update paths if script is moved
# Script je v xvadur_obsidian/xvadur/scripts/, takže root je 3 úrovne hore
SCRIPT_DIR = Path(__file__).parent
XVADUR_ROOT = SCRIPT_DIR.parent
OBSIDIAN_VAULT = XVADUR_ROOT.parent
XVADUR_DIR = XVADUR_ROOT


def extract_entities(text: str) -> Dict[str, List[str]]:
    """
    Extrahuje entity z textu (ľudia, projekty, koncepty, dátumy).

    Returns:
        Dict s kategóriami entít
    """
    entities = {"people": [], "projects": [], "concepts": [], "dates": [], "topics": []}

    # Projekty (často v uvozovkách alebo s veľkými písmenami)
    project_keywords = [
        # Recepcia a jej variácie
        "Recepcia",
        "recepcia",
        "Recepčná",
        "recepčná",
        "recepcna",
        "Recepcna",
        "AI Recepcia",
        "AI recepcia",
        "AI Recepčná",
        "AI recepčná",
        "AI recepcna",
        "AI Recepcna",
        # Vlado a variácie jeho mena
        "Vlado",
        "vlado",
        "Vladislav",
        "vladislav",
        "Quest: Vlado",
        "Quest Vlado",
        "quest vlado",
        "quest: vlado",
        # Biznis (explicitne podľa zadania)
        "biznis",
        "Biznis",
        # Ostatné (pôvodné pre úplnosť, nesúvisiace so zadanim)
        "Magnum Opus",
        "magnum opus",
        "xvadur_console",
        "xvadur console",
    ]

    for keyword in project_keywords:
        if keyword.lower() in text.lower():
            entities["projects"].append(keyword)

    # Koncepty (kľúčové slová) - extrahované z RAG analýzy datasetu
    # Analýza vykonaná: 2025-12-01
    # Zdroj: RAG query synthesis z 664 promptov
    concept_keywords = [
        # Technické termíny (najčastejšie spomínané)
        "RAG",
        "rag",
        "Retrieval-Augmented Generation",
        "MCP",
        "mcp",
        "Meta Cognitive Prompt",
        "Obsidian",
        "obsidian",
        # Osobné koncepty (kľúčové pre identitu)
        "sanitár",
        "sanitar",
        "Sanitary Engineer",
        "architekt",
        "architect",
        "Architekt",
        # Projekty (aktívne projekty)
        "Recepčná",
        "recepčná",
        "Recepcia",
        "recepcia",
        "AI konzola",
        "ai konzola",
        "AI Console",
        "xvadur console",
        "xvadur_console",
        # Filozofické koncepty (osobné témy)
        "transformácia",
        "transformation",
        "Transformácia",
        "identita",
        "identity",
        "Identita",
        "kreativita",
        "creativity",
        "Kreativita",
        "inferiorita",
        "inferiority",
        "Inferiorita",
        # Organizačné koncepty
        "checkpoint",
        "Checkpoint",
        "CHECKPOINT",
        "chronológia",
        "chronology",
        "Chronológia",
        "mapa",
        "map",
        "Mapa",
        # Ďalšie kľúčové koncepty z analýzy
        "sebareflexia",
        "self-reflection",
        "osobný rozvoj",
        "personal development",
        "podnikanie",
        "business",
        "produktivita",
        "productivity",
        "gamifikácia",
        "gamification",
        "XP",
        "xp",
        "experience points",
    ]

    for keyword in concept_keywords:
        if keyword.lower() in text.lower():
            entities["concepts"].append(keyword)

    # Dátumy (formáty: YYYY-MM-DD, DD.MM.YYYY, "pred mesiacom", "minulý rok")
    date_patterns = [
        r"\b(\d{4}-\d{2}-\d{2})\b",  # YYYY-MM-DD
        r"\b(\d{1,2}\.\d{1,2}\.\d{4})\b",  # DD.MM.YYYY
        r"\b(pred\s+(?:mesiacom|rokom|týždňom))\b",  # "pred mesiacom"
        r"\b(minulý|minulý|posledný)\s+(?:rok|mesiac|týždeň)\b",  # "minulý rok"
    ]

    for pattern in date_patterns:
        matches = re.findall(pattern, text, re.IGNORECASE)
        entities["dates"].extend(matches)

    # Témy (heuristika tematických clustrov podobná konceptom; synonymá, varianty, anglické/slovenské páry)
    topic_keywords = [
        # Filozofia & existencia
        "filozofia",
        "philosophy",
        "existencia",
        "existence",
        "ontológia",
        "ontology",
        "bytie",
        "being",
        "vedomie",
        "consciousness",
        "myslenie",
        "thinking",
        "uvedomenie",
        "awareness",
        # Biznis & produktivita
        "biznis",
        "business",
        "ekonomika",
        "economics",
        "podnikanie",
        "entrepreneurship",
        "startupy",
        "startup",
        "spolupráca",
        "collaboration",
        "produktívnosť",
        "productivity",
        "workflow",
        "procesy",
        "processes",
        # Intimita, vzťahy & psychológia
        "intimita",
        "intimacy",
        "vzťahy",
        "relationships",
        "láska",
        "love",
        "priateľstvo",
        "friendship",
        "dôvera",
        "trust",
        "psychológia",
        "psychology",
        "emócie",
        "emocie",
        "emotion",
        "emotions",
        "vnútorný svet",
        "inner world",
        # Vulgarita, autenticita & zraniteľnosť
        "vulgarita",
        "vulgarity",
        "autenticita",
        "authenticity",
        "pravda",
        "truth",
        "úprimnosť",
        "honesty",
        "zraniteľnosť",
        "vulnerability",
        # Trauma, zmena, adaptácia
        "trauma",
        "zmena",
        "change",
        "adaptácia",
        "adaptation",
        "reziliencia",
        "resilience",
        # Identita, osobnosť & komunita
        "identita",
        "identity",
        "profil",
        "profile",
        "osobnosť",
        "personality",
        "spoločenstvo",
        "community",
        "kultúra",
        "culture",
        # Kreativita, hra, experiment
        "kreativita",
        "creativity",
        "tvorivosť",
        "creativeness",
        "improvizácia",
        "improvisation",
        "hra",
        "play",
        "experiment",
        "playfulness",
        # Samota, význam, vnútorná motivácia
        "samota",
        "loneliness",
        "samostatnosť",
        "independence",
        "súdržnosť",
        "cohesion",
        "zmysel",
        "meaning",
        "motív",
        "motivation",
        "drive",
        "purpose",
        "cieľ",
        "goal",
        # Sebareflexia & rozvoj
        "sebareflexia",
        "self-reflection",
        "sebarozvoj",
        "personal development",
        "rast",
        "growth",
        # Paradox objaviteľa, blokátory, mentálne prekážky
        "paradox objaviteľa",
        "explorer's paradox",
        "blokátor",
        "blocker",
        "wyhýbanie",
        "avoidance",
        # Vzory, vzorce, archetypy (pattern recognition)
        "vzorec",
        "pattern",
        "archetyp",
        "archetype",
        # Meta & RAG
        "meta",
        "RAG",
        "retrieval",
        "knowledge graph",
        "inšpirácia",
        "inspiration",
    ]

    for keyword in topic_keywords:
        if keyword.lower() in text.lower():
            entities["topics"].append(keyword)

    # Odstránenie duplikátov
    for key in entities:
        entities[key] = list(set(entities[key]))

    return entities


def find_relevant_documents(
    entity: str, entity_type: str, vault_path: Path
) -> List[str]:
    """
    Nájde relevantné dokumenty v Obsidian vaultu pre danú entitu.

    Args:
        entity: Názov entity
        entity_type: Typ entity (projects, concepts, dates, topics)
        vault_path: Cesta k Obsidian vaultu

    Returns:
        Zoznam názvov dokumentov (bez .md prípony)
    """
    relevant_docs = []
    entity_lower = entity.lower()

    # Projekty
    if entity_type == "projects":
        if "recepcia" in entity_lower or "recepcna" in entity_lower:
            relevant_docs.extend(
                [
                    "Recepcia",
                    "Recepcia_Prompt_v2.0",
                    "Recepcia_Tools_JSON",
                    "Recepcia_Status_Summary",
                    "Recepcia_Session_Close",
                ]
            )
        if "vlado" in entity_lower:
            relevant_docs.extend(["RECEPCIA_VLADO_CHRONOLOGY", "Quest: Vlado"])
        if "magnum opus" in entity_lower:
            relevant_docs.append("CHECKPOINT_LATEST")

    # Koncepty
    if entity_type == "concepts":
        if "checkpoint" in entity_lower:
            relevant_docs.append("CHECKPOINT_LATEST")
        if (
            "chronológia" in entity_lower
            or "chronology" in entity_lower
            or "mapa" in entity_lower
        ):
            relevant_docs.extend(
                [
                    "CHRONOLOGICAL_MAP_2025",
                    "AI_CHRONOLOGY",
                    "NEMOCNICA_CHRONOLOGY",
                    "RECEPCIA_VLADO_CHRONOLOGY",
                ]
            )
        if "rag" in entity_lower:
            relevant_docs.extend(
                ["RAG_SYSTEM_ARCHITECTURE", "RAG_INTEGRATION_COMPLETE"]
            )
        if (
            "identita" in entity_lower
            or "identity" in entity_lower
            or "profil" in entity_lower
        ):
            relevant_docs.append("xvadur_profile")
        if "transformácia" in entity_lower or "transformation" in entity_lower:
            relevant_docs.extend(
                ["UNIQUENESS_ASSESSMENT", "CYCLE_COMPLETION_DECEMBER_2025"]
            )

    # Dátumy
    if entity_type == "dates":
        if "pred mesiacom" in entity_lower or "minulý mesiac" in entity_lower:
            relevant_docs.append("CHRONOLOGICAL_MAP_2025")
        if "minulý rok" in entity_lower or "pred rokom" in entity_lower:
            relevant_docs.extend(["SYNCHRONIZATION_2024_2025", "silvester2024"])

    # Témy
    if entity_type == "topics":
        if "filozofia" in entity_lower:
            relevant_docs.extend(["Heavy is the Crown", "Formát moci"])

    # Odstránenie duplikátov
    return list(set(relevant_docs))


def create_backlinks(content: str, vault_path: Path = OBSIDIAN_VAULT) -> List[str]:
    """
    Vytvorí backlinky na relevantné dokumenty v Obsidian vaultu.

    Args:
        content: Textový obsah pre analýzu
        vault_path: Cesta k Obsidian vaultu

    Returns:
        Zoznam backlinkov v formáte [[DocumentName]]
    """
    # Extrahovať entity
    entities = extract_entities(content)

    # Nájsť relevantné dokumenty
    backlinks = []
    processed_docs = set()

    for entity_type, entity_list in entities.items():
        for entity in entity_list:
            relevant_docs = find_relevant_documents(entity, entity_type, vault_path)
            for doc in relevant_docs:
                if doc not in processed_docs:
                    backlinks.append(f"[[{doc}]]")
                    processed_docs.add(doc)

    # Vždy pridať základné linky ak sú relevantné
    if any(
        keyword in content.lower()
        for keyword in ["checkpoint", "aktuálny stav", "posledný save"]
    ):
        if "CHECKPOINT_LATEST" not in processed_docs:
            backlinks.append("[[CHECKPOINT_LATEST]]")

    if any(
        keyword in content.lower()
        for keyword in ["minulosť", "história", "pred", "chronológia"]
    ):
        if "CHRONOLOGICAL_MAP_2025" not in processed_docs:
            backlinks.append("[[CHRONOLOGICAL_MAP_2025]]")

    return list(set(backlinks))  # Odstránenie duplikátov


def build_knowledge_graph(
    xvadur_documents: List[Dict], vault_path: Path = OBSIDIAN_VAULT
) -> Dict:
    """
    Vytvorí knowledge graph z xvadur dokumentov a ich linkov.

    Args:
        xvadur_documents: Zoznam xvadur dokumentov s metadátami
        vault_path: Cesta k Obsidian vaultu

    Returns:
        Knowledge graph v JSON formáte
    """
    graph = {"nodes": [], "edges": []}

    node_ids = {}
    node_counter = 0

    # Pridať xvadur dokumenty ako nodes
    for doc in xvadur_documents:
        doc_id = f"xvadur_{node_counter}"
        node_ids[doc.get("id", doc_id)] = doc_id
        node_counter += 1

        graph["nodes"].append(
            {
                "id": doc_id,
                "label": doc.get("title", "Untitled"),
                "type": "xvadur_session",
                "date": doc.get("date", ""),
                "xp": doc.get("xp", 0),
            }
        )

        # Pridať linky ako edges
        backlinks = doc.get("backlinks", [])
        for link in backlinks:
            # Extrahovať názov dokumentu z [[DocumentName]]
            match = re.search(r"\[\[([^\]]+)\]\]", link)
            if match:
                target_name = match.group(1)
                target_id = f"doc_{target_name.replace(' ', '_')}"

                # Pridať target node ak ešte neexistuje
                if target_id not in node_ids:
                    graph["nodes"].append(
                        {
                            "id": target_id,
                            "label": target_name,
                            "type": "obsidian_document",
                        }
                    )
                    node_ids[target_name] = target_id

                # Pridať edge
                graph["edges"].append(
                    {"source": doc_id, "target": target_id, "type": "references"}
                )

    return graph


def generate_mermaid_diagram(graph: Dict) -> str:
    """
    Generuje Mermaid diagram z knowledge graphu.

    Args:
        graph: Knowledge graph v JSON formáte

    Returns:
        Mermaid diagram kód
    """
    mermaid = "graph TD\n"

    # Pridať nodes
    for node in graph["nodes"]:
        node_id = node["id"].replace("-", "_").replace(" ", "_")
        label = node["label"]
        node_type = node.get("type", "default")

        if node_type == "xvadur_session":
            mermaid += f'    {node_id}["{label}"]\n'
        else:
            mermaid += f'    {node_id}["{label}"]\n'

    # Pridať edges
    for edge in graph["edges"]:
        source = edge["source"].replace("-", "_").replace(" ", "_")
        target = edge["target"].replace("-", "_").replace(" ", "_")
        mermaid += f"    {source} --> {target}\n"

    return mermaid


def main():
    """Hlavná funkcia - volaná z Cursor agenta alebo terminálu."""
    if len(sys.argv) < 2:
        print(
            json.dumps({"error": "Usage: xvadur_backlinking.py <content> [vault_path]"})
        )
        sys.exit(1)

    content = sys.argv[1]
    vault_path = Path(sys.argv[2]) if len(sys.argv) > 2 else OBSIDIAN_VAULT

    # Vytvoriť backlinky
    backlinks = create_backlinks(content, vault_path)

    # Extrahovať entity
    entities = extract_entities(content)

    # Výstup
    result = {
        "backlinks": backlinks,
        "entities": entities,
        "backlinks_count": len(backlinks),
        "entities_count": sum(len(v) for v in entities.values()),
    }

    print(json.dumps(result, indent=2, ensure_ascii=False))


if __name__ == "__main__":
    main()
