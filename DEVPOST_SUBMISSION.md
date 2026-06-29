# Devpost Submission — paste-ready
Hackathon: Zapdos Labs $1,000 Industrial AI Hackathon · https://1-000-industrial-ai-hackathon.devpost.com/

---

## General info

### Project name  (≤60 chars)
**ShopFloor Copilot — Maintenance Work-Order Agent**   *(48 chars)*

Shorter alt if you prefer: `ShopFloor Copilot` (17) · `ShopFloor Copilot: AI Maintenance Agent` (39)

### Elevator pitch / tagline  (≤200 chars)
**Turn a frontline operator's plain-language fault report into a safe, costed, CMMS-ready maintenance work order in ~20 seconds — and catch the repeat failures a paper binder never could.**  *(~186 chars)*

Shorter alt: `An AI agent that turns "it's making the bad noise again" into a safe, costed, CMMS-ready work order in 20 seconds.` *(~112)*

---

## "Try it out" links
- **Live demo:** https://shopfloor-copilot-production.up.railway.app
- **GitHub repo:** https://github.com/pramodmisra/shopfloor-copilot

## Video demo
Upload `ShopFloor_Copilot_90s.mp4` to YouTube (unlisted is fine) and paste the link here.
Title suggestion: *ShopFloor Copilot — AI maintenance work-order agent (90s demo)*

## Built With  (tags)
`python` `fastapi` `anthropic` `claude` `claude-sonnet-4.6` `llamaparse` `llama-cloud` `pydantic` `javascript` `html` `css` `railway` `osha`

## Image gallery
1. **Thumbnail** (set first): `shopfloor_thumbnail.png` (1200×800, 3:2)
2. `shopfloor-light-hero.png` — landing / "Copi" hero
3. `shopfloor-result.png` — a full generated work order
(All in `C:\Users\Pramod Misra\`.)

---

## Project story  (paste into the description / "About the project" editor)

### Inspiration
On a manufacturing floor, the most expensive minutes are the ones right after a machine starts acting up. The operator who notices it usually isn't the person who can fix it — so they either flag down a maintenance tech who's already busy, or thumb through a binder while the line backs up. Two bad things happen under that time pressure: diagnosis drags out, and someone restarts a faulting machine or skips lockout/tagout to "just check something." Zapdos Labs frames the wedge perfectly — *AI that reads the manual* — and we wanted to take that all the way to the artifact a plant actually runs on: the work order. Not a chatbot that explains conveyors, but an agent that hands a technician a complete, safe, parts-checked, costed job ticket.

### What it does
An operator describes the fault in plain language — *"Line 3 conveyor grinding at the drive end, smells like burning."* ShopFloor Copilot runs an agentic loop that:
1. **Checks the asset's work-order history first** — and flags recurring failures ("BEARING_FAILURE 3× in 8 weeks → this is a misalignment problem, not a bearing problem; fix the root cause, don't swap another bearing"). That's the thing a paper binder can't do.
2. **Reads the equipment manual** to diagnose probable root causes, each tagged with a confidence level and the manual section that supports it.
3. **Confirms parts** — real on-hand quantity and lead time for every part it recommends.
4. **Pulls the matching OSHA lockout/tagout procedure** so the safety steps lead the job.
5. **Dollarizes the impact** — labor + parts + downtime cost (often six figures, driven by the wait on an out-of-stock part) — which makes the business case to stock the part and fix the root cause.
6. **Emits a structured work order + a CMMS-ready payload** (Fiix/UpKeep field shape) — one click to export or "Create in Fiix," with supervisor sign-off required and the safety procedure sourced from the facility's approved energy-control procedure, not invented by the LLM.

And it **works on *your* equipment**: upload your own manual PDF and LlamaParse turns it into the agent's knowledge base — we demo it diagnosing a hydraulic press from an uploaded manual, not just the seeded conveyor. Every run exposes its reasoning trace, so a supervisor sees exactly which tools the agent called and why.

### How we built it
A single FastAPI service serves both the JSON API and a vanilla-JS single-page UI — one process, one Railway deploy. The brain is an Anthropic **Claude `claude-sonnet-4-6`** agentic tool-use loop. We give Claude the active equipment manual in a **prompt-cached** system block (reliable, exact retrieval without the fragility of a vector DB on a 24-hour clock) plus four tools: `lookup_asset_history` (recurring-failure detection), `lookup_part` (MRO catalog: stock, lead time, cost), `get_safety_procedure` (LOTO/PPE by hazard, modeled on OSHA 29 CFR 1910.147), and a **strict** `create_work_order` tool that guarantees the output validates against our Pydantic schema and renders directly. The loop is hard-bounded at 15 steps, every model call is wrapped in retry + exponential backoff, and the API key is read only from the environment. `cmms.py` maps the work order to a Fiix/UpKeep-shaped payload. For "works on your equipment," an upload endpoint sends the operator's PDF to **LlamaParse** (via httpx REST) and swaps it in as the active manual.

### Challenges we ran into
Keeping the demo *believable to an operations manager* meant the diagnosis couldn't be generic. We authored a realistic conveyor manual whose troubleshooting tables map specific symptom patterns (grinding + burning smell → failing drive-pulley bearing; hum-then-trip → mechanical bind) to specific catalog parts, so the agent's reasoning is traceable rather than plausible-sounding. We forced a clean terminal state (always one complete work order) by forcing the `create_work_order` tool on the final step, and tuned the manual length to actually cross Claude's prompt-cache threshold so repeat runs stay fast and cheap.

### Accomplishments that we're proud of
It's genuinely end-to-end and deployable: a real person at a line could use it Monday. Safety is first-class — LOTO steps always precede repair steps, are sourced from the approved procedure, and require supervisor sign-off. The output isn't prose; it's a structured work order a CMMS could ingest. The recurring-failure insight turns "replace the bearing" into "fix the alignment" — the kind of call that saves a plant real money. And it shows its work, which is what earns trust on a floor.

### What we learned
For an industrial agent, the win condition isn't model cleverness — it's whether the output is *safe, specific, and shaped like the artifact the floor already uses*. Strict structured output plus a small set of well-described tools beat an open-ended chatbot on every judging criterion. Prompt-caching the manual was the right call over a vector store for a bounded, single-asset demo.

### What's next
- **Live CMMS write-back** (we export the payload + mock "Create in Fiix" today): real OAuth into Fiix/UpKeep/Maximo and notify the on-call tech.
- **Per-asset parts + history feeds** wired to the customer's CMMS, so a manual upload also brings their real catalog and failure log.
- **Floor-native input**: voice (gloves/noise) and photo of the nameplate or the leak — a natural tie-in to Zapdos's factory-floor video AI.
- **Bilingual EN/ES** — a large share of the US maintenance workforce is Spanish-speaking; accept and answer in the operator's language.
- **OT-network deployment**: runs in the IT DMZ with a floor kiosk, plus an on-prem/edge model option for air-gapped plants (Purdue model / IEC 62443).
- **Feedback loop + fleet view**: technician confirms the actual fix to sharpen per-machine priors; cluster recurring faults to flag the machine that needs a PM, not another work order.

Built by **Pramod Misra** — Director of Data Analytics, Snellings Walters Insurance / founder, 5gVector.

---

## If Devpost asks the judging-criteria questions (paste per field)
- **Does it solve a real operational problem?** Unplanned downtime + unsafe restarts — the most expensive, most time-pressured moment on the floor. The output is the work order plants already run on.
- **Is the AI doing meaningful cognitive work?** It checks asset history, diagnoses from the manual with confidence-ranked causes and cited evidence, weighs an out-of-stock part into a downtime-cost estimate, and selects the right OSHA procedure — across four tools, visible in a reasoning trace.
- **Believable end-to-end workflow?** Plain-language fault → history check → manual diagnosis → parts → safety → costed work order → one-click to the CMMS.
- **Is the value immediately understandable?** A 30-minute triage becomes ~20 seconds, and the screen shows severity, root cause, dollar exposure, and the fix.
- **Would you show it to an ops manager on Monday?** Yes — LOTO-first safety from the approved procedure, supervisor sign-off, real parts availability, CMMS-ready output, a live URL, and it ingests your own equipment manual.

---

## YouTube upload (for the demo video `ShopFloor_Copilot_90s.mp4`)

**Title:** ShopFloor Copilot — AI Maintenance Work-Order Agent (90s demo)

**Description:**
```
A frontline operator describes a machine fault in plain language — and ShopFloor Copilot returns a complete, safety-compliant, costed maintenance work order in about 20 seconds.

It reads the equipment manual, checks the machine's repair history (and flags recurring failures a paper binder never would), confirms spare-parts availability, pulls the matching OSHA lockout/tagout steps, dollarizes the downtime impact, and hands the technician a CMMS-ready work order — one click to Fiix/UpKeep, with supervisor sign-off required.

Built for the Zapdos Labs Industrial AI Hackathon (Operational Intelligence).

▶ Try it live: https://shopfloor-copilot-production.up.railway.app
▶ Code: https://github.com/pramodmisra/shopfloor-copilot

How it works
• Anthropic Claude (claude-sonnet-4-6) agentic tool-use loop — 4 tools, strict structured output
• FastAPI single service, deployed on Railway
• LlamaParse to ingest your own equipment manual (PDF)
• Safety steps sourced from the approved OSHA 29 CFR 1910.147 procedure — not invented by the AI

Chapters
0:00  The problem: unplanned downtime
0:14  What it actually costs
0:26  Meet ShopFloor Copilot
0:38  Live demo — fault → diagnosis → safe work order
1:21  Try it live

#IndustrialAI #Manufacturing #AIagents #PredictiveMaintenance #CMMS #FactoryFloor #OperationalIntelligence
```
Set visibility to **Unlisted** (or Public). Nudge chapter times ±1–2s to match the final upload.

---

## Local asset locations (all in `C:\Users\Pramod Misra\`)
- `ShopFloor_Copilot_90s.mp4` — 90s explainer (problem → impact → solution → demo → CTA, music + subtitles)
- `shopfloor_thumbnail.png` — 1200×800 Devpost thumbnail
- `shopfloor-light-hero.png` · `shopfloor-result.png` — gallery screenshots
