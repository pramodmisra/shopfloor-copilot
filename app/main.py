"""FastAPI app: serves the ShopFloor Copilot UI and the /api/diagnose endpoint."""
from __future__ import annotations

import time
from pathlib import Path

from dotenv import load_dotenv
from fastapi import FastAPI, HTTPException
from fastapi.responses import FileResponse
from fastapi.staticfiles import StaticFiles

from .agent import MODEL, run_agent
from .models import DiagnoseRequest, DiagnoseResponse
from .tools import load_sample_faults

load_dotenv()

STATIC_DIR = Path(__file__).resolve().parent.parent / "static"
app = FastAPI(title="ShopFloor Copilot", version="1.0.0")


@app.get("/healthz")
def healthz() -> dict[str, str]:
    return {"status": "ok"}


@app.get("/api/samples")
def samples() -> dict[str, list]:
    return {"faults": load_sample_faults()}


@app.post("/api/diagnose", response_model=DiagnoseResponse)
def diagnose(req: DiagnoseRequest) -> DiagnoseResponse:
    started = time.monotonic()
    try:
        work_order, trace = run_agent(req.fault, req.asset)
    except RuntimeError as exc:
        raise HTTPException(status_code=502, detail=str(exc)) from exc
    return DiagnoseResponse(
        work_order=work_order,
        trace=trace,
        model=MODEL,
        elapsed_seconds=round(time.monotonic() - started, 1),
    )


@app.get("/")
def index() -> FileResponse:
    return FileResponse(STATIC_DIR / "index.html")


# Serve any other static assets (kept last so it doesn't shadow API routes).
app.mount("/static", StaticFiles(directory=STATIC_DIR), name="static")
