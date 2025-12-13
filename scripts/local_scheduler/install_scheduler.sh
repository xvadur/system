#!/bin/bash
#
# Inštalačný skript pre macOS launchd scheduler
# Spustí sa každú polnoc (00:00) a vykoná dennú rotáciu
#

set -e

WORKSPACE_ROOT="/Users/_xvadur/Desktop/xvadur-workspace"
PLIST_NAME="com.xvadur.daily_rotation"
PLIST_FILE="$WORKSPACE_ROOT/scripts/local_scheduler/${PLIST_NAME}.plist"
LAUNCH_AGENTS_DIR="$HOME/Library/LaunchAgents"
INSTALLED_PLIST="$LAUNCH_AGENTS_DIR/${PLIST_NAME}.plist"

echo "🚀 Inštalácia lokálneho scheduleru pre dennú rotáciu"
echo "=================================================="
echo ""

# 1. Skontroluj, či plist súbor existuje
if [ ! -f "$PLIST_FILE" ]; then
    echo "❌ Chyba: Plist súbor neexistuje: $PLIST_FILE"
    exit 1
fi

# 2. Nájdi správnu Python cestu
PYTHON_PATH=$(which python3)
if [ -z "$PYTHON_PATH" ]; then
    echo "❌ Chyba: python3 nebol nájdený v PATH"
    exit 1
fi
echo "✅ Python nájdený: $PYTHON_PATH"

# 3. Uprav plist súbor s aktuálnou Python cestou
echo "📝 Upravujem plist súbor s aktuálnou Python cestou..."
sed "s|/usr/local/bin/python3|$PYTHON_PATH|g" "$PLIST_FILE" > "/tmp/${PLIST_NAME}.plist.tmp"

# 4. Vytvor logs adresár ak neexistuje
LOGS_DIR="$WORKSPACE_ROOT/logs"
mkdir -p "$LOGS_DIR"
echo "✅ Logs adresár: $LOGS_DIR"

# 5. Uprav log paths v plist
sed "s|/Users/_xvadur/Desktop/xvadur-workspace/logs|$LOGS_DIR|g" "/tmp/${PLIST_NAME}.plist.tmp" > "/tmp/${PLIST_NAME}.plist.tmp2"
sed "s|/Users/_xvadur/Desktop/xvadur-workspace|$WORKSPACE_ROOT|g" "/tmp/${PLIST_NAME}.plist.tmp2" > "/tmp/${PLIST_NAME}.plist"

# 6. Vytvor LaunchAgents adresár ak neexistuje
mkdir -p "$LAUNCH_AGENTS_DIR"
echo "✅ LaunchAgents adresár: $LAUNCH_AGENTS_DIR"

# 7. Odstráň existujúcu službu ak existuje
if [ -f "$INSTALLED_PLIST" ]; then
    echo "🔄 Odstraňujem existujúcu službu..."
    launchctl unload "$INSTALLED_PLIST" 2>/dev/null || true
    rm -f "$INSTALLED_PLIST"
fi

# 8. Skopíruj plist do LaunchAgents
cp "/tmp/${PLIST_NAME}.plist" "$INSTALLED_PLIST"
echo "✅ Plist skopírovaný do: $INSTALLED_PLIST"

# 9. Načítaj službu
echo "📥 Načítavam službu..."
launchctl load "$INSTALLED_PLIST"

# 10. Skontroluj status
if launchctl list | grep -q "$PLIST_NAME"; then
    echo "✅ Služba úspešne nainštalovaná!"
    echo ""
    echo "📋 Informácie:"
    echo "   - Názov služby: $PLIST_NAME"
    echo "   - Spustí sa každú polnoc (00:00)"
    echo "   - Logs: $LOGS_DIR/daily_rotation.*.log"
    echo ""
    echo "🔧 Užitočné príkazy:"
    echo "   - Status: launchctl list | grep $PLIST_NAME"
    echo "   - Odstrániť: launchctl unload $INSTALLED_PLIST && rm $INSTALLED_PLIST"
    echo "   - Manuálne spustenie: python3 $WORKSPACE_ROOT/scripts/daily_rotation.py"
    echo ""
else
    echo "⚠️  Služba bola nainštalovaná, ale možno nie je aktívna"
    echo "   Skontroluj: launchctl list | grep $PLIST_NAME"
fi

# Cleanup
rm -f "/tmp/${PLIST_NAME}.plist.tmp" "/tmp/${PLIST_NAME}.plist.tmp2" "/tmp/${PLIST_NAME}.plist"

echo ""
echo "✨ Hotovo!"










