"""
EXERCISE 2 - A help-desk agent with memory.

GOAL: build an agent that (a) looks answers up in a small FAQ with a tool,
(b) has a persona via a system prompt, and (c) REMEMBERS across turns so a
follow-up question works.

Follow the # TODO markers. The offline stand-in and the two-turn demo are provided.

Run:
    python helpdesk_agent.py
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

FAQ = {
    "refund": "Refunds are processed within 5-7 business days to the original method.",
    "shipping": "Standard shipping is 3-5 days; express is next-day within metros.",
    "warranty": "All products carry a 1-year manufacturer warranty.",
    "returns": "You can return an item within 30 days if it is unused.",
}


# TODO 1: write a tool search_faq(topic: str) -> str that returns FAQ[topic]
#   (lowercased) or a polite "not found" message. Give it a docstring listing
#   the valid topics: refund, shipping, warranty, returns.


# TODO 2: write a SYSTEM_PROMPT that makes the agent a polite support assistant
#   which ALWAYS uses search_faq for policy questions and never makes answers up.
SYSTEM_PROMPT = ""   # <- fill this in


# TODO 3: put your tool in this list.
TOOLS = []


# --- Provided: offline stand-in --------------------------------------------
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
            {"name": "search_faq", "args": {"topic": "refund"}, "id": "c1"}]),
        AIMessage(content="Refunds take 5-7 business days."),
        AIMessage(content="Yes -- that refund goes back to your original "
                          "payment method."),
    ])


if __name__ == "__main__":
    # TODO 4: build the agent with create_agent(model, TOOLS,
    #         system_prompt=SYSTEM_PROMPT, checkpointer=MemorySaver()).
    #         Then ask two turns on the SAME thread_id:
    #           "How long do refunds take?"
    #           "And does it go back to my card?"   <- follow-up needs memory
    #         Print each answer.
    pass
