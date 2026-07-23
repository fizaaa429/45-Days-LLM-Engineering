# 01 · Why a ReAct Agent?

On **Day 23** you built a tool-calling loop **by hand**. On **Day 24** you learned
**LangGraph** — the engine for loops, branches, and memory. Today those two meet:
`create_agent` builds the whole loop for you, on the LangGraph engine, in **one line**.

## ReAct = Reason + Act

An agent doesn't answer in one shot. It runs a little loop:

| Step | What happens |
|------|--------------|
| **Reason** | The model thinks: *"to answer this, I need a tool."* |
| **Act** | It emits a **tool call** (`add`, `run_sql_query`, `search`, …). |
| **Observe** | Your code runs the tool and hands the **result** back. |
| …repeat | The model reasons again with the new information. |
| **Answer** | When it has enough, it replies in plain text and the loop ends. |

That's the **ReAct** pattern (Reason + Act). Day 23's `while` loop *was* ReAct —
you just wrote every line yourself.

## The whole loop, in one line

```python
from langchain.agents import create_agent

agent = create_agent(model, tools)          # <- builds the ReAct loop for you
result = agent.invoke({"messages": [("human", "What is 240 + 360?")]})
```

`create_agent` returns a **compiled LangGraph agent** — literally the Day 24 engine,
pre-wired into the model → tools → model cycle. You stop writing loops and start
*using* one.

## Before vs after

| | Day 23 (by hand) | Day 25 (`create_agent`) |
|--|------------------|--------------------------|
| The loop | You write the `while` + `ToolMessage` plumbing | Built for you |
| Tool results fed back | You append `ToolMessage(...)` | Automatic |
| Safety cap on steps | You add `MAX_STEPS` | `recursion_limit` built in |
| Memory across turns | You pass the list back | `checkpointer` + `thread_id` (module 05) |
| Lines of code | ~15 | **1** |

Writing it by hand first (Day 23) means this one line is **never magic** — you know
exactly what it does.

## Run it

```bash
python why_react.py
```

Runs with **no API key**: a tiny scripted stand-in model drives the *real* agent so
you can watch the reason → act → observe → answer trail offline.

## Gotcha
- `create_agent` lives in **`langchain.agents`** (LangChain 1.x). The older
  LangGraph-level name is `langgraph.prebuilt.create_react_agent` — same idea, and
  `create_agent` is the current, recommended one.

➡ Next: [`02-your-first-agent/`](../02-your-first-agent/README.md) — build and run a real calculator agent on Groq.
