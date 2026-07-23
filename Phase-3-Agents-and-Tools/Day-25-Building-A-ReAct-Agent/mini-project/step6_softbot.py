"""
SoftBot - Step 6: the finished assistant (the brain).

Everything from steps 1-5 in one place: the toolbox, the persona, memory, and a
"How I got this" trace built from the streamed steps. NO Streamlit here, so it
stays testable and importable -- app.py is the thin UI on top (just like Day 23).

Public helpers:
    build_softbot()               -> a compiled agent (real Groq or offline)
    run_turn(agent, text, cfg)    -> (answer_text, trace_list)

Run this file directly for a scripted two-turn demo:
    python step6_softbot.py
"""

import os
from typing import List, Tuple

from dotenv import load_dotenv
from langchain.agents import create_agent
from langchain_core.tools import tool
from langchain_core.messages import AIMessage
from langchain_core.language_models.chat_models import BaseChatModel
from langchain_core.outputs import ChatResult, ChatGeneration
from langgraph.checkpoint.memory import MemorySaver

load_dotenv()
MODEL = "llama-3.1-8b-instant"


# --- The toolbox ------------------------------------------------------------
@tool
def calculator(a: float, b: float, op: str) -> float:
    """Do arithmetic on two numbers. op is one of: add, sub, mul, div."""
    return {"add": a + b, "sub": a - b, "mul": a * b,
            "div": a / b if b else float("nan")}[op]


@tool
def search_handbook(topic: str) -> str:
    """Look up a campus policy note. Topics: fees, hostel, library, exam, wifi."""
    handbook = {
        "fees": "Semester fee is Rs.2500, due by the 10th of the month.",
        "hostel": "Hostel is Rs.1200/month, includes wifi and mess.",
        "library": "Library is open 9am-9pm; 5 books for 14 days.",
        "exam": "Exams need 75% attendance; hall ticket from the portal.",
        "wifi": "Campus wifi: connect to 'Softpro-Net', login with your roll no.",
    }
    return handbook.get(topic.lower(), f"No handbook entry for '{topic}'.")


@tool
def word_count(text: str) -> int:
    """Count the number of words in a piece of text."""
    return len(text.split())


TOOLS = [calculator, search_handbook, word_count]

SYSTEM_PROMPT = (
    "You are SoftBot, the friendly assistant for Softpro School of AI students. "
    "Use search_handbook for any policy/fees/facility question and calculator for "
    "any arithmetic -- never guess numbers or invent policies. If the handbook has "
    "no entry, say so honestly. Keep answers to one or two short sentences."
)


# --- Offline stand-in -------------------------------------------------------
class ScriptedModel(BaseChatModel):
    """Replays scripted steps so the finished agent runs with no API key."""
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


OFFLINE_SCRIPT = [
    AIMessage(content="", tool_calls=[
        {"name": "search_handbook", "args": {"topic": "fees"}, "id": "c1"}]),
    AIMessage(content="The semester fee is Rs.2500, due by the 10th."),
    AIMessage(content="", tool_calls=[
        {"name": "calculator", "args": {"a": 2500, "b": 4, "op": "mul"},
         "id": "c2"}]),
    AIMessage(content="Four semesters at Rs.2500 each come to Rs.10000."),
]


def build_softbot(offline_script: List[AIMessage] = None):
    """Return a compiled SoftBot agent with memory. Real Groq if a key is set,
    else an offline scripted stand-in (pass your own script for tests)."""
    if os.getenv("GROQ_API_KEY"):
        from langchain_groq import ChatGroq
        model = ChatGroq(model=MODEL, temperature=0)
    else:
        model = ScriptedModel(script=offline_script or OFFLINE_SCRIPT)
    return create_agent(model, TOOLS, system_prompt=SYSTEM_PROMPT,
                        checkpointer=MemorySaver())


def run_turn(agent, text: str, config: dict) -> Tuple[str, List[str]]:
    """Run one turn; return (final answer, trace of tool steps for 'How I got this')."""
    trace: List[str] = []
    answer = ""
    for chunk in agent.stream({"messages": [("human", text)]}, config,
                              stream_mode="updates"):
        for node, update in chunk.items():
            last = update["messages"][-1]
            if getattr(last, "tool_calls", None):
                for c in last.tool_calls:
                    trace.append(f"called {c['name']}({c['args']})")
            elif type(last).__name__ == "ToolMessage":
                trace.append(f"got: {last.content}")
            elif last.content:
                answer = last.content
    return answer, trace


if __name__ == "__main__":
    print(f"Using real Groq model: {MODEL}\n" if os.getenv("GROQ_API_KEY")
          else "No GROQ_API_KEY -- using an offline stand-in.\n")

    bot = build_softbot()
    cfg = {"configurable": {"thread_id": "demo"}}

    for q in ["What is the semester fee?", "So what do 4 semesters cost?"]:
        answer, trace = run_turn(bot, q, cfg)
        print(f"You    : {q}")
        print(f"SoftBot: {answer}")
        print("  How I got this:")
        for t in trace:
            print(f"    - {t}")
        print()
