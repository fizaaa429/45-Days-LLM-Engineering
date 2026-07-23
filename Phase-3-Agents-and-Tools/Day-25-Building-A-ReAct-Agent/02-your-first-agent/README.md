# 02 · Your First Agent

An agent needs just two ingredients:

```python
from langchain.agents import create_agent

agent = create_agent(model, tools)          # 1. a model that can call tools
result = agent.invoke({"messages": [        # 2. a list of @tool functions
    ("human", "What is 12 times 8?")
]})
print(result["messages"][-1].content)       # -> "12 x 8 = 96."
```

## The input and output shape

| | Shape | Notes |
|--|-------|-------|
| **Input** | `{"messages": [("human", "…")]}` | Same message list as LangGraph (Day 24). `("human", "…")` is shorthand for a `HumanMessage`. |
| **Output** | `{"messages": [ …full trail… ]}` | The list grows with the agent's steps. The **last** message is the final answer. |

You always read the answer from `result["messages"][-1].content`.

## The tools are just Day 23 tools

```python
@tool
def multiply(a: int, b: int) -> int:
    """Multiply two integers a and b and return the product."""
    return a * b
```

Nothing new here — same `@tool` decorator, same docstring-the-model-reads. The
**only** change from Day 23 is that you no longer write the loop that calls them.

## Run it

```bash
python first_agent.py
```

- **With** a `GROQ_API_KEY` in `.env`, a real Llama model picks the tool.
- **Without** one, an offline scripted stand-in drives the same agent so you still
  see a real run.

## Gotcha
- The agent gives back the **whole conversation**, not just a string. Forgetting
  `["messages"][-1].content` and printing the raw dict is the #1 first-time mistake.

➡ Next: [`03-inside-the-loop/`](../03-inside-the-loop/README.md) — open up those messages and watch the loop tick.
