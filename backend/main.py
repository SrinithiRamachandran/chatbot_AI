# main.py
from fastapi import FastAPI
from pydantic import BaseModel
import requests
import os
from graph import create_graph

# ----------------------------
# FastAPI App
# ----------------------------
app = FastAPI()

# Load Gemini API Key (fallback to hardcoded key if not set in env)
GEMINI_API_KEY = os.getenv(
    "GOOGLE_API_KEY",
    "AIzaSyCXipWpOymOU1hlH6OIaptrtei2mR6pbUg"
)

# Compile LangGraph state
graph = create_graph()
graph_state = graph.compile()

# Request schema
class ChatRequest(BaseModel):
    user_message: str

@app.post("/chat")
async def chat(req: ChatRequest):
    user_msg = req.user_message

    # Correct Gemini endpoint (make sure model exists)
    model = "gemini-2.5-flash"  # or "gemini-pro-latest"
    url = f"https://generativelanguage.googleapis.com/v1beta/models/{model}:generateContent?key={GEMINI_API_KEY}"

    # ✅ Correct payload format
    payload = {
        "contents": [
            {
                "role": "user",
                "parts": [{"text": user_msg}]
            }
        ],
        "generationConfig": {
            "temperature": 0.7,
            "maxOutputTokens": 500
        }
    }

    headers = {"Content-Type": "application/json"}

    try:
        response = requests.post(url, headers=headers, json=payload, timeout=15)
        response.raise_for_status()
    except requests.exceptions.RequestException as e:
        return {"reply": f"Error from Gemini: {str(e)}"}

    data = response.json()

    # ✅ Correct parsing of Gemini response
    try:
        ai_reply = data["candidates"][0]["content"]["parts"][0]["text"]
    except (KeyError, IndexError) as e:
        return {"reply": f"Error parsing Gemini response: {data}"}

    # Update LangGraph state
    state = {"messages": [f"User: {user_msg}", f"Bot: {ai_reply}"]}
    graph_state.invoke(state)

    return {"reply": ai_reply}
