from api_handler import get_ai_feedback, get_ai_rubric_scores
from competition_logic import choose_question, get_user_argumentation, calculate_final_score
from data_logger import log_feedback_data
from datetime import datetime
import uuid

def main():
    print("--- Willkommen beim Argumentations-Tutor und Wettbewerb ---")
    user_id = str(uuid.uuid4())
    # 1. Benutzer wählt eine Diskussionsfrage
    selected_question = choose_question()

    # 2. Argumentation eingeben
    current_argument = get_user_argumentation()

    # 3. KI Feedback erhalten (erste Runde)1
    print("\n--- Sende Text an KI für Feedback.... ---")
    
    # Kombiniere Frage und Argumentation für die KI
    full_user_input_for_ai = f"Diskussionsfrage: '{selected_question}'\n\nMeine Argumentation:\n{current_argument}"
    
    # NEU: Erhalte Rubrik-Scores und detailliertes Feedback separat
    
    rubric_scores = get_ai_rubric_scores(full_user_input_for_ai)
    detailed_feedback = get_ai_feedback(full_user_input_for_ai)

    # Zeige die Rubrik-Bewertung an
    if rubric_scores:
        print("\n--- Rubrik-Bewertung ---")
        for criterion, score in rubric_scores.items():
            print(f"{criterion.replace('_', ' ')}: {score}/5") # Schöner ausgeben
        
        # Berechne und zeige die Gesamtnote
        overall_score = calculate_final_score(rubric_scores)
        print(f"\nGesamtnote für die Argumentation: {overall_score} von möglichen 100 Punkten.")
    else:
        print("\n--- Rubrik-Bewertung konnte nicht extrahiert werden. ---")

    # Zeige das detaillierte Feedback an
    print("\n--- Detailliertes KI-Feedback ---")
    print(detailed_feedback)
    print("---------------------------------")
    log_feedback_data("Initial", datetime.now(), user_id, selected_question, current_argument, detailed_feedback, rubric_scores, overall_score)

    # 4. Überarbeitung anbieten (eine Runde)
    while True:
        decision = input("\nMöchtest du deinen Text überarbeiten? (ja/nein): ").lower().strip()
        
        if decision == 'ja':
            print("\nBitte gib deinen überarbeiteten Text ein:")
            current_argument = input("Dein überarbeiteter Text: ")
            
            # Hole erneut Feedback für den überarbeiteten Text
            print("\n--- Sende überarbeiteten Text an KI für Feedback... ---")
            full_user_input_for_ai = f"Diskussionsfrage: '{selected_question}'\n\nMeine ÜBERARBEITETE Argumentation:\n{current_argument}"

            rubric_scores_revised = get_ai_rubric_scores(full_user_input_for_ai)
            detailed_feedback_revised = get_ai_feedback(full_user_input_for_ai)

            if rubric_scores_revised:
                print("\n--- Rubrik-Bewertung (Überarbeitet) ---")
                for criterion, score in rubric_scores_revised.items():
                    print(f"{criterion.replace('_', ' ')}: {score}/5")
                overall_score_revised = calculate_final_score(rubric_scores_revised)
                print(f"\nGesamtnote (Überarbeitet): {overall_score_revised} von möglichen 100 Punkten.")
            else:
                print("\n--- Rubrik-Bewertung für Überarbeitung konnte nicht extrahiert werden. ---")
            
            print("\n--- Detailliertes KI-Feedback zur Überarbeitung ---")
            print(detailed_feedback_revised)
            print("-----------------------------------------------------")
            log_feedback_data("Revised", datetime.now(), user_id, selected_question, current_argument, detailed_feedback_revised, rubric_scores_revised, overall_score_revised)
            break
            
        elif decision == 'nein':
            print("\nDu hast dich gegen eine Überarbeitung entschieden. Dein aktueller Text wird verwendet.")
            break
        else:
            print("Ungültige Eingabe. Bitte antworte mit 'ja' oder 'nein'.")

    print("\n--- Aktueller Workflow beendet. ----")

if __name__ == "__main__":
    main()

    