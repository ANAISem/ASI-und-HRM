# 🧠 HRM Lokales Reasoning-System

**Sofort einsatzbereites, datenschutzfreundliches Reasoning-System**

## ⚡ Schnellstart (30 Sekunden)

```bash
cd "/Users/bigsur/Desktop/HRM - Hirarchisches Reasoning Model"
bash start_hrm_server.sh
```

Server läuft dann auf: http://localhost:8080

## 🔧 Manuelle Installation

```bash
# Falls Skript nicht funktioniert:
cd "/Users/bigsur/Desktop/HRM - Hirarchisches Reasoning Model"
source ../HRM-Complete/hrm_env_py311/bin/activate
pip install flask torch requests
python hrm_reasoning_server.py
```

## 📡 API-Endpunkte

### 1. Allgemeines Reasoning
```bash
curl -X POST http://localhost:8080/reasoning \
  -H "Content-Type: application/json" \
  -d '{"prompt": "Erkläre Vorteile von hierarchischem Reasoning", "context": "KI-Architektur"}'
```

### 2. Code-Analyse
```bash
curl -X POST http://localhost:8080/analyze \
  -H "Content-Type: application/json" \
  -d '{"code": "def fib(n): return n if n<=1 else fib(n-1)+fib(n-2)", "language": "python"}'
```

### 3. Health-Check
```bash
curl http://localhost:8080/health
```

### 4. Test-Endpunkt
```bash
curl http://localhost:8080/test
```

## 🐍 Python-Client Beispiel

```python
import requests

# Reasoning-Anfrage
response = requests.post('http://localhost:8080/reasoning', json={
    'prompt': 'Wie optimiere ich Algorithmen?',
    'context': 'Python-Optimierung'
})

result = response.json()
print(f"Reasoning: {result['reasoning']}")
print(f"Konfidenz: {result['confidence']}")
```

## 🎯 Verwendungsbeispiele

### Für Code-Reviews (lokal & privat):
```bash
curl -X POST http://localhost:8080/analyze \
  -d '{"code": "Ihr Python-Code hier", "language": "python"}'
```

### Für logische Probleme:
```bash
curl -X POST http://localhost:8080/reasoning \
  -d '{"prompt": "Erkläre QuickSort", "context": "Algorithmen"}'
```

## 🛡️ Datenschutz-Features

- ✅ **100% lokal** - Keine Cloud-Kommunikation
- ✅ **CPU-only** - Keine GPU nötig
- ✅ **105M Parameter** - Kompakt & effizient
- ✅ **Sofort verfügbar** - Nach 5 Sekunden Start

## 🔍 Testen

```bash
python test_hrm_client.py
```

## 📊 Technische Details

- **Modell:** HierarchicalReasoningModel_ACTV1
- **Parameter:** 105,990,146
- **Größe:** ~404 MB RAM
- **Startzeit:** < 5 Sekunden
- **API-Format:** JSON REST

## 🚨 Fehlerbehebung

**Server startet nicht?**
```bash
# Prüfe Python-Umgebung
source ../HRM-Complete/hrm_env_py311/bin/activate
python -c "import torch; print('OK')"

# Manuelle Installation
pip install flask torch requests
```

**Port 8080 belegt?**
```bash
# Server auf anderem Port starten
python hrm_reasoning_server.py  # Standard: 8080
# oder ändere in der Datei: app.run(port=8081)
```

## 🎉 Fertig!

Dein HRM-System ist **sofort einsatzbereit** für:
- Lokales Reasoning
- Private Code-Analysen
- Datenschutz-kritische Aufgaben
- Schnelle Antworten ohne Cloud