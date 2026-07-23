"""
SoftBot - Step 4: give it a persona and rules (system prompt).

Same toolbox as step 3, now with a SYSTEM PROMPT that sets who SoftBot is and how
it must behave: always use a tool instead of guessing, and answer briefly. This is
the difference between "a model with tools" and a product with a personality.

Run:
    python step4_persona.py
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
    "Use search_handbook for any policy/fees/facility question, and calculator "
    "for any arithmetic -- never guess numbers or invent policies. If the handbook "
    "has no entry, say so honestly. Keep answers to one or two short sentences."
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


def build_model():
    if os.getenv("GROQ_API_KEY"):
        from langchain_groq import ChatGroq
        return ChatGroq(model=MODEL, temperature=0)
    return ScriptedModel(script=[
        AIMessage(content="", tool_calls=[
            {"name": "search_handbook", "args": {"topic": "library"}, "id": "c1"}]),
        AIMessage(content="The library is open 9am-9pm, and you can borrow "
                          "5 books for 14 days."),
    ])


if __name__ == "__main__":
    print(f"Using real Groq model: {MODEL}\n" if os.getenv("GROQ_API_KEY")
          else "No GROQ_API_KEY -- using an offline stand-in.\n")

    agent = create_agent(build_model(), TOOLS, system_prompt=SYSTEM_PROMPT)
    question = "When is the library open and how many books can I take?"
    print(f"You    : {question}")
    result = agent.invoke({"messages": [("human", question)]})
    print(f"SoftBot: {result['messages'][-1].content}")
