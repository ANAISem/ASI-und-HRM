#!/bin/bash
# HRM MCP Server Installation für Trae

echo "🚀 Installiere HRM-Modell als lokales Modell in Trae..."

# Virtuelle Umgebung erstellen falls nicht vorhanden
if [ ! -d "venv" ]; then
    echo "📦 Erstelle virtuelle Umgebung..."
    python3 -m venv venv
fi

# Umgebung aktivieren
source venv/bin/activate

# Abhängigkeiten installieren
echo "📥 Installiere MCP-Abhängigkeiten..."
pip install -r requirements_mcp.txt

# MCP-Server ausführbar machen
chmod +x mcp_hrm_server.py

echo "✅ HRM-MCP-Server erfolgreich installiert!"
echo ""
echo "📋 So verwenden Sie HRM in Trae:"
echo "1. Öffnen Sie Trae"
echo "2. Gehen Sie zu Settings → Extensions → MCP Servers"
echo "3. Fügen Sie hinzu:"
echo "   Name: HRM-Local"
echo "   Type: command"
echo "   Command: $(pwd)/venv/bin/python"
echo "   Args: $(pwd)/mcp_hrm_server.py"
echo ""
echo "🎯 Nach der Registrierung steht 'HRM-Local' in der Modell-Liste zur Verfügung!"
echo "💡 Verwenden Sie: 'Use HRM-Local for reasoning' oder 'Analyze with HRM-Local'"