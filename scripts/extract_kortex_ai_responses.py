#!/usr/bin/env python3
"""
Extrakcia AI odpovedí z Kortex AI backup JSON súboru a spárovanie s user promptmi.

Tento skript:
1. Načíta Kortex backup JSON súbor
2. Extrahuje user prompty (is_kai_prompt=True) a AI odpovede (is_kai_prompt=False)
3. Spáruje ich do konverzačných párov podľa session a timestamp
4. Uloží výsledky do JSONL formátu
"""

import json
import sys
from pathlib import Path
from datetime import datetime
from typing import Dict, List, Optional, Any
from collections import defaultdict

# Pridáme workspace root do sys.path
workspace_root = Path(__file__).parent.parent
sys.path.insert(0, str(workspace_root))


def extract_prosemirror_text(content: Dict[str, Any]) -> str:
    """
    Extrahuje text z ProseMirror dokumentu (user prompty).
    
    ProseMirror formát:
    {
        "type": "doc",
        "content": [
            {
                "type": "paragraph",
                "content": [
                    {"type": "text", "text": "..."}
                ]
            }
        ]
    }
    """
    if not isinstance(content, dict):
        return ""
    
    text_parts = []
    
    def traverse_node(node: Dict[str, Any]) -> None:
        if isinstance(node, dict):
            # Ak je to text node, pridáme text
            if node.get("type") == "text" and "text" in node:
                text_parts.append(node["text"])
            
            # Rekurzívne prejdeme cez content
            if "content" in node and isinstance(node["content"], list):
                for child in node["content"]:
                    traverse_node(child)
            
            # Rekurzívne prejdeme cez všetky kľúče (pre nested štruktúry)
            for key, value in node.items():
                if key != "text" and key != "content" and isinstance(value, (dict, list)):
                    if isinstance(value, list):
                        for item in value:
                            traverse_node(item)
                    else:
                        traverse_node(value)
        elif isinstance(node, list):
            for item in node:
                traverse_node(item)
    
    traverse_node(content)
    return "".join(text_parts)


def extract_kai_message_text(content: Dict[str, Any]) -> str:
    """
    Extrahuje text z KAI odpovede (AI odpovede).
    
    KAI formát:
    {
        "type": "kai",
        "generation_status": "complete",
        "data": {
            "type": "message",
            "chunks": ["text", " ", "more text"]
        }
    }
    """
    if not isinstance(content, dict):
        return ""
    
    # Získame data -> chunks
    data = content.get("data", {})
    if isinstance(data, dict):
        chunks = data.get("chunks", [])
        if isinstance(chunks, list):
            # Spojíme všetky chunks do jedného textu
            return "".join(str(chunk) for chunk in chunks if chunk)
    
    return ""


def extract_captures(backup_path: Path) -> tuple[List[Dict], List[Dict]]:
    """
    Extrahuje captures z backup JSON súboru a rozdelí ich na user prompty a AI odpovede.
    
    Returns:
        (user_prompts, ai_responses) - zoznamy captures
    """
    print(f"📖 Načítavam backup súbor: {backup_path}")
    
    with open(backup_path, 'r', encoding='utf-8') as f:
        data = json.load(f)
    
    # Získame captures kolekciu
    ws_db = data.get("workspaceDbJson", {})
    collections = ws_db.get("collections", [])
    
    captures_coll = next((c for c in collections if c.get("name") == "captures"), None)
    
    if not captures_coll:
        raise ValueError("Kolekcia 'captures' sa nenašla v backup súbore")
    
    captures = captures_coll.get("docs", [])
    print(f"✅ Načítaných {len(captures)} captures")
    
    # Rozdelíme captures na user prompty a AI odpovede
    user_prompts = []
    ai_responses = []
    
    for capture in captures:
        is_kai_prompt = capture.get("is_kai_prompt", False)
        
        # Pridáme metadata (content ponecháme ako je, parsovať ho budeme neskôr)
        capture_meta = {
            "uuid": capture.get("uuid"),
            "session": capture.get("session"),
            "date_created": capture.get("date_created"),
            "date_modified": capture.get("date_modified"),
            "workspace": capture.get("workspace"),
            "content": capture.get("content"),  # Môže byť string alebo dict
        }
        
        if is_kai_prompt:
            user_prompts.append(capture_meta)
        else:
            ai_responses.append(capture_meta)
    
    print(f"📊 Rozdelenie:")
    print(f"  User prompty (is_kai_prompt=True): {len(user_prompts)}")
    print(f"  AI odpovede (is_kai_prompt=False): {len(ai_responses)}")
    
    return user_prompts, ai_responses


def extract_text_from_capture(capture: Dict) -> Optional[str]:
    """
    Extrahuje text z capture na základe jeho typu contentu.
    
    Returns:
        Extrahovaný text alebo None ak sa nepodarilo extrahovať
    """
    content_raw = capture.get("content", {})
    
    # Content môže byť string (JSON) alebo už parsed dict
    if isinstance(content_raw, str):
        try:
            content = json.loads(content_raw)
        except (json.JSONDecodeError, TypeError):
            return None
    elif isinstance(content_raw, dict):
        content = content_raw
    else:
        return None
    
    # Skúsime ProseMirror formát (user prompty)
    if content.get("type") == "doc":
        text = extract_prosemirror_text(content)
        if text:
            return text.strip()
    
    # Skúsime KAI formát (AI odpovede)
    if content.get("type") == "kai":
        text = extract_kai_message_text(content)
        if text:
            return text.strip()
    
    return None


def pair_prompts_and_responses(
    user_prompts: List[Dict],
    ai_responses: List[Dict]
) -> List[Dict]:
    """
    Spáruje user prompty s AI odpoveďami podľa session a timestamp.
    
    Returns:
        Zoznam konverzačných párov: [
            {
                "user_prompt": {...},
                "ai_response": {...},
                "session": "...",
                "timestamp": "..."
            },
            ...
        ]
    """
    print("\n🔗 Spárujem prompty a odpovede...")
    
    # Zoskupíme podľa session
    prompts_by_session = defaultdict(list)
    responses_by_session = defaultdict(list)
    
    for prompt in user_prompts:
        session = prompt.get("session")
        if session:
            prompts_by_session[session].append(prompt)
    
    for response in ai_responses:
        session = response.get("session")
        if session:
            responses_by_session[session].append(response)
    
    print(f"  Sessions s user promptmi: {len(prompts_by_session)}")
    print(f"  Sessions s AI odpoveďami: {len(responses_by_session)}")
    
    # Spárujeme podľa session a timestamp
    pairs = []
    
    for session in prompts_by_session.keys():
        prompts = prompts_by_session[session]
        responses = responses_by_session.get(session, [])
        
        # Zoradíme podľa timestamp
        prompts_sorted = sorted(
            prompts,
            key=lambda x: x.get("date_created", ""),
            reverse=False
        )
        responses_sorted = sorted(
            responses,
            key=lambda x: x.get("date_created", ""),
            reverse=False
        )
        
        # Párujeme: user prompt -> najbližšia nasledujúca AI odpoveď
        prompt_idx = 0
        response_idx = 0
        
        while prompt_idx < len(prompts_sorted) and response_idx < len(responses_sorted):
            prompt = prompts_sorted[prompt_idx]
            prompt_time = prompt.get("date_created", "")
            
            # Nájdeme najbližšiu AI odpoveď po tomto prompte
            best_response = None
            best_response_idx = None
            min_time_diff = None
            
            for i in range(response_idx, len(responses_sorted)):
                response = responses_sorted[i]
                response_time = response.get("date_created", "")
                
                if response_time >= prompt_time:
                    # Vypočítame časový rozdiel
                    try:
                        prompt_dt = datetime.fromisoformat(prompt_time.replace('Z', '+00:00'))
                        response_dt = datetime.fromisoformat(response_time.replace('Z', '+00:00'))
                        time_diff = (response_dt - prompt_dt).total_seconds()
                        
                        if min_time_diff is None or time_diff < min_time_diff:
                            min_time_diff = time_diff
                            best_response = response
                            best_response_idx = i
                    except Exception:
                        pass
            
            # Ak sme našli párovanie (do 5 minút), vytvoríme pár
            if best_response and min_time_diff and min_time_diff < 300:  # 5 minút
                pairs.append({
                    "user_prompt": prompt,
                    "ai_response": best_response,
                    "session": session,
                    "timestamp": prompt_time,
                    "time_diff_seconds": min_time_diff,
                })
                response_idx = best_response_idx + 1
            
            prompt_idx += 1
    
    print(f"✅ Spárovaných párov: {len(pairs)}")
    return pairs


def main():
    """Hlavná funkcia skriptu."""
    
    # Cesty k súborom
    backup_path = workspace_root / "xvadur" / "+" / "kortex-backup (1).json"
    output_dir = workspace_root / "xvadur" / "data" / "kortex_extracted"
    output_dir.mkdir(parents=True, exist_ok=True)
    
    # Output súbory
    user_prompts_output = output_dir / "user_prompts.jsonl"
    ai_responses_output = output_dir / "ai_responses.jsonl"
    pairs_output = output_dir / "conversation_pairs.jsonl"
    
    print("🚀 Extrakcia AI odpovedí z Kortex backup\n")
    print(f"📁 Backup súbor: {backup_path}")
    print(f"📁 Output adresár: {output_dir}\n")
    
    # 1. Extrahujeme captures
    user_prompts, ai_responses = extract_captures(backup_path)
    
    # 2. Extrahujeme texty z captures
    print("\n📝 Extrahujem texty z captures...")
    
    user_prompts_with_text = []
    for prompt in user_prompts:
        text = extract_text_from_capture(prompt)
        if text:
            prompt["extracted_text"] = text
            prompt["text_length"] = len(text)
            prompt["word_count"] = len(text.split())
            user_prompts_with_text.append(prompt)
    
    ai_responses_with_text = []
    for response in ai_responses:
        text = extract_text_from_capture(response)
        if text:
            response["extracted_text"] = text
            response["text_length"] = len(text)
            response["word_count"] = len(text.split())
            ai_responses_with_text.append(response)
    
    print(f"✅ Extrahovaných textov:")
    print(f"  User prompty: {len(user_prompts_with_text)} / {len(user_prompts)}")
    print(f"  AI odpovede: {len(ai_responses_with_text)} / {len(ai_responses)}")
    
    # 3. Spárujeme prompty a odpovede
    pairs = pair_prompts_and_responses(user_prompts_with_text, ai_responses_with_text)
    
    # 4. Uložíme výsledky
    print("\n💾 Ukladám výsledky...")
    
    # User prompty
    with open(user_prompts_output, 'w', encoding='utf-8') as f:
        for prompt in user_prompts_with_text:
            f.write(json.dumps(prompt, ensure_ascii=False) + "\n")
    print(f"  ✅ User prompty: {user_prompts_output}")
    
    # AI odpovede
    with open(ai_responses_output, 'w', encoding='utf-8') as f:
        for response in ai_responses_with_text:
            f.write(json.dumps(response, ensure_ascii=False) + "\n")
    print(f"  ✅ AI odpovede: {ai_responses_output}")
    
    # Konverzačné páry
    with open(pairs_output, 'w', encoding='utf-8') as f:
        for pair in pairs:
            f.write(json.dumps(pair, ensure_ascii=False) + "\n")
    print(f"  ✅ Konverzačné páry: {pairs_output}")
    
    print(f"\n🎉 Hotovo! Extrahovaných:")
    print(f"  {len(user_prompts_with_text)} user promptov")
    print(f"  {len(ai_responses_with_text)} AI odpovedí")
    print(f"  {len(pairs)} konverzačných párov")


if __name__ == "__main__":
    main()

