# 03 · Inside the Loop

Module 02's agent gave a one-line answer. But underneath it ran the **same loop you
wrote on Day 23**. Let's open it up.

## The message trail *is* the loop

Every step an agent takes is a **message**. A tool-using answer always looks like this:

```
1. HumanMessage    "Multiply 6 by 7, then add 100."
2. AIMessage       (empty text, but .tool_calls = [multiply(6, 7)])   ← REASON + ACT
3. ToolMessage     "42"                                                ← OBSERVE
4. AIMessage       (empty text, .tool_calls = [add(42, 100)])          ← REASON + ACT
5. ToolMessage     "142"                                               ← OBSERVE
6. AIMessage       "6 x 7 = 42, and 42 + 100 = 142."                   ← ANSWER
```

Model → Tool → Model → Tool → Model. Compare it to Day 23's `while` loop — it's the
exact same shape, just generated for you.

## Two ways to watch it

**Read the final list** — every message is a step:
```python
result = agent.invoke({"messages": [("human", question)]})
for m in result["messages"]:
    print(type(m).__name__)
```

**Stream it live** — `stream_mode="updates"` yields one chunk per node that fires:
```python
for chunk in agent.stream({"messages": [("human", q)]}, stream_mode="updates"):
    for node, update in chunk.items():   # node is "model" or "tools"
        print(node, update["messages"][-1])
```
The two node names — `model` (the LLM reasoning/acting) and `tools` (a tool running)
— are the two halves of the ReAct loop. This is what powers the "How I got this"
step trace you'll build in the mini-project.

## Run it

```bash
python inside_the_loop.py
```

Runs offline (scripted stand-in) or live with a `GROQ_API_KEY`. The offline script
does a **two-tool** question so you see the loop go around **twice**.

## Gotcha
- An `AIMessage` with `.tool_calls` usually has **empty** `.content` — the model is
  "speaking" in tool calls, not text. Don't mistake empty content for "no answer";
  check `.tool_calls` first.

➡ Next: [`04-system-prompt-and-tools/`](../04-system-prompt-and-tools/README.md) — steer the agent and give it a real toolbox.
