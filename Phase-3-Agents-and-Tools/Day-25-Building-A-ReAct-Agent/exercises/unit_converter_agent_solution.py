"""
SOLUTION - unit_converter_agent.

Run:
    python unit_converter_agent_solution.py
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
def celsius_to_fahrenheit(c: float) -> float:
    """Convert a temperature in Celsius to Fahrenheit."""
    return c * 9 / 5 + 32


@tool
def km_to_miles(km: float) -> float:
    """Convert a distance in kilometres to miles."""
    return km * 0.621371


TOOLS = [celsius_to_fahrenheit, km_to_miles]


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
            {"name": "celsius_to_fahrenheit", "args": {"c": 37}, "id": "c1"}]),
        AIMessage(content="37 C is 98.6 F."),
    ])


if __name__ == "__main__":
    print(f"Using real Groq model: {MODEL}\n" if os.getenv("GROQ_API_KEY")
          else "No GROQ_API_KEY -- using an offline stand-in.\n")

    agent = create_agent(build_model(), TOOLS)
    question = "What is 37 Celsius in Fahrenheit?"
    print(f"You  : {question}")
    result = agent.invoke({"messages": [("human", question)]})
    print(f"Agent: {result['messages'][-1].content}")
