from openai import OpenAI
from openai import APIConnectionError, AuthenticationError, InternalServerError
import os
from dotenv import load_dotenv

load_dotenv()

messageSystem = {"role": "system", 
            "content": """Du bist ein KI-Tutor, der Formatives Feedback zu argumentativem Schreiben geben soll. 
            Das Ziel ist es, dem Lernenden zu helfen, ihre Prägnanz, Logik und Überzeugungskraft zu verbessern. Gebe stets 
            umsetzbare, klare und kritische Ratschläge
            """}

messageUser = {"role": "user", "content": """Ich denke die Regierung sollte den Einsatz von Künstlicher Intelligenz regulieren, weil ich Angst habe, dass 
             die Menschheit auslöscht durch Skynet wie in Terminator.
             """}

try:
    client = OpenAI(api_key=os.getenv("OPENAI_API_KEY"))
    response = client.chat.completions.create(
        model="gpt-4o-mini",
        messages=[
            messageSystem,
            messageUser
        ],
    )
    print(response.choices[0].message.content)

except AuthenticationError as e:
    print(f"\nAuthentifizierungsfehler: Dein API-Schlüssel ist wahrscheinlich ungültig oder widerrufen.")
    print(f"Details: {e}")
except APIConnectionError as e:
    print(f"\nVerbindungsfehler: Konnte keine Verbindung zur OpenAI API herstellen.")
    print(f"Details: {e}")
except InternalServerError as e:
    print(f"\nInternalServerError")
    print(f"Details: {e}")
except Exception as e:
    print(f"\nEin unerwarteter Fehler ist aufgetreten:")
    print(f"Details: {e}")

