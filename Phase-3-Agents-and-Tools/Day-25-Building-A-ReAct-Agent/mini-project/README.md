# Mini-Project · SoftBot — a multi-tool campus assistant

One example, **scaled six times**. Each step adds exactly one idea from today's
modules, so you watch a one-line toy grow into a real assistant with a toolbox,
a personality, memory, and a visible "How I got this" trace — then a web UI.

This is your **on-ramp to Project 3** (the Personal Research Agent, which must use
3+ tools). SoftBot already uses three.

## The steps

| Step | File | Adds | Needs a key? |
|-----:|------|------|:---:|
| 1 | [`step1_hello_agent.py`](step1_hello_agent.py) | The smallest agent: one tool, `create_agent`, `.invoke` | No |
| 2 | [`step2_watch_the_loop.py`](step2_watch_the_loop.py) | `.stream()` — see reason → act → observe | No |
| 3 | [`step3_toolbox.py`](step3_toolbox.py) | Three tools; the model routes itself | No |
| 4 | [`step4_persona.py`](step4_persona.py) | A `system_prompt` — persona + rules | No |
| 5 | [`step5_memory.py`](step5_memory.py) | `checkpointer` + `thread_id` — follow-up questions | No |
| 6 | [`step6_softbot.py`](step6_softbot.py) | The finished **brain**: all of the above + a step trace | No |
|   | [`app.py`](app.py) | A Streamlit chat UI on top of step 6 | Yes (to chat) |

Every `stepN` file is **standalone** and runs **offline** — a scripted stand-in
model drives the *real* agent so you see the loop with no API key. Add a
`GROQ_API_KEY` and a real Llama model takes over.

## SoftBot's toolbox

| Tool | Does |
|------|------|
| `search_handbook(topic)` | Looks up a campus note: fees, hostel, library, exam, wifi |
| `calculator(a, b, op)` | add / sub / mul / div |
| `word_count(text)` | Counts words |

## Run it

```bash
pip install langchain langchain-groq streamlit python-dotenv
python step1_hello_agent.py      # ... through step6
python step6_softbot.py          # scripted two-turn demo with a trace
streamlit run app.py             # the web app (needs a key to chat)
```

Put your free key in a `.env` in this folder:
```
GROQ_API_KEY=your_key_here
```

## How the pieces map to the modules

- **Steps 1–2** ⇒ module 01–03 (`create_agent`, the loop, streaming).
- **Steps 3–4** ⇒ module 04 (toolbox + system prompt).
- **Step 5** ⇒ module 05 (memory).
- **Step 6 + app.py** ⇒ everything, plus the Day 23 "brain vs UI" split: `step6_softbot.py`
  has **no Streamlit** (so it stays testable), and `app.py` is the thin UI.

## Checkpoint questions
<details><summary>Why does <code>step6_softbot.py</code> keep Streamlit out of it?</summary>
So the agent logic can be imported and tested (and reused by a CLI, a bot, etc.)
without spinning up a web server. UI and brain stay separate — same rule as Day 23.
</details>
<details><summary>The app never replays old messages to the model. How does it remember?</summary>
The agent's own <code>checkpointer</code> stores history keyed by <code>thread_id</code>.
Each turn we send only the new message; the checkpointer reloads the rest. That's
the <code>create_agent</code> way, vs. Day 16's "pass the whole list back" by hand.
</details>

## Stretch goals
1. Add a 4th tool (e.g. `days_until(date)` or `define(term)`) and confirm the model
   picks it — no routing code needed.
2. Add a "Clear chat" button that resets `st.session_state` **and** starts a new
   `thread_id` (so memory truly resets).
3. Tighten the system prompt so SoftBot refuses off-topic questions politely.

➡ Back to the [day README](../README.md) · Next day: **Day 26 — CrewAI** (role-based multi-agent).
