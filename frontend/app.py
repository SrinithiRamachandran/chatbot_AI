import streamlit as st
import requests

API_URL = "http://127.0.0.1:8000/chat"  # FastAPI backend URL

st.title("🤖 LangGraph + FastAPI + Streamlit Chatbot")

if "history" not in st.session_state:
    st.session_state.history = []

user_input = st.text_input("You: ", "")

if st.button("Send"):
    if user_input:
        try:
            response = requests.post(API_URL, json={"user_message": user_input})
            ai_reply = response.json()["reply"]
        except Exception as e:
            ai_reply = f"Error: {e}"

        st.session_state.history.append(("You", user_input))
        st.session_state.history.append(("Bot", ai_reply))

# Show chat history
for speaker, msg in st.session_state.history:
    st.write(f"**{speaker}:** {msg}")
