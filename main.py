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
    feedback = get_ai_feedback(user_argument)
    print("\n--- KI-Feedback ---")
    print(feedback)
    print("------------------")

    #4. Schleife für Überarbeitung und zweiter Nutzer-Workflow
    #5. Siegerermittlung

    print("\n--- Aktueller Workflow beendet. ----")

if __name__ == "__main__":
    main()