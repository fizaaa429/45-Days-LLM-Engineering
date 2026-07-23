"""
app.py -- the Streamlit front-end for SoftBot.

Same brain (step6_softbot), a web UI on top. Reuses Day 19/22/23 patterns:
chat history in st.session_state, @st.cache_resource for the agent, st.chat_input
/ st.chat_message for the conversation, and a "How I got this" expander that shows
the exact tool steps -- the ReAct loop, made visible.

Memory here is handled by the AGENT's own checkpointer + a per-session thread_id,
not by replaying the whole history each turn (that's the create_agent way).

Setup:
    pip install streamlit langchain langchain-groq python-dotenv
    # put GROQ_API_KEY=... in a .env file in this folder
Run:
    streamlit run app.py
"""

import os
from dotenv import load_dotenv
import streamlit as st

from step6_softbot import build_softbot, run_turn

load_dotenv()

st.set_page_config(page_title="SoftBot", page_icon=":robot_face:")
st.title(":robot_face: SoftBot -- your campus assistant")
st.caption("A ReAct agent built with create_agent. It looks up the handbook and "
           "does the maths for you.")

# --- Sidebar: what SoftBot can do -------------------------------------------
with st.sidebar:
    st.header("SoftBot's tools")
    st.markdown("- **search_handbook** -- fees, hostel, library, exam, wifi\n"
                "- **calculator** -- add / sub / mul / div\n"
                "- **word_count** -- count words in text")
    st.caption("The model picks which tool to use for each question.")

# --- Need a key to chat ------------------------------------------------------
if not os.getenv("GROQ_API_KEY"):
    st.warning("Set GROQ_API_KEY in a .env file to chat with SoftBot. "
               "The agent, tools, and loop are all built -- this just needs a key.")
    st.stop()


# --- Build the agent once and cache it --------------------------------------
@st.cache_resource
def get_agent():
    return build_softbot()


agent = get_agent()

# One thread_id per browser session = this user's private memory.
if "thread_id" not in st.session_state:
    st.session_state.thread_id = "web-session"
    st.session_state.messages = []
config = {"configurable": {"thread_id": st.session_state.thread_id}}

# Replay the visible history on each rerun.
for msg in st.session_state.messages:
    with st.chat_message(msg["role"]):
        st.markdown(msg["content"])
        if msg.get("trace"):
            with st.expander("How I got this"):
                for step in msg["trace"]:
                    st.markdown(f"- {step}")

# --- Handle a new question ---------------------------------------------------
if question := st.chat_input("e.g. What's the hostel fee for 6 months?"):
    st.session_state.messages.append({"role": "user", "content": question})
    with st.chat_message("user"):
        st.markdown(question)

    with st.chat_message("assistant"):
        with st.spinner("Thinking..."):
            answer, trace = run_turn(agent, question, config)
        st.markdown(answer)
        if trace:
            with st.expander("How I got this"):
                for step in trace:
                    st.markdown(f"- {step}")

    st.session_state.messages.append(
        {"role": "assistant", "content": answer, "trace": trace})
