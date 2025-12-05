# 🔄 Lokálny Scheduler pre Dennú Rotáciu

Tento systém nahrádza GitHub Actions lokálnym automatizovaným schedulerom, ktorý sa spúšťa každú polnoc a vykonáva dennú rotáciu session.

## 📋 Čo Robí

Každú polnoc (00:00) sa automaticky spustí skript, ktorý:

1. **Archivuje včerajšiu session** - Presunie do `staging/sessions/yesterday/`
2. **Vytvorí novú session** - Z template do `development/sessions/current/`
3. **Vygeneruje denný review** - Do `staging/review/daily_review.md`
4. **Vypočíta XP a metriky** - Aktualizuje `development/logs/XVADUR_XP.md`
5. **Pushne zmeny na GitHub** - Automatický commit a push

## 🚀 Inštalácia

### 1. Spusti inštalačný skript

```bash
cd /Users/_xvadur/Desktop/xvadur-workspace
./scripts/local_scheduler/install_scheduler.sh
```

Inštalačný skript:
- Nájde správnu Python cestu
- Vytvorí logs adresár
- Nainštaluje macOS launchd službu
- Nastaví automatické spúšťanie každú polnoc

### 2. Overenie inštalácie

```bash
# Skontroluj, či je služba nainštalovaná
launchctl list | grep com.xvadur.daily_rotation

# Skontroluj logs (po prvom spustení)
tail -f logs/daily_rotation.out.log
tail -f logs/daily_rotation.err.log
```

## 🧪 Manuálne Testovanie

Pred prvým spustením otestuj skript manuálne:

```bash
cd /Users/_xvadur/Desktop/xvadur-workspace
python3 scripts/daily_rotation.py
```

## 📝 Logy

Všetky logy sa ukladajú do:
- `logs/daily_rotation.out.log` - štandardný výstup
- `logs/daily_rotation.err.log` - chybové správy

## 🔧 Správa Scheduleru

### Zobraziť Status

```bash
launchctl list | grep com.xvadur.daily_rotation
```

### Odstrániť Scheduler

```bash
launchctl unload ~/Library/LaunchAgents/com.xvadur.daily_rotation.plist
rm ~/Library/LaunchAgents/com.xvadur.daily_rotation.plist
```

### Re-inštalovať

```bash
./scripts/local_scheduler/install_scheduler.sh
```

## ⚙️ Konfigurácia

### Zmeniť Čas Spustenia

Uprav `scripts/local_scheduler/com.xvadur.daily_rotation.plist`:

```xml
<key>StartCalendarInterval</key>
<dict>
    <key>Hour</key>
    <integer>0</integer>  <!-- 0 = polnoc, 7 = 7:00, atď. -->
    <key>Minute</key>
    <integer>0</integer>
</dict>
```

Potom re-inštaluj:
```bash
./scripts/local_scheduler/install_scheduler.sh
```

## ⚠️ Poznámky

- **Scheduler funguje len keď je Mac zapnutý** - Ak je Mac vypnutý o polnoci, skript sa nespustí
- **Git push vyžaduje pripojenie k internetu** - Bez internetu zlyhá git push, ale ostatné kroky sa dokončia
- **Logs sa hromadia** - Pravidelne kontroluj veľkosť log súborov

## 🔍 Troubleshooting

### Scheduler sa nespúšťa

1. Skontroluj, či je služba načítaná:
   ```bash
   launchctl list | grep com.xvadur.daily_rotation
   ```

2. Skontroluj logy:
   ```bash
   cat logs/daily_rotation.err.log
   ```

3. Skús manuálne spustenie:
   ```bash
   python3 scripts/daily_rotation.py
   ```

### Git Push zlyhá

- Skontroluj, či máš nastavený GitHub token v `.env`:
  ```bash
  cat .env | grep GH_TOKEN
  ```
- Skontroluj git konfiguráciu:
  ```bash
  git config --list | grep user
  ```

### Python cesta nie je správna

Inštalačný skript automaticky detekuje Python cestu. Ak máš problém:
1. Zisti Python cestu:
   ```bash
   which python3
   ```
2. Uprav `install_scheduler.sh` a zmeň `PYTHON_PATH` na správnu hodnotu

## 📚 Súvisiace Dokumenty

- `scripts/daily_rotation.py` - Hlavný skript
- `scripts/utils/git_helper.py` - Git push helper
- `docs/SESSION_MANAGEMENT.md` - Session management dokumentácia

---

**Vytvorené:** 2025-12-05  
**Verzia:** 1.0.0

