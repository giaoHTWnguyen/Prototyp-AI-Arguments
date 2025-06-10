discussion_questions = ["Ist Homeoffice die Zukunft der Arbeit?", 
                        ""]

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

#Funktion Nutzer Workflow und Siegerermittlung