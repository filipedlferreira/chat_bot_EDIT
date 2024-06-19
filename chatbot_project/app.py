import streamlit as st
from PIL import Image
import base64
from io import BytesIO
from datetime import datetime
import os
from chatbot import get_answer
from app_functions import image_to_base64, display_logo_and_title, display_gif, display_chat_history, display_intro

# Constants
PAGE_TITLE = "EDIT. - EditAssist"
PAGE_ICON = "logo.jpeg"
LAYOUT = "centered"

# Configure the page
st.set_page_config(
    page_title=PAGE_TITLE,
    page_icon=PAGE_ICON,
    layout=LAYOUT
)

logo_file_path = os.path.join(os.path.dirname(__file__), "logo.jpeg")

try:
    # Load the logo image
    logo_image = Image.open(logo_file_path)
except FileNotFoundError:
    print(f"Error: Logo file not found at {logo_file_path}")
    logo_image = None

# Initialize session state with default values
st.session_state.setdefault("history", [])
st.session_state.setdefault("question", "")

# Initialize the interface
display_intro(logo_image = logo_image)

# Display chat history
display_chat_history()

# Form to submit questions
with st.form(key="question_form", clear_on_submit=True):
    question = st.text_area(" ", value=st.session_state.question, height=150, max_chars=1000, key="question_input_app", label_visibility='collapsed')
    submit_button = st.form_submit_button(label="Enviar")

# Process form submission
if submit_button and question:
    current_time_question = datetime.now().strftime("%H:%M")
    answer = get_answer(question)
    current_time_answer = datetime.now().strftime("%H:%M")
    st.session_state.history.append((f"Eu: {question}", current_time_question))
    st.session_state.history.append((f"EditAssist: {answer}", current_time_answer))
    st.session_state.question = ""
    st.rerun()

# Informações adicionais
st.markdown("""
<div style="text-align: justify;">
    <strong>Os dados pessoais aqui fornecidos e os conteúdos das suas conversações no chat da EDIT serão tratados e conservados com a finalidade de gestão e resolução dos seus pedidos, reclamações, sugestões e para avaliação da qualidade do serviço de chat. O conteúdo pode ser gerado por Inteligência Artificial. Para ter mais informação sobre a forma como a EDIT trata os seus dados consulte a nossa <a href="#">Declaração de Privacidade</a>.</strong>
</div>
""", unsafe_allow_html=True)

# Estilos adicionais
st.markdown("""
<style>
    .stButton button {
        background-color: #003366;
        color: white;
        font-size: 16px;
        padding: 10px 24px;
        border-radius: 8px;
        border: none;
    }
    .gif-container {
        display: flex;
        justify-content: center;
    }
    .stTextInput textarea {
        font-size: 16px;
        padding: 10px;
        border-radius: 8px;
        border: 1px solid #ffffff;
        margin-bottom: 0px; 
    }
    .stImage img {
        display: block;
        margin-left: auto;
        margin-right: auto;
    }
    .stImage figcaption {
        color: white !important;
        text-align: center;
    }
    .header {
        text-align: center;
        color: white;
    }
    .subheader {
        font-size: 20px;
        color: #4CAF50;
    }
    /* Shared styles for both user and bot messages */
    .message-content {
        padding: 10px;
        border-radius: 15px;
        display: inline-block;
        max-width: 80%;
        box-shadow: 0px 1px 3px rgba(0, 0, 0, 0.2);
    }

    /* User message styles */
    .user-message {
        text-align: right;
    }
    .user-message .message-content {
        /* Add user message background color here */
    }
    .user-message .message-time {
        align-self: flex-end;
    }

    /* Bot message styles */
    .bot-message {
        text-align: left;
        align-items: flex-start;
    }
    .bot-message .message-content {
        background-color: #B8E6C1;
    }
    .bot-message .message-time {
        align-self: flex-start;
    }

    /* Shared time style */
    .message-time {
        font-size: 12px;
        color: #999;
        margin-top: 5px;
    }
    </style>
""", unsafe_allow_html=True)
