"""
01 - Why a ReAct agent? From a hand-written loop to one line.

On Day 23 you wrote the tool-calling loop BY HAND -- a `while` loop that:
    1. asks the model,
    2. if the model asked for a tool, runs it and feeds the result back,
    3. repeats until the model gives a plain-text answer.

That pattern has a name: **ReAct** = *Reason + Act*. The model REASONS about what
to do, ACTS by calling a tool, OBSERVES the result, and reasons again -- looping
until it can answer. (Think -> Act -> Observe.)

Today LangChain hands you that entire loop in ONE line:

    from langchain.agents import create_agent
    agent = create_agent(model, tools)

`create_agent` builds a ReAct loop for you (it returns a compiled LangGraph graph
under the hood -- the Day 24 engine). No more hand-written `while`.

This file proves it runs -- with NO API key -- by driving the real agent with a
tiny scripted stand-in model, so you can see the loop happen offline.

Setup:
    pip install langchain langchain-groq python-dotenv
Run:
    python why_react.py
"""

from typing import List

from langchain.agents import create_agent
from langchain_core.tools import tool
from langchain_core.messages import AIMessage
from langchain_core.language_models.chat_models import BaseChatModel
from langchain_core.outputs import ChatResult, ChatGeneration


# --- The tool (same idea as Day 23: a plain function the model can call) ----
@tool
def add(a: int, b: int) -> int:
    """Add two integers a and b and return the sum."""
    return a + b


# ---------------------------------------------------------------------------
# What Day 23 made you write by hand (kept here as a comment, for contrast):
#
#     messages = [SystemMessage(...), HumanMessage(question)]
#     for _ in range(MAX_STEPS):
#         ai = model.invoke(messages)
#         messages.append(ai)
#         if not ai.tool_calls:
#             return ai.content            # <- plain answer, we're done
#         for call in ai.tool_calls:
#             result = TOOL_MAP[call["name"]].invoke(call["args"])
#             messages.append(ToolMessage(result, tool_call_id=call["id"]))
#
# `create_agent(model, tools)` IS that loop -- written, tested, and returned to
# you as a ready-to-run agent. You just .invoke() it.
# ---------------------------------------------------------------------------


# --- Offline stand-in model (so this runs with no key) ----------------------
# It is NOT an LLM. It just replays pre-written steps in order -- first a step
# that asks for the `add` tool, then a step with the final answer. A real model
# decides these on its own; here we script them so the loop can run offline.
class ScriptedModel(BaseChatModel):
    script: List[AIMessage] = []
    step: int = 0

    def bind_tools(self, tools, **kwargs):
        return self  # a real model attaches tool schemas here; we don't need to

    def _generate(self, messages, stop=None, run_manager=None, **kwargs):
        msg = self.script[min(self.step, len(self.script) - 1)]
        object.__setattr__(self, "step", self.step + 1)
        return ChatResult(generations=[ChatGeneration(message=msg)])

    @property
    def _llm_type(self):
        return "scripted-offline"


script = [
    # Step 1: the model REASONS "I should add" and ACTS by calling the tool.
    AIMessage(content="", tool_calls=[
        {"name": "add", "args": {"a": 240, "b": 360}, "id": "call_1"}]),
    # Step 2: having OBSERVED the tool result (600), it gives the final answer.
    AIMessage(content="240 + 360 = 600."),
]

# THE ONE LINE. Everything from Day 23's loop is inside here.
agent = create_agent(ScriptedModel(script=script), [add])

print("Asking the agent: 'What is 240 + 360?'\n")
result = agent.invoke({"messages": [("human", "What is 240 + 360?")]})

# The agent returns the FULL conversation. Watch the ReAct loop in the messages:
print("The full message trail (this is the ReAct loop):")
for m in result["messages"]:
    kind = type(m).__name__
    if getattr(m, "tool_calls", None):
        print(f"  {kind:14} -> ACT: call {m.tool_calls[0]['name']}({m.tool_calls[0]['args']})")
    elif kind == "ToolMessage":
        print(f"  {kind:14} -> OBSERVE: tool returned {m.content!r}")
    elif m.content:
        print(f"  {kind:14} -> {m.content!r}")

print("\nFinal answer:", result["messages"][-1].content)
print("\nThat whole loop -- reason, act, observe, answer -- came from ONE line:")
print("    agent = create_agent(model, tools)")
