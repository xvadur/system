---
created: 2025-11-30
tags:
  - recepcia
  - tools
  - json
  - function-calling
---
# Recepčná: JSON Definície Nástrojov

## 📚 Súvisiace Dokumenty

- [[Recepcia_Prompt_v2.0]] - Kompletný prompt pre Rachel (v2.2) - *Nástroje sú definované v sekcii "Nástroje (Tools)"*
- [[Transkript]] - Testovacia konverzácia
- [[Recepcia]] - Popis projektu
- [[Recepcia_Prompt_Changelog]] - Dokumentácia zmien
- [[Recepcia_Prompt_Audit]] - Audit promptu

> 💡 **Poznámka:** Tento dokument obsahuje technické JSON definície nástrojov pre function calling. Pre popis použitia a workflows pozri [[Recepcia_Prompt_v2.0]].

---

## 🛠️ Nástroje (Tools) - JSON Definície

Tieto JSON definície sú pripravené pre ElevenLabs/Elvi function calling. Všetky nástroje sú navrhnuté podľa promptu v [[Recepcia_Prompt_v2.0]].

---

### 1. `check_availability` - Kontrola dostupnosti termínu

**Popis:** Over dostupnosť konkrétneho termínu pred rezerváciou alebo zmenou termínu.

```json
{
  "type": "webhook",
  "name": "check_availability",
  "description": "Použi tento nástroj, keď potrebuješ overiť dostupnosť termínov. Zadaj start_iso ako začiatok hľadaného intervalu a end_iso ako koniec. Trvanie vyšetrenia je 30 min",
  "disable_interruptions": false,
  "force_pre_tool_speech": "auto",
  "assignments": [],
  "tool_call_sound": null,
  "tool_call_sound_behavior": "auto",
  "execution_mode": "immediate",
  "api_schema": {
    "url": "https://xvadur.app.n8n.cloud/webhook/check_availability",
    "method": "POST",
    "path_params_schema": [],
    "query_params_schema": [],
    "request_body_schema": {
      "id": "body",
      "type": "object",
      "description": "Tento nástroj overuje dostupnosť 30‑minútového termínu pre zadaný dátum a čas. Z transcriptu konverzácie extrahuj presný alebo relatívny čas pacienta a normalizuj ho do ISO 8601 s lokálnym offsetom Europe/Bratislava, bez ‘Z’. Vygeneruj dvojicu parametrov:\n\n- start_iso: začiatok hľadaného intervalu\n- end_iso: koniec hľadaného intervalu (start_iso + 30 min)\n\nPravidlá extrakcie a normalizácie:\n- Presný čas: napr. “21. novembra o 15:30” → start_iso = daný čas, end_iso = +30 minút.\n- Relatívny čas: napr. “zajtra o 10:00”, “v pondelok ráno”. Rozviaž podľa {{system__time_utc}} do Europe/Bratislava. ‘ráno’ = 09:00, ‘obed’ = 12:00, ‘poobede’ = 15:00, ‘večer’ = 18:00.\n- Ak je uvedený len dátum bez času, vyžiadaj konkrétny čas; nástroj nevolaj, kým čas nie je známy.\n- Vždy používaj ISO 8601 s lokálnym offsetom (+01:00 v zime, +02:00 v lete), napr. 2025-11-21T15:30:00+01:00. Nepoužívaj ‘Z’.\n\nKonverzačná logika:\n- Pýtaj sa jednu informáciu naraz. Najprv vyžiadaj preferovaný dátum/čas.\n- Po extrakcii zopakuj dátum a čas pomaly na potvrdenie.\n- Až po potvrdení vytvor start_iso/end_iso a zavolaj nástroj.\n\nVýstupná interpretácia:\n- Nástroj vracia informáciu o dostupnosti daného 30‑min slotu v danom intervale. Ak nedostupné, ponúkni 2–3 najbližšie voľné alternatívy v rovnakom dni alebo nasledujúcich dňoch, komunikované v Europe/Bratislava.\n\nPríklady:\n- “Zajtra 15:30” → start_iso: 2025-11-20T15:30:00+01:00, end_iso: 2025-11-20T16:00:00+01:00\n- “V pondelok ráno” → start_iso: 2025-11-24T09:00:00+01:00, end_iso: 2025-11-24T09:30:00+01:00\n- “21.11. o 10:00” → start_iso: 2025-11-21T10:00:00+01:00, end_iso: 2025-11-21T10:30:00+01:00",
      "properties": [
        {
          "id": "start_iso",
          "type": "string",
          "value_type": "llm_prompt",
          "description": "Začiatok stretnutia vo formáte ISO 8601 s lokálnym offsetom (+01:00 v zime, +02:00 v lete), napr. 2025-11-21T15:30:00+01:00. Nepoužívaj 'Z'.",
          "dynamic_variable": "",
          "constant_value": "",
          "enum": null,
          "is_system_provided": false,
          "required": true
        },
        {
          "id": "end_iso",
          "type": "string",
          "value_type": "llm_prompt",
          "description": "Koncový čas vo formáte ISO 8601 s lokálnym offsetom (+01:00 v zime, +02:00 v lete), napr. 2025-11-21T16:00:00+01:00. Nepoužívaj 'Z'.",
          "dynamic_variable": "",
          "constant_value": "",
          "enum": null,
          "is_system_provided": false,
          "required": true
        }
      ],
      "required": true,
      "value_type": "llm_prompt"
    },
    "request_headers": [
      {
        "type": "value",
        "name": "Content-Type",
        "value": "application/json"
      }
    ],
    "auth_connection": null
  },
  "response_timeout_secs": 20,
  "dynamic_variables": {
    "dynamic_variable_placeholders": {}
  }
}
```

**Očakávaná odpoveď (z n8n webhooku):**
```json
{
  "available": true,
  "message": "Termín je voľný"
}
```
alebo (ak je obsadený):
```json
{
  "available": false,
  "message": "Termín je obsadený",
  "alternative_slots": [
    {
      "start": "2025-12-03T09:30:00+01:00",
      "end": "2025-12-03T10:00:00+01:00"
    },
    {
      "start": "2025-12-03T10:00:00+01:00",
      "end": "2025-12-03T10:30:00+01:00"
    },
    {
      "start": "2025-12-03T10:30:00+01:00",
      "end": "2025-12-03T11:00:00+01:00"
    }
  ]
}
```

**Použitie:**
- Vždy pred `book` - kontrola dostupnosti pred rezerváciou
- Vždy pred `reschedule` - kontrola dostupnosti nového termínu

---

### 2. `get_events` - Vyhľadanie existujúcich rezervácií

**Popis:** Vyhľadaj existujúce rezervácie podľa dátumu. Používa sa len na získanie event_id pre reschedule a cancel.

```json
{
  "type": "webhook",
  "name": "get_events",
  "description": "pouzi nastroj ked potrebujes zistit dostupnost terminov alebo event id existujuceho terminu",
  "disable_interruptions": false,
  "force_pre_tool_speech": "auto",
  "assignments": [],
  "tool_call_sound": null,
  "tool_call_sound_behavior": "auto",
  "execution_mode": "immediate",
  "api_schema": {
    "url": "https://xvadur.app.n8n.cloud/webhook/get_events",
    "method": "POST",
    "path_params_schema": [],
    "query_params_schema": [],
    "request_body_schema": {
      "id": "body",
      "type": "object",
      "description": "Z transcriptu extrahuj údaje na vyhľadanie udalostí pacienta v Google Kalendári. Všetky výstupné časy normalizuj do ISO 8601 s lokálnym offsetom Europe/Bratislava (+01:00 v zime, +02:00 v lete), nepoužívaj ‘Z’. \nVytvor:\n- window_after: začiatok okna vyhľadávania; ak nie sú indície, nastav dnes 00:00.\n- window_before: koniec okna; ak nie sú indície, nastav dnes + 7 dní \n- patient_full_name: celé meno pacienta na filtrovanie.\nAk povie relatívne („v pondelok o 10:00“, „minulý týždeň ráno“), rozrieš podľa systémového UTC času → Europe/Bratislava.\n",
      "properties": [
        {
          "id": "window_before",
          "type": "string",
          "value_type": "llm_prompt",
          "description": "Koniec okna vyhľadávania v ISO 8601 s offsetom Europe/Bratislava;  pri relatívnych frázach vypočítaj.",
          "dynamic_variable": "",
          "constant_value": "",
          "enum": null,
          "is_system_provided": false,
          "required": false
        },
        {
          "id": "window_after",
          "type": "string",
          "value_type": "llm_prompt",
          "description": "Začiatok okna vyhľadávania v ISO 8601 s offsetom Europe/Bratislava; pri relatívnych frázach vypočítaj.",
          "dynamic_variable": "",
          "constant_value": "",
          "enum": null,
          "is_system_provided": false,
          "required": false
        }
      ],
      "required": false,
      "value_type": "llm_prompt"
    },
    "request_headers": [
      {
        "type": "value",
        "name": "Content-Type",
        "value": "application/json"
      }
    ],
    "auth_connection": null
  },
  "response_timeout_secs": 20,
  "dynamic_variables": {
    "dynamic_variable_placeholders": {}
  }
}
```

**Očakávaná odpoveď (z n8n webhooku):**
```json
{
  "events": [
    {
      "event_id": "evt_123456",
      "time_start": "2025-12-03T09:00:00+01:00",
      "time_end": "2025-12-03T09:30:00+01:00",
      "summary": "Peter Horváth",
      "description": "Pretrvávajúci kašeľ, 0902 456 789, 03.09.1984, horvath.peter@gmail.com"
    }
  ]
}
```
alebo (ak nie sú žiadne eventy):
```json
{
  "events": []
}
```

**Použitie:**
- Pri zmene termínu - na vyhľadanie event_id pôvodného vyšetrenia
- Pri zrušení termínu - na vyhľadanie event_id termínu na zrušenie

---

### 3. `book` - Rezervácia nového termínu

**Popis:** Vytvor novú rezerváciu termínu. Používa sa až po získaní všetkých potrebných údajov a po overení dostupnosti pomocou `check_availability`.

```json
{
  "type": "webhook",
  "name": "book",
  "description": "Rezervácia termínu: najprv získaj preferovaný dátum/čas od pacienta, rozviaž relatívne výrazy podľa {{system__time_utc}} do Europe/Bratislava (+01:00/+02:00), normalizuj na ISO 8601 s lokálnym offsetom, nepoužívaj 'Z'. Ak je zadaný len dátum, vyžiadaj čas. Trvanie vyšetrenia je 30 min (end_time = start_time + 30 min).",
  "disable_interruptions": false,
  "force_pre_tool_speech": "auto",
  "assignments": [],
  "tool_call_sound": null,
  "tool_call_sound_behavior": "auto",
  "execution_mode": "immediate",
  "api_schema": {
    "url": "https://xvadur.app.n8n.cloud/webhook/book",
    "method": "POST",
    "path_params_schema": [],
    "query_params_schema": [],
    "request_body_schema": {
      "id": "body",
      "type": "object",
      "description": "Z transcriptu extrahuj start_time (ISO 8601 s offsetom Europe/Bratislava), vypočítaj end_time = start_time + 30 min, a zozbieraj patient_full_name, date_of_birth (DD.MM.RRRR), email, phone (voliteľné), visit_reason (enum). Pri relatívnych výrazoch použij {{system__time_utc}} → Europe/Bratislava; ",
      "properties": [
        {
          "id": "visit_reason",
          "type": "string",
          "value_type": "llm_prompt",
          "description": "Dôvod návštevy; povolené hodnoty: ‘preventívna prehliadka’ | ‘PN’ | ‘odbery’.",
          "dynamic_variable": "",
          "constant_value": "",
          "enum": [
            "preventívna prehliadka",
            "PN",
            "odbery"
          ],
          "is_system_provided": false,
          "required": true
        },
        {
          "id": "start_time",
          "type": "string",
          "value_type": "llm_prompt",
          "description": "Presný dátum a čas začiatku v ISO 8601 s lokálnym offsetom Europe/Bratislava (napr. 2025-11-08T15:30:00+01:00). Rozšír relatívne výrazy (‘zajtra’, ‘budúci pondelok’) podľa {{system__time_utc}}.",
          "dynamic_variable": "",
          "constant_value": "",
          "enum": null,
          "is_system_provided": false,
          "required": true
        },
        {
          "id": "patient_full_name",
          "type": "string",
          "value_type": "llm_prompt",
          "description": "Celé meno a priezvisko pacienta ",
          "dynamic_variable": "",
          "constant_value": "",
          "enum": null,
          "is_system_provided": false,
          "required": true
        },
        {
          "id": "end_time",
          "type": "string",
          "value_type": "llm_prompt",
          "description": "Koniec termínu je vždy start_time + 30 minút, v tom istom ISO 8601 ",
          "dynamic_variable": "",
          "constant_value": "",
          "enum": null,
          "is_system_provided": false,
          "required": true
        },
        {
          "id": "email",
          "type": "string",
          "value_type": "llm_prompt",
          "description": "E‑mailová adresa pacienta ",
          "dynamic_variable": "",
          "constant_value": "",
          "enum": null,
          "is_system_provided": false,
          "required": true
        },
        {
          "id": "date_of_birth",
          "type": "string",
          "value_type": "llm_prompt",
          "description": "Dátum narodenia vo formáte DD.MM.RRRR napr 29.01.1998",
          "dynamic_variable": "",
          "constant_value": "",
          "enum": null,
          "is_system_provided": false,
          "required": true
        },
        {
          "id": "phone",
          "type": "string",
          "value_type": "llm_prompt",
          "description": "Telefónne číslo pacienta (voliteľné, ale odporúčané). Formát: slovenské telefónne číslo (napr. 0902 456 789 alebo +421902456789).",
          "dynamic_variable": "",
          "constant_value": "",
          "enum": null,
          "is_system_provided": false,
          "required": false
        }
      ],
      "required": true,
      "value_type": "llm_prompt"
    },
    "request_headers": [
      {
        "type": "value",
        "name": "Content-Type",
        "value": "application/json"
      }
    ],
    "auth_connection": null
  },
  "response_timeout_secs": 20,
  "dynamic_variables": {
    "dynamic_variable_placeholders": {}
  }
}
```

**Očakávaná odpoveď (z n8n webhooku):**
```json
{
  "success": true,
  "event_id": "evt_123456",
  "message": "Rezervácia úspešne vytvorená",
  "details": {
    "summary": "Peter Horváth",
    "time_start": "2025-12-03T09:00:00+01:00",
    "time_end": "2025-12-03T09:30:00+01:00"
  }
}
```
alebo (pri chybe):
```json
{
  "success": false,
  "error": "Termín je už obsadený",
  "message": "Rezervácia zlyhala"
}
```

**Použitie:**
- Až po získaní všetkých potrebných údajov (meno, dátum narodenia, email, dôvod, telefónne číslo - voliteľné)
- Až po overení dostupnosti pomocou `check_availability`
- Po úspechu vždy prečítať späť pacientovi (over/potvrd)

---

### 4. `cancel` - Zrušenie existujúcej rezervácie

**Popis:** Zruš existujúcu rezerváciu. Event_id musí byť zistené pomocou `get_events` a potvrdené s pacientom.

```json
{
  "type": "webhook",
  "name": "cancel",
  "description": "pouzi tento nástroj ked chceš zrušiť termín rezervácie",
  "disable_interruptions": false,
  "force_pre_tool_speech": "auto",
  "assignments": [],
  "tool_call_sound": null,
  "tool_call_sound_behavior": "auto",
  "execution_mode": "immediate",
  "api_schema": {
    "url": "https://xvadur.app.n8n.cloud/webhook/cancel",
    "method": "POST",
    "path_params_schema": [],
    "query_params_schema": [],
    "request_body_schema": {
      "id": "body",
      "type": "object",
      "description": "pacient nadiktoval voje meno a priezvysko, datum a cas rezervacia, vdaka comu zi zistila event id rezervacie ktoru chce zrusit ",
      "properties": [
        {
          "id": "eventID",
          "type": "string",
          "value_type": "llm_prompt",
          "description": "identifikacne cislo eventu, ktore si zistila podla mena a terminu vysetrenia ",
          "dynamic_variable": "",
          "constant_value": "",
          "enum": null,
          "is_system_provided": false,
          "required": true
        }
      ],
      "required": true,
      "value_type": "llm_prompt"
    },
    "request_headers": [
      {
        "type": "value",
        "name": "Content-Type",
        "value": "application/json"
      }
    ],
    "auth_connection": null
  },
  "response_timeout_secs": 20,
  "dynamic_variables": {
    "dynamic_variable_placeholders": {}
  }
}
```

**Očakávaná odpoveď (z n8n webhooku):**
```json
{
  "success": true,
  "message": "Rezervácia úspešne zrušená",
  "cancelled_event": {
    "event_id": "evt_123456",
    "summary": "Peter Horváth",
    "time_start": "2025-12-03T09:00:00+01:00",
    "time_end": "2025-12-03T09:30:00+01:00"
  }
}
```
alebo (pri chybe):
```json
{
  "success": false,
  "error": "Event nebol nájdený",
  "message": "Zrušenie zlyhalo"
}
```

**Použitie:**
- Až po potvrdení úmyslu zrušiť s pacientom
- Až po kontrole, že ide o správny event (pomocou `get_events`)
- Po úspechu vždy potvrdiť pacientovi

---

### 5. `reschedule` - Zmena rezervácie na nový termín

**Popis:** Zmeň existujúcu rezerváciu na nový termín. Zachovávaj pôvodné údaje pacienta, mení sa len dátum a čas.

```json
{
  "type": "webhook",
  "name": "reschedule",
  "description": "pouzi nastroj ked che pacient zmenit termin vysetrenia \nvsetky casove udaje odosielaj vo formáte ISO \nkazde vysetrenie ma trvanie 30 min.\ntime zone: bratislava/europe (+1/+2)",
  "disable_interruptions": false,
  "force_pre_tool_speech": "auto",
  "assignments": [],
  "tool_call_sound": null,
  "tool_call_sound_behavior": "auto",
  "execution_mode": "immediate",
  "api_schema": {
    "url": "https://xvadur.app.n8n.cloud/webhook/reschedule",
    "method": "POST",
    "path_params_schema": [],
    "query_params_schema": [],
    "request_body_schema": {
      "id": "body",
      "type": "object",
      "description": "z transkriptu extrahuj udalej potrebne pre zmenu rezervacie terminu. \nevent id - pred tym nez pouzijes tento nastroj si pouzila nastroj get_events, pomocou ktoreho si zistila event id \ncasove udaje odosielaj v ISO fromáte, trvanei udalsoti je 30 min., time zone: bratislava/europe",
      "properties": [
        {
          "id": "novy_preferovany_cas",
          "type": "string",
          "value_type": "llm_prompt",
          "description": "novy datum a cas ktory pacient chce rezerovavat.\nodosielaj v iso formáte",
          "dynamic_variable": "",
          "constant_value": "",
          "enum": null,
          "is_system_provided": false,
          "required": true
        },
        {
          "id": "dovod",
          "type": "string",
          "value_type": "llm_prompt",
          "description": "dovod, pre ktory chce pacient navstivit ambulanciu",
          "dynamic_variable": "",
          "constant_value": "",
          "enum": null,
          "is_system_provided": false,
          "required": true
        },
        {
          "id": "after",
          "type": "string",
          "value_type": "llm_prompt",
          "description": "Popíš presný čas konca vyšetrenia ako začiatok + 30 minút. Vypočítaj z hodnoty „before“ a uveď v ISO 8601 s lokálnym offsetom (nepoužívaj ‘Z’). Príklady k vyššie uvedeným:\n\n- before 2025-11-20T07:00:00+01:00 → after 2025-11-20T07:30:00+01:00\n\n- before 2025-11-21T08:30:00+01:00 → after 2025-11-21T09:00:00+01:00\n\n- before 2025-11-25T14:00:00+01:00 → after 2025-11-25T14:30:00+01:00",
          "dynamic_variable": "",
          "constant_value": "",
          "enum": null,
          "is_system_provided": false,
          "required": true
        },
        {
          "id": "email",
          "type": "string",
          "value_type": "llm_prompt",
          "description": "emailova adresa pacienta ",
          "dynamic_variable": "",
          "constant_value": "",
          "enum": null,
          "is_system_provided": false,
          "required": true
        },
        {
          "id": "before",
          "type": "string",
          "value_type": "llm_prompt",
          "description": "Popíš presný čas začiatku požadovaného termínu. Z textu pacienta extrahuj dátum a čas, rozviaž relatívne výrazy voči system__time_utc, konvertuj do Europe/Bratislava (CET/CEST) a normalizuj do ISO 8601 s lokálnym offsetom (nepoužívaj ‘Z’). Ak pacient uvedie len dátum, vyžiadaj konkrétny čas. Príklady:\n\n- „20.11 o 7“ → 2025-11-20T07:00:00+01:00\n\n- „zajtra o 8:30“ (pri zimnom čase) → 2025-11-21T08:30:00+01:00\n\n- „budúci utorok o 14“ → 2025-11-25T14:00:00+01:00",
          "dynamic_variable": "",
          "constant_value": "",
          "enum": null,
          "is_system_provided": false,
          "required": true
        },
        {
          "id": "id_event",
          "type": "string",
          "value_type": "llm_prompt",
          "description": "id ktore je pridelene ku kazdemu eventu",
          "dynamic_variable": "",
          "constant_value": "",
          "enum": null,
          "is_system_provided": false,
          "required": true
        },
        {
          "id": "datum_narodenia",
          "type": "string",
          "value_type": "llm_prompt",
          "description": "Dátum narodenia pacienta vo formáte DD.MM.RRRR (napr. 29.01.1998)",
          "dynamic_variable": "",
          "constant_value": "",
          "enum": null,
          "is_system_provided": false,
          "required": true
        },
        {
          "id": "name",
          "type": "string",
          "value_type": "llm_prompt",
          "description": "meno a  priezvysko pacienta",
          "dynamic_variable": "",
          "constant_value": "",
          "enum": null,
          "is_system_provided": false,
          "required": true
        }
      ],
      "required": true,
      "value_type": "llm_prompt"
    },
    "request_headers": [
      {
        "type": "value",
        "name": "Content-Type",
        "value": "application/json"
      }
    ],
    "auth_connection": null
  },
  "response_timeout_secs": 20,
  "dynamic_variables": {
    "dynamic_variable_placeholders": {}
  }
}
```

**Očakávaná odpoveď (z n8n webhooku):**
```json
{
  "success": true,
  "message": "Zmena termínu prebehla úspešne",
  "old_event": {
    "event_id": "evt_123456",
    "time_start": "2025-12-03T09:00:00+01:00",
    "time_end": "2025-12-03T09:30:00+01:00"
  },
  "new_event": {
    "event_id": "evt_123456",
    "time_start": "2025-12-10T09:00:00+01:00",
    "time_end": "2025-12-10T09:30:00+01:00",
    "summary": "Peter Horváth",
    "description": "Pretrvávajúci kašeľ, 0902 456 789, 03.09.1984, horvath.peter@gmail.com"
  }
}
```
alebo (pri chybe):
```json
{
  "success": false,
  "error": "Nový termín je obsadený",
  "message": "Zmena zlyhala"
}
```

**Použitie:**
- Po získaní súhlasu pacienta so zmenou
- Po určení nového termínu
- Po overení dostupnosti nového termínu pomocou `check_availability`
- Zachovávaj pôvodné údaje pacienta (meno, dátum narodenia, email, dôvod)

**Alternatíva:** Ak `reschedule` nie je dostupný, použij sekvenciu:
1. Vytvor novú rezerváciu pomocou `book` (s pôvodnými údajmi a novým časom)
2. Zruš pôvodnú pomocou `cancel`

---

## 📋 Workflow Nástrojov

### Rezervácia termínu:
1. Pacient povie dátum a čas
2. **`check_availability`** → overenie dostupnosti
3. Ak voľný → zbieranie údajov (meno, dátum narodenia, email, dôvod)
4. **`book`** → vytvorenie rezervácie

### Zmena termínu:
1. **`get_events`** → získanie event_id pôvodného termínu
2. Pacient povie nový dátum a čas
3. **`check_availability`** → overenie dostupnosti nového termínu
4. Ak voľný → **`reschedule`** → zmena termínu

### Zrušenie termínu:
1. **`get_events`** → získanie event_id termínu
2. Potvrdenie s pacientom
3. **`cancel`** → zrušenie termínu

---

## ⚠️ Dôležité Poznámky

### Formáty dát:
- **Dátum:** YYYY-MM-DD (napr. 2025-12-03)
- **Čas (pre check_availability):** HH:MM alebo YYYY-MM-DDTHH:MM:SS
- **Čas (pre book/reschedule):** YYYY-MM-DDTHH:MM:SS (ISO 8601)

### Validácia:
- Všetky nástroje by mali validovať formáty dát pred volaním
- Ak formát nie je správny, agent by mal požiadať pacienta o opravu

### Error Handling:
- Ak nástroj vráti chybu, agent by mal:
  1. Informovať pacienta o probléme
  2. Ponúknuť eskaláciu na personál
  3. Alebo navrhnúť alternatívu

---

## 🔗 Integrácia s Backendom

Tieto JSON definície sú pripravené pre:
- **ElevenLabs/Elvi** - Function calling
- **n8n** - Workflow automation
- **Google Calendar API** - Rezervácie

Backend by mal implementovať:
- Validáciu formátov dát
- Kontrolu dostupnosti termínov
- Vytváranie/zmena/zrušenie eventov v kalendári
- Error handling a meaningful error messages

---

**Verzia:** 1.0  
**Dátum:** 2025-11-30  
**Status:** ✅ Ready for Implementation  
**Založené na:** [[Recepcia_Prompt_v2.0]] (v2.2)

