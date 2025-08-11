#!/usr/bin/env python3
"""
Download-Skript für HRM-Modelle von Hugging Face
Phase 2: Trainierte Modelle einbinden und Mock-Systeme ersetzen
"""

import os
from huggingface_hub import snapshot_download

def download_hrm_checkpoints():
    """Lade die verfügbaren HRM-Checkpoints herunter."""
    
    # Verzeichnis für Modelle erstellen
    models_dir = "/Users/bigsur/Desktop/ASI und HRM /models"
    os.makedirs(models_dir, exist_ok=True)
    
    # Verfügbare Checkpoints
    checkpoints = {
        "arc-2": "sapientinc/HRM-checkpoint-ARC-2",
        "sudoku-extreme": "sapientinc/HRM-checkpoint-sudoku-extreme", 
        "maze-30x30": "sapientinc/HRM-checkpoint-maze-30x30-hard"
    }
    
    downloaded = {}
    
    for name, repo_id in checkpoints.items():
        print(f"Lade {name} herunter...")
        try:
            path = snapshot_download(
                repo_id=repo_id,
                cache_dir=os.path.join(models_dir, name),
                local_dir=os.path.join(models_dir, name)
            )
            downloaded[name] = path
            print(f"✓ {name} erfolgreich heruntergeladen: {path}")
        except Exception as e:
            print(f"✗ Fehler beim Download von {name}: {e}")
    
    return downloaded

if __name__ == "__main__":
    print("=== Phase 2: HRM-Modelle herunterladen ===")
    models = download_hrm_checkpoints()
    print(f"\nInsgesamt {len(models)} Modelle heruntergeladen.")
    for name, path in models.items():
        print(f"- {name}: {path}")