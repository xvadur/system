#!/bin/bash

# 🧹 Skript na vyčistenie cache súborov na Macu
# Bezpečné vymazanie dočasných súborov, ktoré môžu byť obnovené

echo "🧹 Začínam čistenie cache súborov..."
echo ""

# Zaznamenaj aktuálne miesto pred čistením
SPACE_BEFORE=$(df -h / | awk 'NR==2 {print $3}')

echo "📊 Miesto pred čistením: $SPACE_BEFORE"
echo ""

# 1. Yarn cache
if command -v yarn &> /dev/null; then
    echo "🧶 Čistím Yarn cache..."
    yarn cache clean
fi

# 2. npm cache
if command -v npm &> /dev/null; then
    echo "📦 Čistím npm cache..."
    npm cache clean --force
fi

# 3. pip cache
if command -v pip &> /dev/null; then
    echo "🐍 Čistím pip cache..."
    pip cache purge
fi

# 4. Vymazanie konkrétnych cache priečinkov
echo "🗑️  Vymazávam cache priečinky aplikácií..."

CACHE_DIRS=(
    "$HOME/Library/Caches/com.todesktop.230313mzl4w4u92.ShipIt"
    "$HOME/Library/Caches/Dia"
    "$HOME/Library/Caches/company.thebrowser.dia"
    "$HOME/Library/Caches/com.openai.atlas"
    "$HOME/Library/Caches/Arc"
    "$HOME/Library/Caches/Cypress"
    "$HOME/Library/Caches/curseforge-updater"
)

for dir in "${CACHE_DIRS[@]}"; do
    if [ -d "$dir" ]; then
        SIZE=$(du -sh "$dir" 2>/dev/null | cut -f1)
        echo "  Vymazávam: $(basename "$dir") ($SIZE)"
        rm -rf "$dir"
    fi
done

# 5. Docker cleanup (len ak existuje)
if command -v docker &> /dev/null; then
    echo ""
    read -p "🐳 Chceš vyčistiť aj Docker? (y/n) " -n 1 -r
    echo
    if [[ $REPLY =~ ^[Yy]$ ]]; then
        echo "Čistím Docker..."
        docker system prune -a --volumes -f
    fi
fi

# Zaznamenaj miesto po čistení
SPACE_AFTER=$(df -h / | awk 'NR==2 {print $3}')

echo ""
echo "✅ Čistenie dokončené!"
echo "📊 Miesto po čistení: $SPACE_AFTER"
echo ""
echo "💡 Tip: Pre detailnú analýzu pozri: development/data/mac_storage_analysis.md"


