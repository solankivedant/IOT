# PROJECT REPORT
## Cold-Chain Integrity & Last-Mile Reefer Monitoring System
### An IoT Working Prototype for Industry 5.0 — Raspberry Pi 4 Build

**Course:** ECE-504 — Internet of Things
**Semester:** Monsoon Semester, 2026
**Group No.:** 4 — Sky is the Limit
**Document:** Project Report (Build, Enhancement and Test Record)
**Revision:** R2 — aligned to the components actually issued from stores

---

## Abstract

Refrigerated transport is the weakest link in India's food and pharmaceutical supply chains. Cargo loses its protective cold environment silently, and the loss is discovered only at delivery, when it is already unrecoverable. This report documents the design, build plan, and enhancement set for an IoT-based Cold-Chain Integrity and Last-Mile Reefer Monitoring System built around a Raspberry Pi 4 Model B.

The system continuously senses cargo temperature at two independent points and monitors door status, applies three lightweight and fully explainable rules — a threshold check, a rate-of-change check, and a new inter-probe differential check — and responds immediately through local actuation (buzzer, warning light, and an automatic compressor-restart relay), a new on-unit OLED display for the driver, remote SMS alerting with GPS location, and cloud logging. Every reading is time-stamped from an independent GPS clock and cryptographically linked to the reading before it, so the record cannot be silently altered and a trip can end with a verifiable digital cold-chain certificate.

This revision differs from the earlier Detailed Project Report (DPR) in one important way: it is written against the components actually issued for the build, not the components originally specified. Two of those changes — a second temperature probe and a 0.96-inch I2C OLED display — are not cost overheads to be absorbed quietly. They are treated here as the basis of a deliberate feature upgrade, described in full in Section 7.

---

## Contents

1. Introduction
2. Problem Statement
3. Existing Systems and Their Limitations
4. Objectives
5. Component List as Issued, and How It Differs from the DPR
6. System Architecture
7. Enhancements — What We Are Adding to the Project
8. Working Principle — Software Logic
9. Data Model and the Tamper-Evident Chain
10. Pin Connection Reference and I2C Address Map
11. Power Budget and the USB-C Supply Design Note
12. Build Sequence
13. Testing Methodology
14. Results and Output Display
15. Cost Analysis
16. Team Roles and Work Split
17. Project Timeline
18. Risks and Mitigations
19. Advantages
20. Limitations of the Prototype
21. Future Scope
22. Conclusion
23. References
24. Appendix A — OLED Screen Layouts
25. Appendix B — Sample Log Record and Certificate

---

## 1. Introduction

### 1.1 What This Project Is

This project is an embedded IoT system that continuously monitors the internal condition of a refrigerated ("reefer") transport vehicle or cold storage unit, and takes both local and remote action the moment that condition drifts outside safe limits. It combines a Raspberry Pi 4 Model B, two waterproof temperature probes, a magnetic door sensor, a combined 4G/GPS HAT, a UPS/battery backup, an on-unit OLED display, and a cloud service into a single working unit that can be fitted inside a truck.

### 1.2 Why This Project Matters

Post-harvest and cold-chain losses in India are estimated at roughly ₹92,000 crore annually, driven largely by breaks in the cold chain that go undetected until goods reach their destination. Less than 10% of Indian horticultural produce is ever covered by organised cold-chain infrastructure, and even where refrigerated transport exists there is typically no continuous, tamper-proof way to verify that it actually worked. The consequences are not only economic — vaccines and medicines carry zero tolerance for temperature failure.

The project sits in the Industry 5.0 paradigm rather than plain automation. The goal is not to remove the driver or the fleet manager from the loop, but to give them timely, trustworthy information so that they can act. The OLED display added in this revision is a direct expression of that idea: the human closest to the cargo — the driver — is the only person who can fix a problem in the next ten minutes, so the system now speaks to that person directly instead of only reporting to a distant dashboard.

### 1.3 Relationship to the Detailed Project Report

The DPR (Cold_Chain_DPR.docx) remains the design authority for the concept, the market case, and the five-layer architecture. This Project Report supersedes it on three specific points:

- **Bill of materials** — rewritten against the issued component list (Section 5).
- **Power architecture** — the 12 V battery, LM2596 buck converter, and inline fuse are replaced by a regulated 5 V 3 A USB-C supply with a UPS/power-bank buffer (Sections 5 and 11).
- **Feature set** — the second temperature probe and the OLED display enable eight new capabilities that the DPR did not specify (Section 7).

Everything else in the DPR — the problem framing, the market analysis, the five-layer model, and the certificate concept — carries forward unchanged.

---

## 2. Problem Statement

Despite the existence of refrigerated transport infrastructure in India, there is no widely adopted, tamper-proof mechanism to continuously verify that temperature-sensitive cargo remains within safe limits throughout transit. Four specific problems remain unresolved:

- **No continuous monitoring.** Manual spot-checks miss failures that occur between checks. A compressor can fail for hours before anyone notices.
- **No tamper-evidence.** Conventional digital temperature logs can be edited or fabricated after the fact, so they carry little weight in a commercial dispute.
- **No early warning.** Most existing systems alert only once cargo has already left the safe range, by which point damage may already be done.
- **No standardised proof of compliance.** Shipper, carrier, and receiver have no shared, objective record with which to resolve a spoilage dispute or satisfy a regulatory audit.

A fifth problem, specific to single-sensor designs and addressed for the first time in this revision:

- **No way to distinguish a real excursion from a failed or displaced sensor.** A single probe that has been unplugged, has drifted, or has been quietly moved outside the cargo box produces a log that looks perfectly compliant. One sensor cannot detect its own failure.

---

## 3. Existing Systems and Their Limitations

A range of IoT-based cold-chain monitoring approaches have been documented in the literature and in commercial products. Wireless-sensor-network and RFID-based systems have been proposed for tracking temperature and humidity across warehouses and containers [1][2][4][6], and GSM/SMS-based alerting for refrigerated containers has also been demonstrated [6]. Commercial Indian fleet-tracking platforms typically log temperature at intervals of two to fifteen minutes with basic threshold alerts.

Four gaps recur across most existing systems:

| Gap | What most systems do | What this project does |
|---|---|---|
| Tamper-evidence | Treated as a UI restriction — "we do not let you edit it" | SHA-256 chain computed on the device before the data leaves it (Section 9) |
| Local recovery | Notify a human and wait | Fire the relay and attempt an automatic compressor restart within the same control cycle |
| Slow failures | Threshold alerts only | Rate-of-change rule catches a failing compressor before the threshold is crossed |
| Sensor integrity | Assumed — a single probe is trusted absolutely | Two independent probes cross-check each other; disagreement is itself a logged event |

---

## 4. Objectives

1. Continuously measure cargo temperature at two independent points and door status at a fixed interval.
2. Detect threshold breaches, dangerous rate-of-change trends, and inter-probe disagreement using simple, explainable rules — not a black-box model — so that the logic can be verified by an auditor.
3. Respond locally within seconds through a buzzer, a warning light, an OLED message to the driver, and a relay that attempts to restart the cooling unit.
4. Respond remotely by sending an SMS alert carrying the vehicle's live GPS location.
5. Store every reading — not only faults — and protect that data against corruption even when power is cut without warning.
6. Cryptographically link each reading to the one before it so that tampering is detectable, and generate a verifiable cold-chain certificate at the end of each trip.
7. Keep the entire safety-critical loop functional with zero network connectivity.

---

## 5. Component List as Issued, and How It Differs from the DPR

### 5.1 Components issued for the build

| # | Component | Qty | Segment | Purpose in the system |
|---|---|---|---|---|
| 1 | Raspberry Pi 4 Model B, 4 GB | 1 | Processing | Main controller; runs all logic in Python |
| 2 | DS18B20 waterproof temperature sensor | 2 | Sensing | Probe A near the cooling outlet, Probe B at the far corner of the cargo box |
| 3 | 4.7 kΩ resistor | 1 | Sensing | Single pull-up for the shared 1-Wire bus |
| 4 | MC-38 magnetic reed switch | 1 | Sensing | Door open / closed detection |
| 5 | 5 V active buzzer module | 1 | Actuation | Local audible alarm |
| 6 | 5 mm red LED | 1 | Actuation | Visual warning indicator |
| 7 | 220 Ω resistor | 1 | Actuation | Current limiting for the LED |
| 8 | 5 V DC fan | 1 | Actuation | Stands in for the reefer compressor during demonstration |
| 9 | 5 V 1-channel relay module | 1 | Actuation | Switches the fan — the auto-restart path |
| 10 | SIM7600 4G/GPS HAT | 1 | Communication | SMS alerting, data uplink, GPS location and GPS time |
| 11 | 32 GB high-endurance microSD card | 1 | Storage | Boots the Pi; holds the local log database |
| 12 | 5 V 3 A USB-C power supply | 1 | Power | Primary bench and demonstration supply |
| 13 | Small UPS HAT / power bank | 1 | Power | Ride-through on power loss; enables a clean shutdown |
| 14 | Jumper wires, assorted | 20–25 | Assembly | Internal connections |
| 15 | GPIO terminal block / breakout | 1 | Assembly | Vibration-resistant screw connections |
| 16 | 0.96-inch I2C OLED display | 1 | Output | On-unit driver-facing status and alert display |

### 5.2 Differences from the DPR bill of materials

| Item | DPR specified | Issued | Consequence for the design |
|---|---|---|---|
| DS18B20 probes | 1 | 2 | Enables dual-zone sensing, differential compressor diagnostics, and sensor cross-validation (Section 7, A1 and A2) |
| OLED display | Not specified | 1 × 0.96" I2C | Enables a driver-facing HMI and on-unit chain verification (Section 7, A3 and A4) |
| Main power | 12 V battery → 5 A fuse → LM2596 buck | 5 V 3 A USB-C supply | Buck converter, fuse, and 12 V rail are removed. Simpler, but the peak-current headroom shrinks — analysed in Section 11 |
| Backup power | UPS HAT with battery-backed RTC | UPS HAT / power bank | If the issued unit is a plain power bank it provides no RTC and no power-fail signal. Mitigated in software by anchoring time to GPS — Section 7, A5 |
| Enclosure | IP65 box + 4 cable glands | Not issued | Prototype is bench-mounted. Listed as a deployment prerequisite in Section 20 |
| SIM card | Listed separately | Not listed | Required for SMS and uplink testing; to be arranged before Stage 7 of the build |
| 4.7 kΩ pull-up | 1 (one probe) | 1 (two probes) | Correct as issued — the 1-Wire bus needs exactly one pull-up regardless of how many devices share it |

**Note on the shared 1-Wire bus.** Both DS18B20 probes connect to the same GPIO4 data line and share the single 4.7 kΩ pull-up to 3.3 V. Each sensor carries a unique factory-programmed 64-bit ROM address, so the Pi can read them individually over one wire. The two ROM IDs must be recorded during Stage 3 of the build and pinned in the configuration file, so that "Probe A" always means the same physical probe in every log record — otherwise the zone labels can swap between reboots and the differential diagnostics become meaningless.

---

## 6. System Architecture

The system is organised into six layers. The Sensing Layer reads the physical world; the Processing Layer runs the decision logic on the Pi; three parallel output paths (Actuation, Local Display, and Communication) act on that decision; the Cloud Layer verifies and stores; and the Output Layer presents results to people.

| Layer | Elements | Function |
|---|---|---|
| 1 — Sensing | DS18B20 × 2, MC-38 reed switch, SIM7600 GPS | Cargo temperature at two points, door state, location, speed, and UTC time |
| 2 — Processing | Raspberry Pi 4B, Python service, SQLite store | Reads sensors, applies the three rules, writes the hash-chained record |
| 3a — Actuation | Buzzer, red LED, relay → fan | Immediate local response; attempts automatic recovery |
| 3b — Local display | 0.96" I2C OLED | Driver-facing status, alert reason, and chain verification code |
| 3c — Communication | SIM7600 4G/GPS HAT | SMS alert with GPS link; buffered data uplink |
| 4 — Cloud | Ingest, chain verification, alert fan-out | Re-verifies the chain, stores history, notifies the fleet manager |
| 5 — Output | Fleet dashboard, SMS, trip certificate | Human-readable results and the evidence artefact |

The defining architectural choice is unchanged from the DPR and is worth restating: Layers 3a and 3b act immediately and locally, without waiting for Layer 4. The buzzer, LED, relay, and OLED all respond within the same control cycle that reads the sensors, so the system remains fully protective with zero network coverage. Communication and cloud add remote visibility and long-term record-keeping on top of a loop that is already complete without them.

---

## 7. Enhancements — What We Are Adding to the Project

This is the section that distinguishes this report from the DPR. The enhancements are grouped by what they cost. Tier A items require no components beyond those already issued — they are pure software, and every one of them should be built. Tier B items need small additional purchases and are ranked by value per rupee.

### 7.1 Tier A — Enhancements using only the issued components

#### A1. Dual-zone sensing with differential compressor diagnostics

Place Probe A in the cold-air stream near the cooling outlet and Probe B at the far corner of the cargo box — the worst-case position, farthest from the cooling source. The difference between the two readings, ΔT = T_B − T_A, is a direct and continuously available indicator of cooling system health:

| Observed pattern | Physical meaning | System response |
|---|---|---|
| Both probes stable, ΔT small and steady | Normal operation, good air circulation | Log only |
| Both probes rising together | Cooling unit is failing or has stopped | Full alert; relay restart attempted |
| ΔT widening over time | Poor air circulation, blocked evaporator, or overloaded cargo | Warning-level alert; logged for maintenance |
| Probe B rising alone | Localised warm zone — a door seal leak or a hot spot | Warning-level alert; logged with GPS position |

A single-probe system sees none of this. It can report only that the cargo is warming, never why. This one change moves the project from monitoring to diagnosis, and it costs nothing beyond the second probe already issued.

#### A2. Sensor cross-validation — catching a failed or defeated probe

Two probes checking each other close the fifth problem raised in Section 2. The rule is simple and auditable:

- If the two probes disagree by more than 2.0 °C for 10 consecutive minutes, raise SENSOR_DISAGREE.
- If either probe stops responding on the 1-Wire bus, raise PROBE_FAULT and immediately fall back to single-probe threshold monitoring, with the degraded state recorded in every subsequent log entry.
- If a probe returns the DS18B20 power-on default of +85.0 °C, treat it as an unread conversion, not a real temperature — a classic 1-Wire failure signature that a naive implementation logs as a catastrophic excursion.

The commercially important case is the first of those rules: a probe that has been quietly lifted out of the cargo and left in the cab produces a log that looks flawless. With two probes, that action produces a permanent, timestamped SENSOR_DISAGREE record on the trip certificate.

#### A3. Driver-facing OLED human-machine interface

The 0.96-inch SSD1306 OLED becomes the Industry 5.0 human-in-the-loop element. Five screens rotate on a four-second cycle, with the alert screen latching until the condition clears:

| Screen | Content |
|---|---|
| HOME | Both probe temperatures, ΔT, door state, one-word system status |
| TRIP | Trip ID, elapsed time, minimum and maximum temperature so far |
| LINK | 4G signal bars, GPS fix status, number of records queued for upload |
| CHAIN | Records logged, chain-verified indicator, six-character chain code |
| ALERT | Reason, current value, safe limit, and the action the system has already taken |

The ALERT screen matters most. A buzzer tells the driver that something is wrong; the OLED tells them what is wrong and whether the system has already tried to fix it — which is the difference between panic and a correct decision to reroute to the nearest working cold store.

#### A4. On-unit chain verification code

The CHAIN screen displays the last six hexadecimal characters of the current chain head hash. An inspector, a receiving clerk, or an examiner can compare that six-character code against the value shown in the cloud record. If they match, the on-device log and the cloud record are provably the same data. If they differ, one of the two has been altered.

This is a genuinely useful property delivered by a ₹250 display: field-verifiable tamper-evidence with no laptop, no app, and no network connection required at the point of inspection.

#### A5. GPS-anchored time, removing the dependence on a battery-backed RTC

The DPR assumed a UPS HAT with a battery-backed real-time clock. The issued item may be a plain power bank with no RTC at all, which would leave the Pi with no trustworthy clock after a power cut — and a temperature log with an unreliable timestamp is worthless as evidence.

The SIM7600 HAT solves this at no extra cost. It supplies UTC from the GNSS constellation and from cellular network time. The service therefore:

1. Takes GPS UTC as the authoritative time source, falling back to cellular network time, and only then to the system clock.
2. Records the time source used in every log record, so an auditor can see exactly which readings carry satellite-grade timestamps.
3. Logs a TIME_SYNC event whenever the clock is corrected, with both the old and the new value — so a time jump is itself part of the evidence chain rather than a hole in it.

This is arguably more defensible than the original RTC design: a GPS timestamp is externally sourced and far harder to manipulate than a battery-backed chip sitting inside the same box as the person who might want to manipulate it.

#### A6. Power-loss event logging — turning a gap into evidence

With the UPS or power bank buffering the supply, the service detects loss of mains power and writes a POWER_LOSS record into the chain before shutting down, then writes a POWER_RESTORE record on the next boot. The two records bracket the outage.

The reasoning is the same as for the time source: an unexplained gap in a log is a weakness an opposing party can exploit in a dispute. A gap that is explicitly opened and closed by two chained records is evidence of exactly what happened and for how long.

#### A7. Motion-adaptive sampling

Use GPS speed to choose the sampling interval: 60 seconds while moving, 300 seconds while stationary for more than ten minutes, reverting to 60 seconds instantly on any alert condition. This matches the behaviour described in the system architecture document, reduces SD card wear and mobile data cost during long parked periods, and concentrates data density exactly where risk is highest. Every interval change is itself logged, so the record explains its own sample spacing.

#### A8. Door dwell timer and geofenced stop classification

The reed switch currently reports only open or closed. Two rules make it far more useful:

- **Dwell timer** — a door held open beyond a configured limit (for example 180 seconds) escalates from a logged event to a full alert, since extended door-open time is one of the most common preventable causes of a temperature excursion.
- **Stop classification** — compare the GPS position at the moment of a door-open event against a list of planned delivery stops. A door opened at a planned stop is routine and logged quietly. A door opened at an unplanned location triggers an immediate SMS, because that is the signature of cargo tampering or theft.

### 7.2 Tier B — Small additions worth proposing

| Priority | Addition | Approx. cost | What it buys |
|---|---|---|---|
| 1 | DS3231 I2C RTC module | ₹150 | A hardware clock independent of GPS coverage; makes A5 a belt-and-braces design rather than a single-source one. Needed only if the issued backup unit has no RTC |
| 2 | IP65 enclosure + 4 cable glands | ₹650 | The prototype cannot be vehicle-mounted without it; required for any real trial |
| 3 | ADXL345 3-axis accelerometer | ₹200 | Shock and harsh-braking events (impact damage is a distinct spoilage cause), plus reliable motion detection for A7 without depending on a GPS fix |
| 4 | SHT31 or DHT22 humidity sensor | ₹250–450 | Humidity is a first-order quality factor for fruit, vegetables, and several pharmaceutical products; a temperature-only certificate is incomplete for produce |
| 5 | Second relay channel | ₹90 | Independent control of a solenoid door lock, listed as future scope in the DPR |
| 6 | Passive buzzer in place of the active one | ₹40 | Distinct alert tones for distinct fault classes, so the driver can identify the fault type before looking at the display |

Total for the full Tier B set is approximately ₹1,600 — under 10% of the hardware already committed.

### 7.3 Software and cloud additions

- **Local SQLite store instead of flat files.** Atomic transactions mean a power cut mid-write cannot leave a half-written record. At roughly 120 bytes per record and 1,440 records per day, thirty days of full-resolution data occupies about 5 MB — a rounding error on a 32 GB card, so there is no reason to thin the data.
- **Store-and-forward uplink with the chain intact.** Records queue locally when there is no coverage and upload with their original timestamps and hashes preserved on reconnection. Rural coverage gaps must never become chain gaps.
- **MQTT over TLS** for the uplink, closing the unencrypted-transport limitation the DPR acknowledged.
- **Certificate generation service** producing a one-page PDF per trip with a QR code linking to the online verification record.
- **Fleet dashboard** with a vehicle list, live temperature plot with the safe band shaded, live map, and event log.
- **Systemd service with watchdog** so monitoring restarts automatically after any crash or reboot, and every restart is logged as an event.

### 7.4 Where to spend the effort

| Enhancement | Implementation effort | Value to the project | Verdict |
|---|---|---|---|
| A1 Dual-zone diagnostics | Low | Very high | Build first |
| A2 Sensor cross-validation | Low | Very high | Build first |
| A3 OLED HMI | Medium | High | Build first |
| A5 GPS time anchoring | Low | High | Build first |
| A6 Power-loss logging | Low | High | Build |
| A4 Chain code on OLED | Low | Medium, high demo value | Build |
| A7 Motion-adaptive sampling | Low | Medium | Build |
| A8 Door dwell + geofence | Medium | Medium | Build if time allows |
| B1 DS3231 RTC | Low | High if no RTC is present | Buy after confirming the backup unit |
| B2 Enclosure | Low | Required for field trial | Buy before any vehicle test |

---

## 8. Working Principle — Software Logic

The Raspberry Pi runs a deterministic decision loop implemented as a Python systemd service. A machine-learning model is deliberately avoided: a rule that can be stated in one sentence is also a rule that can be defended in a dispute or an audit.

### 8.1 The control loop

1. **Acquire** — read both DS18B20 probes by ROM address, read the reed switch, read GPS position, speed, and UTC.
2. **Validate** — discard the +85.0 °C power-on artefact and any out-of-range value; if a probe is unreadable, mark the cycle degraded.
3. **Evaluate** — apply the three rules in order:
   - Threshold. Is either probe outside the configured safe range for this cargo, for example 2–8 °C for vaccines?
   - Rate of change. Has either probe risen by more than 1.0 °C over the last 5 minutes, even while still inside the safe range? This is what catches a slowly failing compressor before the threshold is crossed.
   - Differential. Do the probes disagree by more than 2.0 °C for 10 consecutive minutes, or is ΔT widening consistently?
4. **Act** — on any breach, fire all outputs together within the same cycle: buzzer, LED, relay restart attempt, OLED alert screen, SMS with GPS link.
5. **Record** — write the reading, all rule outcomes, and any actions taken as one hash-chained record.
6. **Uplink** — send the record if coverage exists; otherwise queue it.
7. **Repeat** — after the interval chosen by the motion-adaptive rule.

An alert is never "acknowledged and forgotten". If a condition persists, it re-fires every cycle until it clears — with SMS rate-limited to one message per fault per fifteen minutes, so a six-hour failure does not produce three hundred text messages and a fleet manager who has stopped reading them.

### 8.2 System states

| State | Entry condition | Buzzer | LED | Relay | OLED |
|---|---|---|---|---|---|
| NORMAL | All rules pass | Off | Off | As scheduled | Rotating screens |
| WARNING | Differential or dwell rule breached | Two short beeps per cycle | Slow blink | Unchanged | ALERT screen, warning styling |
| ALARM | Threshold or rate-of-change breached | Continuous | Solid on | Restart attempted | ALERT screen, latched |
| DEGRADED | One probe faulty or no GPS fix | Single beep on entry | Double blink | Unchanged | Degraded banner on HOME |
| SHUTDOWN | Power loss detected | Three beeps | Off | Off | "POWER LOSS — LOGGING" then blank |

---

## 9. Data Model and the Tamper-Evident Chain

### 9.1 Record structure

Every cycle produces exactly one record:

| Field | Description |
|---|---|
| seq | Monotonic sequence number within the trip; gaps are detectable |
| trip_id | Unique trip identifier, issued at trip start |
| ts_utc | UTC timestamp |
| ts_src | Time source used: GPS, NET, or SYS |
| t_a, t_b | Probe A and Probe B temperatures in °C |
| delta_t | T_B − T_A |
| door | OPEN or CLOSED |
| lat, lon, speed | GPS position and speed |
| relay | Cooling relay state |
| flags | Any rule breaches or events raised this cycle |
| prev_hash | SHA-256 hash of the previous record |
| hash | SHA-256 over this record's canonical form including prev_hash |

### 9.2 How the chain works

Each record's hash is computed over its own canonical JSON form including the previous record's hash. Changing any value in any past record changes that record's hash, which breaks the prev_hash link of every record that follows it. To alter one reading convincingly, a tamperer would have to recompute every subsequent record in the trip — and the chain head would still not match the value already displayed on the OLED, already uploaded to the cloud, and already printed on the certificate.

The trip opens with a genesis record carrying the trip ID, vehicle ID, configured safe range, and both probe ROM IDs, with prev_hash set to all zeros. It closes with a terminal record carrying the trip summary and the final chain head.

This is not a blockchain and does not claim to be one. It is the hash-chaining primitive that a blockchain is built from, applied at the edge, without a distributed ledger's cost or complexity. For the purpose at hand — proving a log was not edited after the fact — it is sufficient, and it is honest about what it is.

---

## 10. Pin Connection Reference and I2C Address Map

Pin numbers use Raspberry Pi BCM GPIO numbering.

### 10.1 Signal connections

| From (Pi) | To | Notes |
|---|---|---|
| GPIO4 | DS18B20 Probe A and Probe B — both data pins | Shared 1-Wire bus. One 4.7 kΩ pull-up between this line and 3.3 V serves both. Each probe is addressed by its unique 64-bit ROM ID |
| 3.3 V | DS18B20 V_DD (both) | Normal-powered mode; parasite power is not used |
| GPIO27 | MC-38 reed switch, one wire | Other wire to GND. Internal pull-up enabled in software; debounce in software |
| GPIO2 (SDA) / GPIO3 (SCL) | OLED SDA/SCL, UPS HAT | Shared I2C bus — see the address map below |
| GPIO17 | Buzzer module, signal pin | Digital output |
| GPIO22 | LED anode via 220 Ω | Cathode to GND |
| GPIO23 | Relay module, IN | Opto-isolated input; relay coil powered from the 5 V rail |
| USB / UART (internal) | SIM7600 4G/GPS HAT | Presents as a serial device; carries SMS, data, GPS, and time |

### 10.2 I2C address map

| Device | Address | Note |
|---|---|---|
| SSD1306 OLED, 0.96" | 0x3C | 0x3D on some modules — confirm with i2cdetect -y 1 during Stage 5 |
| UPS HAT | 0x14 typical | Varies by manufacturer; confirm before assuming |
| DS3231 RTC (Tier B, optional) | 0x68 | No conflict with either of the above |

All three addresses are distinct, so the OLED, the UPS HAT, and an optional RTC coexist on one I2C bus with no arbitration issue.

### 10.3 Power connections

| From | To | Notes |
|---|---|---|
| 5 V 3 A USB-C supply | UPS HAT / power bank input | Mains supply feeds the backup unit first, so the unit acts as a buffer |
| UPS HAT / power bank output | Raspberry Pi 5 V input | Powers the Pi, both HATs, and the 5 V peripheral rail |
| 5 V rail | Buzzer, relay coil, fan (through the relay), OLED V_CC | Fan is switched by the relay's COM/NO contacts |
| All GND | Single common ground point | Every module's ground must return to the same point as the Pi |

---

## 11. Power Budget and the USB-C Supply Design Note

Replacing the 12 V battery and buck converter with a 5 V 3 A USB-C supply removes three components and simplifies the build, but it also removes the headroom the buck converter provided. The budget is worth stating explicitly, because it is the one place where the issued list is genuinely tight.

| Load | Typical current @ 5 V | Peak current @ 5 V |
|---|---|---|
| Raspberry Pi 4B (4 GB), light load | 0.60 A | 1.25 A |
| SIM7600 4G/GPS HAT, idle / registered | 0.10 A | 2.00 A during transmit burst |
| 0.96" OLED | 0.02 A | 0.03 A |
| Active buzzer | — | 0.03 A |
| Red LED via 220 Ω | 0.01 A | 0.01 A |
| Relay coil, energised | — | 0.07 A |
| 5 V DC fan | — | 0.15 A |
| DS18B20 × 2, during conversion | 0.003 A | 0.003 A |
| Total | ≈ 0.73 A | ≈ 3.54 A |

Typical draw is comfortable. The worst case — a 4G transmit burst occurring at the exact moment the relay, fan, and buzzer all fire — exceeds the 3 A supply. That combination is not a rare corner case; it is precisely what happens during an alert, which is the one moment the system must not brown out.

Three mitigations, applied together:

1. **Route mains power through the UPS/power bank**, so that the battery absorbs the transmit burst rather than the supply. This is the primary mitigation and costs nothing.
2. **Sequence the outputs in firmware** — energise the relay and fan, wait 500 ms for the inrush to settle, then trigger the SMS transmission. The driver perceives no delay; the supply sees two smaller peaks instead of one large one.
3. **Add 1000 µF of bulk capacitance across the 5 V rail** near the HAT to smooth the burst. Roughly ₹20.

If the prototype exhibits any unexplained reboot during Stage 8 testing, this is the first place to look — and a 5 V 4 A supply resolves it outright for about ₹250.

---

## 12. Build Sequence

Build and test in this order. Testing each segment before adding the next means a fault is always in the part just added, not buried in a fully wired board.

**Stage 1 — Power.** Confirm the USB-C supply holds 5 V under load with the Pi connected. Confirm the UPS/power bank passes power through and charges. Determine whether it exposes an RTC or a power-fail signal — this decision drives whether Tier B item B1 is needed.

**Stage 2 — Brain.** Flash Raspberry Pi OS to the high-endurance card with Raspberry Pi Imager. Boot, enable SSH, enable the 1-Wire and I2C interfaces.

**Stage 3 — Temperature probes.** Wire Probe A with the 4.7 kΩ pull-up to GPIO4 and confirm a plausible reading. Add Probe B to the same bus. Record both ROM IDs and pin them to physical positions in the configuration file — this step is easy to skip and expensive to skip. Verify both probes independently in a fridge and at room temperature.

**Stage 4 — Door sensor.** Wire the reed switch to GPIO27. Confirm a clean state change as a magnet approaches and retreats, and confirm software debouncing suppresses any chatter.

**Stage 5 — OLED and I2C.** Connect the OLED to SDA/SCL. Run i2cdetect -y 1 and confirm the expected addresses appear with no collision. Render a test screen, then implement the five-screen rotation.

**Stage 6 — Actuators.** Wire and individually verify the buzzer on GPIO17, the LED on GPIO22, and the relay on GPIO23. Connect the fan through the relay's COM/NO contacts and confirm switching does not disturb the Pi.

**Stage 7 — Connectivity.** Attach the SIM7600 HAT with an active SIM. Confirm 4G registration, send a test SMS, obtain a GPS fix near a window or outdoors, and confirm GPS UTC is readable — the last of these is a prerequisite for the time-anchoring enhancement.

**Stage 8 — Integration.** Run the full Python service: acquire, validate, evaluate all three rules, act, record with hash chaining, uplink. Install it as a systemd service with a watchdog so it restarts on boot and after any crash.

**Stage 9 — Full simulated trip.** Warm Probe A by hand to cross the threshold; warm it slowly to trigger the rate rule without crossing the threshold; separate the probes to trigger the differential rule; open the door sensor; cut mains power mid-trip. Confirm every output responds, every event is chained, and the chain verifies end to end.

**Stage 10 — Housing.** Mount the assembly in an enclosure (Tier B item B2), route the probe and antenna leads through cable glands, and re-run Stage 9 in the final housing to confirm nothing shifted during assembly.

---

## 13. Testing Methodology

### 13.1 Unit tests

| Component | Procedure | Expected result |
|---|---|---|
| DS18B20 × 2 | Compare both probes against a reference thermometer at room temperature and in a fridge | Both within ±0.5 °C of the reference and within ±0.5 °C of each other |
| 1-Wire bus | List devices with both probes connected | Exactly two unique ROM IDs enumerate reliably across ten consecutive reboots |
| MC-38 reed switch | Move a magnet near and away while reading the GPIO | Clean state transitions with no bounce after debouncing |
| OLED | Render all five screens in sequence | All screens legible; rotation timing correct; no I2C errors over a 30-minute run |
| Buzzer / LED / Relay | Trigger each individually from a test script | Each responds immediately and independently |
| SIM7600 SMS | Check registration, send a test message | Message received on a handset within 30 seconds |
| SIM7600 GPS | Read GNSS output outdoors for 2–3 minutes | Valid fix with latitude, longitude, and UTC |
| Backup power | Remove mains power with the Pi running | Pi continues running; power-loss condition is detectable in software |

### 13.2 Integration tests

- Both probes plus the OLED reading and rendering in the same loop without I2C or 1-Wire timing conflicts.
- Relay and fan switching while the SIM7600 transmits — the specific test for the Section 11 power concern.
- UPS HAT and SIM7600 HAT sharing the GPIO header without interference.
- Hash chain remaining unbroken across a deliberate mid-trip service restart.

### 13.3 Formal test cases

| ID | Description | Input | Expected output |
|---|---|---|---|
| TC-01 | Normal operation | Both probes in range, door closed | No alert; record logged; HOME screen rotating |
| TC-02 | Threshold breach | Probe A warmed above the safe range | Buzzer, LED, relay restart, OLED ALERT, SMS, chained record — all together |
| TC-03 | Rate-of-change breach | Probe A warmed 1.5 °C in 4 minutes, still in range | Same full response as TC-02; flag records the rate rule |
| TC-04 | Differential breach (new) | Probes separated; ΔT held above 2 °C for 10 minutes | WARNING state; SENSOR_DISAGREE logged; OLED shows the disagreement |
| TC-05 | Probe removed mid-trip (new) | Probe B unplugged from the 1-Wire bus | PROBE_FAULT logged; DEGRADED state; single-probe fallback active; every later record marked degraded |
| TC-06 | +85 °C artefact rejection (new) | Force a power-on default read | Value discarded, not logged as an excursion; retry on the next cycle |
| TC-07 | Door opened unexpectedly | Reed switch opened away from a planned stop | Door event logged with GPS; SMS sent |
| TC-08 | Door dwell exceeded (new) | Door held open beyond 180 seconds | Escalation from event to WARNING; buzzer sounds |
| TC-09 | Network unavailable | SIM7600 with no signal during an alert | Alert stored locally and queued; transmitted automatically on reconnection with the original timestamp |
| TC-10 | Sudden power interruption | Mains cut without warning | POWER_LOSS record written before shutdown; clean shutdown; POWER_RESTORE on reboot; chain unbroken across the gap |
| TC-11 | Time source fallback (new) | GPS fix lost mid-trip | ts_src changes from GPS to NET or SYS; TIME_SYNC event logged on the next correction |
| TC-12 | Chain tamper detection (new) | Edit one temperature value directly in the stored log | Verification reports the exact record at which the chain breaks; OLED chain code no longer matches the cloud value |

The six test cases marked "new" exist only because of the enhancements in Section 7.

---

## 14. Results and Output Display

### 14.1 On-unit display

The OLED is the first output a human sees. During normal running it cycles quietly through status screens; on an alert it latches to the ALERT screen with the reason, the current value, the safe limit, and the action already taken. Full layouts appear in Appendix A.

### 14.2 SMS alert format

```
ALERT: Vehicle GJ-01-EF-9012
RATE: Probe A rising 1.4C/5min (now 7.4C, limit 8.0C)
Probe B 7.9C | Door CLOSED
Cooling relay restart attempted 11:24
Loc: maps.google.com/?q=23.0225,72.5714
```

### 14.3 Fleet dashboard

A vehicle list with per-vehicle status markers, a live temperature plot showing both probes with the safe band shaded, a ΔT trace beneath it as the compressor-health indicator, a live map, and a running event log.

### 14.4 Cold-chain certificate

| Field | Source |
|---|---|
| Trip and vehicle ID | Genesis record |
| Start and end time and location | GPS timestamp and position |
| Temperature range, both probes | Trip minimum and maximum per probe |
| Maximum observed ΔT | Compressor-health summary for the trip |
| Door-open events, count and duration | Reed switch log with GPS positions |
| Excursions | Every threshold, rate, and differential breach with start and end times |
| Sensor integrity result | Any PROBE_FAULT or SENSOR_DISAGREE periods |
| Power continuity | Any POWER_LOSS intervals, bracketed and accounted for |
| Chain verification result | Pass or fail, with the chain head hash and a verification QR code |

### 14.5 Notes for the live demonstration

- Keep the assembly open or in a transparent box so that the buzzer, LED, and relay are visible as they fire.
- Hold a cup of warm water near Probe A to trigger the threshold alert on demand; warm it slowly with a hand to trigger the rate rule instead.
- Separate the two probes — one in a cold container, one in the open — to demonstrate the differential rule. This is the most visually convincing demonstration in the project, because the OLED explains the diagnosis as it happens.
- Unplug Probe B mid-demonstration to show PROBE_FAULT and the graceful degradation to single-probe mode.
- Pull the power mid-demonstration and show the clean shutdown, then the POWER_LOSS and POWER_RESTORE pair bracketing the gap in the log.
- Finish by editing one value in the stored log and running the verifier, which will name the exact record where the chain breaks.

---

## 15. Cost Analysis

### 15.1 Issued components

| Component | Qty | Unit (₹) | Total (₹) |
|---|---|---|---|
| Raspberry Pi 4 Model B, 4 GB | 1 | 6,500 | 6,500 |
| SIM7600 4G/GPS HAT | 1 | 5,500 | 5,500 |
| UPS HAT / power bank | 1 | 1,200 | 1,200 |
| 32 GB high-endurance microSD | 1 | 700 | 700 |
| 5 V 3 A USB-C supply | 1 | 600 | 600 |
| DS18B20 waterproof probe | 2 | 250 | 500 |
| GPIO terminal breakout | 1 | 350 | 350 |
| 0.96" I2C OLED display | 1 | 250 | 250 |
| 5 V DC fan | 1 | 150 | 150 |
| MC-38 reed switch | 1 | 120 | 120 |
| Jumper wires, assorted | ~25 | — | 120 |
| 5 V 1-channel relay module | 1 | 90 | 90 |
| Active buzzer module | 1 | 60 | 60 |
| LED, resistors (4.7 kΩ, 220 Ω) | 3 | — | 10 |
| Hardware total as issued | | | ≈ 16,150 |

Prices are indicative Indian retail figures for 2026 and will vary with supplier.

### 15.2 Recommended additions

| Addition | Cost (₹) |
|---|---|
| IP65 enclosure and cable glands | 650 |
| DS3231 RTC module | 150 |
| ADXL345 accelerometer | 200 |
| SHT31 humidity sensor | 350 |
| Bulk capacitor and misc. passives | 50 |
| Tier B total | ≈ 1,400 |

### 15.3 Recurring costs

SIM data and SMS: ₹150–300 per month. Cloud hosting beyond the prototype: approximately ₹1,500 per month shared across a fleet.

### 15.4 Cost commentary

At roughly ₹16,150, this build costs about 2.7 times an equivalent ESP32 design (≈ ₹6,050). The premium buys Python-based development, a combined 4G/GPS HAT in place of two modules, straightforward OLED and SQLite support, and processing headroom for later analytics. For a production fleet rollout the ESP32 variant remains the correct commercial choice; the Pi is the correct choice for a prototype that has to be built, debugged, extended, and demonstrated within one semester by a four-person team.

It is also worth noting what the two extra components actually cost. The second DS18B20 and the OLED together come to ₹500 — about 3% of the build — and between them they enable eight of the fourteen enhancements listed in Section 7, including six of the twelve test cases in Section 13.3.

---

## 16. Team Roles and Work Split

Group 4 — Sky is the Limit. Four members, with ownership split so that no two people are blocked on the same component. Names to be entered against each role before submission.

| Role | Responsibility | Member |
|---|---|---|
| Hardware and wiring | Probe placement and ROM-ID mapping, power rail and budget verification, relay and actuator wiring, enclosure and mounting | |
| Firmware and sensing | Control loop, three-rule engine, OLED screens, GPS time anchoring, systemd service and watchdog | |
| Data integrity and backend | Hash chain, SQLite store, store-and-forward uplink, chain verifier, certificate generation | |
| Cloud, dashboard and documentation | Dashboard, alert fan-out, test execution and records, report and demonstration material | |

The integrity and backend role carries the core intellectual property of the project. If the hash chain is implemented loosely, the tamper-evidence claim becomes marketing copy rather than a property of the system, and the certificate loses the one quality that distinguishes it from any other temperature log.

---

## 17. Project Timeline

| Week | Milestone | Exit criterion |
|---|---|---|
| 1 | Component verification and power characterisation | 5 V rail holds under load; backup unit's RTC capability determined |
| 2 | Sensing segment complete | Both probes enumerate reliably; ROM IDs pinned; door sensor debounced |
| 3 | Display and actuation complete | Five OLED screens rendering; buzzer, LED, relay all verified individually |
| 4 | Connectivity complete | 4G registered, test SMS delivered, GPS fix and UTC obtained |
| 5 | Control loop and rule engine | All three rules firing correctly against simulated inputs |
| 6 | Chain, storage and uplink | Chain verifies end to end; store-and-forward proven across a coverage gap |
| 7 | Full system test | TC-01 to TC-12 executed and recorded |
| 8 | Enclosure, certificate, demonstration | Certificate generated from a real logged trip; demonstration rehearsed |

---

## 18. Risks and Mitigations

| Risk | Likelihood | Impact | Mitigation |
|---|---|---|---|
| Peak current exceeds the 3 A supply during an alert | Medium | High — reboot at the worst moment | Route power through the UPS buffer, sequence outputs in firmware, add bulk capacitance (Section 11) |
| Backup unit has no RTC or power-fail signal | Medium | Medium — untrustworthy timestamps | GPS time anchoring (A5); add a DS3231 for ₹150 if confirmed |
| Probe ROM IDs not pinned; zone labels swap on reboot | Medium | High — differential diagnostics become meaningless | Record and pin both IDs during Stage 3; assert on mismatch at every startup |
| SD card corruption from an unclean shutdown | Medium | High — trip data lost | SQLite with atomic transactions, UPS ride-through, clean shutdown on power loss |
| No SIM card available in time for Stage 7 | Medium | Medium — blocks SMS and uplink testing | Arrange the SIM during Week 1; the loop and chain are independently testable without it |
| I2C address collision between OLED and UPS HAT | Low | Low | Verified with i2cdetect at Stage 5; addresses are configurable on both devices |
| GPS fix unavailable indoors during the demonstration | High | Low | Cache the last known fix and label it clearly as cached; demonstrate a live fix near a window beforehand |

---

## 19. Advantages

- The core safety function works with no internet connection at all — buzzer, LED, relay, and OLED respond locally within the same control cycle.
- Two probes diagnose rather than merely detect. The system distinguishes a cooling failure from a circulation problem from a localised hot spot, and can detect its own sensor failure.
- Slow failures are caught early by the rate-of-change rule, before a hard threshold is crossed.
- Automatic recovery is attempted rather than only notifying a human and waiting.
- The driver is informed, not just alarmed. The OLED states the fault and the action already taken, supporting a correct decision instead of a panicked one.
- Records are tamper-evident and field-verifiable. The six-character chain code on the display can be checked against the cloud record with no equipment at all.
- Timestamps are externally anchored to GPS, which is harder to manipulate than a clock inside the same enclosure as the data.
- Gaps in the record are themselves recorded, so an outage is accounted for rather than being a blind spot an opposing party can exploit.

---

## 20. Limitations of the Prototype

- **Single point of failure.** One Pi and one sensor set; a production unit on a critical route would need redundancy.
- **Higher cost and power draw** than a microcontroller equivalent — roughly 2.7× the hardware cost and considerably more continuous current, which matters for a vehicle parked with the engine off.
- **Peak current headroom is thin** on the issued 3 A supply, as analysed in Section 11.
- **No enclosure was issued**, so the prototype is bench-mounted and not yet vehicle-ready.
- **The chain is a software hash chain, not a signed ledger.** It proves the log was not edited; it does not cryptographically bind the log to a specific device identity. Device-key signing is the natural next step.
- **Transport encryption is not implemented** in the prototype; MQTT over TLS is specified but not yet built.
- **Humidity, shock, and fuel level are not measured**, so the certificate covers temperature and door integrity only.
- **Two probes are the minimum for cross-validation, not the ideal.** With two sensors in disagreement the system knows something is wrong but cannot always determine which probe is at fault; three would allow majority voting.

---

## 21. Future Scope

1. **Three-probe majority voting** to identify which sensor has failed, not merely that they disagree.
2. **Device-key signing** — each unit holds a private key and signs its chain head, binding the record to a specific physical device.
3. **Humidity and shock sensing** to extend the certificate from temperature-only to full cargo-condition coverage.
4. **Fuel-level sensing** on the reefer's independent diesel tank, catching siphoning before it becomes a cooling failure.
5. **Solenoid door lock** on the second relay channel for high-value cargo.
6. **Predictive maintenance** from compressor cycling patterns and ΔT trends accumulated over several seasons — the Pi has the headroom for it.
7. **Multi-vehicle fleet dashboard** with role-based access for drivers, fleet managers, and auditors.
8. **PMKSY and FSSAI reporting integration**, so the generated certificate can be submitted for scheme reporting without manual reformatting.
9. **Migration to an ESP32 production variant** once the feature set is stable, cutting per-unit cost for fleet rollout while keeping the identical data model and chain format.

---

## 22. Conclusion

This project demonstrates that a reliable, tamper-evident cold-chain monitoring system can be built from widely available components, using a Raspberry Pi to trade higher hardware cost and power draw for simpler development and easier debugging.

The revision documented here started from a constraint — the components issued did not match the components specified — and turned it into the most significant improvement in the project. A second temperature probe and a ₹250 display, together about 3% of the build cost, take the system from detection to diagnosis, give it the ability to detect its own sensor failures, and put a field-verifiable integrity check in front of the one human who can actually act on it.

By combining simple, explainable rules with local actuation, driver-facing feedback, and remote alerting, the prototype closes the four gaps most common in existing systems: it acts without depending on connectivity, it attempts automatic recovery rather than only notifying, it validates its own sensors instead of trusting them blindly, and it produces a record trustworthy enough to serve as evidence. The bill of materials, wiring reference, build sequence, and test plan in this report are sufficient to reproduce the prototype and extend it toward a field-ready product.

---

## 23. References

1. "An IoT Smart System for Cold Supply Chain Storage and Transportation Management," Engineering, Technology & Applied Science Research. https://www.etasr.com/index.php/ETASR/article/view/6857
2. C. K. M. Lee, Y. Lv, K. K. H. Ng, W. Ho, and K. L. Choy, "Design and application of Internet of things-based warehouse management system for smart logistics," International Journal of Production Research, vol. 56, no. 8, pp. 2753–2768, 2018. DOI: 10.1080/00207543.2017.1394592
3. M. Humayun, N. Jhanjhi, B. Hamid, and G. Ahmed, "Emerging Smart Logistics and Transportation Using IoT and Blockchain," IEEE Internet of Things Magazine, vol. 3, no. 2, pp. 58–62, 2020. DOI: 10.1109/IOTM.0001.190009
4. "IoT based cold chain logistics monitoring," IEEE Conference Publication. https://ieeexplore.ieee.org/document/8392059/
5. "IoT-Driven Cold Chain Management for Real-Time Monitoring and Alerts for Perishable Goods," IEEE Conference Publication, 2024. https://ieeexplore.ieee.org/document/10940754/
6. "Internet of Things enabled real time cold chain monitoring in a container port," Journal of Shipping and Trade, Springer Nature. https://link.springer.com/article/10.1186/s41072-022-00110-z
7. Ministry of Food Processing Industries, Government of India, "Revised Guidelines for the Integrated Cold Chain and Value Addition Infrastructure Scheme (PMKSY)," 22 May 2025. https://mofpi.gov.in/en/announcements/revised-operational-guidelines-dated-22052025-respect-component-scheme-integrated-cold
8. Raspberry Pi Ltd., "Raspberry Pi 4 Model B Product Brief" (manufacturer datasheet).
9. Analog Devices / Maxim Integrated, "DS18B20 Programmable Resolution 1-Wire Digital Thermometer" (manufacturer datasheet).
10. Solomon Systech, "SSD1306 — 128 × 64 Dot Matrix OLED/PLED Segment/Common Driver with Controller" (manufacturer datasheet).
11. SIMCom Wireless Solutions, "SIM7600 Series AT Command Manual" and "Hardware Design Guide" (manufacturer documentation).
12. Group 4, Detailed Project Report — Cold-Chain Integrity & Last-Mile Reefer Monitoring System, ECE-504, August 2026.

---

## 24. Appendix A — OLED Screen Layouts

128 × 64 pixels, SSD1306, I2C address 0x3C. Screens rotate every 4 seconds; the ALERT screen latches until the condition clears.

HOME

```
+------------------------+
| COLD-CHAIN    [NORMAL] |
| A  4.2C    B  5.1C     |
| dT 0.9C    DOOR CLOSED |
| GJ-01-EF-9012   11:24  |
+------------------------+
```

TRIP

```
+------------------------+
| TRIP 2026-0914-071     |
| Elapsed      04:12:30  |
| Min 3.8C    Max 6.1C   |
| Excursions          0  |
+------------------------+
```

LINK

```
+------------------------+
| 4G  ....|   GPS  FIX   |
| Queued records      0  |
| Last uplink   11:23:40 |
| SMS sent today      2  |
+------------------------+
```

CHAIN

```
+------------------------+
| CHAIN        VERIFIED  |
| Records          4,381 |
| Head      ...9F2A1C    |
| Time src           GPS |
+------------------------+
```

ALERT (latched)

```
+------------------------+
| !! RATE ALERT !!       |
| A 7.4C rising 1.4C/5m  |
| Limit 8.0C   B 7.9C    |
| RELAY RESTART 11:24    |
+------------------------+
```

---

## 25. Appendix B — Sample Log Record and Certificate

Sample chained record

```
{
  "seq": 4381,
  "trip_id": "2026-0914-071",
  "ts_utc": "2026-09-14T11:24:00Z",
  "ts_src": "GPS",
  "t_a": 7.4,
  "t_b": 7.9,
  "delta_t": 0.5,
  "door": "CLOSED",
  "lat": 23.0225,
  "lon": 72.5714,
  "speed": 42.1,
  "relay": "RESTART_ATTEMPTED",
  "flags": ["RATE_BREACH"],
  "prev_hash": "8c1f...4b2e",
  "hash": "e77d...9f2a1c"
}
```

Certificate summary block

```
COLD-CHAIN INTEGRITY CERTIFICATE
Trip 2026-0914-071   Vehicle GJ-01-EF-9012
Ahmedabad 06:58 IST  ->  Anand 11:41 IST

Probe A   min 3.8C   max 7.4C
Probe B   min 4.1C   max 7.9C
Max dT observed: 1.2C

Door events: 2 (both at planned stops)
Excursions:  1 rate-of-change, 11:24-11:31, recovered
Sensor integrity: OK, both probes active throughout
Power continuity: unbroken

CHAIN VERIFIED   4,381 of 4,381 records
Head hash e77d...9f2a1c
```

---

Prepared by Group 4 — Sky is the Limit · ECE-504 Internet of Things · Monsoon Semester 2026
