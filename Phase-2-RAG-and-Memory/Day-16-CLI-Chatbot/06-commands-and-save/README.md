# 06 — Commands & Saving the Conversation

The bot works. Let's make it feel like a real tool by adding **slash commands** and the ability to
**save and reload** a conversation. The trick is simple: before sending a line to the model, check
if it's a *command* and handle it ourselves.

## Command dispatch
```python
if user_text == "/reset":
    messages = [{"role": "system", "content": SYSTEM_PROMPT}]   # wipe history, keep persona
    continue
```

We intercept lines that start with `/` and act on them instead of calling the API. Today's commands:

| Command | What it does |
|---------|--------------|
| `/exit` or `/quit` | leave the chat |
| `/reset` | clear the conversation (but keep the system prompt) |
| `/history` | print how many turns are stored |
| `/save` | write the whole `messages` list to `chat_history.json` |
| `/load` | read it back and continue where you left off |

## Saving is just the list -> JSON
Here's the nice payoff of using a plain list of dicts: it's **already** JSON-shaped. Saving is one line.

```python
import json

with open("chat_history.json", "w", encoding="utf-8") as f:
    json.dump(messages, f, indent=2, ensure_ascii=False)
```

Loading is the mirror image (`json.load`). Because the file *is* the conversation, you can close the
program, reopen it, `/load`, and the bot picks up with full memory of the earlier chat.

> This is why the `messages` format is everywhere: it's human-readable, trivially serialisable, and
> portable across providers. The same JSON you save here could be replayed into Gemini or OpenAI.

## `/reset` keeps the system prompt
Note the detail: reset rebuilds the list with the system message still at index 0. You want a fresh
conversation, not a personality wipe.

Run it:
```bash
python chatbot_full.py
```
Chat a little, `/save`, `/exit`, run it again, `/load`, then ask about something from before.

➡ Next: practise in [../exercises/](../exercises/), then **Day 17 — Embeddings**.
