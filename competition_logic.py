discussion_questions_categorized = {
    "Arbeitswelt & Technologie": [
        "Ist Homeoffice die Zukunft der Arbeit?",
        "Verliert ein Hochschulstudium an Wert für den Berufserfolg?",
        "Sollten wir Gene verändern, um Babys zu optimieren?",
        "Kann künstliche Intelligenz menschliche Arbeit komplett ersetzen?"
    ],
    "Gesellschaft & Ethik": [
        "Sollten Schulen Drogentests für Schüler einführen?",
        "Sind Klima-Protest-Blockaden moralisch vertretbar?",
        "Sollte Fleischkonsum zur Erreichung von Klimazielen reduziert werden?",
        "Sollte die Todesstrafe für schwere Verbrechen wiedereingeführt werden?"
    ],
    "Gleichberechtigung & Vielfalt (Geschlechtervielfalt, LGBTIQ+-Rechte)": [
        "Wird der Lohnunterschied zwischen Männern und Frauen verursacht durch Diskriminierung?",
        "Muss die Förderung von Vielfalt auch traditionelle Familienwerte schützen?",
        "Ist Gendersprache eine nötige Entwicklung oder überflüssig?",
        "Ist die Einführung von Quoten ein effektives oder notwendiges Mittel, um Gleichheit der Geschlechter zu erreichen?"
    ],
    "Persönliche Werte": [
        "Ab wann sollte ein junger Mensch das Elternhaus verlassen und wer entscheidet darüber?",
        "Bremsen Traditionen die persönliche Entfaltung?",
        "Sollte man immer die Wahrheit sagen, auch wenn sie verletzend ist?",
        "Ist Geld der Schlüssel zum Glück?",
        "Nimmt die Gründung einer Familie die persönliche Freiheit?"
    ]
}

#Choose_question: Funktion wird nicht mehr genutzt!!! --> iteration aller Frage im Terminal
# def choose_question() -> str: #Algorithmus zur Auswahl einer Frage aus dem Diskussionskatalog
#     print("\n--- Verfügbare Diskussionsfragen ---")
#     for i, question in enumerate(discussion_questions): #Iteration durch den Katalog, es wird eine ID zu jeder Frage gemappt für schnelleren Zugriff
#         print(f"{i+1}. {question}")
#     print("------------------------------")

#     while True:
#         try:
#             chosen_id = int(input("\nBitte wähle die Nummer der Diskussionsfrage aus: "))
#             if 1 <= chosen_id <= len(discussion_questions):
#                 choose_question = discussion_questions[chosen_id-1]
#                 print(f"\nDu hast gewählt: '{choose_question}'")
#                 return choose_question
#             else:
#                 print("Ungültige Wahl. Bitte eine Nummer aus der Liste eingeben.")
#         except ValueError:
#             print("Ungültige Eingabe. Bitte gib eine Zahl ein")

def get_user_argumentation() -> str:
    print("\nBitte schreibe deine Argumentation:")
    return input("Dein Text: ")


def calculate_final_score(rubric_scores: dict) -> int: #Hier wird die Gewichtung der Kriterien aus dem Rubrik zusammengerechnet. Eine eigene Gewichtung zu berechnen ist besser, um damit die Halluzination und Rechenkraft der LLM zu senken
    #Gewichtung
    gewichtung_logik = 0.45
    gewichtung_praegnanz = 0.20
    gewichtung_ueberzeugungskraft = 0.35

    #Extraktion der Kriterien aus dem Dictionary (wurde aus der JSON Datei umgewandelt)
    logik_score = rubric_scores.get("Logik_Kohärenz", 0)
    praegnanz_score = rubric_scores.get("Prägnanz_Klarheit", 0)
    ueberzeugungskraft_score = rubric_scores.get("Überzeugungskraft_Argumentstärke", 0)

    max_score_per_criterion = 5

    total_score = ( #Gesamtberechnung
        (logik_score / max_score_per_criterion) * gewichtung_logik +
        (praegnanz_score / max_score_per_criterion) * gewichtung_praegnanz +
        (ueberzeugungskraft_score / max_score_per_criterion) * gewichtung_ueberzeugungskraft
    )

    #Skalierung auf 100
    final_score_100 = round(total_score * 100)
    return final_score_100



#Funktion Nutzer Workflow und Siegerermittlung