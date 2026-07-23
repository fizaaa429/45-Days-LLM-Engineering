"""
SoftBot - Step 5: memory across turns.

Toolbox + persona + MEMORY. Compile with a checkpointer and pass a thread_id, and
SoftBot remembers earlier turns -- so a student can ask a follow-up ("...and for 6
months?") without repeating themselves.

Run:
    python step5_memory.py
"""

import os
from typing import List

from dotenv import load_dotenv
from langchain.agents import create_agent
from langchain_core.tools import tool
from langchain_core.messages import AIMessage
from langchain_core.language_models.chat_models import BaseChatModel
from langchain_core.outputs import ChatResult, ChatGeneration
from langgraph.checkpoint.memory import MemorySaver

load_dotenv()
MODEL = "llama-3.1-8b-instant"


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
    "Use search_handbook for policy/fees questions and calculator for arithmetic; "
    "never guess. Keep answers short."
)


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


if os.getenv("GROQ_API_KEY"):
    from langchain_groq import ChatGroq
    model = ChatGroq(model=MODEL, temperature=0)
    print(f"Using real Groq model: {MODEL}\n")
else:
    # Turn 1: look up hostel fee + answer. Turn 2 (follow-up): calculate 6 months.
    model = ScriptedModel(script=[
        AIMessage(content="", tool_calls=[
            {"name": "search_handbook", "args": {"topic": "hostel"}, "id": "c1"}]),
        AIMessage(content="Hostel is Rs.1200 per month."),
        AIMessage(content="", tool_calls=[
            {"name": "calculator",
             "args": {"a": 1200, "b": 6, "op": "mul"}, "id": "c2"}]),
        AIMessage(content="For 6 months that's Rs.7200."),
    ])
    print("No GROQ_API_KEY -- using an offline stand-in.\n")


# checkpointer + thread_id = memory.
agent = create_agent(model, TOOLS, system_prompt=SYSTEM_PROMPT,
                     checkpointer=MemorySaver())
config = {"configurable": {"thread_id": "roll-42"}}


def say(text: str) -> None:
    result = agent.invoke({"messages": [("human", text)]}, config)
    print(f"You    : {text}")
    print(f"SoftBot: {result['messages'][-1].content}\n")


say("What's the hostel fee?")
say("And for 6 months?")     # a follow-up -- only works because SoftBot remembers

stored = agent.get_state(config).values["messages"]
print(f"(Thread 'roll-42' now holds {len(stored)} messages -- the whole chat.)")
