discussion_questions = ["Ist Homeoffice die Zukunft der Arbeit?", 
                        "Sollten Schulen Drogentests für Schüler verpflichtend machen?",
                        "Ist der Lohnunterschied zwischen Männern und Frauen das Ergebnis von Diskriminierung?",
                        "Sollten wir die Entwicklung von autonomer KI stärker regulieren oder sogar stoppen?",
                        "Sollte eine 4-Tage-Woche flächendeckend eingeführt werden, auch wenn das potenziell weniger Lohn bedeuten könnte? Was ist wichtiger: Karriere oder Freizeit?",
                        "Ist es moralisch vertretbar, dass Klimaaktivisten durch Aktionen wie das Festkleben auf den Straßen oder das Besprühen von Kunstwerken den Alltag stören und Sachschaden verursachen,"
                        "um auf die Klimakrise aufmerksam zu machen?",
                        "Sollte der Fleischkonsum aus ökologischen und ethischen Gründen drastisch reduziert oder sogar verboten werden, um Klimaziele zu erreichen und Tierleid zu mindern?",
                        "Angesichts der steigenden Zahl an Studierenden und akademischen Abschlüssen: Verliert ein Hochschulstudium zunehmend an Wert als Garant für beruflichen Erfolg und ein hohes Einkommen?",
                        "Muss in Deutschland die Förderung von Geschlechtervielfalt und LGBTIQ+- Rechten gestoppt werden, um traditionelle Familienwerte zu schützten?",
                        "Ist die Gendersprache in öffentlichen Einrichtungen und Schulen eine notwendige Weiterentwicklung für mehr Gleichberechtigung oder überflüssig?",
                        "Sollte die Todesstrafe für besonders schwere Verbrechen wieder eingeführt werden, um Gerechtigkeit zu schaffen und potenzielle Täter abzuschrecken?",
                        "Sollten wir Gene verändern dürfen, um Babys schlauer oder talentierter zu machen?"
                        ]
from api_handler import get_ai_feedback

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


def user_revision_workflow(max_revisions: int = 2) -> str: #Prozess zur Überarbeitung der Argumentation

    current_argumentation = get_user_argumentation()
    for i in range(max_revisions):
        print(f"\n--- Runde {i+1} von {max_revisions}: Feedback erhalten ---")
        # Hole Feedback von der KI
        feedback = get_ai_feedback(current_argumentation)
        print("\n --- KI-Feedback ---")
        print(feedback)
        print("------------")
#Funktion Nutzer Workflow und Siegerermittlung