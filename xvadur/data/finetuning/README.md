# OpenAI Fine-tuning Dataset - Status

**Dátum vytvorenia:** 2025-12-04  
**Status:** ✅ Dataset pripravený, ⏸️ Pozastavené (budget)

---

## ✅ Čo je Hotové

### 1. Dataset Pripravený
- **Súbor:** `openai_finetuning_dataset.jsonl`
- **Veľkosť:** 15.42 MB
- **Príklady:** 1,822 konverzačných párov
- **Formát:** OpenAI fine-tuning formát (messages array)
- **Validácia:** ✅ Všetky príklady sú platné

### 2. Štatistiky
- **Celkový počet príkladov:** 1,822
- **Platných príkladov:** 1,822 (100%)
- **Neplatných príkladov:** 0
- **Priemerná dĺžka user promptu:** 3,626 znakov
- **Priemerná dĺžka AI odpovede:** 4,572 znakov
- **Odhadovaný počet tokenov:** ~3.7M tokenov

### 3. Skript
- **Súbor:** `scripts/prepare_openai_finetuning.py`
- **Funkcionalita:** Konverzia conversation pairs → OpenAI formát
- **Validácia:** Automatická validácia podľa OpenAI požiadaviek

---

## ⏸️ Pozastavené

**Dôvod:** Budget obmedzenia (AutoTrain je platený, OpenAI má kvótu)

**Čo zostáva:**
- Upload datasetu do finetuning platformy
- Spustenie tréningu
- Testovanie finetuned modelu

---

## 📋 Možnosti Neskôr (Keď Bude Budget)

### 1. OpenAI Fine-tuning
- **Náklady:** ~$10-50 (tréning) + ~$0.03/1K tokenov (inference)
- **Výhody:** Najjednoduchšie, Playground UI
- **Nevýhody:** Drahšie, kvóty

### 2. Hugging Face AutoTrain
- **Náklady:** ~$0.50-2/hodinu tréningu
- **Výhody:** Lacnejšie, open-source modely
- **Nevýhody:** Stále platené

### 3. Together AI
- **Náklady:** ~$0.30-0.50/hodinu tréningu
- **Výhody:** Lacnejšie ako OpenAI, podobné API
- **Nevýhody:** Stále platené

### 4. Lokálne Riešenie (Ollama + LoRA)
- **Náklady:** Zadarmo (ak máš GPU)
- **Výhody:** Plná kontrola, žiadne limity
- **Nevýhody:** Potrebuješ GPU, zložitejšie setup

---

## 🚀 Ďalšie Kroky (Keď Bude Budget)

1. **Vybrať platformu** (OpenAI, Hugging Face, Together AI, alebo lokálne)
2. **Upload datasetu** (`openai_finetuning_dataset.jsonl`)
3. **Spustiť tréning** (1-3 hodiny)
4. **Testovať finetuned model**
5. **Integrovať do produkcie** (AI recepčná, osobné AI)

---

## 📁 Súbory

- `openai_finetuning_dataset.jsonl` - Pripravený dataset (15.42 MB, 1,822 príkladov)
- `finetuning_stats.json` - Štatistiky datasetu
- `scripts/prepare_openai_finetuning.py` - Skript na konverziu

---

## 💡 Alternatívy (Zatiaľ Bez Finetuningu)

Namiesto finetuningu môžeš použiť:

1. **RAG systém** - Už máš funkčný RAG systém, ktorý môže poskytovať kontext
2. **System prompts** - Vylepšiť system prompts s tvojím kontextom
3. **Few-shot learning** - Pridať príklady do promptov
4. **Rozšírenie RAG** - Pridať AI odpovede do RAG indexu (už plánované)

---

**Vytvorené:** 2025-12-04  
**Status:** ⏸️ Pozastavené (budget)  
**Pripravené na:** Finetuning neskôr, keď bude budget


