"""
Validácia JSON schém v XVADUR systéme

Skontroluje konzistenciu medzi dokumentáciou a implementáciou.
"""

import json
import sys
from pathlib import Path
from typing import Dict, List, Any, Optional
from dataclasses import dataclass

# Add workspace root to path
workspace_root = Path(__file__).parent.parent.parent
sys.path.insert(0, str(workspace_root))


@dataclass
class SchemaValidationResult:
    """Výsledok validácie schémy."""
    file_path: str
    is_valid: bool
    errors: List[str]
    warnings: List[str]
    actual_fields: Dict[str, Any]
    documented_fields: Dict[str, Any]


class SchemaValidator:
    """Validátor JSON schém pre XVADUR systém."""
    
    # Dokumentované schémy z ARCHITECTURE.md
    DOCUMENTED_SCHEMAS = {
        "conversations.jsonl": {
            "session": "string",
            "timestamp": "string (ISO format)",
            "user_prompt": "object",
            "ai_response": "object"
        },
        "prompts_log.jsonl": {
            "timestamp": "string (ISO format)",
            "role": "string",
            "content": "string",
            "metadata": "object"
        },
        "xp_history.jsonl": {
            "timestamp": "string (ISO format)",
            "total_xp": "number",
            "level": "number",
            "next_level_xp": "number",
            "xp_needed": "number",
            "streak_days": "number",
            "breakdown": {
                "from_work": "object",
                "from_activity": "object",
                "bonuses": "object"
            }
        },
        "XVADUR_LOG.jsonl": {
            "timestamp": "string (ISO format)",
            "date": "string (YYYY-MM-DD)",
            "time": "string (HH:MM)",
            "title": "string",
            "type": "string",
            "status": "string",
            "files_changed": "array (optional)",
            "xp_estimate": "number (optional)",
            "completed": "array (optional)",
            "results": "object (optional)",
            "decisions": "array (optional)",
            "quest_id": "number (optional)",
            "xp_earned": "number (optional)",
            "notes": "string (optional)"
        },
        "SAVE_GAME_LATEST.json": {
            "metadata": "object",
            "status": "object",
            "narrative": "object",
            "quests": "array",
            "instructions": "object"
        },
        "XVADUR_XP.json": {
            "status": "object",
            "breakdown": "object",
            "last_updated": "string"
        }
    }
    
    def __init__(self, workspace_root: Path):
        self.workspace_root = workspace_root
        self.results: List[SchemaValidationResult] = []
    
    def validate_file(self, file_path: Path, schema_name: str) -> SchemaValidationResult:
        """Validuje jeden JSONL súbor proti dokumentovanej schéme."""
        errors = []
        warnings = []
        actual_fields = {}
        documented_fields = self.DOCUMENTED_SCHEMAS.get(schema_name, {})
        
        if not file_path.exists():
            # conversations.jsonl je legacy súbor - neexistovanie nie je chyba
            if "conversations.jsonl" in schema_name:
                warnings.append(f"Súbor neexistuje (legacy formát): {file_path}")
                return SchemaValidationResult(
                    file_path=str(file_path),
                    is_valid=True,  # Legacy súbor - nie je chyba
                    errors=errors,
                    warnings=warnings,
                    actual_fields={},
                    documented_fields=documented_fields
                )
            else:
                errors.append(f"Súbor neexistuje: {file_path}")
                return SchemaValidationResult(
                    file_path=str(file_path),
                    is_valid=False,
                    errors=errors,
                    warnings=warnings,
                    actual_fields={},
                    documented_fields=documented_fields
                )
        
        # Načítaj prvých 10 záznamov pre analýzu
        sample_records = []
        try:
            with open(file_path, 'r', encoding='utf-8') as f:
                for i, line in enumerate(f):
                    if i >= 10:  # Len prvých 10 záznamov
                        break
                    line = line.strip()
                    if not line:
                        continue
                    try:
                        record = json.loads(line)
                        sample_records.append(record)
                    except json.JSONDecodeError as e:
                        errors.append(f"Chybný JSON na riadku {i+1}: {e}")
        except Exception as e:
            errors.append(f"Chyba pri čítaní súboru: {e}")
            return SchemaValidationResult(
                file_path=str(file_path),
                is_valid=False,
                errors=errors,
                warnings=warnings,
                actual_fields={},
                documented_fields=documented_fields
            )
        
        if not sample_records:
            warnings.append("Súbor je prázdny alebo neobsahuje platné JSON záznamy")
            return SchemaValidationResult(
                file_path=str(file_path),
                is_valid=True,  # Prázdny súbor nie je chyba
                errors=errors,
                warnings=warnings,
                actual_fields={},
                documented_fields=documented_fields
            )
        
        # Analyzuj polia v skutočných záznamoch
        all_fields = set()
        for record in sample_records:
            all_fields.update(record.keys())
        
        actual_fields = {field: self._infer_type(sample_records, field) for field in all_fields}
        
        # Porovnaj s dokumentáciou
        if not documented_fields:
            warnings.append(f"Schéma pre {schema_name} nie je dokumentovaná")
        else:
            # Skontroluj povinné polia
            documented_required = {k: v for k, v in documented_fields.items() if not k.endswith("(optional)")}
            
            for field in documented_required:
                if field not in actual_fields:
                    errors.append(f"Chýba povinné pole: {field}")
            
            # Skontroluj nečakané polia
            for field in actual_fields:
                if field not in documented_fields:
                    warnings.append(f"Nečakané pole v implementácii: {field} (nie je v dokumentácii)")
        
        is_valid = len(errors) == 0
        
        return SchemaValidationResult(
            file_path=str(file_path),
            is_valid=is_valid,
            errors=errors,
            warnings=warnings,
            actual_fields=actual_fields,
            documented_fields=documented_fields
        )
    
    def _infer_type(self, records: List[Dict], field: str) -> str:
        """Odhadne typ poľa na základe vzoriek."""
        types = set()
        for record in records:
            if field in record:
                value = record[field]
                if isinstance(value, str):
                    types.add("string")
                elif isinstance(value, int):
                    types.add("number")
                elif isinstance(value, float):
                    types.add("number")
                elif isinstance(value, bool):
                    types.add("boolean")
                elif isinstance(value, list):
                    types.add("array")
                elif isinstance(value, dict):
                    types.add("object")
                elif value is None:
                    types.add("null")
        
        if len(types) == 1:
            return list(types)[0]
        elif len(types) > 1:
            return f"union({', '.join(sorted(types))})"
        else:
            return "unknown"
    
    def validate_json_file(self, file_path: Path, schema_name: str) -> SchemaValidationResult:
        """Validuje jeden JSON súbor (nie JSONL)."""
        errors = []
        warnings = []
        actual_fields = {}
        documented_fields = self.DOCUMENTED_SCHEMAS.get(schema_name, {})
        
        if not file_path.exists():
            errors.append(f"Súbor neexistuje: {file_path}")
            return SchemaValidationResult(
                file_path=str(file_path),
                is_valid=False,
                errors=errors,
                warnings=warnings,
                actual_fields={},
                documented_fields=documented_fields
            )
        
        try:
            with open(file_path, 'r', encoding='utf-8') as f:
                data = json.load(f)
        except json.JSONDecodeError as e:
            errors.append(f"Chybný JSON: {e}")
            return SchemaValidationResult(
                file_path=str(file_path),
                is_valid=False,
                errors=errors,
                warnings=warnings,
                actual_fields={},
                documented_fields=documented_fields
            )
        except Exception as e:
            errors.append(f"Chyba pri čítaní súboru: {e}")
            return SchemaValidationResult(
                file_path=str(file_path),
                is_valid=False,
                errors=errors,
                warnings=warnings,
                actual_fields={},
                documented_fields=documented_fields
            )
        
        # Analyzuj polia v JSON objekte
        def extract_fields(obj, prefix=""):
            """Rekurzívne extrahuje polia z JSON objektu."""
            fields = {}
            if isinstance(obj, dict):
                for key, value in obj.items():
                    field_name = f"{prefix}.{key}" if prefix else key
                    field_type = self._infer_type([{"value": value}], "value")
                    fields[field_name] = field_type
                    if isinstance(value, dict):
                        fields.update(extract_fields(value, field_name))
            return fields
        
        actual_fields = extract_fields(data)
        
        # Kontrola chýbajúcich dokumentovaných polí
        for doc_field in documented_fields.keys():
            if doc_field not in actual_fields:
                warnings.append(f"Pole '{doc_field}' je dokumentované, ale nie je v súbore")
        
        is_valid = len(errors) == 0
        
        return SchemaValidationResult(
            file_path=str(file_path),
            is_valid=is_valid,
            errors=errors,
            warnings=warnings,
            actual_fields=actual_fields,
            documented_fields=documented_fields
        )
    
    def validate_all(self) -> List[SchemaValidationResult]:
        """Validuje všetky JSON/JSONL súbory v systéme."""
        files_to_validate = [
            ("development/data/prompts_log.jsonl", "prompts_log.jsonl"),
            ("development/data/xp_history.jsonl", "xp_history.jsonl"),
            ("development/logs/XVADUR_LOG.jsonl", "XVADUR_LOG.jsonl"),
            ("development/data/conversations.jsonl", "conversations.jsonl"),
            ("development/sessions/save_games/SAVE_GAME_LATEST.json", "SAVE_GAME_LATEST.json"),
            ("development/logs/XVADUR_XP.json", "XVADUR_XP.json"),
        ]
        
        results = []
        for file_path_str, schema_name in files_to_validate:
            file_path = self.workspace_root / file_path_str
            # JSON súbory validovať inak ako JSONL
            if schema_name.endswith('.json') and not schema_name.endswith('.jsonl'):
                result = self.validate_json_file(file_path, schema_name)
            else:
                result = self.validate_file(file_path, schema_name)
            results.append(result)
        
        self.results = results
        return results
    
    def print_report(self):
        """Vytlačí report validácie."""
        print("=" * 80)
        print("📋 VALIDÁCIA JSON SCHÉM - XVADUR SYSTÉM")
        print("=" * 80)
        print()
        
        total_files = len(self.results)
        valid_files = sum(1 for r in self.results if r.is_valid)
        files_with_errors = sum(1 for r in self.results if r.errors)
        files_with_warnings = sum(1 for r in self.results if r.warnings)
        
        print(f"📊 Prehľad:")
        print(f"   Celkom súborov: {total_files}")
        print(f"   ✅ Platné: {valid_files}")
        print(f"   ❌ S chybami: {files_with_errors}")
        print(f"   ⚠️  S varovaniami: {files_with_warnings}")
        print()
        
        for result in self.results:
            file_name = Path(result.file_path).name
            status = "✅" if result.is_valid else "❌"
            
            print(f"{status} {file_name}")
            print(f"   Cesta: {result.file_path}")
            
            if result.errors:
                print(f"   ❌ Chyby ({len(result.errors)}):")
                for error in result.errors:
                    print(f"      - {error}")
            
            if result.warnings:
                print(f"   ⚠️  Varovania ({len(result.warnings)}):")
                for warning in result.warnings:
                    print(f"      - {warning}")
            
            if result.actual_fields:
                print(f"   📋 Skutočné polia ({len(result.actual_fields)}):")
                for field, field_type in sorted(result.actual_fields.items()):
                    doc_type = result.documented_fields.get(field, "❓ nie je v dokumentácii")
                    marker = "✅" if field in result.documented_fields else "⚠️"
                    print(f"      {marker} {field}: {field_type} (dokumentované: {doc_type})")
            
            print()
        
        print("=" * 80)
        
        # Odporúčania
        print("\n💡 Odporúčania:")
        
        # Kontrola konverzácií
        conv_result = next((r for r in self.results if "conversations.jsonl" in r.file_path), None)
        if conv_result and conv_result.actual_fields:
            if "user_prompt" in conv_result.actual_fields and "user" in conv_result.documented_fields:
                print("   ⚠️  conversations.jsonl používa 'user_prompt' namiesto 'user'")
                print("      Potrebné: Aktualizovať dokumentáciu alebo implementáciu")
        
        # Kontrola XP histórie
        xp_result = next((r for r in self.results if "xp_history.jsonl" in r.file_path), None)
        if xp_result and xp_result.actual_fields:
            if "next_level_xp" in xp_result.actual_fields and "next_level_xp" not in xp_result.documented_fields:
                print("   ⚠️  xp_history.jsonl obsahuje 'next_level_xp' a 'xp_needed'")
                print("      Potrebné: Aktualizovať dokumentáciu")
        
        print()


def main():
    """Hlavná funkcia."""
    validator = SchemaValidator(workspace_root)
    results = validator.validate_all()
    validator.print_report()
    
    # Exit code: 0 ak všetko OK, 1 ak sú chyby
    has_errors = any(r.errors for r in results)
    sys.exit(1 if has_errors else 0)


if __name__ == "__main__":
    main()

