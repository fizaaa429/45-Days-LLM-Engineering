# 04 — Appending Messages (Memory!)

This is the heart of the whole day. The fix for the amnesia in Step 3 is one sentence:

> **Keep one `messages` list for the whole conversation, and append every turn to it.**

## The idea
Instead of building a fresh one-item list each call, we make a list **once** and let it grow:

```python
messages = []                                              # the conversation, kept alive

while True:
    user_text = input("You: ")
    messages.append({"role": "user", "content": user_text})   # 1. add what the user said

    reply = call_model(messages)                              # 2. send the WHOLE history

    messages.append({"role": "assistant", "content": reply})  # 3. add what the bot said
    print("Bot:", reply)
```

Every loop adds **two** messages — the user's, then the assistant's. So after a few turns the list
looks like a transcript:

```python
[
  {"role": "user",      "content": "My name is Riya."},
  {"role": "assistant", "content": "Nice to meet you, Riya!"},
  {"role": "user",      "content": "What is my name?"},
  {"role": "assistant", "content": "Your name is Riya."},   # <-- it knows now!
]
```

## Why this works
The model is still stateless — but now **we** carry the state. On every call we re-send the entire
transcript, so the model reads the whole story before answering. The "memory" lives in *your list*,
not in the model.

| Step 2/3 (no memory) | Step 4 (memory) |
|----------------------|-----------------|
| new `[one message]` each call | one list that **grows** |
| model sees only the latest line | model sees the **whole** conversation |
| forgets instantly | remembers everything in the list |

## Why append the assistant's reply too?
Easy to forget this one. If you only append the user's messages, the bot won't remember **its own**
previous answers — it'll contradict itself. The transcript must include both sides.

## The catch (we'll handle it later)
The list grows forever, and every call re-sends all of it. That costs more tokens each turn and
eventually overflows the context window (Day 9). Real apps **trim** or **summarise** old turns —
you'll do exactly that when we build memory for agents in Phase 3.

Run it (needs `GROQ_API_KEY` in `.env`) and try: *"My name is Riya."* then *"What is my name?"*
```bash
python chatbot.py
```

➡ Next: [05-system-prompt](../05-system-prompt/) — give your bot a personality.
