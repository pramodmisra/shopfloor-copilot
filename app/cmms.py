"""Map a WorkOrder to a CMMS-ready payload (Fiix / UpKeep / Maximo field shape).

This is the 'lands in your system of record, not a dead-end screen' piece — the
payload mirrors the fields a corrective work order carries in a real CMMS so an
integration can POST it directly.
"""
from __future__ import annotations

from typing import Any

from .models import WorkOrder

# CMMS priority codes mapped from our severity (Fiix-style P1/P2/P3).
_PRIORITY = {"emergency": "P1 - Emergency", "urgent": "P2 - High", "routine": "P3 - Scheduled"}


def to_cmms_payload(wo: WorkOrder) -> dict[str, Any]:
    """Return a generic corrective-WO payload an integration could POST to a CMMS."""
    return {
        "workOrderNumber": wo.work_order_id,
        "type": "Corrective",
        "assetCode": wo.asset,
        "priority": _PRIORITY.get(wo.severity, "P3 - Scheduled"),
        "description": wo.reported_symptom,
        "failureDiagnosis": [
            {"cause": c.cause, "confidence": c.confidence} for c in wo.probable_causes
        ],
        "estimatedLaborHours": wo.cost_impact.labor_hours,
        "estimatedTotalCostUsd": wo.cost_impact.total_cost_usd,
        "estimatedDowntimeHours": wo.cost_impact.downtime_hours,
        "safetyProcedure": wo.safety_steps,
        "tasks": [{"sequence": i + 1, "task": s} for i, s in enumerate(wo.repair_steps)],
        "partsRequired": [
            {"partNumber": p.part_number, "description": p.name, "availability": p.availability}
            for p in wo.required_parts
        ],
        "recurringFailure": wo.recurrence.is_recurring,
        "requiresSupervisorSignOff": wo.requires_supervisor_signoff,
        "createdBy": "ShopFloor Copilot",
        "status": "Awaiting sign-off",
    }
