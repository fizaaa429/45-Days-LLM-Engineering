"""
04 - Steering the agent: a system prompt + a real toolbox.

Two upgrades over the toy calculator:

    1. A SYSTEM PROMPT -- create_agent(model, tools, system_prompt="...").
       This is the agent's job description. It sets the persona and the rules
       ("always use a tool, never guess the maths").

    2. MULTIPLE TOOLS -- you hand over a toolbox and let the MODEL pick which
       tool(s) each question needs. You never write "if question is about X...";
       the model routes itself. That self-routing is what makes it an agent.

Here the toolbox is a tiny "study assistant": a calculator, a word counter, and a
notes lookup. Ask a mixed question and watch the model choose.

Setup:
    pip install langchain langchain-groq python-dotenv
Run:
    python system_prompt_and_tools.py
"""

import os
from typing import List

from dotenv import load_dotenv
from langchain.agents import create_agent
from langchain_core.tools import tool
from langchain_core.messages import AIMessage
from langchain_core.language_models.chat_models import BaseChatModel
from langchain_core.outputs import ChatResult, ChatGeneration

load_dotenv()
MODEL = "llama-3.1-8b-instant"


# --- The toolbox: three unrelated tools; the model decides which to use ------
@tool
def calculator(a: float, b: float, op: str) -> float:
    """Do arithmetic on two numbers. op is one of: add, sub, mul, div."""
    return {"add": a + b, "sub": a - b, "mul": a * b,
            "div": a / b if b else float("nan")}[op]


@tool
def word_count(text: str) -> int:
    """Count the number of words in a piece of text."""
    return len(text.split())


@tool
def lookup_note(topic: str) -> str:
    """Look up a short study note by topic. Topics: python, groq, rag, agent."""
    notes = {
        "python": "Python is a high-level language; indentation defines blocks.",
        "groq": "Groq serves open models fast and has a genuinely free tier.",
        "rag": "RAG = retrieve relevant text, then answer grounded in it.",
        "agent": "An agent loops: reason, call a tool, observe, repeat.",
    }
    return notes.get(topic.lower(), f"No note found for '{topic}'.")


TOOLS = [calculator, word_count, lookup_note]

SYSTEM_PROMPT = (
    "You are StudyBot, a concise study assistant for engineering students. "
    "Always use a tool for arithmetic, counting, or looking up a note -- never "
    "guess. After using tools, answer in one short, friendly sentence."
)


# --- Offline stand-in (same helper as the other modules) --------------------
class ScriptedModel(BaseChatModel):
    script: List[AIMessage] = []
    step: int = 0

    def bind_tools(self, tools, **kwargs):
        return self

    def _generate(self, messages, stop=None, run_manager=None, **kwargs):
        msg = self.script[min(self.step, len(self.script) - 1)]
        object.__setattr__(self, "step", self.step + 1)
        return ChatResult(generations=[ChatGeneration(message=msg)])

    @property
    def _llm_type(self):
        return "scripted-offline"


HAVE_KEY = bool(os.getenv("GROQ_API_KEY"))


def build_model():
    """Fresh model each call (the offline stand-in carries step state)."""
    if HAVE_KEY:
        from langchain_groq import ChatGroq
        return ChatGroq(model=MODEL, temperature=0)
    # Scripts using TWO different tools for one question: look up + calculate.
    return ScriptedModel(script=[
        AIMessage(content="", tool_calls=[
            {"name": "lookup_note", "args": {"topic": "agent"}, "id": "c1"}]),
        AIMessage(content="", tool_calls=[
            {"name": "calculator", "args": {"a": 3, "b": 4, "op": "mul"},
             "id": "c2"}]),
        AIMessage(content="An agent loops: reason, act, observe. And 3 x 4 = 12."),
    ])


print(f"Using real Groq model: {MODEL}\n" if HAVE_KEY
      else "No GROQ_API_KEY -- offline stand-in picks tools from a script.\n")

# system_prompt is passed straight into create_agent.
agent = create_agent(build_model(), TOOLS, system_prompt=SYSTEM_PROMPT)

question = "Give me the note on 'agent', and also what is 3 times 4?"
print(f"You     : {question}\n")

# Stream so we can see which tools the model chose, in order.
print("Tools the agent chose:")
for chunk in agent.stream({"messages": [("human", question)]},
                          stream_mode="updates"):
    for node, update in chunk.items():
        last = update["messages"][-1]
        if getattr(last, "tool_calls", None):
            c = last.tool_calls[0]
            print(f"   -> {c['name']}({c['args']})")

# Fresh agent for the final answer (the offline stand-in replays from step 0).
final = create_agent(build_model(), TOOLS, system_prompt=SYSTEM_PROMPT).invoke(
    {"messages": [("human", question)]})
print(f"\nStudyBot: {final['messages'][-1].content}")
print("\nYou never told it which tool to use -- the system prompt set the rules, "
      "and the model routed itself.")
