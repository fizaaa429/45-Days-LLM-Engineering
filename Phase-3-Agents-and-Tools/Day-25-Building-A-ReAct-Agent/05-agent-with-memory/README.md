# 05 · An Agent That Remembers

By default, each `invoke()` is a **blank slate**. Tell the agent your name, ask for
it next turn, and it has no idea — because you sent a brand-new message list.

To make it conversational, add the **same memory you learned on Day 24**: a
**checkpointer** + a **`thread_id`**.

## Two changes

**1. Compile with a checkpointer:**
```python
from langgraph.checkpoint.memory import MemorySaver
agent = create_agent(model, tools, checkpointer=MemorySaver())
```

**2. Pass a `thread_id` on every call:**
```python
config = {"configurable": {"thread_id": "student-1"}}
agent.invoke({"messages": [("human", "Hi, I'm Aditi.")]}, config)
agent.invoke({"messages": [("human", "What is my name?")]}, config)  # → "Aditi"
```

Each turn you send **only the new message** — the checkpointer reloads the rest of
the conversation from where it saved it.

## thread_id = which conversation

| `thread_id` | What it means |
|-------------|----------------|
| Same id across calls | Same memory — the agent remembers earlier turns |
| A new id | A fresh, **isolated** conversation (no shared history) |

This is how one deployed agent serves many users at once: one `thread_id` per user
(or per chat session). It's identical to Day 24's chatbot — the only difference is
this agent **also has tools**.

## Run it

```bash
python agent_with_memory.py
```

Shows the agent recalling a name across two turns, the stored message count, then a
second `thread_id` that starts clean. Works offline; a Groq key makes the recall a
real model's doing.

## Gotcha
- `MemorySaver` keeps history **in RAM** — restart the process and it's gone. For
  persistence across restarts, swap in a SQLite/Postgres checkpointer (same API).
- Forgetting the `config` (the `thread_id`) on a call makes that turn amnesiac even
  though the checkpointer exists — the id is what ties turns together.

➡ Next: the [`mini-project/`](../mini-project/README.md) — build **SoftBot**, a multi-tool assistant, one step at a time.
