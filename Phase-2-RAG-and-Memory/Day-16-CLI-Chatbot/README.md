# Day 16 — Build a CLI Chatbot (Conversation Memory)

Yesterday you shipped a one-shot app (the summarizer). Today you build something that **remembers
the conversation** — a chatbot you talk to in your terminal. The single idea that makes a chatbot
work is small but powerful: **keep a list of messages and append every turn to it.**

We build it in **6 steps**, and each step exposes a problem the next step fixes — so you understand
*why* every line is there, not just *what* it does.

## Learning objectives
By the end of today you can:
- Run an interactive **chat loop** in the terminal (`input()` + `while True`)
- Explain why a plain LLM call has **no memory** between turns
- Maintain a **`messages` list** and **append** each user + assistant turn
- Send the **whole history** on every call so the model has context
- Shape behaviour with a **system prompt**
- Add chat **commands** (`/reset`, `/save`, `/load`) and persist history to JSON

## Modules (work through them in order)

| # | Module | What it teaches | The "aha" |
|--:|--------|-----------------|-----------|
| 01 | [single-turn](01-single-turn/) | One message in -> one reply out | A call is just request -> response |
| 02 | [chat-loop](02-chat-loop/) | `while True` + `input()` + `/exit` | Now it's interactive... |
| 03 | [no-memory-problem](03-no-memory-problem/) | Watch it forget your name | Each call is independent |
| 04 | [appending-messages](04-appending-messages/) | Keep + **append** a `messages` list | **Memory!** (the core lesson) |
| 05 | [system-prompt](05-system-prompt/) | Give the bot a persona | Shaping behaviour |
| 06 | [commands-and-save](06-commands-and-save/) | `/reset`, `/save`, `/load` to JSON | Polish + real feel |

Then practise in **[exercises/](exercises/)**.

## Provider: Groq (free + fast)
We use **Groq** — a free, very fast hosted API that speaks the standard `messages` chat format
(the same `[{"role": ..., "content": ...}]` shape you'll see everywhere, including OpenAI).

## Setup
```bash
pip install -r requirements.txt        # needs: groq, python-dotenv
```
Get a **free** key at [console.groq.com/keys](https://console.groq.com/keys) and put it in a `.env`:
```bash
# .env  (never commit this)
GROQ_API_KEY=your_key_here
```

## How to run
```bash
python 01-single-turn/single_turn.py
```

## Today's exercise
Extend the chatbot: add a **token/turn counter** and a **persona picker**. See [`exercises/`](exercises/).

> The `messages` list you build today is the same structure that powers RAG (Phase 2) and agents
> (Phase 3) — there you'll *inject* retrieved facts and tool results into this very list.

➡ Next (Day 17): Embeddings fundamentals — turning text into vectors.
