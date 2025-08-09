#!/usr/bin/env python3
"""
HRM Chat Interface für Trae
Diese Datei ermöglicht die direkte Kommunikation mit Ihrem lokalen HRM-Modell
über die OpenAI-kompatible API. Sie können sie direkt in Trae ausführen.
"""

import requests
import json
import sys
from typing import List, Dict, Optional

class HRMChat:
    def __init__(self, base_url="http://127.0.0.1:8000"):
        self.base_url = base_url
        self.model = "hrm-local-model"
        self.conversation_history: List[Dict[str, str]] = []
    
    def chat(self, message: str, system_prompt: Optional[str] = None) -> str:
        """Sendet eine Nachricht an das HRM-Modell und gibt die Antwort zurück."""
        
        # Erstelle die Messages-Struktur
        messages = []
        if system_prompt:
            messages.append({"role": "system", "content": system_prompt})
        
        # Füge Konversationshistorie hinzu
        messages.extend(self.conversation_history)
        messages.append({"role": "user", "content": message})
        
        # API-Anfrage
        payload = {
            "model": self.model,
            "messages": messages,
            "max_tokens": 2000,
            "temperature": 0.7
        }
        
        try:
            response = requests.post(
                f"{self.base_url}/v1/chat/completions",
                json=payload,
                headers={"Content-Type": "application/json"},
                timeout=30
            )
            response.raise_for_status()
            
            result = response.json()
            assistant_message = result["choices"][0]["message"]["content"]
            
            # Speichere die Nachrichten in der Historie
            self.conversation_history.append({"role": "user", "content": message})
            self.conversation_history.append({"role": "assistant", "content": assistant_message})
            
            # Begrenze die Historie auf die letzten 10 Nachrichten
            if len(self.conversation_history) > 20:
                self.conversation_history = self.conversation_history[-20:]
            
            return assistant_message
            
        except requests.exceptions.ConnectionError:
            return "❌ Fehler: HRM-Server nicht erreichbar. Stelle sicher, dass 'openai_proxy_server.py' läuft."
        except Exception as e:
            return f"❌ Fehler: {str(e)}"
    
    def clear_history(self):
        """Löscht die Konversationshistorie."""
        self.conversation_history = []
    
    def research_mode(self, topic: str) -> str:
        """Spezialmodus für tiefgreifende Recherche."""
        system_prompt = """Du bist ein Experte für tiefgründige Recherche und Analyse. 
        Strukturiere deine Antworten klar und tiefgründig. Berücksichtige verschiedene Perspektiven 
        und liefere konkrete, umsetzbare Erkenntnisse."""
        
        return self.chat(f"Bitte analysiere folgendes Thema tiefgründig: {topic}", system_prompt)
    
    def brainstorm_mode(self, problem: str) -> str:
        """Spezialmodus für Brainstorming und kreative Lösungen."""
        system_prompt = """Du bist ein kreativer Brainstorming-Partner. Denke unkonventionell 
        und liefere innovative, aber praktikable Lösungsansätze. Sei mutig in deinen Ideen."""
        
        return self.chat(f"Brainstorming-Auftrag: {problem}", system_prompt)
    
    def code_mode(self, code_context: str, request: str) -> str:
        """Spezialmodus für Code-Analyse und -Verbesserung."""
        system_prompt = """Du bist ein erfahrener Software-Entwickler. Analysiere Code 
        gründlich und gib präzise, umsetzbare Verbesserungsvorschläge."""
        
        return self.chat(f"Code-Kontext: {code_context}\n\nAnfrage: {request}", system_prompt)

# Interaktive Nutzung im Terminal
if __name__ == "__main__":
    chat = HRMChat()
    
    print("🧠 HRM Chat Interface gestartet")
    print("💡 Tipp: Der Server läuft auf http://127.0.0.1:8000")
    print("📝 Befehle: 'exit' zum Beenden, 'clear' zum Löschen der Historie")
    print("🎯 Modi: 'research <Thema>', 'brainstorm <Problem>', 'code <Code> <Frage>'")
    print("-" * 50)
    
    mode = None
    
    while True:
        try:
            user_input = input("\n💬 Du: ").strip()
            
            if user_input.lower() == 'exit':
                print("👋 Auf Wiedersehen!")
                break
            elif user_input.lower() == 'clear':
                chat.clear_history()
                print("🗑️ Historie gelöscht!")
                continue
            elif user_input.startswith('research '):
                response = chat.research_mode(user_input[9:])
                print(f"🔍 HRM: {response}")
                continue
            elif user_input.startswith('brainstorm '):
                response = chat.brainstorm_mode(user_input[11:])
                print(f"💡 HRM: {response}")
                continue
            elif user_input.startswith('code '):
                parts = user_input[5:].split(' ', 1)
                if len(parts) == 2:
                    response = chat.code_mode(parts[0], parts[1])
                    print(f"💻 HRM: {response}")
                else:
                    print("❌ Syntax: code <Code-Datei-Inhalt> <Frage>")
                continue
            
            response = chat.chat(user_input)
            print(f"🤖 HRM: {response}")
            
        except KeyboardInterrupt:
            print("\n👋 Auf Wiedersehen!")
            break
        except Exception as e:
            print(f"❌ Fehler: {e}")