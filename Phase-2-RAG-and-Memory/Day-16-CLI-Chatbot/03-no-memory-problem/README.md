# 03 — The "No Memory" Problem

This is the most important module of the day — not because of the code, but because of the
**problem it reveals**. Our chat loop *looks* like it works, but the bot can't remember anything
you said a second ago.

## See it for yourself
This script makes **two separate calls**:
1. We tell it: *"My name is Riya."*
2. We ask it: *"What is my name?"*

A human would answer "Riya." Our bot **can't** — and prints something like *"I don't know your
name."* Run it:

```bash
python no_memory.py
```

## Why does it forget?
Because each call sends **only one message**:

```python
ask("My name is Riya.")      # messages = [ {user: "My name is Riya."} ]
ask("What is my name?")      # messages = [ {user: "What is my name?"} ]  <- a fresh list!
```

The API is **stateless**. The model isn't a running program that remembers you — it's a function
that gets *only the list of messages you hand it*, every single time. The first call's message is
**gone** by the time the second call happens.

> Mental model: the model has total amnesia between calls. The *only* thing it knows is the list of
> messages in front of it right now.

## So what's the fix?
If the model only knows what's in the list... then we have to **keep the list and add to it.**
Don't throw the history away — **append** each turn so the next call carries the whole story.

That one idea is the entire next module.

➡ Next: [04-appending-messages](../04-appending-messages/) — give the bot a memory.
