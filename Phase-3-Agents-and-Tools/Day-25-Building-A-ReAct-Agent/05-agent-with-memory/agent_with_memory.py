"""
05 - An agent that REMEMBERS: checkpointer + thread_id.

By default each agent.invoke() is a blank slate -- ask "what is my name?" after
telling it, and it won't know. To make an agent conversational, give it the SAME
memory tool you met on Day 24:

    from langgraph.checkpoint.memory import MemorySaver
    agent = create_agent(model, tools, checkpointer=MemorySaver())

Then pass a thread_id with every call:

    config = {"configurable": {"thread_id": "student-1"}}
    agent.invoke({"messages": [("human", "Hi, I'm Aditi.")]}, config)
    agent.invoke({"messages": [("human", "What's my name?")]}, config)  # -> Aditi

Each turn you send ONLY the new message; the checkpointer reloads the rest.
Different thread_id = a different, isolated conversation. This is exactly Day 24's
memory -- now on an agent that also has tools.

Setup:
    pip install langchain langchain-groq python-dotenv
Run:
    python agent_with_memory.py
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
def add(a: int, b: int) -> int:
    """Add two integers a and b and return the sum."""
    return a + b


class ScriptedModel(BaseChatModel):
    """Offline stand-in. For the memory demo it doesn't call tools -- it just
    proves the history survives by echoing what it has been told."""
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
        AIMessage(content="Nice to meet you, Aditi!"),     # student-1, turn 1
        AIMessage(content="Your name is Aditi."),          # student-1, turn 2
        AIMessage(content="I don't have any earlier messages here, "
                          "so I don't know your name."),   # student-2, fresh
    ])
    print("No GROQ_API_KEY -- offline stand-in (still shows memory persisting).\n")


# The ONE new argument: checkpointer. That's what makes memory persist.
agent = create_agent(model, [add], checkpointer=MemorySaver())

# thread_id names the conversation. Same id -> same memory.
config = {"configurable": {"thread_id": "student-1"}}


def say(text: str) -> None:
    result = agent.invoke({"messages": [("human", text)]}, config)
    print(f"You  : {text}")
    print(f"Agent: {result['messages'][-1].content}\n")


say("Hi, my name is Aditi.")
say("What is my name?")          # remembers -> Aditi (with a real key)

# Peek at what's stored on this thread -- the whole conversation is saved.
stored = agent.get_state(config).values["messages"]
print(f"Stored on thread 'student-1': {len(stored)} messages.\n")

# A different thread_id starts clean -- no shared memory.
other = {"configurable": {"thread_id": "student-2"}}
fresh = agent.invoke({"messages": [("human", "What is my name?")]}, other)
print("New thread 'student-2' has no history:")
print("Agent:", fresh["messages"][-1].content)
print("\nSame agent, two thread_ids, two separate memories -- just like Day 24.")
