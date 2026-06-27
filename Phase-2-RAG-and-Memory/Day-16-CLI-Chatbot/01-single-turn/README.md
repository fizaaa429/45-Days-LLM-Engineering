# 01 — Single Turn: One Message In, One Reply Out

Before we build a *chat*, let's make the smallest possible thing: send **one** message to the model
and print its reply. This is the same Groq call you saw on Day 12 — we're just looking closely at
the **shape of a message** because everything today is built on it.

## The shape of a message
Every chat API speaks in **messages**. A message is a dict with two keys:

```python
{"role": "user", "content": "Hello!"}
```

- `role` — who is speaking: `"user"` (you), `"assistant"` (the model), or `"system"` (instructions).
- `content` — the actual text.

And you don't send *one* message — you always send a **list** of them:

```python
messages = [
    {"role": "user", "content": "Hello!"},
]
```

Right now the list has just **one** item. The entire lesson today is: **what happens as this list
grows.**

## The call
```python
chat = client.chat.completions.create(
    model="llama-3.3-70b-versatile",
    messages=messages,                       # <-- a LIST of messages
)
reply = chat.choices[0].message.content      # the assistant's text
```

The reply comes back buried in `chat.choices[0].message.content`. We pull it out and print it.

| You send | You get back |
|----------|--------------|
| `messages` (a list of role/content dicts) | `chat.choices[0].message.content` (the reply text) |

## Gotchas
- The reply is **not** `chat.text`. It's `chat.choices[0].message.content` — the chat format
  supports multiple "choices", and we take the first.
- Model names change. If `llama-3.3-70b-versatile` stops working, check
  [console.groq.com/docs/models](https://console.groq.com/docs/models) for a current free model.

Run it (needs `GROQ_API_KEY` in `.env`):
```bash
python single_turn.py
```

➡ Next: [02-chat-loop](../02-chat-loop/) — wrap this in a loop so you can keep talking.
