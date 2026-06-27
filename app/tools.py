"""Tool schemas + handlers for the maintenance agent.

Three tools give the agent its cognitive workspace:
  - lookup_part(query)            -> parts catalog (stock, lead time, cost)
  - get_safety_procedure(hazard)  -> LOTO / PPE steps by hazard type
  - create_work_order(...)        -> the validated, structured final deliverable
"""
from __future__ import annotations

import json
from pathlib import Path
from typing import Any

DATA_DIR = Path(__file__).resolve().parent.parent / "data"


def _load(name: str) -> dict[str, Any]:
    with open(DATA_DIR / name, encoding="utf-8") as f:
        return json.load(f)


_PARTS = _load("parts_catalog.json")["parts"]
_SAFETY = _load("safety_procedures.json")["procedures"]


def load_manual() -> str:
    """The full equipment manual — cached in the system prompt."""
    return (DATA_DIR / "manual_conveyor.md").read_text(encoding="utf-8")


def load_sample_faults() -> list[dict[str, str]]:
    return _load("sample_faults.json")["faults"]


# --- Tool handlers ---------------------------------------------------------

def lookup_part(query: str) -> str:
    """Substring match against part number / name / fitted asset."""
    q = (query or "").lower().strip()
    hits = [
        p for p in _PARTS
        if q in p["part_number"].lower()
        or q in p["name"].lower()
        or any(q in a.lower() for a in p["fits_assets"])
    ]
    if not hits:
        return json.dumps({"matches": [], "note": f"No catalog part matched '{query}'."})
    return json.dumps({"matches": hits[:8]})


def get_safety_procedure(hazard: str) -> str:
    """Return the LOTO/PPE procedure for a hazard type (electrical/mechanical/thermal/general)."""
    key = (hazard or "general").lower().strip()
    proc = _SAFETY.get(key) or _SAFETY["general"]
    return json.dumps({"hazard_type": key, "procedure": proc})


# --- Tool schemas (sent to the API) ---------------------------------------

TOOL_SCHEMAS: list[dict[str, Any]] = [
    {
        "name": "lookup_part",
        "description": (
            "Look up MRO spare parts by part number, name keyword, or asset tag. "
            "Returns on-hand quantity, lead time in days, unit cost, and bin location. "
            "Call this to confirm parts availability before recommending them in a work order."
        ),
        "input_schema": {
            "type": "object",
            "properties": {
                "query": {"type": "string", "description": "Part number, keyword (e.g. 'bearing', 'v-belt'), or asset tag."}
            },
            "required": ["query"],
        },
    },
    {
        "name": "get_safety_procedure",
        "description": (
            "Get the OSHA lockout/tagout (LOTO) and PPE procedure for a hazard type. "
            "Call this whenever a repair requires de-energizing or contacting the equipment."
        ),
        "input_schema": {
            "type": "object",
            "properties": {
                "hazard": {
                    "type": "string",
                    "enum": ["electrical", "mechanical", "thermal", "general"],
                    "description": "The dominant hazard for this repair.",
                }
            },
            "required": ["hazard"],
        },
    },
    {
        "name": "create_work_order",
        "description": (
            "Emit the final, complete maintenance work order. Call this exactly once, last, "
            "after you have diagnosed the fault, looked up required parts, and retrieved the "
            "relevant safety procedure. This is the deliverable handed to the technician."
        ),
        "strict": True,
        "input_schema": {
            "type": "object",
            "additionalProperties": False,
            "properties": {
                "asset": {"type": "string"},
                "reported_symptom": {"type": "string"},
                "severity": {"type": "string", "enum": ["emergency", "urgent", "routine"]},
                "probable_causes": {
                    "type": "array",
                    "items": {
                        "type": "object",
                        "additionalProperties": False,
                        "properties": {
                            "cause": {"type": "string"},
                            "confidence": {"type": "string", "enum": ["high", "medium", "low"]},
                            "evidence": {"type": "string"},
                        },
                        "required": ["cause", "confidence", "evidence"],
                    },
                },
                "safety_steps": {"type": "array", "items": {"type": "string"}},
                "repair_steps": {"type": "array", "items": {"type": "string"}},
                "required_parts": {
                    "type": "array",
                    "items": {
                        "type": "object",
                        "additionalProperties": False,
                        "properties": {
                            "part_number": {"type": "string"},
                            "name": {"type": "string"},
                            "availability": {"type": "string"},
                        },
                        "required": ["part_number", "name", "availability"],
                    },
                },
                "estimated_downtime": {"type": "string"},
                "escalate": {"type": "boolean"},
                "escalation_reason": {"type": ["string", "null"]},
            },
            "required": [
                "asset", "reported_symptom", "severity", "probable_causes",
                "safety_steps", "repair_steps", "required_parts",
                "estimated_downtime", "escalate", "escalation_reason",
            ],
        },
    },
]

# Tools the agent may call and loop on (create_work_order is terminal, handled separately).
LOOPING_TOOLS = {"lookup_part": lookup_part, "get_safety_procedure": get_safety_procedure}


def run_looping_tool(name: str, tool_input: dict[str, Any]) -> str:
    """Dispatch a non-terminal tool call. Raises KeyError for unknown tools."""
    handler = LOOPING_TOOLS[name]
    return handler(**tool_input)
