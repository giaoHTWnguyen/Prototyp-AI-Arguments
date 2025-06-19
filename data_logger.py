import json
from datetime import datetime
import os
import logging

DATA_FILE_JSONL = "feedback_data.jsonl"

def log_feedback_data(text_version: str, timestamp: datetime, user_id: str, question: str, argument: str, feedback: str, rubric_scores: dict, overall_score: int):

    timestamp_str = timestamp.strftime("%Y-%m-%d %H:%M:%S")  #JSON kann keine datetime-Objekte direkt speichern
    #Extraktion der Scores aus dem Dictionary
    record = {
        "text_version": text_version,
        "timestamp": timestamp_str,
        "user_id": user_id,
        "rubric_scores": rubric_scores,
        "overall_score": overall_score,
        "question": question,
        "argument": argument,
        "feedback": feedback
    }

    #Öffnet und Erstelle die JSONL-Datei im Anhangmodus, Initialisierung eines Writers, der Dictionary versteht, schreibt eine Header-Zeile, falls die Datei neu ist 
    try:
        with open(DATA_FILE_JSONL, mode='a', newline='', encoding='utf-8') as file: #Kontext Manager zum korrenten Schließen von der JSONL-Datei, Mode a bedeutet Anhängen, falls Datei schon existiert einfach Werte anhängen
            file.write(json.dumps(record, ensure_ascii=False) + '\n')
        logging.info(f"Daten in {DATA_FILE_JSONL} geloggt.")
    except Exception as e:
        logging.error(f"Fehler beim Schreiben in {DATA_FILE_JSONL}: {e}")
