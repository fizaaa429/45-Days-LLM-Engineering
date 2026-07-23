"""
SoftBot - Step 3: a real toolbox.

Now SoftBot gets THREE tools and has to pick the right one(s) per question:
    - calculator     : arithmetic (fees, hostel costs...)
    - search_handbook: look up a campus policy note
    - word_count     : count words in some text

You never route by hand -- the model reads each tool's docstring and chooses.
Ask a mixed question and it uses more than one.

Run:
    python step3_toolbox.py
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


# --- SoftBot's toolbox (reused by steps 4-6) --------------------------------
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


# --- Offline stand-in -------------------------------------------------------
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


def build_model():
    if os.getenv("GROQ_API_KEY"):
        from langchain_groq import ChatGroq
        return ChatGroq(model=MODEL, temperature=0)
    # Uses TWO tools: look up the hostel fee, then multiply by 6 months.
    return ScriptedModel(script=[
        AIMessage(content="", tool_calls=[
            {"name": "search_handbook", "args": {"topic": "hostel"}, "id": "c1"}]),
        AIMessage(content="", tool_calls=[
            {"name": "calculator",
             "args": {"a": 1200, "b": 6, "op": "mul"}, "id": "c2"}]),
        AIMessage(content="Hostel is Rs.1200/month, so 6 months is Rs.7200."),
    ])


if __name__ == "__main__":
    print(f"Using real Groq model: {MODEL}\n" if os.getenv("GROQ_API_KEY")
          else "No GROQ_API_KEY -- using an offline stand-in.\n")

    question = "What's the hostel fee, and what would 6 months cost?"
    print(f"You: {question}\n")

    print("Tools SoftBot chose:")
    for chunk in create_agent(build_model(), TOOLS).stream(
            {"messages": [("human", question)]}, stream_mode="updates"):
        for node, update in chunk.items():
            last = update["messages"][-1]
            if getattr(last, "tool_calls", None):
                c = last.tool_calls[0]
                print(f"   -> {c['name']}({c['args']})")

    final = create_agent(build_model(), TOOLS).invoke(
        {"messages": [("human", question)]})
    print(f"\nSoftBot: {final['messages'][-1].content}")
