# GitHub Repository Setup Guide - AION HRM Intelligent Router

## Schritt-für-Schritt Anleitung

### 1. Repository auf GitHub erstellen
1. Gehe zu [github.com](https://github.com)
2. Klicke auf "New repository" (grüner Button)
3. Repository-Name: `AION-HRM-Intelligent-Router`
4. Beschreibung: `AION HRM Intelligent Router System - Advanced AI reasoning with hierarchical models and intelligent routing`
5. Wähle "Private" oder "Public" (je nach Präferenz)
6. NICHT "Initialize this repository with a README" ankreuzen
7. Klicke auf "Create repository"

### 2. Lokales Repository mit GitHub verbinden

Nachdem das Repository erstellt wurde, führe diese Befehle aus:

```bash
cd "/Users/bigsur/Desktop/ASI und HRM "
git remote remove origin
git remote add origin https://github.com/DEIN_USERNAME/AION-HRM-Intelligent-Router.git
git branch -M main
git push -u origin main
```

### 3. Erste Push-Bestätigung

Das erste Push kann einige Minuten dauern, da viele Dateien hochgeladen werden.

### 4. Verifizierung

Nach erfolgreichem Push:
- Gehe zu deinem neuen Repository auf GitHub
- Du solltest alle Dateien und Ordner sehen
- Die README.md und alle Projektdateien sollten sichtbar sein

### 5. Nächste Schritte

- [ ] Repository auf GitHub erstellt
- [ ] Lokales Repository mit GitHub verbunden
- [ ] Erster Push erfolgreich durchgeführt
- [ ] Repository online überprüft

## Alternative: SSH-Methode

Wenn du SSH-Keys eingerichtet hast, kannst du stattdessen:

```bash
git remote add origin git@github.com:DEIN_USERNAME/AION-HRM-Intelligent-Router.git
git push -u origin main
```

## Wichtige Hinweise

- Das Repository enthält sensible Daten in `.env` Dateien - diese sind bereits in `.gitignore` aufgenommen
- Alle API-Keys und Secrets sind ausgeschlossen
- Die `.env.hrm.example` Datei enthält Beispielkonfigurationen ohne echte Secrets

## Repository-Struktur

```
AION-HRM-Intelligent-Router/
├── ASI/                          # Haupt-ASI Projekt
│   ├── src/intelligent-router/   # HRM Routing System
│   ├── app/                      # Next.js App
│   └── package.json
├── HRM-Complete/                 # Vollständiges HRM
├── HRM/                          # Lokales HRM Setup
└── README.md
```

## Support

Bei Problemen:
1. Überprüfe deine GitHub Credentials
2. Stelle sicher, dass du angemeldet bist
3. Überprüfe die Repository-URL
4. Bei großen Dateien: Überprüfe Git LFS falls nötig