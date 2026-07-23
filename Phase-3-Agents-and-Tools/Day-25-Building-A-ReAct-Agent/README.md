# Day 25 — Building a ReAct Agent (`create_agent`)

**Phase 3 · Agents & Tools — Day 5.** Two days ago (Day 23) you wrote the
tool-calling loop **by hand** — a `while` over `.tool_calls`, appending
`ToolMessage`s until the model gave a plain answer. Yesterday (Day 24) you learned
**LangGraph** — the engine for loops, branches, and memory. **Today those meet:**
`create_agent` builds that entire ReAct loop for you, on the LangGraph engine, in
**one line**.

> **What you learn:** what the **ReAct** pattern is (Reason → Act → Observe), how
> `create_agent(model, tools)` replaces your hand-written loop, how to read/stream
> the agent's steps, how to steer it with a **system prompt** and a **toolbox**, and
> how to give it **memory** — all on free **Groq**, **LangChain 1.x**.

## From a hand-written loop to one line

```python
from langchain.agents import create_agent

agent  = create_agent(model, tools)                       # the whole ReAct loop
result = agent.invoke({"messages": [("human", "…")]})
answer = result["messages"][-1].content
```

| | Day 23 (by hand) | Day 25 (`create_agent`) |
|--|------------------|--------------------------|
| The loop | ~15 lines of `while` + `ToolMessage` | **1 line** |
| Feed tool results back | you append them | automatic |
| Step cap | your `MAX_STEPS` | `recursion_limit` built in |
| Memory | pass the list back yourself | `checkpointer` + `thread_id` |

Because you built it by hand first, this one line is **never magic** — you know
exactly what's inside it (it returns a compiled LangGraph agent, Day 24's engine).

## The mental model: ReAct
- **Reason** — the model decides *"I need a tool for this."*
- **Act** — it emits a tool call.
- **Observe** — your code runs the tool; the result goes back to the model.
- …loop until it can **answer** in plain text.

## Learning objectives
By the end of today you can:
- Explain the **ReAct** loop and how `create_agent` implements it.
- Build an agent from a **model + a list of tools**, and read the final answer.
- **Stream** an agent's steps and read its message trail (Reason/Act/Observe).
- Steer an agent with a **`system_prompt`** and let it **self-route** across a toolbox.
- Give an agent **memory** with a `checkpointer` + `thread_id`.

## What this reuses
| From    | Idea used here                                              |
|---------|-------------------------------------------------------------|
| Day 23  | `@tool` functions + the tool-calling loop — now automated   |
| Day 24  | The LangGraph engine, `MemorySaver`, `thread_id` — under `create_agent` |
| Day 21  | `ChatGroq`, message objects                                 |
| Day 19  | Streamlit chat UI (`session_state`, `chat_input`, `cache_resource`) |

## Start here
1. **Slides:** open [`presentation/index.html`](presentation/index.html) — *One line
   that replaces your loop* (speaker notes in [`presentation/README.md`](presentation/README.md)).
2. **Concepts:** run the modules `01 → 05` below.
3. **Build:** the [`mini-project/`](mini-project/README.md) — **SoftBot**, a multi-tool
   campus assistant scaled from one line to a memoried web app in 6 steps.

## Module index
| # | Folder | You learn |
|---|--------|-----------|
| 01 | [`01-why-react/`](01-why-react/README.md) | ReAct = Reason + Act; the hand-loop collapses to `create_agent(model, tools)` |
| 02 | [`02-your-first-agent/`](02-your-first-agent/README.md) | Build & invoke a real calculator agent; the input/output shape |
| 03 | [`03-inside-the-loop/`](03-inside-the-loop/README.md) | Read & `stream()` the steps — it's Day 23's loop, automated |
| 04 | [`04-system-prompt-and-tools/`](04-system-prompt-and-tools/README.md) | A `system_prompt` + a toolbox the model routes itself |
| 05 | [`05-agent-with-memory/`](05-agent-with-memory/README.md) | Memory: `checkpointer` + `thread_id` |

### Mini-project (today's build)
| Folder | Build |
|--------|-------|
| [`mini-project/`](mini-project/README.md) | **SoftBot** — 6 steps: hello-agent → watch-the-loop → toolbox → persona → memory → finished brain + a Streamlit UI. Steps 1–6 need no key. |

### Exercises
| Folder | Practise |
|--------|----------|
| [`exercises/`](exercises/README.md) | Unit-converter agent (author tools + `create_agent`) · Help-desk agent (tool + system prompt + memory) |

## How to run

**Setup (once).** Install with the real CPython (see repo `CLAUDE.md`):
```bash
pip install langchain langchain-groq langgraph streamlit python-dotenv
```
A free Groq key is only needed for *live* answers. Put it in a `.env`:
```
GROQ_API_KEY=your_key_here
```
Get one at [console.groq.com/keys](https://console.groq.com/keys).

**Run the modules in order:**
```bash
python 01-why-react/why_react.py
python 02-your-first-agent/first_agent.py
python 03-inside-the-loop/inside_the_loop.py
python 04-system-prompt-and-tools/system_prompt_and_tools.py
python 05-agent-with-memory/agent_with_memory.py
```
**Every module runs with no key** — a tiny scripted stand-in model drives the *real*
agent so you can watch the ReAct loop offline. Add a `GROQ_API_KEY` and a real Llama
model takes over the reasoning.

## Today's exercise
Do both in [`exercises/`](exercises/README.md):
1. **Unit-converter agent** — write two tools, build the agent, let it self-route.
2. **Help-desk agent** — a lookup tool + a system prompt + memory across turns.

## Latest-syntax notes (LangChain 1.x)
- `from langchain.agents import create_agent` — the current, recommended name.
  (`langgraph.prebuilt.create_react_agent` is the older LangGraph-level equivalent.)
- Build: `create_agent(model, tools, system_prompt=..., checkpointer=...)`.
- Invoke: `agent.invoke({"messages": [("human", "…")]}, config)`; the answer is the
  **last** message: `result["messages"][-1].content`.
- Stream steps: `agent.stream(inputs, config, stream_mode="updates")` — one chunk per
  node (`model` / `tools`).
- Memory: compile with a `checkpointer` (`MemorySaver`) and pass a `thread_id`.

## The big idea
> Day 23 taught you the loop by writing it. Day 24 taught you the engine that runs
> loops. Today they fuse: `create_agent(model, tools)` gives you a real ReAct agent
> in one line — it reasons, calls tools, observes, and answers on its own. From here
> on you *use* agents; you don't hand-build the loop.

➡ Next: **Day 26 — CrewAI** — when one agent isn't enough, give several agents roles
and let them collaborate.
