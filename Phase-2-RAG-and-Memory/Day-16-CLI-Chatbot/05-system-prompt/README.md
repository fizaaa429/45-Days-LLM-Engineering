# 05 — The System Prompt (Give It a Personality)

Your bot remembers now, but it's generic. The **system prompt** is how you set its *role, tone, and
rules* — once, up front, before the user says anything.

## A third role
Remember the three roles? `user`, `assistant`, and now **`system`**. A system message is an
instruction *about how to behave*, not part of the chit-chat. It goes **first** in the list:

```python
messages = [
    {"role": "system", "content": "You are Sparky, a cheerful tutor for Indian B.Tech students. "
                                  "Explain simply, use small examples, and keep replies under 4 sentences."},
]
```

Then the conversation appends on top of it exactly like before. Because it stays at the top of the
list, the model re-reads those instructions on **every** turn — so the personality sticks.

## What a good system prompt sets
- **Identity** — "You are Sparky, a coding tutor."
- **Audience** — "...for first-year students who know only basic Python."
- **Tone** — "Friendly, encouraging, no jargon."
- **Rules / limits** — "Keep answers under 4 sentences. If unsure, say so."

## Try this
Run it, then ask the same question with two different system prompts (edit `SYSTEM_PROMPT`):
- *"You are a pirate."*  vs  *"You are a formal professor."*

Same question, completely different voice — and you never told the user-facing code anything about
tone. That's the power of the system message.

```bash
python chatbot_persona.py
```

> Heads-up: the system prompt **guides** behaviour, it doesn't *lock* it. A user can still try to
> talk around it — defending against that ("prompt injection") is a Phase 3 topic.

➡ Next: [06-commands-and-save](../06-commands-and-save/) — `/reset`, `/save`, `/load`.
