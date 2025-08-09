# HRM-Modell in Trae nutzen - Komplette Anleitung

## 🎯 Ziel
Das HRM-Modell als lokales KI-Modell in Trae verwenden und aus der Modell-Liste auswählen.

## 📋 Schnellstart

### 1. Installation ausführen
```bash
# Im Terminal ausführen:
./install_hrm_in_trae.sh
```

### 2. In Trae registrieren
1. Öffne Trae
2. Gehe zu **Settings** → **Extensions** → **MCP Servers**
3. Klicke auf **Add Server**
4. Konfiguriere:
   - **Name**: `HRM-Local`
   - **Type**: `command`
   - **Command**: `/Users/bigsur/Desktop/HRM - Hirarchisches Reasoning Model/venv/bin/python`
   - **Args**: `/Users/bigsur/Desktop/HRM - Hirarchisches Reasoning Model/mcp_hrm_server.py`

## 🔧 Manuelle Installation (falls benötigt)

### Vorbereitung
```bash
# Virtuelle Umgebung erstellen
python3 -m venv venv
source venv/bin/activate

# Abhängigkeiten installieren
pip install -r requirements_mcp.txt
```

### Server starten
```bash
# MCP-Server starten
python mcp_hrm_server.py
```

## 🎮 Verwendung in Trae

### Als Modell auswählen
Nach erfolgreicher Registrierung:
1. Öffne eine neue Konversation
2. In der Modell-Auswahl: **HRM-Local** auswählen
3. Oder verwende: `@HRM-Local` in der Eingabe

### Verwendungsbeispiele
```
# Direkte Verwendung
@HRM-Local Analysiere diesen Python-Code

# Als Standardmodell setzen
Settings → AI → Default Model → HRM-Local

# Für spezielle Aufgaben
@HRM-Local Führe hierarchisches Reasoning für diese Funktion durch
```

## 🏗️ Technische Details

### Modell-Parameter
- **Parameter**: 105 Millionen
- **Größe**: ~404 MB RAM
- **Typ**: Hierarchical Reasoning Model
- **Lokal**: 100% CPU-basiert

### MCP-Endpunkte
- **Tool**: `hrm_reasoning`
- **Funktion**: Code-Analyse und Reasoning
- **Privacy**: Keine Cloud-Kommunikation

### Beispiel-API-Aufruf
```python
# Beispiel für direkte Nutzung
import requests

response = requests.post('http://localhost:8000/reason', json={
    'prompt': 'Analysiere diese Funktion',
    'code': 'def fibonacci(n): return n if n <= 1 else fibonacci(n-1) + fibonacci(n-2)'
})
```

## 🛠️ Fehlerbehebung

### Server startet nicht
```bash
# Überprüfe Python-Pfad
which python
# Sollte sein: /Users/bigsur/Desktop/HRM - Hirarchisches Reasoning Model/venv/bin/python

# Überprüfe Dateipfade
ls -la mcp_hrm_server.py
```

### Trae erkennt Server nicht
1. **Neustart**: Trae komplett neu starten
2. **Pfad prüfen**: Absolute Pfade verwenden
3. **Berechtigungen**: `chmod +x` für Skripte

### Performance-Optimierung
```bash
# Für schnelleren Start
export PYTORCH_MPS_HIGH_WATERMARK_RATIO=0.0
```

## 📊 Monitoring

### Server-Status prüfen
```bash
# Health-Check
curl -X POST http://localhost:8000/health

# Logs anzeigen
tail -f server.log
```

### Ressourcen-Überwachung
- **CPU**: `htop` oder Activity Monitor
- **RAM**: `free -h` oder Activity Monitor
- **GPU**: Nicht verwendet (CPU-only)

## 🔄 Updates

### Server aktualisieren
```bash
# Neue Version installieren
git pull origin main
pip install -r requirements_mcp.txt --upgrade
```

### Konfiguration anpassen
```bash
# Server-Konfiguration bearbeiten
nano mcp_hrm_server.py
```

## 🆘 Support

### Häufige Fragen
**Q: Warum erscheint HRM-Local nicht in der Liste?**
A: Überprüfe die MCP-Server-Einstellungen und starte Trae neu.

**Q: Kann ich HRM als Standardmodell setzen?**
A: Ja, in Settings → AI → Default Model → HRM-Local auswählen.

**Q: Ist meine Daten sicher?**
A: Ja, 100% lokale Verarbeitung, keine Cloud-Kommunikation.

### Debug-Modus
```bash
# Mit Debug-Logging starten
DEBUG=1 python mcp_hrm_server.py
```

---

**✅ Fertig!** Das HRM-Modell ist nun als lokales Modell in Trae verfügbar.