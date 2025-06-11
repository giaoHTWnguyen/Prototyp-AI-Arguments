from api_handler import get_ai_feedback
from competition_logic import choose_question, get_user_argumentation

def main():
    print("--- Willkommen beim Argumentations-Tutor und Wettbewerb")
    #1. Benutzer wählt eine Diskussionsfrage
    selected_question = choose_question()
    #2. Argumentation eingeben
    user_argument = get_user_argumentation()

    #3. KI Feedback erhalten
    print("\n--- Sende Text an KI für Feedback.... ---")
    feedback = get_ai_feedback(selected_question, user_argument)
    print("\n--- KI-Feedback ---")
    print(feedback)
    print("------------------")

    #Anbieten Überarbeitung der Argumentation
    while True:
        decision = input("\nMöchtest du deinen Text überarbeiten? (ja/nein): ").lower().strip()
        if decision == 'ja':
            print("\nBitte gib deinen überarbeiteten Text ein:")
            current_argument = input("dein überarbeiteter Text: ")
            print("\n--- Sende Text an KI für Feedback.... ---")
            feedback = get_ai_feedback(selected_question, current_argument)

            print("\n--- KI-Feedback zur Überarbeitung ---")
            print(feedback)
            print("-------------------------------------")
        elif decision == 'nein':
            print("\nDu hast dich gegen eine Überarbeitung entschieden. Der Workflow wird hiermit beendet.")
            break
        else:
            print("Ungültige Eingabe. Bitte antworte mit 'ja' oder 'nein'.")

    #4. Schleife für Überarbeitung und zweiter Nutzer-Workflow
    #5. Siegerermittlung

    print("\n--- Aktueller Workflow beendet. ----")

if __name__ == "__main__":
    main()