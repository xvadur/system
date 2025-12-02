# 🗺️ Knowledge Graph Guide: Ako vizualizovať svoje dáta v Obsidiane

## 📋 Prehľad

Tento guide ti ukáže, ako vytvoriť knowledge graf a vizualizácie z tvojich dát (prompty, chronológie, mapy).

---

## 🎯 Možnosti Vizualizácie

### 1. **Obsidian Graph View** (Už máš nastavený)
- **Čo to je:** Built-in graf, ktorý automaticky zobrazuje linky medzi poznámkami
- **Ako používať:**
  - Otvor Graph View (Ctrl+G / Cmd+G)
  - Používaj `[[linky]]` v poznámkach
  - Farba podľa cesty (už máš nastavené v `.obsidian/graph.json`)

**Tip:** Pridaj viac `[[linkov]]` do svojich chronológií a máp!

---

### 2. **Obsidian Canvas** (Už máš plugin)
- **Čo to je:** Vizuálny workspace, kde môžeš umiestniť poznámky a kresliť spojenia
- **Ako používať:**
  - Vytvor nový Canvas (`Ctrl+N` → "Canvas")
  - Drag & drop poznámky
  - Kresli spojenia medzi nimi

**Automatizácia:** Skript `generate_knowledge_graph.py` môže vygenerovať Canvas JSON!

---

### 3. **Mermaid Diagrams** (Built-in v Obsidian)
- **Čo to je:** Text-based diagramy (flowcharts, grafy, atď.)
- **Ako používať:**
  ```markdown
  ```mermaid
  graph TD
      A[AI] --> B[Recepčná]
      A --> C[n8n]
      B --> D[Vlado]
  ```
  ```

**Automatizácia:** Skript generuje Mermaid diagramy z tvojich dát!

---

### 4. **Dataview Plugin** (Už máš nainštalovaný)
- **Čo to je:** Query language pre Obsidian poznámky
- **Ako používať:**
  ```markdown
  ```dataview
  TABLE file.ctime as "Dátum"
  FROM "Atlas/Maps"
  WHERE contains(file.name, "CHRONOLOGY")
  SORT file.ctime DESC
  ```
  ```

**Príklady:**
- Zobraziť všetky chronológie
- Nájsť poznámky s konkrétnymi tagmi
- Vytvoriť časovú os

---

### 5. **Smart Connections Plugin** (Už máš nainštalovaný)
- **Čo to je:** AI-powered automatické nájdenie súvislostí
- **Ako používať:**
  - Plugin automaticky nájde súvislosti medzi poznámkami
  - Zobrazuje "related notes" v sidebar

---

## 🛠️ Automatizácia: `generate_knowledge_graph.py`

### Čo robí:
1. **Extrahuje entity** z promptov (ľudia, miesta, projekty, koncepty)
2. **Vytvorí graf** spojení medzi entitami
3. **Generuje výstupy:**
   - Obsidian Canvas JSON
   - Mermaid diagramy
   - Obsidian poznámky s automatickými linkami

### Použitie:

```bash
# Generovať všetko
python3 xvadur_brave/scripts/generate_knowledge_graph.py --all

# Len Canvas
python3 xvadur_brave/scripts/generate_knowledge_graph.py --canvas

# Len Mermaid
python3 xvadur_brave/scripts/generate_knowledge_graph.py --mermaid

# Len Obsidian poznámky
python3 xvadur_brave/scripts/generate_knowledge_graph.py --notes
```

### Výstupy:
- `xvadur_obsidian/Atlas/KnowledgeGraph/knowledge_graph.canvas` - Canvas súbor
- `xvadur_obsidian/Atlas/KnowledgeGraph/knowledge_graph.mmd` - Mermaid diagram
- `xvadur_obsidian/Atlas/KnowledgeGraph/Entities/` - Poznámky s entitami

---

## 📊 Príklady Vizualizácií

### 1. Chronologická Mapa (Už máš)
- `AI_CHRONOLOGY.md` - Všetko o AI
- `NEMOCNICA_CHRONOLOGY.md` - Všetko o nemocnici
- `18_27_ROKOV_CHRONOLOGY.md` - Tvoja cesta 18-27

### 2. Tematická Mapa (Už máš)
- `RECEPCIA_VLADO_CHRONOLOGY.md` - Recepčná + Vlado

### 3. Entity Graf (Nové)
- Automaticky extrahované entity z promptov
- Spojenia medzi entitami

---

## 🎨 Vylepšenia

### 1. **Pridaj viac linkov do chronológií**
V existujúcich chronológiách môžeš pridať:
```markdown
## 📆 2025-09-15

**12:31** | Výskyty: vlado (1x)

> ...text o [[Vlado]] a [[AI recepčná]]...
```

### 2. **Vytvor index poznámok**
```markdown
# 🗺️ Mapa Môjho Života

## Chronológie
- [[AI_CHRONOLOGY]]
- [[NEMOCNICA_CHRONOLOGY]]
- [[18_27_ROKOV_CHRONOLOGY]]

## Projekty
- [[AI recepčná]]
- [[n8n workflows]]
```

### 3. **Použi Dataview pre automatické zoznamy**
```markdown
```dataview
TABLE file.ctime as "Dátum"
FROM "Atlas/Maps"
WHERE contains(file.name, "CHRONOLOGY")
SORT file.ctime DESC
```


---

## 🚀 Ďalšie Možnosti

### 1. **Externé Nástroje**
- **Gephi** - Pokročilá vizualizácia grafov
- **Cytoscape** - Network analysis
- **D3.js** - Custom vizualizácie

### 2. **Obsidian Pluginy**
- **Juggl** - Pokročilý graf view
- **Graph Analysis** - Analýza grafu
- **Templater** - Automatizácia poznámok

### 3. **RAG + Knowledge Graph**
- Kombinuj RAG vyhľadávanie s knowledge grafom
- Nájdi súvislosti medzi entitami
- Vytvor tematické mapy

---

## 📝 Checklist

- [ ] Spusti `generate_knowledge_graph.py --all`
- [ ] Otvor Canvas v Obsidiane
- [ ] Pridaj `[[linky]]` do chronológií
- [ ] Vytvor index poznámok
- [ ] Experimentuj s Dataview queries
- [ ] Použi Smart Connections pre AI-powered súvislosti

---

## 💡 Tipy

1. **Začni jednoducho:** Pridaj `[[linky]]` do existujúcich chronológií
2. **Automatizuj:** Použi skripty na generovanie grafov
3. **Experimentuj:** Skús rôzne pluginy a vizualizácie
4. **Iteruj:** Knowledge graf sa vyvíja s tvojimi dátami

---

**Otázky?** Pozri sa na existujúce mapy v `Atlas/Maps/` alebo spusti skript a pozri sa, čo vygeneruje!

