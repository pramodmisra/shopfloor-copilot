"""Parse an uploaded equipment-manual PDF into Markdown via the LlamaParse REST API.

Uses httpx directly (no heavy SDK) so the agent can diagnose against the operator's
OWN equipment manual, not just the seeded one. Key: LLAMA_CLOUD_API_KEY (env).
"""
from __future__ import annotations

import os
import time

import httpx

_BASE = "https://api.cloud.llamaindex.ai/api/v1/parsing"
_MAX_POLLS = 30      # explicit bound on the polling loop
_POLL_SECONDS = 3.0


class ManualParseError(RuntimeError):
    """Raised when LlamaParse cannot produce markdown for the upload."""


def _key() -> str:
    key = os.environ.get("LLAMA_CLOUD_API_KEY")
    if not key:
        raise ManualParseError("LLAMA_CLOUD_API_KEY is not set in the environment.")
    return key


def parse_pdf_to_markdown(file_bytes: bytes, filename: str) -> str:
    """Upload a document to LlamaParse, poll to completion, return Markdown."""
    headers = {"Authorization": f"Bearer {_key()}", "accept": "application/json"}
    with httpx.Client(timeout=60.0) as client:
        up = client.post(
            f"{_BASE}/upload", headers=headers,
            files={"file": (filename, file_bytes, "application/pdf")},
            data={"result_type": "markdown"},
        )
        up.raise_for_status()
        job_id = up.json()["id"]

        for _ in range(_MAX_POLLS):
            status = client.get(f"{_BASE}/job/{job_id}", headers=headers).json().get("status")
            if status in ("SUCCESS", "COMPLETED"):
                break
            if status in ("ERROR", "FAILED", "CANCELLED"):
                raise ManualParseError(f"LlamaParse job ended with status {status}.")
            time.sleep(_POLL_SECONDS)
        else:
            raise ManualParseError("LlamaParse timed out before the document finished parsing.")

        res = client.get(f"{_BASE}/job/{job_id}/result/markdown", headers=headers)
        res.raise_for_status()
        markdown = res.json().get("markdown", "").strip()

    if len(markdown) < 200:
        raise ManualParseError("Parsed manual was too short to be usable.")
    return markdown
