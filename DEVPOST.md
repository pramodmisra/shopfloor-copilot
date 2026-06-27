# ShopFloor Copilot — Devpost Submission

**Tagline:** The maintenance work-order agent. An operator types what's wrong; it reads the manual, diagnoses the cause, checks parts and safety, and writes the work order — in 20 seconds.

---

## Inspiration
On a manufacturing floor, the most expensive minutes are the ones right after a machine starts acting up. The operator who notices it usually isn't the person who can fix it — so they either flag down a maintenance tech who's already busy, or thumb through a binder while the line backs up. Two bad things happen under that time pressure: diagnosis drags out, and someone restarts a faulting machine or skips lockout/tagout to "just check something." Zapdos Labs frames the wedge perfectly — *AI that reads the manual* — and we wanted to take that all the way to the artifact a plant actually runs on: the work order. Not a chatbot that explains conveyors, but an agent that hands a technician a complete, safe, parts-checked job ticket.

## What it does
An operator describes the fault in plain language — *"Line 3 conveyor grinding at the drive end, smells like burning."* ShopFloor Copilot runs an agentic loop that:
1. **Checks the asset's work-order history first** — and flags recurring failures ("BEARING_FAILURE 3× in 8 weeks → this is a misalignment problem, not a bearing problem; fix the root cause, don't swap another bearing"). That's the thing a paper binder can't do.
2. **Reads the equipment manual** to diagnose probable root causes, each tagged with a confidence level and the manual section that supports it.
3. **Confirms parts** — real on-hand quantity and lead time for every part it recommends.
4. **Pulls the matching OSHA lockout/tagout procedure** so the safety steps lead the job.
5. **Dollarizes the impact** — labor + parts + downtime cost. The burning-smell case lands at ~$274K total exposure (driven by a 3-day wait on an out-of-stock bearing), which makes the case to stock the part and fix the root cause.
6. **Emits a structured work order** and a **CMMS-ready payload** (Fiix/UpKeep field shape) — one click to export or "Create in Fiix," with supervisor sign-off required and the safety procedure sourced from the facility's approved energy-control procedure, not invented by the LLM.

And it **works on *your* equipment**: upload your own manual PDF and LlamaParse turns it into the agent's knowledge base — we demo it diagnosing a hydraulic press from an uploaded manual, not just the seeded conveyor. Every run exposes its reasoning trace, so a supervisor sees exactly which tools the agent called and why. A burning smell is correctly escalated to "emergency."

## How we built it
A single FastAPI service serves both the JSON API and a vanilla-JS single-page UI — one process, one Railway deploy. The brain is an Anthropic **Claude `claude-sonnet-4-6`** agentic tool-use loop. We give Claude the active equipment manual in a **prompt-cached** system block (reliable, exact retrieval without the fragility of a vector DB on a 24-hour clock) plus four tools: `lookup_asset_history` (recent work orders → recurring-failure detection), `lookup_part` (MRO catalog: stock, lead time, cost, bin), `get_safety_procedure` (LOTO/PPE by hazard, modeled on OSHA 29 CFR 1910.147), and a **strict** `create_work_order` tool that guarantees the output validates against our Pydantic schema and renders directly. The loop is hard-bounded at 15 steps, every model call is wrapped in retry + exponential backoff, and the API key is read only from the environment. `cmms.py` maps the work order to a Fiix/UpKeep-shaped payload. For "works on your equipment," `/api/upload_manual` sends the operator's PDF to **LlamaParse** (via httpx REST — no heavy SDK) and swaps it in as the active manual. Seed data — manual, parts catalog, safety procedures, asset history, demo faults — lives as JSON/Markdown so the same engine repoints at any asset.

## Challenges we ran into
Keeping the demo *believable to an operations manager* meant the diagnosis couldn't be generic. We authored a realistic conveyor manual with troubleshooting tables that map specific symptom patterns (grinding + burning smell → failing drive-pulley bearing; hum-then-trip → mechanical bind) to specific catalog parts, so the agent's reasoning is traceable rather than plausible-sounding. We also had to force a clean terminal state — the agent must always end with one complete work order — which we solved by forcing the `create_work_order` tool on the final step if needed. And we tuned the manual length to actually cross Claude's prompt-cache threshold so repeat demo runs stay fast and cheap.

## Accomplishments that we're proud of
It's genuinely end-to-end and genuinely deployable: a real person at a line could use it Monday. Safety is first-class — LOTO steps always precede repair steps, and hazards drive severity. The output isn't prose; it's a structured work order a CMMS could ingest. And the agent shows its work, which is what earns trust on a floor.

## What we learned
For an industrial agent, the win condition isn't model cleverness — it's whether the output is *safe, specific, and shaped like the artifact the floor already uses*. Strict structured output plus a small set of well-described tools beat an open-ended chatbot on every one of the judging criteria. Prompt caching the manual was the right call over a vector store for a bounded, single-asset demo.

## What's next
- **Live CMMS write-back** (we export the payload + mock "Create in Fiix" today): real OAuth into Fiix/UpKeep/Maximo and notify the on-call tech.
- **Per-asset parts + history feeds** wired to the customer's CMMS, so the manual upload also brings in their real catalog and failure log.
- **Floor-native input**: voice (gloves/noise), photo of the nameplate or the leak — a natural tie-in to Zapdos's factory-floor video AI.
- **Bilingual EN/ES** — a large share of the US maintenance workforce is Spanish-speaking; accept and answer in the operator's language.
- **OT-network deployment**: runs in the IT DMZ with a floor kiosk, plus an on-prem/edge model option for air-gapped plants (Purdue model / IEC 62443).
- **Feedback loop + fleet view**: technician confirms the actual fix to sharpen per-machine priors; cluster recurring faults to flag the machine that needs a PM, not another work order.

**Built by Pramod Misra** — Director of Data Analytics, Snellings Walters Insurance / founder, 5gVector.
