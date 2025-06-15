# Projektname: KI-Argumentationstutor und Evaluation

## Beschreibung

Dieses Projekt ist ein interaktiver KI-Tutor, der Benutzern dabei hilft, ihre argumentativen Schreibfähigkeiten zu verbessern. Die Benutzer reichen ihre Argumentation zu vorgegebenen Diskussionsfragen ein, erhalten strukturiertes Feedback und können ihren Text überarbeiten. Ziel ist es, Logik, Prägnanz, Überzeugungskraft und die Nutzung von Belegen zu stärken. Dieses Projekt wurde ihm Rahmen des Modul "Informatik und Gesellschaft" hervorgerufen, um diesen Prototypen bei der Langen Nacht der Wissenschaften 2025 zu testen.

## Features

- **Interaktives Feedback:** Erhalte detailliertes und formatives Feedback von einer KI zu deiner Argumentation.
- **Rubrik-Bewertung:** Dein Text wird nach Kriterien wie Logik, Prägnanz, Überzeugungskraft bewertet.
- **Überarbeitungsmöglichkeit:** Optimiere deinen Text basierend auf dem erhaltenen KI-Feedback.
- **Flexible Diskussionsfragen:** Wähle aus einer Liste von kontroversen Themen.

## Installation

Um dieses Projekt lokal auszuführen, sollten diese Schritte befolgt werden:

1. **Virtuelle Umgebung erstellen (empfehlenswert**)
   ```bash
   python -m venv venv
   # Auf Windows:
   .\venv\Scripts\activate
   # Auf macOS/Linux:
   source venv/bin/activate
   ```
2. **Abhängigkeiten installieren:**
   ```bash
   pip install -r requirements.txt
   ```
3. **OpenAI API-Schlüssel einrichten:**

- Erstelle eine Datei namens `.env` im Hauptverzeichnis des Projektes.
- Füge deinen OpenAI API-Schlüssel in dieser Datei hinzu:

  ```
  OPENAI_API_KEY="dein_openai_api_schluessel_hier"
  ```

- Füge `.env` zu deiner `.gitignore`-Datei hinzu

## Projektstruktur

- .env #Umgebungsvariablen wie API-Schlüssel
- main.py #Hauptprogramm, steuert den Workflow, von hier soll auch das Programm gestartet werden!
- api_handler.py #Kommunikation mit der OpenAI API
- competition_logic.py #Logik für Diskussionsfragen und Benutzerinteratkion
- README.md #Diese Datei
- requirements.txt #benötigte Python-Bibliotheken
