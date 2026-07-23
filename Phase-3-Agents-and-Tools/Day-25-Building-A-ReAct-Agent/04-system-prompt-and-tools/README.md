# 04 · System Prompt + a Real Toolbox

Two upgrades turn the toy calculator into a real agent.

## 1. A system prompt = the agent's job description

```python
agent = create_agent(model, tools, system_prompt=(
    "You are StudyBot, a concise study assistant. "
    "Always use a tool for arithmetic or lookups -- never guess."
))
```

The system prompt sets the **persona** and the **rules**. "Never guess the maths,
always use the tool" is a classic one — it stops the model from doing shaky mental
arithmetic when a reliable tool is right there.

## 2. Multiple tools = the model routes itself

Hand over a **toolbox** and let the model pick:

```python
TOOLS = [calculator, word_count, lookup_note]
agent = create_agent(model, TOOLS, system_prompt=SYSTEM_PROMPT)
```

You never write `if question is about maths: ...`. Ask *"give me the note on 'agent'
and what is 3 × 4?"* and the model calls **`lookup_note`** and **`calculator`** on
its own, in order. **That self-routing is what makes it an agent** — not a script.

| Question | Tool the model picks |
|----------|----------------------|
| "What is 45 × 12?" | `calculator` |
| "How many words in this paragraph?" | `word_count` |
| "Explain RAG" | `lookup_note` |
| A mix of the above | several, in sequence |

## Run it

```bash
python system_prompt_and_tools.py
```

Streams the tools the agent chose, then prints its final one-sentence answer.
Offline, a scripted stand-in shows it calling **two** different tools for one
question.

## Gotcha
- A tool's **docstring and argument names are the model's only instructions** for
  when/how to call it. Vague docstrings → wrong tool picked. Write them like you're
  explaining the tool to a new teammate.

➡ Next: [`05-agent-with-memory/`](../05-agent-with-memory/README.md) — give the agent memory so it remembers across turns.
