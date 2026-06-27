# ShopFloor Copilot — Devpost Submission

**Tagline:** The maintenance work-order agent. An operator types what's wrong; it reads the manual, diagnoses the cause, checks parts and safety, and writes the work order — in 20 seconds.

---

## Inspiration
On a manufacturing floor, the most expensive minutes are the ones right after a machine starts acting up. The operator who notices it usually isn't the person who can fix it — so they either flag down a maintenance tech who's already busy, or thumb through a binder while the line backs up. Two bad things happen under that time pressure: diagnosis drags out, and someone restarts a faulting machine or skips lockout/tagout to "just check something." Zapdos Labs frames the wedge perfectly — *AI that reads the manual* — and we wanted to take that all the way to the artifact a plant actually runs on: the work order. Not a chatbot that explains conveyors, but an agent that hands a technician a complete, safe, parts-checked job ticket.

## What it does
An operator describes the fault in plain language — *"Line 3 conveyor grinding at the drive end, smells like burning."* ShopFloor Copilot runs an agentic loop that (1) reads the equipment manual to diagnose probable root causes, each tagged with a confidence level and the manual section that supports it; (2) calls a parts-lookup tool to confirm real on-hand quantity and lead time for every part it recommends; (3) pulls the matching OSHA lockout/tagout procedure so the safety steps lead the job; and (4) emits a structured work order — severity, ordered repair steps, required parts with availability, safety steps, downtime estimate, and an escalation flag. A burning smell is correctly escalated to "emergency." Every run exposes its reasoning trace, so a supervisor can see exactly which tools the agent called and why.

## How we built it
A single FastAPI service serves both the JSON API and a vanilla-JS single-page UI — one process, one Railway deploy. The brain is an Anthropic **Claude `claude-sonnet-4-6`** agentic tool-use loop. We give Claude the full ConvTech CT-2000 conveyor manual in a **prompt-cached** system block (reliable, exact retrieval without the fragility of a vector DB on a 24-hour clock) plus three tools: `lookup_part` (MRO catalog: stock, lead time, cost, bin), `get_safety_procedure` (LOTO/PPE by hazard type, modeled on OSHA 29 CFR 1910.147), and a **strict** `create_work_order` tool that guarantees the final output validates against our Pydantic schema and renders directly into the work-order card. The loop is hard-bounded at 15 steps, every model call is wrapped in retry + exponential backoff, and the API key is read only from the environment. Seed data — manual, parts catalog, safety procedures, demo faults — lives as JSON/Markdown so the same engine repoints at any asset.

## Challenges we ran into
Keeping the demo *believable to an operations manager* meant the diagnosis couldn't be generic. We authored a realistic conveyor manual with troubleshooting tables that map specific symptom patterns (grinding + burning smell → failing drive-pulley bearing; hum-then-trip → mechanical bind) to specific catalog parts, so the agent's reasoning is traceable rather than plausible-sounding. We also had to force a clean terminal state — the agent must always end with one complete work order — which we solved by forcing the `create_work_order` tool on the final step if needed. And we tuned the manual length to actually cross Claude's prompt-cache threshold so repeat demo runs stay fast and cheap.

## Accomplishments that we're proud of
It's genuinely end-to-end and genuinely deployable: a real person at a line could use it Monday. Safety is first-class — LOTO steps always precede repair steps, and hazards drive severity. The output isn't prose; it's a structured work order a CMMS could ingest. And the agent shows its work, which is what earns trust on a floor.

## What we learned
For an industrial agent, the win condition isn't model cleverness — it's whether the output is *safe, specific, and shaped like the artifact the floor already uses*. Strict structured output plus a small set of well-described tools beat an open-ended chatbot on every one of the judging criteria. Prompt caching the manual was the right call over a vector store for a bounded, single-asset demo.

## What's next
- Ingest the real equipment manual (PDF) and CMMS parts feed per asset — the seed JSON is already the seam.
- Write the work order back to the maintenance system (Maximo/Fiix/UpKeep) and notify the on-call tech.
- Voice input at the line (hands/gloves busy) and photo input ("here's the nameplate / the leak").
- A feedback loop: técnico marks the actual fix, and the agent's diagnosis priors improve per machine.
- Fleet view: cluster recurring faults to flag the machine that needs a PM, not another work order.

**Built by Pramod Misra** — Director of Data Analytics, Snellings Walters Insurance / founder, 5gVector.
