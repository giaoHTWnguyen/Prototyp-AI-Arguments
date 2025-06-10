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

SYSTEM_PROMPT_TUTOR = {"role": "system", 
            "content": """Du bist ein KI-Tutor, der Formatives Feedback zu argumentativem Schreiben geben soll. 
            Das Ziel ist es, dem Lernenden zu helfen, ihre Prägnanz, Logik und Überzeugungskraft zu verbessern. Gebe stets 
            umsetzbare, klare und kritische Ratschläge
            """}

def get_ai_feedback(user_text: str) -> str: #Sende den Text des Benutzers an die KI und gibt das generierte Feedback zurück

    messages = [
        SYSTEM_PROMPT_TUTOR,
        {"role": "user", "content": user_text}
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

