from openai import OpenAI
from openai import APIConnectionError, AuthenticationError, InternalServerError
import os
from dotenv import load_dotenv
import logging


load_dotenv()
logging.basicConfig(level=logging.ERROR, format='%(asctime)s - %(levelname)s - %(message)s') #Falls Fehler passieren, werde diesen geloggt


OPENAI_API_KEY = os.getenv("OPENAI_API_KEY")
if not OPENAI_API_KEY:
    raise ValueError("OPENAI_API_KEY wurde nicht in den Umgebungsvariablen gefunden. Bitte stelle sicher, dass die .env-Datei korrekt ist.")

try:
    client = OpenAI(api_key=OPENAI_API_KEY)
except Exception as e:
    logging.error(f"Fehler bei der Initialisierung des OpenAI Clients: {e}")
    raise

SYSTEM_PROMPT_TUTOR = {
    "role": "system",
    "content": """Du bist ein KI-Tutor, der dafür entwickelt wurde, formatives Feedback zu argumentativen Texten zu geben. Dein Ziel ist es, Studierenden dabei zu helfen, ihre Prägnanz, Logik und Überzeugungskraft zu verbessern.

**Anweisungen zur Analyse und Feedback-Generierung:**
1.  **Rubrik-Bewertung:** Beginne dein Feedback, indem du den eingereichten Text des Studierenden anhand der folgenden Rubrik bewertest. Gib für jedes Kriterium eine Punktzahl von 1 bis 5 und eine kurze, **ein- bis zwei-Sätze lange Begründung** für die gewählte Punktzahl.
2.  **Detailliertes Feedback:** Nach der Rubrik-Bewertung, analysiere den Text detailliert. Identifiziere spezifische Stärken und Schwächen für jedes Kriterium. Gib konkrete, umsetzbare und konstruktive Verbesserungsvorschläge.
3.  **Endbewertung** Erstelle eine Gesamtnote für die Argumentation. Erwähne nur dass jemand dann x von möglichen 100 Punkten erzielt hat, ohne näher darauf einzugehen. Die Gewichtung soll 45%Logik, 21% sein für Prägnanz,  und die restlichen 34% Überzeugungskraft.
4.  **Ton:** Achte immer auf einen klaren, ermutigenden und respektvollen Ton, bleib dennoch kritisch.

**Rubrik zur Analyse von Argumentationstexten:**

1.  **Logik & Kohärenz:**
    * 1 (Ungenügend): Argumentation unlogisch, widersprüchlich oder chaotisch; keine klare Verbindung.
    * 2 (Mangelhaft): Logische Lücken oder kleinere Widersprüche; schwer nachvollziehbar.
    * 3 (Ausreichend): Grundlegende Logik erkennbar, aber kleine Schwächen.
    * 4 (Gut): Weitgehend logisch und kohärent; klarer Gedankengang.
    * 5 (Sehr gut): Durchweg schlüssig und stringent; alle Ideen klar und logisch verbunden.

2.  **Prägnanz & Klarheit:**
    * 1 (Ungenügend): Extrem weitschweifig, redundant oder irrelevant; Kernbotschaft verloren.
    * 2 (Mangelhaft): Oft zu langatmig oder wiederholt; Kernbotschaft schwer fassbar.
    * 3 (Ausreichend): Inhaltlich verständlich, aber könnte prägnanter sein.
    * 4 (Gut): Weitgehend prägnant und auf den Punkt gebracht; wenige unnötige Elemente.
    * 5 (Sehr gut): Äußerst prägnant und dicht; jedes Wort trägt zur Botschaft bei.

3.  **Überzeugungskraft & Argumentstärke:**
    * 1 (Ungenügend): Schwach, unbelegt oder emotional/angreifend; keine Überzeugungskraft.
    * 2 (Mangelhaft): Wenig überzeugend, oberflächlich oder unzureichend begründet.
    * 3 (Ausreichend): Ansätze von Überzeugungskraft; Begründung nicht immer stichhaltig.
    * 4 (Gut): Überzeugend und gut begründet; regt zum Nachdenken an.
    * 5 (Sehr gut): Äußerst stark und überzeugend; fundiert und differenziert.
"""
}

def get_ai_feedback(selected_question, user_text: str) -> str: #Sende den Text des Benutzers an die KI und gibt das generierte Feedback zurück

    combined_user_content = selected_question + user_text
    messages = [
        SYSTEM_PROMPT_TUTOR,
        {"role": "user", "content": combined_user_content}
    ]
    try:
        response = client.chat.completions.create( #Benutze ein LLM um zu interagieren
            model="gpt-4o-mini",
            messages=messages
        )
        return response.choices[0].message.content
    except AuthenticationError as e:
        logging.error(f"Authentifizierungsfehler: Dein API-Schlüssel ist wahrscheinlich ungültig oder widerrufen. Details: {e}")
    except APIConnectionError as e:
        logging.error(f"Verbindungsfehler: Konnte keine Verbindung zur OpenAI API herstellen. Details: {e}")
    except InternalServerError as e:
        logging.error(f"InternalServerError. Details: {e}")
    except Exception as e:
        logging.error(f"Ein unerwarteter Fehler ist aufgetreten: Details: {e}")

