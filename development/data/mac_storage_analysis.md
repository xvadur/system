# 📊 Analýza pamäte MacBooku - Akčný plán

**Dátum:** $(date +%Y-%m-%d)  
**Aktuálny stav:** 212.4 GB použité z 245.11 GB (86.6% plné)

---

## 🔍 Nájdené dočasné súbory (na vymazanie)

### ✅ Bezpečné na vymazanie (celkovo ~20+ GB):

1. **Cache súbory (13 GB celkovo):**
   - `com.todesktop.230313mzl4w4u92.ShipIt`: **3.5 GB** - dočasné súbory aplikácie
   - `Yarn cache`: **2.7 GB** - npm balíčky (možno obnoviť)
   - `Dia browser cache`: **1.7 GB**
   - `company.thebrowser.dia`: **1.5 GB**
   - `com.openai.atlas`: **772 MB** - OpenAI cache
   - `Arc browser cache`: **705 MB**
   - `Cypress cache`: **533 MB** - testovací framework
   - `curseforge-updater`: **455 MB**
   - `pip cache`: **350 MB** - Python balíčky

2. **npm cache**: **1.3 GB** - možno bezpečne vymazať (balíčky sa stiahnu znova)

3. **Docker data**: **2.2 GB** - ak nepoužívaš Docker aktívne

4. **Systémové dočasné súbory**: **1.3 GB** (`/private/var/folders`)

**Celkovo možno uvoľniť: ~20 GB**

---

## 📁 Čo presunúť na externý disk

### 1. **Documents (19.86 GB)** - PRIORITA
- Staré projekty
- Dokumenty, ktoré nepotrebuješ často
- Zálohy súborov

### 2. **Photos (8.25 GB)** - PRIORITA
- Staré fotky (použi iCloud Photos alebo externý disk)
- Veľké video súbory

### 3. **Developer (1.76 GB)**
- Staré projekty
- Zálohy repozitárov

### 4. **Mail (2.47 GB)**
- Staré emaily (export do .mbox súborov)

---

## 🛠️ Konkrétne kroky na vyčistenie

### Krok 1: Vymazanie cache súborov (bezpečné)

```bash
# Yarn cache
yarn cache clean

# npm cache
npm cache clean --force

# pip cache
pip cache purge

# Vymazanie konkrétnych cache priečinkov
rm -rf ~/Library/Caches/com.todesktop.230313mzl4w4u92.ShipIt
rm -rf ~/Library/Caches/Dia
rm -rf ~/Library/Caches/company.thebrowser.dia
rm -rf ~/Library/Caches/com.openai.atlas
rm -rf ~/Library/Caches/Arc
rm -rf ~/Library/Caches/Cypress
rm -rf ~/Library/Caches/curseforge-updater
```

### Krok 2: Docker cleanup (ak nepoužívaš)

```bash
docker system prune -a --volumes
```

### Krok 3: macOS Storage Management

1. **System Settings > General > Storage > Recommendations**
   - Zapni "Optimize Storage"
   - Zapni "Empty Trash Automatically"
   - Zapni "Reduce Clutter"

2. **Time Machine lokálne zálohy:**
   ```bash
   # Skontroluj lokálne Time Machine snapshots
   tmutil listlocalsnapshots /
   
   # Vymaž staré snapshots (ak máš externý Time Machine disk)
   sudo tmutil deletelocalsnapshots [datum]
   ```

### Krok 4: Presun súborov na externý disk

**Odporúčaná štruktúra na externom disku:**
```
/external-disk/
  ├── Documents/
  │   ├── Old Projects/
  │   └── Archives/
  ├── Photos/
  │   └── Archive/
  └── Developer/
      └── Old Repos/
```

---

## 📈 Očakávané výsledky

Po vykonaní všetkých krokov:
- **Vymazanie cache**: ~20 GB
- **Presun Documents**: ~15 GB (nechaj len aktívne projekty)
- **Presun Photos**: ~6 GB (nechaj len posledné fotky)
- **Celkovo uvoľnené**: ~41 GB

**Nový stav:** ~171 GB použité (70% plné) ✅

---

## ⚠️ Dôležité poznámky

1. **System Data (78.73 GB)** je veľké, ale obsahuje:
   - Lokálne Time Machine snapshots
   - Systémové cache
   - Virtual memory files
   - Časť sa vyčistí automaticky po vymazaní cache

2. **macOS (50.91 GB)** - toto je normálne, systém potrebuje toto miesto

3. **Applications (48.27 GB)** - skontroluj, či nepotrebuješ všetky aplikácie

4. **Pred vymazaním:** Vytvor zálohu dôležitých súborov!

---

## 🔄 Pravidelné údržba

1. **Mesačne:** Vymaž cache súbory
2. **Kvartálne:** Presuň staré projekty na externý disk
3. **Použi nástroje:**
   - CleanMyMac X (platený)
   - DaisyDisk (platený)
   - GrandPerspective (zdarma) - vizualizácia miesta na disku

---

## ✅ Quick Win - Najrýchlejšie riešenie

```bash
# Spusti tento skript pre rýchle vyčistenie (bezpečné)
yarn cache clean
npm cache clean --force
pip cache purge
rm -rf ~/Library/Caches/com.todesktop.230313mzl4w4u92.ShipIt
rm -rf ~/Library/Caches/Dia
rm -rf ~/Library/Caches/company.thebrowser.dia
```

**To uvoľní ~10 GB za 5 minút!**

