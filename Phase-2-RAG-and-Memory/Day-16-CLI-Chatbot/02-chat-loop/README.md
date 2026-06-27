# 02 — The Chat Loop

A single call is boring — you ask once and the program ends. A *chat* keeps going. We wrap the call
from Step 1 in a **`while True` loop** so you can type message after message, and we add a way to
**quit** cleanly.

## The pattern
```python
while True:
    user_text = input("You: ")          # 1. read what the user typed
    if user_text.lower() in {"/exit", "/quit"}:
        break                            # 2. let them leave
    reply = ask(user_text)               # 3. send it, get a reply
    print("Bot:", reply)                 # 4. show it -> loop again
```

Three habits worth copying:
- **A quit command.** Never trap the user in an infinite loop — `/exit` breaks out.
- **Skip empty input.** If they just hit Enter, don't waste an API call.
- **A clear prompt** (`You: `) so they know it's their turn.

## But notice...
Each time through the loop we still send **only the current message**:

```python
messages = [{"role": "user", "content": user_text}]   # just THIS turn
```

So the bot answers each line in isolation. It feels like a conversation, but it isn't one yet —
the model has no idea what you said a moment ago. Step 3 proves it.

Run it (needs `GROQ_API_KEY` in `.env`):
```bash
python chat_loop.py
```

➡ Next: [03-no-memory-problem](../03-no-memory-problem/) — watch the bot forget your name.
