#!/bin/bash

echo "🚀 Starte HRM-Reasoning-Server..."
echo "🔄 Installiere Abhängigkeiten..."

# Aktiviere die richtige Umgebung
source ../HRM-Complete/hrm_env_py311/bin/activate

# Installiere zusätzliche Pakete
pip install -r requirements_server.txt

echo "✅ Abhängigkeiten installiert"
echo "🎯 Starte Server..."

# Starte den Server
python hrm_reasoning_server.py