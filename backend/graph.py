from langgraph.graph import StateGraph, END
from typing import TypedDict

# Define state schema
class ChatState(TypedDict):
    messages: list

# Helper to add a message to state
def add_message(state: ChatState, msg: str):
    state["messages"].append(msg)
    return state

# Create conversation flow graph
def create_graph():
    graph = StateGraph(ChatState)

    # Add nodes
    graph.add_node("start", lambda state: add_message(state, "Conversation started."))
    graph.add_node("respond", lambda state: state)  # AI response handled in backend

    # Entry & exit points
    graph.set_entry_point("start")
    graph.add_edge("start", "respond")
    graph.add_edge("respond", END)

    return graph
