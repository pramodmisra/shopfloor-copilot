# 🛠️ ShopFloor Copilot — Maintenance Work-Order Agent

> Built for the Zapdos Labs **$1,000 Industrial AI Hackathon** (Operational Intelligence). Turns a frontline operator's plain-language fault report into a complete, safety-compliant maintenance work order in ~20 seconds.

**Live demo:** _<add Railway URL>_ · **Theme:** AI agents that solve a real operational problem for the American Industrial Revolution.

## The problem
When a machine acts up, the operator's options are: flag down a busy maintenance tech, or flip through a binder. Diagnosis and work-order paperwork eat 20–40 minutes per event, and the highest-cost mistake — restarting a faulting machine, or skipping lockout/tagout — happens under exactly that time pressure. Unplanned downtime runs ~$260K/hour in some plants.

## What it does
An operator types what they see — *"Line 3 conveyor grinding at the drive end, smells like burning."* ShopFloor Copilot:
1. **Reads the equipment manual** and diagnoses the probable root cause(s) with confidence + the manual section that supports each.
2. **Looks up the required spare parts** and reports real stock / lead time from the MRO catalog.
3. **Pulls the matching OSHA lockout/tagout (LOTO) procedure** so the safety steps come first.
4. **Emits a structured work order**: severity, ordered repair steps, parts, safety steps, downtime estimate, and an escalation flag.

Every run shows its work — the collapsible agent-reasoning trace exposes each tool call.

## Tech stack
FastAPI · Anthropic Claude (`claude-sonnet-4-6`) agentic tool-use loop · Pydantic · vanilla JS single-page UI. One service, deployable on Railway.

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
