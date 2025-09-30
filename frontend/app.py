import streamlit as st
import requests

# ---------- Configuration ----------
API_URL = "http://127.0.0.1:8000/chat"  # FastAPI backend URL
st.set_page_config(page_title="🤖 LangGraph Chatbot", page_icon="🤖", layout="wide")

# ---------- Page Title ----------
st.markdown(
    """
    <h1 style='text-align: center; color: #4B8BBE;'>
        🤖 LangGraph Chatbot
    </h1>
    <p style='text-align: center; color: #306998; font-size: 16px;'>
        Ask questions and get smart AI answers in real-time!
    </p>
    """,
    unsafe_allow_html=True
)

# ---------- Chat History ----------
if "history" not in st.session_state:
    st.session_state.history = []

# Scrollable chat container
chat_container = st.container()

# ---------- User Input ----------
with st.form(key="chat_form", clear_on_submit=True):
    user_input = st.text_input("Type your message here...")
    submit_button = st.form_submit_button(label="Send")

if submit_button and user_input:
    try:
        response = requests.post(API_URL, json={"user_message": user_input})
        ai_reply = response.json().get("reply", "Sorry, no response received.")
    except Exception as e:
        ai_reply = f"Error: {e}"

    st.session_state.history.append(("You", user_input))
    st.session_state.history.append(("Bot", ai_reply))

# ---------- Display Chat History ----------
for speaker, msg in st.session_state.history:
    if speaker == "You":
        st.markdown(
            f"<div style='text-align: right; background-color:#FFD7BA; padding:10px; border-radius:10px; margin:5px 0;'>"
            f"**{speaker}:** {msg}</div>",
            unsafe_allow_html=True
        )
    else:
        st.markdown(
            f"<div style='text-align: left; background-color:#BAE1FF; padding:10px; border-radius:10px; margin:5px 0;'>"
            f"**{speaker}:** {msg}</div>",
            unsafe_allow_html=True
        )
