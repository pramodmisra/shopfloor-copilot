# 2-Minute Demo Video Script — ShopFloor Copilot

> Record screen + voiceover. Have the app open at the live URL with the input box empty. Total ~2:00.

### [0:00–0:15] Hook — the problem
> "On a plant floor, the most expensive minutes are right after a machine starts acting up. The operator who notices it usually can't fix it — so they flag down a busy tech or thumb through a binder while the line backs up. And under that pressure, someone restarts a faulting machine or skips lockout/tagout."

*(On screen: the empty ShopFloor Copilot UI.)*

### [0:15–0:30] The ask
> "ShopFloor Copilot is an AI agent that reads the equipment manual and turns a plain-language fault report into a complete, safe work order — in about 20 seconds."

*(Click the first demo chip: "Line 3 conveyor grinding at the drive end… burning smell." Click **Diagnose**.)*

### [0:30–1:30] Live demo — the core workflow
While it runs (button shows "Agent working… reading manual, checking parts & safety"):
> "Watch what it's doing. It's reading the conveyor manual, diagnosing the cause, then calling tools — one to check spare-parts stock, one to pull the OSHA lockout/tagout procedure."

*(Work-order card renders.)*
> "Here's the work order. Severity: **emergency** — because it caught the burning smell. Probable root cause: a failing drive-pulley bearing — and notice it cites the exact manual section as evidence. Confidence: high."

*(Scroll to safety + parts.)*
> "Safety steps come first — full lockout/tagout, verify zero energy, treat the burning smell as urgent. Then the repair steps. Then the parts it actually needs — bearing 6206, in stock; and it flagged the one part that's on a 3-day lead. This is a job ticket a tech can act on right now."

*(Expand "Show agent reasoning".)*
> "And it shows its work — every tool call the agent made. That's what earns trust on a floor."

### [1:30–1:50] Architecture — one slide
> "Under the hood: a FastAPI service and a Claude agentic loop. The full manual is prompt-cached; three tools — parts, safety, and a strict work-order writer that guarantees structured output. One service, deployed live on Railway."

*(Show ARCHITECTURE.md data-flow diagram, or the architecture slide.)*

### [1:50–2:00] Close + what's next
> "Point it at your real manual and CMMS, write the order back to your maintenance system, add voice input at the line — and you've turned a 30-minute triage into 20 seconds. ShopFloor Copilot. Thanks."

---

**Recording tips:** run one warm-up diagnosis first so the prompt cache is hot and the demo run is fast. Keep the burning-smell fault as the hero (clear emergency severity reads well). If you have time, run a second chip (the "hum then overload trips" one) to show a different diagnosis.
