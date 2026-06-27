# 2-Minute Demo Video Script — ShopFloor Copilot

> Record screen + voiceover. Have the app open at the live URL with the input box empty. Total ~2:00.

### [0:00–0:15] Hook — the problem
> "On a plant floor, the most expensive minutes are right after a machine starts acting up. The operator who notices it usually can't fix it — so they flag down a busy tech or thumb through a binder while the line backs up. And under that pressure, someone restarts a faulting machine or skips lockout/tagout."

*(On screen: the empty ShopFloor Copilot UI.)*

### [0:15–0:30] The ask
> "ShopFloor Copilot is an AI agent that reads the equipment manual and turns a plain-language fault report into a complete, safe work order — in about 20 seconds."

*(Click the first demo chip: "Line 3 conveyor grinding at the drive end… burning smell." Click **Diagnose**.)*

### [0:30–1:30] Live demo — the core workflow
While it runs (button shows "Agent working… reading manual, checking parts & safety"):
> "Watch what it's doing. It's reading the conveyor manual, diagnosing the cause, then calling tools — one to check spare-parts stock, one to pull the OSHA lockout/tagout procedure."

*(Work-order card renders.)*
> "Here's the work order. Severity **emergency** — it caught the burning smell. But look at the top: a **recurring-failure** flag. The agent checked this machine's history and found this bearing has failed three times in eight weeks — so it's telling me to stop swapping bearings and fix the *root cause*: shaft alignment. That's the thing a binder can never tell you."

*(Point to the cost panel.)*
> "And it dollarizes the impact: **$274,000 total exposure** — because the bearing is out of stock on a three-day lead, that's 72 hours of downtime. That number is the business case to stock the part and fix the alignment."

*(Scroll to safety + parts.)*
> "Safety comes first — full lockout/tagout, and notice the note: these steps come from the facility's *approved* OSHA energy-control procedure, not invented by the AI, and the work order **requires supervisor sign-off**. Then the repair steps, then the exact parts with real availability."

*(Click "Create in Fiix CMMS".)*
> "And it's not a dead-end screen — one click pushes a CMMS-ready work order into Fiix, so the tech doesn't re-key anything."

*(Expand "Show agent reasoning".)*
> "It shows its work — every tool call: history, parts, safety. That's what earns trust on a floor."

### [1:30–1:50] Architecture — one slide
> "Under the hood: a FastAPI service and a Claude agentic loop. The full manual is prompt-cached; three tools — parts, safety, and a strict work-order writer that guarantees structured output. One service, deployed live on Railway."

*(Show ARCHITECTURE.md data-flow diagram, or the architecture slide.)*

### [1:50–2:00] Close — works on YOUR equipment + what's next
> "And it's not locked to one machine — upload your own equipment manual and LlamaParse makes it the agent's knowledge base. Here it's diagnosing a hydraulic press from a manual we just uploaded."

*(Optional: show the uploaded-manual diagnosis, or just say it.)*
> "Voice input at the line, bilingual for the floor, live CMMS write-back next. A 30-minute triage becomes 20 seconds. ShopFloor Copilot. Thanks."

---

**Recording tips:**
- Run one warm-up diagnosis first so the prompt cache is hot (warm runs ~45s vs ~75s cold).
- Keep the burning-smell fault as the hero — emergency + recurring + $274K reads beautifully.
- **Demo the conveyor faults FIRST, upload your own manual LAST.** The uploaded manual becomes the active manual for everyone until the next deploy, so don't upload before showing the conveyor demo. (To reset to the seeded conveyor manual, redeploy: `railway redeploy` / push.)
- For the upload beat, have a real OEM manual PDF (or the included press-manual test PDF) ready.
