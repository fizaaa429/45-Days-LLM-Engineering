"""
SOLUTION - helpdesk_agent.

Run:
    python helpdesk_agent_solution.py
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


@tool
def search_faq(topic: str) -> str:
    """Look up a support policy. Topics: refund, shipping, warranty, returns."""
    return FAQ.get(topic.lower(), f"No FAQ entry for '{topic}'.")


SYSTEM_PROMPT = (
    "You are a polite customer-support assistant. For any policy question "
    "(refunds, shipping, warranty, returns) you MUST call search_faq and answer "
    "from what it returns -- never invent a policy. Keep replies short and warm."
)

TOOLS = [search_faq]


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
    print(f"Using real Groq model: {MODEL}\n" if os.getenv("GROQ_API_KEY")
          else "No GROQ_API_KEY -- using an offline stand-in.\n")

    agent = create_agent(build_model(), TOOLS, system_prompt=SYSTEM_PROMPT,
                        checkpointer=MemorySaver())
    config = {"configurable": {"thread_id": "cust-1"}}

    for q in ["How long do refunds take?", "And does it go back to my card?"]:
        result = agent.invoke({"messages": [("human", q)]}, config)
        print(f"You  : {q}")
        print(f"Agent: {result['messages'][-1].content}\n")
