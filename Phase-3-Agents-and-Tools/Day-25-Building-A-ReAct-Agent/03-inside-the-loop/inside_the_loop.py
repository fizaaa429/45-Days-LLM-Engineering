"""
03 - Inside the loop: watch reason -> act -> observe, step by step.

In module 02 the agent gave a one-line answer. But underneath, it ran the SAME
loop you wrote on Day 23. This module opens it up two ways:

    1. Read the final message list -- every step is a message.
    2. Use agent.stream(..., stream_mode="updates") to watch each node fire live.

The message trail of a tool-using agent always looks like:

    HumanMessage   your question
    AIMessage      (empty text, but has .tool_calls)   <- REASON + ACT
    ToolMessage    the tool's result                    <- OBSERVE
    AIMessage      the final plain-text answer           <- ANSWER

That is exactly Day 23's loop -- now produced for you.

Setup:
    pip install langchain langchain-groq python-dotenv
Run:
    python inside_the_loop.py
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
def add(a: int, b: int) -> int:
    """Add two integers a and b and return the sum."""
    return a + b


@tool
def multiply(a: int, b: int) -> int:
    """Multiply two integers a and b and return the product."""
    return a * b


TOOLS = [add, multiply]


class ScriptedModel(BaseChatModel):
    """Offline stand-in: replays scripted steps so the loop runs with no key."""
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
    """Return a FRESH model each call (the offline stand-in has step state,
    so each demo run below needs its own copy)."""
    if HAVE_KEY:
        from langchain_groq import ChatGroq
        return ChatGroq(model=MODEL, temperature=0)
    # Scripts a TWO-tool question: multiply, then add the result -> two loops.
    return ScriptedModel(script=[
        AIMessage(content="", tool_calls=[
            {"name": "multiply", "args": {"a": 6, "b": 7}, "id": "c1"}]),
        AIMessage(content="", tool_calls=[
            {"name": "add", "args": {"a": 42, "b": 100}, "id": "c2"}]),
        AIMessage(content="6 x 7 = 42, and 42 + 100 = 142."),
    ])


print(f"Using real Groq model: {MODEL}\n" if HAVE_KEY
      else "No GROQ_API_KEY -- using an offline scripted stand-in.\n")
question = "Multiply 6 by 7, then add 100 to the result."
agent = create_agent(build_model(), TOOLS)

# --- Way 1: stream the steps as they happen -------------------------------
# stream_mode="updates" yields one chunk per node that ran: "model" (the LLM
# reasoning/acting) and "tools" (a tool being run). This is the loop, live.
print(f"You: {question}\n")
print("Watching the loop tick (stream_mode='updates'):")
for chunk in agent.stream({"messages": [("human", question)]},
                          stream_mode="updates"):
    for node, update in chunk.items():
        last = update["messages"][-1]
        if getattr(last, "tool_calls", None):
            c = last.tool_calls[0]
            print(f"  [{node:5}] REASON+ACT  -> call {c['name']}({c['args']})")
        elif type(last).__name__ == "ToolMessage":
            print(f"  [{node:5}] OBSERVE     -> tool returned {last.content!r}")
        elif last.content:
            print(f"  [{node:5}] ANSWER      -> {last.content!r}")

# --- Way 2: the same run, read from the final message list ----------------
# Fresh agent so the offline stand-in replays its script from the start.
print("\nThe same idea, read from the final message list:")
result = create_agent(build_model(), TOOLS).invoke(
    {"messages": [("human", question)]})
for i, m in enumerate(result["messages"], 1):
    print(f"  {i}. {type(m).__name__}")

print("\nModel -> Tool -> Model -> Tool -> Model. That's Day 23's loop, automated.")
