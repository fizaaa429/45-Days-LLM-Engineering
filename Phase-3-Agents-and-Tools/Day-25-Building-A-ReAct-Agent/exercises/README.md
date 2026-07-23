# Day 25 · Exercises

Practise building agents with `create_agent`. Both run **offline** (a scripted
stand-in drives the real agent) — add a `GROQ_API_KEY` to see a real model choose.

> **Work the muscle, not the memory.** Plan before you code, struggle for ~20 min
> before peeking, and after you solve it, cover the solution and rewrite it. (The
> five practice rules from the Problem-Solving Bootcamp apply here too.)

## 1. Unit-converter agent — [`unit_converter_agent.py`](unit_converter_agent.py)
Write **two** conversion tools (`celsius_to_fahrenheit`, `km_to_miles`), drop them
in a list, and build the agent with `create_agent(model, TOOLS)`. Ask a question
and watch the model pick the right tool — you write **zero** routing logic.

**You'll practise:** authoring `@tool` functions with model-readable docstrings, and
the two-ingredient `create_agent(model, tools)` call.

## 2. Help-desk agent with memory — [`helpdesk_agent.py`](helpdesk_agent.py)
Build a support agent that looks answers up in a small FAQ (`search_faq`), has a
persona (`system_prompt`), and **remembers** across turns (`checkpointer` +
`thread_id`) so a follow-up like *"and does it go back to my card?"* works.

**You'll practise:** a lookup tool, a steering system prompt, and agent memory —
the full stack from modules 04 and 05.

## Running
```bash
python unit_converter_agent.py      # your work
python unit_converter_agent_solution.py
python helpdesk_agent.py
python helpdesk_agent_solution.py
```

Each file has `# TODO` markers; the offline stand-in model and the demo harness are
provided, so once your tools + `create_agent` call are right, it just runs.
