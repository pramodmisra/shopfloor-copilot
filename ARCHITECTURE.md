# Architecture — ShopFloor Copilot

## System components
- **FastAPI app** (`app/main.py`) — serves the single-page UI at `/`, the agent at `POST /api/diagnose`, demo faults at `GET /api/samples`, and `GET /healthz`. One service, so one Railway deploy.
- **Agent loop** (`app/agent.py`) — a manual, bounded Claude tool-use loop. Manual is prompt-cached in the system block; every call wrapped in retry + exponential backoff.
- **Tools** (`app/tools.py`) — schemas + handlers for `lookup_part`, `get_safety_procedure`, and the strict terminal `create_work_order`.
- **Models** (`app/models.py`) — Pydantic contracts (`DiagnoseRequest`, `WorkOrder`, `AgentStep`, `DiagnoseResponse`); fully type-hinted.
- **Seed data** (`data/`) — equipment manual (Markdown), parts catalog, safety procedures, demo faults (JSON). The seam where a real plant plugs in its own manual/CMMS.
- **UI** (`static/index.html`) — vanilla HTML/CSS/JS, no build step. Renders the work-order card + collapsible agent-reasoning trace.

## Data flow
```
Operator fault text
   │  POST /api/diagnose  {fault, asset}
   ▼
run_agent()  ── system = persona + FULL manual (cache_control: ephemeral)
   │
   ├─ loop (≤ MAX_STEPS=15):
   │     Claude → tool_use?
   │        ├─ lookup_part(query)         → parts catalog JSON  ──┐
   │        ├─ get_safety_procedure(hzd)  → LOTO/PPE JSON       ──┤ results fed back
   │        └─ create_work_order(...)  [strict] → TERMINAL  ──────┘
   │     (final step forces create_work_order if not yet emitted)
   ▼
WorkOrder (Pydantic-validated) + AgentStep[] trace
   │  DiagnoseResponse  {work_order, trace, model, elapsed_seconds}
   ▼
UI renders work-order card + reasoning trace
```

## Key technical decisions
- **Prompt-cache the manual, not a vector DB.** On a 24-hour clock, embeddings + a vector store add fragility for no accuracy gain on a single small manual. Caching the manual in the system prefix gives exact, reliable retrieval; the manual is sized above Claude's cache threshold so repeat runs are fast and cheap. The tools supply the agentic cognitive work judges want.
- **Strict `create_work_order` tool as the terminal action.** `strict: true` + `additionalProperties: false` guarantees the final output validates against the `WorkOrder` schema — no JSON parsing roulette, the card always renders.
- **Hard-bounded loop (15 steps) + forced finish.** No runaway agent; if the budget nears exhaustion the last call forces the work-order tool, so the endpoint always returns a complete deliverable or a clean 502.
- **Safety is structural, not prompted-and-hoped.** A dedicated safety tool returns OSHA-modeled LOTO steps by hazard; the persona requires safety steps before repair steps and maps burning smell/smoke → `emergency` severity.
- **Single service, env-only secrets, pinned deps.** Deploy simplicity + the project's code standards: functions ≤60 lines, type hints throughout, retry/backoff on all LLM calls, `ANTHROPIC_API_KEY` from the environment only.

## Model
`claude-sonnet-4-6` — the speed/intelligence balance that suits a live, judged demo with possibly repeated runs. Swappable via `MODEL` in `app/agent.py`.
