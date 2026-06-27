# ConvTech CT-2000 Series Belt Conveyor — Operation & Maintenance Manual (Excerpt)

**Asset family:** CT-2000 horizontal/incline belt conveyor
**Demo asset tag:** CONV-L3 (Line 3 packaging conveyor)
**Drive:** 2 HP 56C gearmotor (MTR-2HP-56C) via L095 jaw coupling (CPL-JAW-L095), controlled by a 3 HP 240V VFD (VFD-3HP-240) with a class-10 thermal overload relay (OVL-RLY-9A).

> SAFETY: All maintenance must follow the facility energy-control (lockout/tagout) procedure per OSHA 29 CFR 1910.147 before any guard is removed or any contact is made with the belt, drive, or electrical enclosure. Rotating drives and pinch points at the head/tail pulleys can cause severe entanglement injuries.

---

## 1. Major Components

| Component | Part number | Notes |
|---|---|---|
| Main drive belt (V-belt) | BLT-V-A42 | Motor sheave to drive pulley; check tension monthly |
| Drive pulley bearing | BRG-6206-2RS | Sealed; lubricated for life but inspect for heat/noise |
| Idler / head pulley bearing | BRG-6204-2RS | Sealed ball bearing |
| Gearmotor | MTR-2HP-56C | 230/460V; thermal protected |
| Thermal overload relay | OVL-RLY-9A | Class 10, set to motor FLA (7–10A band) |
| Variable frequency drive | VFD-3HP-240 | Has internal DC bus — discharge before service |
| Idler roller | ROL-IDL-48 | Supports belt; flat spots cause vibration |
| Belt cleaner / scraper | BLT-CLN-48 | Keeps carryback off return belt |
| Jaw coupling | CPL-JAW-L095 | Spider insert wears; causes startup clunk/squeal |
| Take-up assembly | — | Screw take-up at tail; sets belt tension and tracking |
| Proximity sensor | PXS-IND-18 | Speed/zero-speed feedback to VFD |
| E-stop pushbutton | EST-BTN-22 | Pull-to-reset; cuts control power |

---

## 2. Routine Maintenance Schedule

| Interval | Task |
|---|---|
| Daily | Walk the line; listen for grinding/squeal; check belt tracking and carryback. |
| Weekly | Inspect belt edges for fraying; verify scraper contact; check for material buildup at pulleys. |
| Monthly | Check V-belt tension and condition; grease per-asset points with EP2 (LUB-EP2-14); inspect coupling spider. |
| Quarterly | Verify motor amp draw against FLA; inspect bearings for heat with IR thermometer; check shaft alignment with shim kit (SHIM-SS-KIT). |

---

## 3. Troubleshooting Guide

### 3.1 Grinding / rumbling noise + burning smell at drive end
**Likely causes (most to least common):**
1. **Failing drive-pulley bearing (BRG-6206-2RS).** A dry or spalled bearing grinds and overheats; the burning smell is scorched grease or overheated steel. This is the highest-probability cause when noise localizes to the drive end *and* a burning smell is present.
2. Motor overheating from sustained overload (check amp draw vs. FLA; relay OVL-RLY-9A may be near trip).
3. Misaligned or worn jaw coupling (CPL-JAW-L095) chewing its spider insert.

**Action:** STOP the conveyor and hit the E-stop now. Lock out (mechanical + electrical), let components cool, verify with IR thermometer. If the drive-pulley bearing is hot/rough, replace BRG-6206-2RS. Inspect the coupling spider while open. Verify motor amp draw on restart. **A burning smell or smoke means a hot bearing can seize and ignite — this is an emergency: stop and lock out immediately, do not keep running the line.**

### 3.2 Belt mistracking / drifting to one side, rubbing frame
**Likely causes:**
1. Take-up out of square (belt tension uneven side-to-side) — most common after a tension adjustment or heavy load.
2. Material buildup on a pulley or idler crowning the belt to one side.
3. Worn or flat-spotted idler roller (ROL-IDL-48).

**Action:** Lock out. Clean pulleys/idlers. Adjust the screw take-up 1/4 turn at a time toward the side the belt drifts *away from*, run briefly, re-check. Replace ROL-IDL-48 if flat-spotted. Mistracking is rarely an emergency but causes belt edge damage if left — schedule promptly.

### 3.3 Motor hums then thermal overload trips on start
**Likely causes:**
1. **Mechanical bind / jam** — seized bearing, jammed product, or frozen pulley drawing locked-rotor current. The hum-then-trip pattern is classic for a motor that cannot turn its load.
2. Single-phasing (a blown fuse FUS-CC-10 or loose lead) — motor hums but cannot start.
3. Overload relay (OVL-RLY-9A) set too low or failed.
4. Failed start capacitor / VFD fault (check VFD-3HP-240 fault code).

**Action:** Lock out. Manually rotate the drive by hand to feel for a bind; clear any jam. Check fuses (FUS-CC-10) and tighten leads. Verify the overload is set to motor FLA. Do NOT repeatedly reset and re-energize a humming motor — locked-rotor current overheats the windings within seconds.

### 3.4 Belt slipping / squealing on startup, product slipping on incline
**Likely causes:**
1. **Loose or glazed main drive V-belt (BLT-V-A42)** — the squeal on startup is the V-belt slipping in the sheave; under-tension also lets the belt slip under incline load.
2. Worn coupling spider (CPL-JAW-L095) causing a lash/clunk then squeal.
3. Belt under-tensioned at the take-up, or worn/glazed conveyor belt surface losing grip on the incline.

**Action:** Lock out. Inspect and re-tension or replace the V-belt (BLT-V-A42). Check the coupling spider. Verify take-up tension. Glazed belt surface or worn lagging may need belt replacement (lacing kit TKN-LACE-A1).

### 3.5 Carryback / spillage on return side
Worn or mis-set belt scraper (BLT-CLN-48). Re-tension or replace the scraper blade. Not safety-critical but a slip/housekeeping hazard.

---

## 4. Electrical Notes
- Main disconnect is at the motor control panel. The VFD (VFD-3HP-240) retains a charged DC bus for several minutes after power-off — **always verify 0V at the bus terminals before contact.**
- Overload relay OVL-RLY-9A trip indicates a real condition — never bypass. Investigate the mechanical or electrical root cause.
- Control fuses are Class CC time-delay (FUS-CC-10). A repeatedly blowing fuse indicates a short or overload, not a fuse problem.

### 3.6 VFD fault / will not run from HMI
**Likely causes:** overcurrent (OC) fault from a mechanical bind; overvoltage (OV) on rapid deceleration; lost speed feedback from the proximity sensor (PXS-IND-18); blown control fuse (FUS-CC-10).
**Action:** Read the VFD (VFD-3HP-240) fault code at the keypad before clearing. OC almost always traces to the same mechanical bind described in 3.3 — clear the bind, do not just clear the fault. Verify the proximity sensor gap (1–3 mm) and PNP wiring. Replace FUS-CC-10 only after confirming no downstream short.

### 3.7 Intermittent stops / E-stop nuisance trips
**Likely causes:** loose E-stop wiring at EST-BTN-22; a sticking pushbutton; vibration-loosened control terminals.
**Action:** Lock out control power. Inspect and re-seat the E-stop contact block; replace EST-BTN-22 if the contact is intermittent. Torque control terminals to spec.

---

## 4. Specifications (CONV-L3)

| Parameter | Value |
|---|---|
| Belt width | 48 in |
| Belt speed | 65 ft/min nominal (VFD-adjustable 30–90 ft/min) |
| Incline | 12° at labeler transition |
| Motor | 2 HP, 1750 rpm, 56C frame, 230/460 V, FLA 7.0/3.5 A |
| Overload setting | Class 10, dial to motor FLA (7.0 A on 230 V) |
| V-belt | A-section, 42 in pitch length (BLT-V-A42), deflection 1/64 in per in of span |
| Drive pulley bearing | 6206-2RS, grease EP2, replace if radial play > 0.005 in |
| Idler bearing | 6204-2RS |
| Coupling | L095 jaw, spider replace at > 1/8 in backlash |
| Take-up | screw type, 4 in travel, set belt sag 2% of span |

---

## 5. Belt Tracking & Tension Procedure
1. Lock out the drive (mechanical procedure) before touching the belt.
2. Confirm the conveyor frame is square and level; most tracking faults are a frame or take-up squareness issue, not the belt.
3. With the drive still locked out, clean all pulleys and idlers of buildup.
4. Restore power and jog briefly. Observe which side the belt drifts toward.
5. Lock out again. Adjust the take-up on the side the belt drifts **toward** by 1/4 turn (tightening that side steers the belt away from it).
6. Repeat jog-and-adjust in 1/4-turn steps. Never adjust more than 1/4 turn between runs.
7. Final belt sag should be ~2% of the span between idlers. Over-tension accelerates bearing wear; under-tension causes slip (see 3.4).

## 6. Motor Alignment Procedure
1. Lock out (electrical + mechanical) and verify zero energy.
2. Check coupling backlash; replace the L095 spider (CPL-JAW-L095) if > 1/8 in.
3. Use a straightedge across the coupling hubs for rough angular alignment.
4. Shim the motor feet with the stainless shim kit (SHIM-SS-KIT) to correct soft foot and parallel offset.
5. Re-torque the motor hold-down bolts in a cross pattern, then re-check alignment.
6. Hand-rotate the drive one full revolution to confirm no bind before restoring power.

## 7. Lubrication
- Drive and idler bearings are sealed-for-life but should be monitored; do not over-grease.
- Apply EP2 (LUB-EP2-14) only at designated zerk fittings on the take-up bearings, monthly, one to two pumps.
- Wipe excess grease — accumulated grease is a fire load near a hot bearing.

## 8. When to Escalate
Escalate to maintenance supervisor / OEM if: motor megger (insulation resistance) test fails, the VFD throws a hardware fault that will not clear after the mechanical cause is removed, structural frame damage is found, the repair requires confined-space entry or work-at-height beyond the technician's authorization, or a bearing/motor replacement exceeds the on-shift parts and skill available.
