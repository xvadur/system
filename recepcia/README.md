# 📞 Recepčná - AI Hlasový Asistent

**Status:** ✅ Funkčná, pripravená na produkciu (s blokátormi)  
**Dátum aktualizácie:** 2025-12-03

---

## 📋 Prehľad

AI recepčná (Rachel) pre zdravotníctvo - hlasový asistent, ktorý odpovedá na prichádzajúce hovory pacientov, najčastejšie kvôli objednaniu na vyšetrenie, predpisaniu liekov, alebo bežnej otázke.

**Hlavná úloha:** Keď pacient zavolá na ambulanciu, ako prvé počuje:
> "Dobrý deň, dovolali ste sa do ambulancie detského lekára, ja som virtuálna recepčná Rachel, ako vám môžem pomôcť?"

---

## 📊 Aktuálny Status

### ✅ Čo je Hotové
- **Prompt v2.5** - Kompletný, funkčný
- **5 nástrojov** - check_availability, get_events, book, cancel, reschedule
- **End-to-end test úspešný** - Twilio + ElevenLabs + n8n + Google Calendar
- **Rezervačný systém funguje** - Integrácia kompletná
- **30.11 - Call s Vladom** - Ukázaná recepčná, fungovala ako mala
- **1.12 - Cvičenie s Vladom** - Skamaratili sa, Vlado považuje Adama za parťáka

### ⏳ Čo Treba
- **Konverzačná logika** - Upraviť vetvenia konverzácie
- **Zber údajov o hovoroch do databázy** - Implementovať tracking
- **Knowledge Base** - FAQ, kontakty, typy návštev
- **Email Notifikácie** - Potvrdenie rezervácie, pripomienka

### 🔴 Blokátory
- **SIP Trunk** - Vlado rieši cez O2 (slovenské čísla)
- **ElevenLabs Enterprise** - Potrebné (rok dopredu, locknut)

---

## 📁 Dokumenty v Tento Foldri

1. **Recepcia.md** - Hlavný dokument o projekte, koncept, workflow
2. **Recepcia_Prompt.md** - Pôvodný prompt
3. **Recepcia_Prompt_v2.0.md** - Kompletný prompt v2.5 (aktuálna verzia)
4. **Recepcia_Tools_JSON.md** - JSON definície všetkých 5 nástrojov
5. **Recepcia_Status_Summary.md** - Status summary (Production Ready)
6. **Recepcia_Session_Close.md** - Session close z 1.12 - Call s Vladom

---

## 🎯 Kľúčové Informácie

### Vzťah s Vladom
- **30.11** - Volali spolu, ukázal mu recepčnú, ktorá fungovala ako mala
- **1.12** - Boli spolu cvičiť a skamaratili sa
- **Vlado považuje Adama za parťáka** - "spadol z neba" a naplnil presne tú funkciu, ktorú si mu v hlave pridelil ešte pred spoznaním

### Technická Architektúra
- **1 n8n backend** - spoločný pre všetkých
- **Každá ambulancia:**
  - 1 SIP Trunk (telefónne číslo)
  - 1 Agent (ElevenLabs)
  - 1 číslo = 1 agent

### Skalovateľnosť
- **Modulárna architektúra** - Keď je základňa solidná, dá sa skalovať na stovky ambulancií
- **Príklad: 20 Fíriem**
  - 20 agentov (20 čísel)
  - 1 n8n backend (spoločný)
  - 20 SIP Trunkov (každá ambulancia má svoje číslo)

---

## 🚀 Next Steps

1. **Upraviť konverzačnú logiku** - Logické vetvenia konverzácie
2. **Implementovať zber údajov o hovoroch do databázy** - Tracking hovorov
3. **Variables setup** - Nastavenie premenných
4. **Knowledge Base** - FAQ, kontakty, typy návštev
5. **Email Notifikácie** - Potvrdenie rezervácie, pripomienka

---

## 📝 Poznámky

- Recepčná je v zmysle promptu hotová a funkčná
- Blokátor recepčnej je uvoľnený - teraz sa pracuje na vylepšeniach
- Vzťah s Vladom sa posunul z "blokátora" na "parťáka" - významný psychologický posun

---

**Súvisiace dokumenty:**
- `xvadur/save_games/SAVE_GAME_LATEST.md` - Aktuálny status questu
- `xvadur/logs/XVADUR_LOG.md` - Chronologický log
- `xvadur/data/sessions/Utorok_2025-12-02.md` - Session dokument

