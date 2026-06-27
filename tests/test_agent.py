"""Smoke tests — run with `pytest`. The live-agent test skips without ANTHROPIC_API_KEY."""
from __future__ import annotations

import json
import os

import pytest

from app.models import WorkOrder
from app.tools import (
    TOOL_SCHEMAS,
    get_safety_procedure,
    load_manual,
    load_sample_faults,
    lookup_part,
)


def test_tool_schemas_well_formed() -> None:
    names = {t["name"] for t in TOOL_SCHEMAS}
    assert {"lookup_part", "get_safety_procedure", "create_work_order"} <= names
    for tool in TOOL_SCHEMAS:
        assert tool["input_schema"]["type"] == "object"
        assert "required" in tool["input_schema"]
    wo = next(t for t in TOOL_SCHEMAS if t["name"] == "create_work_order")
    assert wo["strict"] is True
    assert wo["input_schema"]["additionalProperties"] is False


def test_lookup_part_finds_bearing() -> None:
    out = json.loads(lookup_part("bearing"))
    assert out["matches"], "expected at least one bearing match"
    assert any(m["part_number"].startswith("BRG-") for m in out["matches"])


def test_lookup_part_miss_is_graceful() -> None:
    out = json.loads(lookup_part("nonexistent-zzz"))
    assert out["matches"] == []


def test_safety_procedure_has_loto_steps() -> None:
    out = json.loads(get_safety_procedure("electrical"))
    assert out["hazard_type"] == "electrical"
    assert len(out["procedure"]["loto_steps"]) >= 5


def test_manual_is_cacheable_size() -> None:
    # Sonnet 4.6 caches at >=2048 tokens; ~4 chars/token heuristic -> need >~8KB.
    assert len(load_manual()) > 8000


def test_sample_faults_present() -> None:
    faults = load_sample_faults()
    assert len(faults) >= 3
    assert all("text" in f for f in faults)


@pytest.mark.skipif(not os.environ.get("ANTHROPIC_API_KEY"), reason="no API key")
def test_live_agent_produces_work_order() -> None:
    from app.agent import run_agent

    wo, trace = run_agent(
        "Line 3 conveyor grinding at the drive end with a burning smell.", "CONV-L3"
    )
    assert isinstance(wo, WorkOrder)
    assert wo.severity in ("emergency", "urgent")  # burning smell -> high severity
    assert wo.safety_steps, "work order must carry safety steps"
    assert wo.probable_causes
    assert wo.cost_impact.total_cost_usd > 0  # dollarized impact computed
    assert wo.recurrence.is_recurring  # CONV-L3 has prior bearing failures in history
    assert any(s.kind == "tool_call" for s in trace)
