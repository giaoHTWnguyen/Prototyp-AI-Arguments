from openai import OpenAI
from openai import APIConnectionError, AuthenticationError, InternalServerError
import os
from dotenv import load_dotenv
import logging
import json


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

SYSTEM_PROMPT_RUBRIC_EVAL = {
    "role": "system",
    "content" : """Du bist ein KI-Assistent, der ausschließlich dazu dient, argumentative Texte anhand einer vorgegebenen Rubrik zu bewerten. "
    Deine Antwort muss **ausschließlich** ein JSON-Objekt sein, das die Punktzahlen von 0 bis 5 für jedes Kriterium enthält. Du darfst keinen weiteren Text oder Begründungen liefern.
    
    **Rubrik zur Analyse von Argumentationstexten:**

1.  **Logik & Kohärenz:**
    * 0 (Nicht vorhanden): Keine Argumentation gegeben
    * 1 (Ungenügend): Argumentation unlogisch, widersprüchlich oder chaotisch; keine klare Verbindung.
    * 2 (Mangelhaft): Logische Lücken oder kleinere Widersprüche; schwer nachvollziehbar.
    * 3 (Ausreichend): Grundlegende Logik erkennbar, aber kleine Schwächen.
    * 4 (Gut): Weitgehend logisch und kohärent; klarer Gedankengang.
    * 5 (Sehr gut): Durchweg schlüssig und stringent; alle Ideen klar und logisch verbunden.

2.  **Prägnanz & Klarheit:**
    * 0 (Nicht vorhanden): Keine Prägnanz & Klarheit gegeben
    * 1 (Ungenügend): Extrem weitschweifig, redundant oder irrelevant; Kernbotschaft verloren.
    * 2 (Mangelhaft): Oft zu langatmig oder wiederholt; Kernbotschaft schwer fassbar.
    * 3 (Ausreichend): Inhaltlich verständlich, aber könnte prägnanter sein.
    * 4 (Gut): Weitgehend prägnant und auf den Punkt gebracht; wenige unnötige Elemente.
    * 5 (Sehr gut): Äußerst prägnant und dicht; jedes Wort trägt zur Botschaft bei.

3.  **Überzeugungskraft & Argumentstärke:**
    * 0 (Nicht vorhanden): Keine Überzeugungskraft & Argumentstärke gegeben
    * 1 (Ungenügend): Schwach, unbelegt oder emotional/angreifend; keine Überzeugungskraft.
    * 2 (Mangelhaft): Wenig überzeugend, oberflächlich oder unzureichend begründet.
    * 3 (Ausreichend): Ansätze von Überzeugungskraft; Begründung nicht immer stichhaltig.
    * 4 (Gut): Überzeugend und gut begründet; regt zum Nachdenken an.
    * 5 (Sehr gut): Äußerst stark und überzeugend; fundiert und differenziert.
    
**Beispiel-JSON-Antwort**

    {
        "Logik_Kohärenz": 4,
        "Prägnanz_Klarheit": 3,
        "Überzeugungskraft_Argumentstärke": 5
    }
"""    
}


SYSTEM_PROMPT_TUTOR = {
    "role": "system",
    "content": """Du bist ein KI-Tutor, der dafür entwickelt wurde, formatives Feedback zu argumentativen Texten zu geben. Dein Ziel ist es, Studierenden dabei zu helfen, ihre Prägnanz, Logik und Überzeugungskraft zu verbessern.
    **Ton:** Achte immer auf einen klaren, ermutigenden und respektvollen Ton, bleib dennoch kritisch.
"""
}

SYSTEM_PROMPT_COMPARISON_TUTOR = {
    "role": "system",
    "content": """Du bist ein KI-Tutor, der darauf spezialisiert ist, eine **prägnante Schlussfolgerung** über die Entwicklung eines argumentativen Textes zu ziehen, indem du zwei Versionen vergleichst.

    **Deine Hauptaufgabe ist es, dem Nutzer auf den Punkt zu sagen, wie sich der Text verbessert oder verändert hat.**

    **Anweisungen zur Schlussfolgerung:**
    1.  Vergleiche den "Originaltext" mit dem "Überarbeiteten Text" unter dem Aspekt der **Gesamtentwicklung**.
    2.  Formuliere eine Schlussfolgerung, die zusammenfasst, ob und wie der überarbeitete Text in Bezug auf **Logik, Klarheit und Überzeugungskraft** besser geworden ist.
    3.  **Fokus auf das Ergebnis:** Beschreibe kurz 1-2 der **wesentlichsten Verbesserungen**, die zur positiven Entwicklung beigetragen haben.
    4.  **Vermeide detaillierte Vergleiche oder Aufzählungen einzelner Punkte.** Die Schlussfolgerung soll das Endergebnis des Vergleichs sein.
    **Ton:** Achte immer auf einen klaren, ermutigenden und respektvollen Ton, bleib dennoch kritisch.
    """
}


#Generische API-Aufruffunktion mit zentraler Fehlerbehebung
def _call_open_api(messages: list, model: str = "gpt-4o-mini", response_format: dict = None) -> str:
    try:
        completion_params = { #Parameter aus den Funktionen werden hier verarbeitet
            "model": model,
            "messages": messages
        }
        if response_format: #Prüfung ob ein spezifisches AUsgabeformat Parameter übergeben wurde, die if-Bedingunge stellt sicher, dass response format zu den completion_params hinzugefügt wird wenn es wirklich gebraucht wird
            completion_params["response_format"] = response_format

        response = client.chat.completions.create(**completion_params) #use ** before dictionary to unpack it
        return response.choices[0].message.content
    #Fehlerbehandlungen
    except AuthenticationError as e:
        logging.error(f"Authentifizierungsfehler: Dein API-Schlüssel ist wahrscheinlich ungültig oder widerrufen. Details: {e}")
    except APIConnectionError as e:
        logging.error(f"Verbindungsfehler: Konnte keine Verbindung zur OpenAI API herstellen. Details: {e}")
    except InternalServerError as e:
        logging.error(f"InternalServerError. Details: {e}")
    except Exception as e:
        logging.error(f"Ein unerwarteter Fehler ist aufgetreten: Details: {e}")

def get_ai_rubric_scores(user_text: str) -> dict: #Sende den Text des Benutzers an die KI und gibt das generierte Feedback zurück

    messages = [
        SYSTEM_PROMPT_RUBRIC_EVAL,
        {"role": "user", "content": user_text}
    ]
    
    full_response_content =  _call_open_api(messages, response_format={"type": "json_object"})

    try:  #Prozess um die Informationen der Kriterien und Scores der Rubrik von JSON in ein Python Dictionary zu speichern      
        json_start = full_response_content.find('{')
        json_end = full_response_content.find('}') + 1 #+1 um die schließende Klammer mitzunehmen
        if json_start != -1 and json_end != -1 and json_start < json_end:
            json_part = full_response_content[json_start:json_end]
            rubric_scores = json.loads(json_part) #parse JSON string and convert into Python Dictionary
            return rubric_scores
        
        else:
            return {}, full_response_content
    except json.JSONDecoder as jde:
        logging.error(f"Fehler beim Parsen des JSON-Feedbacks von der KI: {jde}. Antwort war: {full_response_content}")
        return {}, full_response_content

def get_ai_comparison_feedback(question:str, original_argument: str, revised_argument: str) -> str: #Sende den Text des Benutzers an die KI und gibt das generierte Feedback zurück

    user_content = f"""
        Diskussionsfrage:
        {question}
        Ursprüngliche Argumentation:
        {original_argument}
        Überarbeitete Argumentation:
        {revised_argument}
    """

    messages = [
        SYSTEM_PROMPT_COMPARISON_TUTOR,
        {"role": "user", "content": user_content}
    ]
    return _call_open_api(messages=messages)

def get_ai_feedback(user_text: str) -> str: #Sende den Text des Benutzers an die KI und gibt das generierte Feedback zurück

    messages = [
        SYSTEM_PROMPT_TUTOR,
        {"role": "user", "content": user_text}
    ]
    return _call_open_api(messages=messages )
