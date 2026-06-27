"""FastAPI app: serves the ShopFloor Copilot UI and the /api/diagnose endpoint."""
from __future__ import annotations

import time
from pathlib import Path

from dotenv import load_dotenv
from fastapi import FastAPI, File, HTTPException, UploadFile
from fastapi.responses import FileResponse
from fastapi.staticfiles import StaticFiles

from .agent import MODEL, run_agent
from .cmms import to_cmms_payload
from .llamaparse import ManualParseError, parse_pdf_to_markdown
from .models import DiagnoseRequest, DiagnoseResponse
from .tools import load_sample_faults, manual_source, set_manual_override

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
        cmms_payload=to_cmms_payload(work_order),
        trace=trace,
        model=MODEL,
        manual_source=manual_source(),
        elapsed_seconds=round(time.monotonic() - started, 1),
    )


@app.post("/api/upload_manual")
async def upload_manual(file: UploadFile = File(...)) -> dict[str, object]:
    """Parse an uploaded equipment-manual PDF (via LlamaParse) and make it the active manual."""
    raw = await file.read()
    if len(raw) > 20_000_000:
        raise HTTPException(status_code=413, detail="Manual exceeds 20 MB.")
    try:
        markdown = parse_pdf_to_markdown(raw, file.filename or "manual.pdf")
    except ManualParseError as exc:
        raise HTTPException(status_code=502, detail=str(exc)) from exc
    set_manual_override(markdown, f"Uploaded: {file.filename}")
    return {"ok": True, "manual_source": manual_source(), "chars": len(markdown)}


@app.get("/")
def index() -> FileResponse:
    return FileResponse(STATIC_DIR / "index.html")


# Serve any other static assets (kept last so it doesn't shadow API routes).
app.mount("/static", StaticFiles(directory=STATIC_DIR), name="static")
