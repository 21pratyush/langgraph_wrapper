import json
import streamlit as st
from dotenv import load_dotenv
from graph_runtime import build_graph_from_json, get_llm

# Load .env
load_dotenv()

# === Load JSON (can also be from file or API) ===
with open("chat_bot.json", "r") as f:
    graph_json = json.load(f)

llm = get_llm(graph_json["llm"])
workflow = build_graph_from_json(graph_json, llm=llm)
app = workflow.compile()

# === Streamlit UI ===
st.title("🔄 JSON-Driven LangGraph + Gemini ChatBot")

user_query = st.text_input("Ask me anything:")

if st.button("Send") and user_query:
    initial_state = {"user_input": user_query, "response": None}
    result = app.invoke(initial_state)
    if result and "response" in result:
        st.write("🤖:", result["response"])
    else:
        st.error("No response generated")
