"""The maintenance work-order agent: a bounded, manual-grounded tool-use loop."""
from __future__ import annotations

import os
import random
import time
from typing import Any

import anthropic

from .models import AgentStep, WorkOrder
from .tools import TOOL_SCHEMAS, load_manual, run_looping_tool

MODEL = "claude-sonnet-4-6"  # fast + capable; right tier for a live demo
MAX_STEPS = 15               # hard bound on the agentic loop (per code standards)
MAX_TOKENS = 4096

_SYSTEM_PERSONA = (
    "You are ShopFloor Copilot, a maintenance triage agent for a manufacturing plant. "
    "A frontline operator reports a fault in plain language. Your job: diagnose the probable "
    "root cause USING ONLY the equipment manual below, then build ONE complete work order.\n\n"
    "Use the tools every time:\n"
    "- lookup_asset_history(asset): check FIRST. If the same component/failure code has failed "
    "recently, set recurrence.is_recurring=true and recommend a root-cause fix or PM (e.g. check "
    "alignment, upgrade the bearing) — not just another like-for-like swap. Say so in the note.\n"
    "- lookup_part(query): confirm every part you recommend; report its real availability.\n"
    "- get_safety_procedure(hazard): retrieve LOTO/PPE for the dominant hazard.\n"
    "- create_work_order(...): emit the deliverable LAST, exactly once.\n\n"
    "Rules: ground every probable cause in a specific manual section. LOTO safety steps ALWAYS "
    "precede repair steps. Burning smell / smoke / fire risk = 'emergency'; tripping overload or "
    "hot bearing = 'urgent'. Be decisive and concise.\n\n"
    "Cost: compute cost_impact using LOADED LABOR RATE $95/hr and LINE-3 DOWNTIME COST $3,800/hr. "
    "parts_cost_usd = sum of unit costs from lookup_part. labor_cost_usd = labor_hours x 95. "
    "downtime_cost_usd = downtime_hours x 3800. total_cost_usd = labor + parts + downtime. "
    "Be realistic about hours; if a part is on lead time, downtime_hours reflects the wait.\n\n"
    "=== EQUIPMENT MANUAL ===\n"
)


def _client() -> anthropic.Anthropic:
    """API key comes from the environment only — never hardcoded."""
    if not os.environ.get("ANTHROPIC_API_KEY"):
        raise RuntimeError("ANTHROPIC_API_KEY is not set in the environment.")
    return anthropic.Anthropic(max_retries=4)


def _build_system() -> list[dict[str, Any]]:
    """System prompt with the manual cached (prefix-stable -> cheap repeat calls)."""
    return [{
        "type": "text",
        "text": _SYSTEM_PERSONA + load_manual(),
        "cache_control": {"type": "ephemeral"},
    }]


def _create_with_backoff(client: anthropic.Anthropic, **kwargs: Any) -> anthropic.types.Message:
    """Explicit exponential backoff on top of the SDK's own retries (no silent swallowing)."""
    last_exc: Exception | None = None
    for attempt in range(5):
        try:
            return client.messages.create(**kwargs)
        except (anthropic.RateLimitError, anthropic.APIStatusError) as exc:
            if isinstance(exc, anthropic.APIStatusError) and exc.status_code < 500 \
                    and not isinstance(exc, anthropic.RateLimitError):
                raise  # 4xx (except 429) are not retryable
            last_exc = exc
            time.sleep(min(1.0 * (2 ** attempt) + random.uniform(0, 0.5), 20.0))
    raise last_exc  # type: ignore[misc]


def _work_order_from_tool(block: Any, fallback_asset: str) -> WorkOrder:
    data = dict(block.input)
    data.setdefault("asset", fallback_asset)
    data["work_order_id"] = "WO-" + time.strftime("%Y%m%d-") + str(random.randint(1000, 9999))
    return WorkOrder.model_validate(data)


def run_agent(fault: str, asset: str) -> tuple[WorkOrder, list[AgentStep]]:
    """Run the bounded tool-use loop and return the work order plus an observable trace."""
    client = _client()
    system = _build_system()
    user = f"Asset: {asset}\nOperator fault report: {fault}"
    messages: list[dict[str, Any]] = [{"role": "user", "content": user}]
    trace: list[AgentStep] = [AgentStep(kind="thinking", label="Reading the equipment manual and triaging the report")]

    for _ in range(MAX_STEPS):
        force = _ == MAX_STEPS - 1  # last step: force the deliverable
        resp = _create_with_backoff(
            client, model=MODEL, max_tokens=MAX_TOKENS, system=system,
            tools=TOOL_SCHEMAS, messages=messages,
            tool_choice={"type": "tool", "name": "create_work_order"} if force else {"type": "auto"},
        )
        tool_uses = [b for b in resp.content if b.type == "tool_use"]
        wo_block = next((b for b in tool_uses if b.name == "create_work_order"), None)
        if wo_block is not None:
            trace.append(AgentStep(kind="tool_call", label="create_work_order", detail="Issuing work order"))
            return _work_order_from_tool(wo_block, asset), trace
        if not tool_uses:  # model talked but called nothing — nudge it forward
            messages.append({"role": "assistant", "content": resp.content})
            messages.append({"role": "user", "content": "Continue: gather what you need, then call create_work_order."})
            continue

        messages.append({"role": "assistant", "content": resp.content})
        results = []
        for tu in tool_uses:
            trace.append(AgentStep(kind="tool_call", label=tu.name, detail=tu.input))
            out = run_looping_tool(tu.name, dict(tu.input))
            trace.append(AgentStep(kind="tool_result", label=f"{tu.name} → result", detail=out))
            results.append({"type": "tool_result", "tool_use_id": tu.id, "content": out})
        messages.append({"role": "user", "content": results})

    raise RuntimeError("Agent exhausted its step budget without producing a work order.")
