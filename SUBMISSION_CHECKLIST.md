# Devpost Submission Checklist — $1,000 Industrial AI Hackathon

**Hackathon:** https://1-000-industrial-ai-hackathon.devpost.com/ · **Deadline:** Jun 27, 2026 @ 8:00pm EDT

## Devpost project fields
- [ ] **Project name:** ShopFloor Copilot
- [ ] **Tagline:** The maintenance work-order agent — operator types the fault; it reads the manual, diagnoses, checks parts & safety, writes the work order in 20s.
- [ ] **Description:** paste from `DEVPOST.md` (Inspiration → What it does → How we built it → Challenges → Accomplishments → What we learned → What's next).
- [ ] **Built with:** Python, FastAPI, Anthropic Claude (claude-sonnet-4-6), Pydantic, JavaScript, Railway.
- [x] **Try it / live demo URL:** https://shopfloor-copilot-production.up.railway.app
- [x] **Public code repo URL:** https://github.com/pramodmisra/shopfloor-copilot
- [ ] **Demo video:** record from `DEMO_SCRIPT.md` (~2 min), upload to YouTube (unlisted is fine), paste link.
- [ ] **Screenshots:** (1) work-order card for the burning-smell fault; (2) expanded agent-reasoning trace; (3) the input screen with demo chips.
- [ ] **Theme/category:** AI agents that solve a real operational problem (Operational Intelligence).

## Pre-submit verification
- [ ] `pytest` green (6 offline + 1 live).
- [ ] Live Railway URL loads, demo chips populate, a diagnosis returns a full work order.
- [ ] `ANTHROPIC_API_KEY` set in Railway env (NOT in the repo). `.env` is gitignored.
- [ ] README live-URL placeholder filled in.

## Judging-criteria self-check (judges = real ops managers)
- [ ] **Real problem** — unplanned downtime + unsafe restart, the costliest floor moment.
- [ ] **Cognitive work** — manual-grounded diagnosis + 3-tool reasoning + confidence weighting.
- [ ] **End-to-end** — fault → diagnosis → parts → safety → issued work order.
- [ ] **Clear value** — 30-min triage → 20s; legible in one screen.
- [ ] **Deployable Monday** — LOTO-first, real parts availability, live URL.

## Notes
- Remote/online submission is eligible (hybrid event). In-person final demos are in Austin at 5:30pm CST — on-site teams have a live-demo edge, but the Devpost entry stands on its own.
