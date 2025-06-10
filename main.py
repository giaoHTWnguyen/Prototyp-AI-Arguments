from openai import OpenAI
from openai import APIConnectionError, AuthenticationError, InternalServerError
import os
from dotenv import load_dotenv
import logging


load_dotenv()
logging.basicConfig(level=logging.ERROR, format='%(asctime)s - %(levelname)s - %(message)s')


OPENAI_API_KEY = os.getenv("OPENAI_API_KEY")
if not OPENAI_API_KEY:
    raise ValueError("OPENAI_API_KEY wurde nicht in den Umgebungsvariablen gefunden. Bitte stelle sicher, dass deine .env-Datei korrekt ist.")

SYSTEM_PROMPT = {"role": "system", 
            "content": """Du bist ein KI-Tutor, der Formatives Feedback zu argumentativem Schreiben geben soll. 
            Das Ziel ist es, dem Lernenden zu helfen, ihre Prägnanz, Logik und Überzeugungskraft zu verbessern. Gebe stets 
            umsetzbare, klare und kritische Ratschläge
            """}

discussion_questions = ["Was geht", 
                        ""]

user_argumentation = input("Dein Text: ")
USER_PROMPT = {"role": "user", "content": user_argumentation}

try:
    client = OpenAI(api_key=OPENAI_API_KEY)
    response = client.chat.completions.create(
        model="gpt-4o-mini",
        messages=[
            SYSTEM_PROMPT,
            USER_PROMPT
        ],
    )
    print("\n--- KI-Feedback ---")
    print(response.choices[0].message.content)
    print("---------------------")

except AuthenticationError as e:
    logging.error(f"Authentifizierungsfehler: Dein API-Schlüssel ist wahrscheinlich ungültig oder widerrufen. Details: {e}")
except APIConnectionError as e:
    logging.error(f"Verbindungsfehler: Konnte keine Verbindung zur OpenAI API herstellen. Details: {e}")
except InternalServerError as e:
    logging.error(f"InternalServerError. Details: {e}")
except Exception as e:
    logging.error(f"Ein unerwarteter Fehler ist aufgetreten: Details: {e}")

