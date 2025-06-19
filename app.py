#streamlit_app-p
#https://docs.streamlit.io/develop/api-reference

import streamlit as st

from datetime import datetime
import uuid

#Backend-Logik importieren aus anderen Dateien

from api_handler import get_ai_feedback, get_ai_rubric_scores
from competition_logic import discussion_questions_categorized, get_user_argumentation, calculate_final_score
from data_logger import log_feedback_data

# Streamlit App Konfiguration

st.set_page_config(page_title="Argumentations-Tutor KI", layout="wide")
st.title("🗣️ KI-Argumentations-Tutor und Feedback-System")
st.markdown("Verbessere deine schriftliche Argumentation und Ideen mit intelligentem Feedback!")

# Session State Management
# Die States (Zustände) zwischen Interaktionen und Seiten-Reloads müssen persistiert werden, Streamlit führt bei jeder Interaktion das Skript neu au, wodurch normale Variablen ihren Inhalt verlieren
# normalerweise haben die meisten Frameworks State im Client oder Server, aber Streamlit ist keine klassische Web App sondern eher eine Skript Engine die auf alles reagiert
# Müssen also ein persistent Dictionary anlegen, um nicht die Variablen zu verlieren

if 'user_id' not in st.session_state:
    st.session_state.user_id = str(uuid.uuid4()) #Genriert eine einmalige ID pro Browsersitzung
    st.info(f"Aktuelle Benutzer-ID: {st.session_state.user_id}")

# Initialisierung aller benötigten Session State Variablen
if 'selected_question' not in st.session_state:
    st.session_state.selected_question = ""
if 'original_argument' not in st.session_state:
    st.session_state.original_argument = ""
if 'current_argument' not in st.session_state: # Hält den Text, der gerade angezeigt/bearbeitet wird
    st.session_state.current_argument = ""
if 'initial_feedback_generated' not in st.session_state:
    st.session_state.initial_feedback_generated = False
if 'rubric_scores' not in st.session_state:
    st.session_state.rubric_scores = {}
if 'overall_score' not in st.session_state:
    st.session_state.overall_score = 0
if 'detailed_feedback' not in st.session_state:
    st.session_state.detailed_feedback = ""
if 'rubric_scores_revised' not in st.session_state:
    st.session_state.rubric_scores_revised = {}
if 'overall_score_revised' not in st.session_state:
    st.session_state.overall_score_revised = 0
if 'detailed_feedback_revised' not in st.session_state:
    st.session_state.detailed_feedback_revised = ""
if 'revision_mode' not in st.session_state:
    st.session_state.revision_mode = False # Steuert, ob der Revisionsbereich angezeigt wird
#if 'comparison_feedback' not in st.session_state:
#    st.session_state.comparison_feedback = ""

# Diskussionsfrage auswählen

st.subheader("1. Wähle eine Diskussionsfrage")

category_options = ["--- Wähle eine Kategorie ---"] + list(discussion_questions_categorized.keys())

selected_category_from_dropdown = st.selectbox(
    "Verfügbare Kategorien:",
    category_options,
    key="question_selector",
    index=0
)
#Aktualisiert die ausgewählte Kategorie im Session State
if selected_category_from_dropdown != "--- Wähle eine Kategorie ---":
    st.session_state.selected_category = selected_category_from_dropdown
else:
    st.session_state.selected_category = ""
    st.session_state.selected_question = ""

# Dynamische Anzeige der Frage basierend auf der Kategorie

if st.session_state.selected_category:
    question_in_category = discussion_questions_categorized[st.session_state.selected_category]
    question_display_options = ["--- Wähle eine Frage ---"] + question_in_category

    selected_question_from_dropdown = st.selectbox(
        "Wähle eine Frage:",
        question_display_options,
        key="question_selector_by_category", #eindeutiger Schlüssel für dieses Widget
        index = 0
    )
    #Frage aktualisieren im Session State
    if selected_question_from_dropdown != "--- Wähle eine Frage ---":
        st.session_state.selected_question = selected_question_from_dropdown
    else:
        st.session_state.selected_question = ""
else:
    st.selectbox(
        "Wähle eine Frage",
        ["--- Bitte zuerst eine Kategorie wählen"],
        key="question_selector_placeholder",
        disabled=True #Widget deaktivieren
    )
    st.session_state.selected_question = ""

# 2. Argumentation eingeben

st.subheader("2. Schreibe oder füge deine Argumentation ein")

user_argumentation_input = st.text_area(
    "Dein Text:",
    value=st.session_state.current_argument,
    height=200,
    help="Schreibe hier deine Argumentation, zu der du ein Feedback erhalten möchtest.",
    key="initial_argument_input"
)

# Button Anforderung Feedback

if st.button("Feedback zur ersten Version erhalten", key="get_initial_feedback_btn"):
    #Validierung: Prüfung ob eine Frage ausgewählt ist und Text eingegeben wurde
    if not st.session_state.selected_question or st.session_state.selected_question.startswith("---"):
        st.warning("Bitte wähle zuerst eine Diskussionsfrage aus.")
    elif not user_argumentation_input:
        st.warning("Bitte gib deinen Argumentationstext ein.")
    else:
        # Initialen Text speichern und ihn als aktuellen Text setzen
        st.session_state.original_argument = user_argumentation_input
        st.session_state.current_argument = user_argumentation_input

        #Kombination Frage und Argumentation für KI
        with st.spinner("Sende Text an KI für Feedback ... Dies wird einen kleinen Moment dauern."):
            full_user_input_for_ai =f"Diskussionsfrage: '{st.session_state.selected_question}'\n\nMeine ÜBERARBEITETE Argumentation:\n{st.session_state.current_argument}"

            #Rubrik Scores holen
            st.session_state.rubric_scores = get_ai_rubric_scores(full_user_input_for_ai)
            st.session_state.detailed_feedback = get_ai_feedback(full_user_input_for_ai)

            #Gesamtscore Berechnen
            if st.session_state.rubric_scores:
                st.session_state.overall_score = calculate_final_score(st.session_state.rubric_scores)
            else:
                st.session_state.overall_score = 0 #Standardwert bei Fehler
            
            #Marker, dass initiales Feedback generiert wurde und Revisionsmodus aktivieren
            st.session_state.initial_feedback_generated = True
            st.session_state.revision_mode = True
        
        st.success("Feedback generiert!")

        # Logge initialen Daten in JSONL-Datei

        log_feedback_data(
            text_version="Initial",
            timestamp=datetime.now(),
            user_id=st.session_state.user_id,
            question=st.session_state.selected_question,
            argument=st.session_state.original_argument, # Logge den originalen Text
            feedback=st.session_state.detailed_feedback,
            rubric_scores=st.session_state.rubric_scores,
            overall_score=st.session_state.overall_score,
            #comparison_feedback=None # Für die erste Version gibt es kein Vergleichs-Feedback
        )
        st.sidebar.success("Initiale Daten geloggt!")
        #st.rerun() #Rerun triggern, damit Feedback-Anzeige sofort erscheint
    
    # Anzeige Feedback
    if st.session_state.initial_feedback_generated:
        st.subheader("3. Dein KI-Feedback")

        st.markdown("--- Rubrik-Bewertung ---")
        if st.session_state.rubric_scores:
            for criterion, score in st.session_state.rubric_scores.items():
                st.write(f"**{criterion.replace('_', ' ')}:** {score}/5") # Ersetzt Unterstriche für bessere Lesbarkeit
            st.success(f"**Gesamtnote für die Argumentation:** {st.session_state.overall_score} von möglichen 100 Punkten.")
        else:
            st.error("Rubrik-Bewertung konnte nicht extrahiert werden oder ein Fehler ist aufgetreten.")
        #Detailliertes Feedback anzeigen
        st.markdown("### Detailliertes Feedback")
        st.info(st.session_state.detailed_feedback)

# 4. Überarbeitung anbieten
if st.session_state.revision_mode:
    st.subheader("4. Überarbeite deinen Text")

     # Textbereich für die überarbeitete Version, mit dem aktuellen Text als Startpunkt
    revised_argument_input = st.text_area(
        "Deine überarbeitete Version des Textes:", 
        value=st.session_state.current_argument, #Speichere das originelle Argument um es direkt hier zu bearbeiten
        height=200, 
        key="revised_text_area", # Eindeutiger Schlüssel
        help="Nimm das Feedback der KI auf und überarbeite deinen Text hier." #Tooltip
    )

    #Button zum Anfordern des Feedbacks zur Überarbeitung

    if st.button("Feedback zur überarbeiteten Version erhalten", key="get_revised_feedback_btn"):
        if not revised_argument_input:
            st.warning("Bitte gib deinen überarbeiteten Text ein.")
        else:
            st.session_state.current_argument = revised_argument_input #Aktualisiert den aktuellen Text
            with st.spinner("Sende überarbeiteten Text an KI für Feedback und Vergleich... Dies kann einen Moment dauern."):
                full_user_input_for_ai_revised = f"Diskussionsfrage: '{st.session_state.selected_question}'\n\nMeine ÜBERARBEITETE Argumentation:\n{st.session_state.current_argument}"
                #Rubric Scores und Feedback holen
                st.session_state.rubric_scores_revised = get_ai_rubric_scores(full_user_input_for_ai_revised)
                st.session_state.detailed_feedback_revised = get_ai_feedback(full_user_input_for_ai_revised)

                #<--- hier Vergleichsfeedback einbauen
                st.session_state.overall_score_revised = 0
                if st.session_state.rubric_scores_revised:
                    st.session_state.overall_score_revised = calculate_final_score(st.session_state.rubric_scores_revised)
                    st.subheader("--- Rubrik-Bewertung (Überarbeitet) ---")
                    if st.session_state.rubric_scores_revised:
                        for criterion, score in st.session_state.rubric_scores_revised.items():
                            st.write(f"**{criterion.replace('_', ' ')}:** {score}/5")
                        st.success(f"**Gesamtnote (Überarbeitet):** {st.session_state.overall_score_revised} von möglichen 100 Punkten.")
                else:
                    st.error("Rubrik-Bewertung für Überarbeitung konnte nicht extrahiert werden.")
                st.subheader("--- Detailliertes KI-Feedback zur Überarbeitung ---")
                st.info(st.session_state.detailed_feedback_revised)

                log_feedback_data(
                    text_version="Revised",
                    timestamp=datetime.now(),
                    user_id=st.session_state.user_id,
                    question=st.session_state.selected_question,
                    argument=st.session_state.current_argument, # Logge den überarbeiteten Text
                    feedback=st.session_state.detailed_feedback_revised,
                    rubric_scores=st.session_state.rubric_scores_revised,
                    overall_score=st.session_state.overall_score_revised,
                    #comparison_feedback=None # Für die erste Version gibt es kein Vergleichs-Feedback
                )
                st.sidebar.success("Revised Daten geloggt!")
                st.success("Überarbeitungsprozess abgeschlossen!")
                st.session_state.revision_mode = False #Revisionsmodus deaktivieren
# Seitenlisten Elemente

st.sidebar.markdown("---")
# Button zum Zurücksetzen der App-Sitzung
if st.sidebar.button("Neue Sitzung starten", key="reset_btn"):
    st.session_state.clear()
    st.rerun()

st.sidebar.markdown("---")
st.sidebar.header("Über diese App")
st.sidebar.info("Dies ist ein KI-gestützter Tutor zur Verbesserung der Argumentationsfähigkeiten.")
