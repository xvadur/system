# Cursor Rules

Tento adresár obsahuje projektovo-špecifické pravidlá pre Cursor AI.

## Čo sú Cursor Rules?

Cursor Rules sú pravidlá v **MDC formáte** (Markdown Cursor), ktoré definujú, ako má Cursor AI generovať kód v tomto projekte. Odlišujú sa od `.cursorrules` (globálny systémový prompt) tým, že sú **projektovo-špecifické** a zamerané na **kódové konvencie**.

### MDC Formát

Každé pravidlo má **frontmatter** (YAML metadata) na začiatku:

```markdown
---
description: Popis pravidla
globs: ["**/*.tsx", "**/*.ts"]  # Glob patterns pre súbory
alwaysApply: false  # true = aplikovať vždy, false = len keď glob match
---

# Názov Pravidla
Obsah pravidla...
```

- **`description`:** Popis, čo pravidlo robí
- **`globs`:** Glob patterns pre súbory, na ktoré sa pravidlo vzťahuje (napr. `["**/*.tsx"]` pre React komponenty)
- **`alwaysApply`:** `true` = aplikovať vždy (napr. meta-pravidlá), `false` = len keď glob pattern matchuje súbor

## Štruktúra

```
cursor/rules/
├── 00-cursor-rules-rule.mdc      # Meta-pravidlo: Ako fungujú pravidlá
├── 01-self-improve.mdc            # Self-improve mechanizmus
├── 02-directory-structure.mdc    # Štruktúra projektu
├── 03-tech-stack.mdc              # Tech stack a best practices
└── README.md                     # Tento súbor
```

## Ako to Funguje?

1. **Načítanie:** Cursor automaticky načíta všetky `.mdc` súbory z `cursor/rules/`
2. **Aplikácia:** Pravidlá sa aplikujú na všetky generované zmeny v kóde
3. **Poradie:** Číslovanie súborov (`00-`, `01-`, ...) určuje prioritu

## Generovanie Nových Pravidiel

### Automaticky (Self-Improve)
- Cursor automaticky generuje nové pravidlá z opakujúcich sa chýb
- Pozri `01-self-improve.md` pre detaily

### Manuálne
- Použiť `/Generate Cursor Rules` command v Cursor
- Alebo vytvoriť nový `.mdc` súbor v `cursor/rules/` (vždy používať `.mdc` extension, nie `.md`)

## Rozdiel medzi `.cursorrules` a `cursor/rules/`

- **`.cursorrules`:** Globálny systémový prompt (osobný profil, workflow, filozofia)
- **`cursor/rules/`:** Projektovo-špecifické pravidlá (kódové konvencie, tech stack, štruktúra)

## Príklady Použitia

### Príklad 1: Generovanie React Komponentu
Cursor použije:
- `03-tech-stack.md` → Funkcionálne komponenty, TypeScript, TailwindCSS (globs: `["**/*.tsx"]`)
- `02-directory-structure.md` → Umiestnenie v `xvadur_agent/xvadur_console/components/`

### Príklad 2: Generovanie Python Funkcie
Cursor použije:
- `03-tech-stack.md` → Type hints, error handling, docstrings
- `02-directory-structure.md` → Umiestnenie v správnom adresári

## Poznámka

Tento systém je inšpirovaný:
- Video: https://www.youtube.com/watch?v=FpJ48a5S5lU
- Príklad implementácie: https://github.com/danmindru/page-ui/tree/d49ce6aaf8a92fa3d90ac20848b757a2aff8ea0e/.cursor/rules

## Dôležité

- **Vždy používať `.mdc` extension** (nie `.md`)
- **Naming:** kebab-case pre názvy súborov (napr. `tech-stack.mdc`)
- **Frontmatter:** Vždy obsahovať `description`, `globs`, `alwaysApply`

