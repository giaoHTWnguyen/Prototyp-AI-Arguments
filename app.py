import streamlit as st
from api_handler import get_ai_rubric_scores, get_ai_feedback
from competition_logic import choose_question, calculate_final_score

from datetime import datetime