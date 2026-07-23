"""
SoftBot - Step 1: the smallest possible agent.

ONE tool, ONE line to build the agent, ONE question. This is the seed we grow
across the 6 steps into a full multi-tool campus assistant with memory.

Run:
    python step1_hello_agent.py
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


# --- Offline stand-in so every step runs with no API key --------------------
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
    model = ScriptedModel(script=[
        AIMessage(content="", tool_calls=[
            {"name": "calculator",
             "args": {"a": 2500, "b": 4, "op": "mul"}, "id": "c1"}]),
        AIMessage(content="4 semesters at Rs.2500 each is Rs.10000."),
    ])
    print("No GROQ_API_KEY -- using an offline stand-in.\n")


# The whole agent: a model + a list of tools.
agent = create_agent(model, [calculator])

question = "If one semester costs Rs.2500, what do 4 semesters cost?"
print(f"You    : {question}")
result = agent.invoke({"messages": [("human", question)]})
print(f"SoftBot: {result['messages'][-1].content}")
