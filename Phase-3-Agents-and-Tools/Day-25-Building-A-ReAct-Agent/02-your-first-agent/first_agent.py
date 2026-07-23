"""
02 - Your first real agent: create_agent(model, tools).

Two things make an agent:
    1. a MODEL that can call tools,
    2. a list of TOOLS (plain @tool functions -- exactly like Day 23).

    agent = create_agent(model, tools)
    agent.invoke({"messages": [("human", "...")]})   # -> runs the ReAct loop

The input is a dict with a "messages" list (same message shape as LangGraph,
Day 24). The output is that list, grown with everything the agent did; the LAST
message is the final answer.

With GROQ_API_KEY set, a real Llama model chooses which tool to call. Without a
key, an offline scripted stand-in drives the same agent so you still see it work.

Setup:
    pip install langchain langchain-groq python-dotenv
    echo GROQ_API_KEY=your_key > .env      # optional; runs offline without it
Run:
    python first_agent.py
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


# --- The tools: two plain functions, each with a docstring the model reads ---
@tool
def add(a: int, b: int) -> int:
    """Add two integers a and b and return the sum."""
    return a + b


@tool
def multiply(a: int, b: int) -> int:
    """Multiply two integers a and b and return the product."""
    return a * b


TOOLS = [add, multiply]


# --- Offline stand-in model (same helper used across today's modules) -------
class ScriptedModel(BaseChatModel):
    """NOT an LLM -- replays pre-written steps so the agent loop runs with no key."""
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
    """Real Groq model if we have a key, else a scripted offline stand-in."""
    if os.getenv("GROQ_API_KEY"):
        from langchain_groq import ChatGroq
        print(f"Using real Groq model: {MODEL}\n")
        return ChatGroq(model=MODEL, temperature=0)
    print("No GROQ_API_KEY -- using an offline scripted stand-in.\n")
    return ScriptedModel(script=[
        AIMessage(content="", tool_calls=[
            {"name": "multiply", "args": {"a": 12, "b": 8}, "id": "call_1"}]),
        AIMessage(content="12 x 8 = 96."),
    ])


# --- Build the agent and ask it a question ----------------------------------
model = build_model()
agent = create_agent(model, TOOLS)      # <- the ReAct loop, ready to use

question = "What is 12 times 8?"
print(f"You  : {question}")
result = agent.invoke({"messages": [("human", question)]})

# The agent returns the whole message list; the final answer is the last one.
print(f"Agent: {result['messages'][-1].content}")

print(f"\n(The agent exchanged {len(result['messages'])} messages to get there -- "
      f"module 03 opens up what they were.)")
