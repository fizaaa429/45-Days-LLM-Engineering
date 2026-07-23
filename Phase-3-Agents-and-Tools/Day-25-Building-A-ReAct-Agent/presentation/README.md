# Day 25 deck — *The ReAct agent: one line that replaces your loop* (speaker notes)

Open [`index.html`](index.html) in any browser. `→` / `Space` to advance, `F` for fullscreen.
14 slides ≈ 30 min, leaving the rest of the 3-hour block for the modules + mini-project.

**The through-line:** Day 23 you *wrote* the tool-calling loop. Day 24 you learned the *engine*
(LangGraph). Today they fuse: `create_agent(model, tools)` builds the whole ReAct loop in one line.
Keep returning to the phrase **"same loop, less typing"** — the one-liner is never magic because they
already built it by hand.

| # | Slide | Time | What to say / do |
|---|-------|------|------------------|
| 1 | Cover | 1′ | "Two days ago you wrote ~15 lines to make a model act. Tonight it's one line — and you'll know exactly what's inside it." |
| 2 | Day 23 loop, by hand | 3′ | Read the `while` aloud. This is *recap* — most of them wrote this. Land: "it worked, but every new agent meant re-typing this plumbing." |
| 3 | ReAct = Reason + Act | 3′ | Walk the loop diagram. The red backward arrow = "not done, reason again." Say clearly: **Day 23's `while` was already ReAct** — they just wrote every line. |
| 4 | The one line | 3′ | The reveal. Live-type `create_agent(model, tools)` if you can. Key payoff: it returns a **compiled LangGraph agent** = yesterday's engine. Stress "never magic — you built it by hand." |
| 5 | Two ingredients | 3′ | Model + list of tools. Tools are unchanged Day-23 `@tool` functions. Hammer the #1 beginner bug: the answer is `result["messages"][-1].content`, not the raw dict. |
| 6 | The message trail | 3′ | Point at the 6-message trail; map each to Reason/Act/Observe/Answer. "This is Day 23's loop, generated for you." An `AIMessage` with tool_calls usually has **empty** content — check `.tool_calls`, not content. |
| 7 | Stream the steps | 3′ | `stream_mode="updates"` → one chunk per node. Two node names: `model` and `tools` = the two halves of ReAct. This stream is what feeds the "How I got this" trace later. |
| 8 | System prompt + toolbox | 4′ | Two upgrades: the system prompt sets persona + rules ("never guess the maths"); many tools → **the model routes itself**, you write zero `if`. Then the punchline: docstrings are the model's only instructions — write them well. |
| 9 | Memory | 3′ | Identical to Day 24: `checkpointer` + `thread_id`. Same bot, now with tools. One `thread_id` per user = many private chats from one agent. |
| 10 | By hand vs create_agent | 2′ | The scoreboard. Note the last row: both "understand what it does" are ✅ — *because* they built it first. Chains/hand-loops aren't shameful; this is just less typing. |
| 11 | Mini-project | 3′ | Sell it: **SoftBot**, one example scaled 6 times, each step = one concept. On-ramp to Project 3 (needs 3+ tools; SoftBot has 3). All six steps run with no key. |
| 12 | Roadmap | 2′ | The motivation slide: 23 tools → 24 engine → 25 one line → 26 many agents. "Day 23's `while` was a graph with a backward edge; `create_agent` draws that graph for you." |
| 13 | Recap | 2′ | Read the five bullets; class fills blanks. Then point them at modules → mini-project → exercises. |
| 14 | Close | 1′ | "You wrote the loop; now you just use it. From here you compose agents." Tee up Day 26. |

## Q&A ammo
- **"`create_agent` vs `create_react_agent`?"** Same idea. `create_agent` (in `langchain.agents`) is
  the current LangChain 1.x name; `langgraph.prebuilt.create_react_agent` is the older LangGraph-level
  one. Teach `create_agent`.
- **"Why did we bother writing the loop by hand on Day 23, then?"** So this line isn't a black box.
  When an agent misbehaves (wrong tool, infinite loop, bad final answer) you can picture the exact
  `while` it's running and debug it. That's the whole reason Day 23 came first.
- **"Can I still see/control the loop?"** Yes — `.stream()` shows every step; `recursion_limit` caps
  it; and because it's a compiled LangGraph, you can inspect/extend the graph (Day 24 skills apply).
- **"Does it work without an API key?"** The *machinery* does — every module here drives the real
  agent with a scripted stand-in model so students see the loop offline. Real reasoning needs a Groq
  key (free tier).
- **"When would I NOT use create_agent?"** When you need custom control flow the prebuilt loop doesn't
  cover (multiple specialised sub-graphs, human-in-the-loop approvals mid-loop, unusual routing) —
  then you hand-build the graph in LangGraph (Day 24). `create_agent` is the fast path for the common
  ReAct shape.
- **"How is this different from Day 24's chatbot?"** Day 24's chatbot just talked. This agent has
  **tools** and decides when to call them. Add tools to a `MessagesState` graph + a tools node + a
  loop and you've basically re-derived `create_agent`.

## If you're short on time
Cut slides 7 (stream) and 10 (scoreboard) — mention them verbally. Never cut 3 (ReAct), 4 (the one
line), or 12 (roadmap): those carry the day's whole argument.
