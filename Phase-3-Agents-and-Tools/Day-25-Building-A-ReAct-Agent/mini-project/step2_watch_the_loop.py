"""
SoftBot - Step 2: watch the loop.

Same one-tool agent as step 1, but instead of just reading the final answer we
STREAM the steps -- so you see the reason -> act -> observe cycle happen. This is
the trace we'll surface to the user later as "How I got this".

Run:
    python step2_watch_the_loop.py
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
             "args": {"a": 1200, "b": 3, "op": "mul"}, "id": "c1"}]),
        AIMessage(content="3 months of hostel at Rs.1200 is Rs.3600."),
    ])
    print("No GROQ_API_KEY -- using an offline stand-in.\n")


agent = create_agent(model, [calculator])
question = "Hostel is Rs.1200 a month. How much for 3 months?"
print(f"You: {question}\n")

print("How SoftBot works it out:")
for chunk in agent.stream({"messages": [("human", question)]},
                          stream_mode="updates"):
    for node, update in chunk.items():
        last = update["messages"][-1]
        if getattr(last, "tool_calls", None):
            c = last.tool_calls[0]
            print(f"   think/act -> {c['name']}({c['args']})")
        elif type(last).__name__ == "ToolMessage":
            print(f"   observe   -> {last.content}")
        elif last.content:
            print(f"\nSoftBot: {last.content}")
