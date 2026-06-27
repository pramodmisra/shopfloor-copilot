"""Pydantic models for ShopFloor Copilot — typed request/response contracts."""
from __future__ import annotations

from typing import Any, Literal

from pydantic import BaseModel, Field


class DiagnoseRequest(BaseModel):
    """Inbound fault report from the shop floor."""

    fault: str = Field(..., min_length=3, max_length=2000)
    asset: str = Field(default="CONV-L3", max_length=64)


class RequiredPart(BaseModel):
    part_number: str
    name: str
    availability: str  # human-readable: "in stock (4)" or "order — 3 day lead"


class ProbableCause(BaseModel):
    cause: str
    confidence: Literal["high", "medium", "low"]
    evidence: str  # what in the manual/report points here


class WorkOrder(BaseModel):
    """Structured maintenance work order — the agent's final deliverable."""

    work_order_id: str
    asset: str
    reported_symptom: str
    severity: Literal["emergency", "urgent", "routine"]
    probable_causes: list[ProbableCause]
    safety_steps: list[str]
    repair_steps: list[str]
    required_parts: list[RequiredPart]
    estimated_downtime: str
    escalate: bool
    escalation_reason: str | None = None


class AgentStep(BaseModel):
    """One observable step of the agent's reasoning loop (for the trace panel)."""

    kind: Literal["thinking", "tool_call", "tool_result"]
    label: str
    detail: Any = None


class DiagnoseResponse(BaseModel):
    work_order: WorkOrder
    trace: list[AgentStep]
    model: str
    elapsed_seconds: float
