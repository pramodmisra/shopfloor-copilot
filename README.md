# 🛠️ ShopFloor Copilot — Maintenance Work-Order Agent

> Built for the Zapdos Labs **$1,000 Industrial AI Hackathon** (Operational Intelligence). Turns a frontline operator's plain-language fault report into a complete, safety-compliant maintenance work order in ~20 seconds.

**Live demo:** https://shopfloor-copilot-production.up.railway.app · **Repo:** https://github.com/pramodmisra/shopfloor-copilot · **Theme:** AI agents that solve a real operational problem for the American Industrial Revolution.

## The problem
When a machine acts up, the operator's options are: flag down a busy maintenance tech, or flip through a binder. Diagnosis and work-order paperwork eat 20–40 minutes per event, and the highest-cost mistake — restarting a faulting machine, or skipping lockout/tagout — happens under exactly that time pressure. Unplanned downtime runs ~$260K/hour in some plants.

## What it does
An operator types what they see — *"Line 3 conveyor grinding at the drive end, smells like burning."* ShopFloor Copilot:
1. **Checks asset history** and flags **recurring failures** ("bearing 3× in 8 weeks → fix the root cause, not another swap").
2. **Reads the equipment manual** and diagnoses probable root cause(s) with confidence + the manual section that supports each.
3. **Looks up spare parts** — real stock / lead time from the MRO catalog.
4. **Pulls the matching OSHA lockout/tagout (LOTO) procedure** so safety steps come first (sourced from the facility procedure, not invented).
5. **Dollarizes the impact** — labor + parts + downtime cost (the burning-smell case = ~$274K exposure).
6. **Emits a structured work order + CMMS-ready payload** (Fiix/UpKeep shape) — one-click export / "Create in Fiix," supervisor sign-off required.

**Works on your equipment:** upload your own manual PDF → **LlamaParse** makes it the agent's knowledge base (demo includes diagnosing a hydraulic press from an uploaded manual). Every run shows its work — a collapsible reasoning trace of each tool call.

## Tech stack
FastAPI · Anthropic Claude (`claude-sonnet-4-6`) agentic tool-use loop (4 tools, strict structured output) · **LlamaParse** (manual ingestion) · Pydantic · vanilla JS single-page UI. One service, deployable on Railway.

## Quick start
```bash
pip install -r requirements.txt
cp .env.example .env            # add your ANTHROPIC_API_KEY
uvicorn app.main:app --reload   # open http://localhost:8000
```

```bash
pytest                          # 6 offline tests + 1 live test (needs the key)
curl -X POST localhost:8000/api/diagnose \
  -H 'content-type: application/json' \
  -d '{"fault":"Line 3 conveyor grinding at the drive end, burning smell"}'
```

## How it's built
See [ARCHITECTURE.md](ARCHITECTURE.md). The agent runs a **bounded** tool-use loop (max 15 steps), caches the full equipment manual in the prompt, and wraps every model call in retry + exponential backoff. The final work order is produced via a **strict** `create_work_order` tool, so the output is schema-guaranteed and renders directly.

## Why it wins the criteria
| Judging criterion | How ShopFloor Copilot answers it |
|---|---|
| Real operational problem | Unplanned downtime + unsafe restarts — the costliest, most time-pressured moment on the floor |
| Meaningful cognitive work | Diagnoses from a manual, reasons across 3 tools, weighs causes by confidence |
| Believable end-to-end | Fault report → diagnosis → parts → safety → issued work order, in one flow |
| Clear value | A 30-minute triage becomes 20 seconds; value legible in one screen |
| Deployable Monday | LOTO-first safety, real parts availability, live URL — usable by a tech today |

— Pramod Misra · Snellings Walters Insurance / 5gVector
