"""
EXERCISE 1 - A unit-converter agent.

GOAL: build a ReAct agent with create_agent that has TWO conversion tools and
picks the right one per question -- no routing code from you.

Follow the # TODO markers. The offline stand-in model and the demo are provided,
so once your tools + agent are correct, `python unit_converter_agent.py` just runs.

Run:
    python unit_converter_agent.py
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


# TODO 1: write a tool that converts Celsius to Fahrenheit.
#   - decorate it with @tool
#   - name it celsius_to_fahrenheit, take (c: float) -> float
#   - write a one-line docstring the MODEL will read (F = c * 9/5 + 32)


# TODO 2: write a second tool km_to_miles(km: float) -> float
#   (1 km = 0.621371 miles). Give it a clear docstring too.


# TODO 3: put your two tools in this list.
TOOLS = []  # <- add your tools


# --- Provided: an offline stand-in so this runs with no key -----------------
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
    # TODO 4: build the agent with create_agent(build_model(), TOOLS)
    #         then .invoke a question like "What is 37 Celsius in Fahrenheit?"
    #         and print the final answer (result["messages"][-1].content).
    pass
