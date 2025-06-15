discussion_questions = ["Ist Homeoffice die Zukunft der Arbeit?", 
                        "Sollten Schulen Drogentests für Schüler verpflichtend machen?",
                        "Ist der Lohnunterschied zwischen Männern und Frauen das Ergebnis von Diskriminierung?",
                        "Was ist wichtiger: Karriere oder Freizeit?",
                        "Ist es moralisch vertretbar, dass Klimaaktivisten sich auf den Straßen festkleben um auf die Klimakrise aufmerksam zu machen?",
                        "Sollte der Fleischkonsum reduziert oder sogar verboten werden, um Klimaziele zu erreichen und Tierleid zu mindern?",
                        "Angesichts der steigenden Zahl an Studierenden und akademischen Abschlüssen: Verliert ein Hochschulstudium zunehmend an Wert als Garant für beruflichen Erfolg und ein hohes Einkommen?",
                        "Muss in Deutschland die Förderung von Geschlechtervielfalt und LGBTIQ+- Rechten gestoppt werden, um traditionelle Familienwerte zu schützten?",
                        "Ist die Gendersprache in öffentlichen Einrichtungen und Schulen eine notwendige Weiterentwicklung für mehr Gleichberechtigung oder überflüssig?",
                        "Sollte die Todesstrafe für besonders schwere Verbrechen wieder eingeführt werden, um Gerechtigkeit zu schaffen und potenzielle Täter abzuschrecken?",
                        "Sollten wir Gene verändern dürfen, um Babys schlauer oder talentierter zu machen?"
                        ]

def choose_question() -> str: #Algorithmus zur Auswahl einer Frage aus dem Diskussionskatalog
    print("\n--- Verfügbare Diskussionsfragen ---")
    for i, question in enumerate(discussion_questions): #Iteration durch den Katalog, es wird eine ID zu jeder Frage gemappt für schnelleren Zugriff
        print(f"{i+1}. {question}")
    print("------------------------------")

    while True:
        try:
            chosen_id = int(input("\nBitte wähle die Nummer der Diskussionsfrage aus: "))
            if 1 <= chosen_id <= len(discussion_questions):
                choose_question = discussion_questions[chosen_id-1]
                print(f"\nDu hast gewählt: '{choose_question}'")
                return choose_question
            else:
                print("Ungültige Wahl. Bitte eine Nummer aus der Liste eingeben.")
        except ValueError:
            print("Ungültige Eingabe. Bitte gib eine Zahl ein")

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