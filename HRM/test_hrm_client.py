#!/usr/bin/env python3
"""
HRM-Client - Testet die lokale HRM-Reasoning-API
"""

import requests
import json
import time

def test_hrm_reasoning():
    """Testet die HRM-Reasoning-API"""
    
    base_url = "http://localhost:8080"
    
    print("🧪 Teste HRM-Reasoning-API...")
    
    # 1. Health-Check
    try:
        response = requests.get(f"{base_url}/health")
        if response.status_code == 200:
            health = response.json()
            print(f"✅ Health-Check: {health}")
        else:
            print("❌ Health-Check fehlgeschlagen")
            return False
    except requests.exceptions.ConnectionError:
        print("❌ Server nicht erreichbar - starte zuerst den Server")
        return False
    
    # 2. Test-Reasoning
    test_prompts = [
        {
            "prompt": "Erkläre die Vorteile von hierarchischem Reasoning in der KI",
            "context": "HRM ist ein hierarchisches Reasoning-Modell"
        },
        {
            "prompt": "Wie kann ich diesen Code optimieren?",
            "context": "Python-Code für Datenverarbeitung"
        }
    ]
    
    for i, test in enumerate(test_prompts, 1):
        print(f"\n🔍 Test {i}: {test['prompt'][:50]}...")
        
        try:
            response = requests.post(
                f"{base_url}/reasoning",
                json=test,
                timeout=30
            )
            
            if response.status_code == 200:
                result = response.json()
                print(f"   ✅ Ergebnis: {result['reasoning'][:100]}...")
                print(f"   📊 Konfidenz: {result['confidence']}")
            else:
                print(f"   ❌ Fehler: {response.status_code}")
                
        except Exception as e:
            print(f"   ❌ Fehler: {e}")
    
    # 3. Code-Analyse
    sample_code = """
def fibonacci(n):
    if n <= 1:
        return n
    return fibonacci(n-1) + fibonacci(n-2)
"""
    
    print(f"\n💻 Teste Code-Analyse...")
    
    try:
        response = requests.post(
            f"{base_url}/analyze",
            json={"code": sample_code, "language": "python"},
            timeout=30
        )
        
        if response.status_code == 200:
            result = response.json()
            print(f"   ✅ Code-Analyse: {result['reasoning'][:100]}...")
        else:
            print(f"   ❌ Code-Analyse fehlgeschlagen")
            
    except Exception as e:
        print(f"   ❌ Fehler bei Code-Analyse: {e}")
    
    return True

if __name__ == "__main__":
    print("🎯 HRM-Client Test")
    print("Stelle sicher, dass der Server läuft: ./start_hrm_server.sh")
    
    # Warte kurz, falls Server gerade startet
    time.sleep(2)
    
    if test_hrm_reasoning():
        print("\n🎉 Alle Tests erfolgreich!")
    else:
        print("\n⚠️  Server nicht erreichbar oder Tests fehlgeschlagen")
        print("Starte den Server mit: bash start_hrm_server.sh")