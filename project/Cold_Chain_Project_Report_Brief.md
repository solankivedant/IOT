# PROJECT REPORT
## Cold-Chain Integrity & Last-Mile Reefer Monitoring System
### An IoT Prototype for Industry 5.0 — Raspberry Pi 4 Build

**Course:** ECE-504 — Internet of Things
**Semester:** Monsoon Semester, 2026
**Group No.:** 4 — Sky is the Limit

## Abstract

Refrigerated transport is the weakest link in India's food and pharmaceutical supply chains: cargo loses its cold environment silently, and the loss is discovered only at delivery when it is already unrecoverable. This report presents an IoT-based Cold-Chain Integrity and Last-Mile Reefer Monitoring System built on a Raspberry Pi 4 Model B. The system senses cargo temperature at two independent points and monitors door status, applies three explainable rules — threshold, rate-of-change, and inter-probe differential — and responds immediately through local actuation (buzzer, warning LED, automatic compressor-restart relay), an on-unit OLED display for the driver, and SMS alerting with GPS location. Every reading is time-stamped from GPS and cryptographically linked to the previous one, so the record cannot be silently altered and each trip ends with a verifiable cold-chain certificate.

## 1. Introduction and Problem Statement

Post-harvest and cold-chain losses in India are estimated at roughly ₹92,000 crore annually, driven largely by breaks in the cold chain that go undetected until goods reach their destination. Less than 10% of Indian horticultural produce is covered by organised cold-chain infrastructure, and even where refrigerated transport exists there is usually no continuous, tamper-proof way to verify it actually worked. For vaccines and medicines the tolerance for failure is zero.

Five specific problems remain unresolved in current practice:

- **No continuous monitoring.** Manual spot-checks miss failures between checks; a compressor can fail for hours before anyone notices.
- **No tamper-evidence.** Conventional digital logs can be edited after the fact, so they carry little weight in a dispute.
- **No early warning.** Most systems alert only after cargo has already left the safe range, by which point damage is done.
- **No standardised proof of compliance.** Shipper, carrier, and receiver have no shared objective record.
- **No way to tell a real excursion from a failed sensor.** A single probe that has been unplugged, has drifted, or has been quietly moved out of the cargo box produces a log that looks perfectly compliant. One sensor cannot detect its own failure.

The project sits in the **Industry 5.0** paradigm rather than plain automation: the aim is not to remove the driver or fleet manager from the loop, but to give them trustworthy information in time to act.

## 2. Objectives

1. Continuously measure cargo temperature at two independent points, plus door status, at a fixed interval.
2. Detect threshold breaches, dangerous warming trends, and inter-probe disagreement using simple rules that an auditor can verify — not a black-box model.
3. Respond locally within seconds: buzzer, warning LED, OLED message to the driver, and a relay that attempts to restart the cooling unit.
4. Respond remotely by SMS carrying the live GPS location.
5. Log every reading, protected against corruption from sudden power loss.
6. Hash-chain each reading to the previous one so tampering is detectable, and generate a verifiable trip certificate.
7. Keep the entire safety-critical loop working with **zero network connectivity**.

## 3. Components Used

| # | Component | Qty | Purpose |
|---|---|---|---|
| 1 | Raspberry Pi 4 Model B, 4 GB | 1 | Main controller; runs all logic in Python |
| 2 | DS18B20 waterproof temperature sensor | 2 | Probe A at the cooling outlet, Probe B at the far corner |
| 3 | 4.7 kΩ resistor | 1 | Single pull-up for the shared 1-Wire bus |
| 4 | MC-38 magnetic reed switch | 1 | Door open / closed detection |
| 5 | 5 V active buzzer module | 1 | Local audible alarm |
| 6 | 5 mm red LED + 220 Ω resistor | 1 each | Visual warning indicator |
| 7 | 5 V DC fan | 1 | Stands in for the reefer compressor |
| 8 | 5 V 1-channel relay module | 1 | Switches the fan — the auto-restart path |
| 9 | SIM7600 4G/GPS HAT | 1 | SMS, data uplink, GPS location and GPS time |
| 10 | 32 GB high-endurance microSD | 1 | Boots the Pi; holds the local log database |
| 11 | 5 V 3 A USB-C power supply | 1 | Primary supply |
| 12 | Small UPS HAT / power bank | 1 | Ride-through on power loss; clean shutdown |
| 13 | 0.96-inch I2C OLED display | 1 | Driver-facing status and alert display |
| 14 | GPIO terminal block / breakout | 1 | Vibration-resistant screw connections |
| 15 | Jumper wires, assorted | 20–25 | Internal connections |

**Note on the 1-Wire bus.** Both DS18B20 probes share the same GPIO4 data line and the single 4.7 kΩ pull-up. Each carries a unique factory 64-bit ROM address, so the Pi reads them individually over one wire. Both ROM IDs must be recorded during the build and pinned in the config file, so "Probe A" always means the same physical probe — otherwise zone labels can swap between reboots and the differential logic becomes meaningless.

## 4. System Architecture

| Layer | Elements | Function |
|---|---|---|
| 1 — Sensing | DS18B20 × 2, reed switch, SIM7600 GPS | Temperature at two points, door state, location, speed, UTC |
| 2 — Processing | Raspberry Pi 4B, Python service, SQLite | Applies the three rules; writes the hash-chained record |
| 3a — Actuation | Buzzer, LED, relay → fan | Immediate local response; attempts automatic recovery |
| 3b — Local display | 0.96" I2C OLED | Driver-facing status, alert reason, chain verification code |
| 3c — Communication | SIM7600 4G/GPS HAT | SMS alert with GPS link; buffered data uplink |
| 4 — Cloud | Ingest, chain verification, alerting | Re-verifies the chain, stores history, notifies the fleet manager |
| 5 — Output | Dashboard, SMS, trip certificate | Human-readable results and the evidence artefact |

The defining choice: **layers 3a and 3b act locally without waiting for the cloud.** Buzzer, LED, relay, and OLED all respond within the same control cycle that reads the sensors, so the system stays fully protective with no network coverage. Communication and cloud add remote visibility on top of a loop that is already complete without them.

## 5. Working Principle

The Pi runs a deterministic loop as a Python systemd service. A machine-learning model is deliberately avoided: a rule that can be stated in one sentence is a rule that can be defended in an audit.

**Acquire** both probes by ROM address, the reed switch, and GPS position, speed and UTC → **Validate**, discarding the DS18B20 +85.0 °C power-on artefact and any out-of-range value → **Evaluate** the three rules → **Act** on any breach by firing all outputs together in the same cycle → **Record** the reading, rule outcomes and actions as one hash-chained entry → **Uplink**, or queue if there is no coverage → **Repeat**.

The three rules:

| Rule | Condition | Catches |
|---|---|---|
| Threshold | Either probe outside the configured safe range, e.g. 2–8 °C for vaccines | An excursion that has already happened |
| Rate of change | Either probe rising more than 1.0 °C in 5 minutes, even while still in range | A slowly failing compressor, **before** the threshold is crossed |
| Differential | Probes disagree by more than 2.0 °C for 10 consecutive minutes | A failed or displaced sensor, poor air circulation, a localised hot spot |

An alert is never "acknowledged and forgotten" — if the condition persists it re-fires every cycle until it clears, with SMS rate-limited to one message per fault per fifteen minutes so a six-hour failure does not produce three hundred texts and a fleet manager who has stopped reading them.

| State | Entry condition | Buzzer | LED | Relay | OLED |
|---|---|---|---|---|---|
| NORMAL | All rules pass | Off | Off | As scheduled | Rotating screens |
| WARNING | Differential or door-dwell breach | Two beeps/cycle | Slow blink | Unchanged | ALERT screen |
| ALARM | Threshold or rate-of-change breach | Continuous | Solid | Restart attempted | ALERT, latched |
| DEGRADED | One probe faulty, or no GPS fix | One beep on entry | Double blink | Unchanged | Degraded banner |
| SHUTDOWN | Power loss detected | Three beeps | Off | Off | "POWER LOSS" then blank |

## 6. Tamper-Evident Logging

Every cycle writes one record: sequence number, trip ID, UTC timestamp, time source, both probe temperatures, ΔT, door state, GPS position and speed, relay state, any rule flags, the previous record's hash, and its own SHA-256 hash.

Each hash is computed over the record's canonical form **including the previous record's hash**. Changing any past value changes that record's hash and breaks the link of every record after it. To alter one reading convincingly, a tamperer would have to recompute the entire remaining trip — and the chain head would still not match the value already shown on the OLED, already uploaded to the cloud, and already printed on the certificate.

This is not a blockchain and does not claim to be one. It is the hash-chaining primitive a blockchain is built from, applied at the edge without a distributed ledger's cost. For proving a log was not edited after the fact, it is sufficient.

## 7. Enhancements Added to the Project

The second temperature probe and the OLED display together cost about ₹500 — roughly 3% of the build — and between them enable everything in this section. All of the following are software-only; no component beyond those listed in Section 3 is required.

**Dual-zone differential diagnostics.** Probe A sits in the cold-air stream at the cooling outlet, Probe B at the far corner of the cargo box — the worst-case position. The gap between them, ΔT, is a continuous indicator of cooling health:

| Pattern | Meaning | Response |
|---|---|---|
| ΔT small and steady | Normal operation, good circulation | Log only |
| Both probes rising together | Cooling unit failing or stopped | Full alert; relay restart attempted |
| ΔT widening over time | Blocked evaporator or overloaded cargo | Warning; logged for maintenance |
| Probe B rising alone | Localised hot spot or door-seal leak | Warning; logged with GPS position |

A single-probe system reports only *that* cargo is warming, never *why*. This moves the project from monitoring to diagnosis.

**Sensor cross-validation.** If the probes disagree beyond tolerance, the system raises `SENSOR_DISAGREE`; if a probe stops responding, `PROBE_FAULT` with fallback to single-probe monitoring and every later record marked degraded. The commercially important case: a probe quietly lifted out of the cargo and left in the cab produces a flawless-looking log on a single-probe system, but a permanent timestamped disagreement record here.

**Driver-facing OLED interface.** Five screens rotate every four seconds, with ALERT latching until the condition clears — HOME (both temperatures, ΔT, door, status), TRIP (ID, elapsed, min/max), LINK (signal, GPS fix, queued records), CHAIN (records logged, verified indicator, chain code), ALERT (reason, value, limit, action already taken). A buzzer tells the driver *something* is wrong; the OLED tells them *what*, and whether the system has already tried to fix it.

**On-unit chain verification.** The CHAIN screen shows the last six hex characters of the current chain head. An inspector or receiving clerk compares that against the cloud record — if they match, the two are provably the same data. Field-verifiable tamper-evidence with no laptop, app, or network.

**GPS-anchored time.** If the issued backup unit is a plain power bank it has no RTC, leaving no trustworthy clock after a power cut — and a log with an unreliable timestamp is worthless as evidence. The SIM7600 supplies UTC from GNSS, falling back to network time and only then to the system clock, with the source recorded in every entry. A GPS timestamp is externally sourced and harder to manipulate than a battery-backed chip inside the same box as the person who might want to manipulate it.

**Power-loss bracketing.** The service writes `POWER_LOSS` into the chain before shutting down and `POWER_RESTORE` on the next boot. An unexplained gap is a weakness in a dispute; a gap opened and closed by two chained records is evidence.

**Motion-adaptive sampling.** 60 seconds while moving, 300 seconds when stationary over ten minutes, reverting to 60 seconds instantly on any alert — reducing SD wear and data cost while concentrating density where risk is highest.

**Door dwell and stop classification.** A door held open beyond 180 seconds escalates to a full alert. A door opened at an unplanned GPS location triggers immediate SMS, since that is the signature of tampering or theft.

## 8. Circuit Connections

Pin numbers use Raspberry Pi BCM GPIO numbering.

| From (Pi) | To | Notes |
|---|---|---|
| GPIO4 | DS18B20 Probe A and Probe B, both data pins | Shared 1-Wire bus; one 4.7 kΩ pull-up to 3.3 V serves both |
| 3.3 V | DS18B20 V_DD (both) | Normal-powered mode; parasite power not used |
| GPIO27 | MC-38 reed switch, one wire | Other wire to GND; internal pull-up and debounce in software |
| GPIO2 / GPIO3 | OLED SDA / SCL, UPS HAT | Shared I2C bus |
| GPIO17 | Buzzer module, signal pin | Digital output |
| GPIO22 | LED anode via 220 Ω | Cathode to GND |
| GPIO23 | Relay module, IN | Opto-isolated; coil from the 5 V rail; fan on COM/NO |
| USB / UART | SIM7600 4G/GPS HAT | Serial device; carries SMS, data, GPS and time |

**I2C addresses:** OLED 0x3C (0x3D on some modules), UPS HAT typically 0x14, optional DS3231 RTC 0x68. All distinct — confirm with `i2cdetect -y 1` during the build.

**Power path:** the USB-C supply feeds the UPS / power bank, whose output powers the Pi, both HATs, and the 5 V peripheral rail. Every module's ground returns to a single common point.

## 9. Power Budget

| Load | Typical @ 5 V | Peak @ 5 V |
|---|---|---|
| Raspberry Pi 4B, light load | 0.60 A | 1.25 A |
| SIM7600 4G/GPS HAT | 0.10 A | 2.00 A during transmit burst |
| OLED, buzzer, LED, relay coil, fan | 0.03 A | 0.29 A |
| DS18B20 × 2 | 0.003 A | 0.003 A |
| **Total** | **≈ 0.73 A** | **≈ 3.54 A** |

Typical draw is comfortable, but the worst case — a 4G transmit burst at the exact moment the relay, fan and buzzer fire — exceeds the 3 A supply. That is not a corner case; it is precisely what happens during an alert, the one moment the system must not brown out. Three mitigations applied together: route mains power **through** the UPS so the battery absorbs the burst; sequence the outputs in firmware, energising the relay and fan then waiting 500 ms before transmitting; and add 1000 µF of bulk capacitance near the HAT. A 5 V 4 A supply removes the problem outright for about ₹250.

## 10. Build and Test Sequence

Build in stages, testing each before adding the next, so a fault is always in the part just added:

1. **Power** — confirm 5 V under load; determine whether the backup unit offers an RTC or power-fail signal.
2. **Brain** — flash Raspberry Pi OS; enable SSH, 1-Wire and I2C.
3. **Probes** — Probe A with pull-up on GPIO4, then Probe B on the same bus; **record and pin both ROM IDs**; verify against a reference thermometer at room temperature and in a fridge.
4. **Door sensor** — reed switch on GPIO27; confirm clean transitions after debouncing.
5. **OLED** — confirm I2C addresses with no collision; render the five-screen rotation.
6. **Actuators** — buzzer, LED, and relay verified individually; fan through the relay contacts.
7. **Connectivity** — SIM7600 registers on 4G, sends a test SMS, returns a GPS fix and readable UTC.
8. **Integration** — full service with all three rules, hash chaining and uplink, installed as a systemd service with a watchdog.
9. **Simulated trip** — trigger each rule in turn, open the door, cut power mid-trip; confirm every output responds and the chain verifies end to end.
10. **Housing** — mount in an enclosure, route leads through cable glands, re-run stage 9 in the final housing.

### Test cases

| ID | Description | Expected output |
|---|---|---|
| TC-01 | Normal operation, both probes in range | No alert; record logged; HOME screen rotating |
| TC-02 | Threshold breach — Probe A warmed above range | Buzzer, LED, relay restart, OLED alert, SMS, chained record, all together |
| TC-03 | Rate breach — 1.5 °C in 4 minutes, still in range | Same full response; flag identifies the rate rule |
| TC-04 | Differential breach — probes separated 10 minutes | WARNING state; `SENSOR_DISAGREE` logged and displayed |
| TC-05 | Probe B unplugged mid-trip | `PROBE_FAULT`; DEGRADED state; single-probe fallback; later records marked |
| TC-06 | Forced +85 °C power-on artefact | Value discarded, not logged as an excursion; retry next cycle |
| TC-07 | Door opened away from a planned stop | Event logged with GPS; SMS sent |
| TC-08 | Door held open beyond 180 seconds | Escalation to WARNING; buzzer sounds |
| TC-09 | Alert raised with no 4G signal | Stored and queued; sent on reconnection with original timestamp |
| TC-10 | Mains cut without warning | `POWER_LOSS` written before shutdown; `POWER_RESTORE` on reboot; chain unbroken |
| TC-11 | GPS fix lost mid-trip | Time source falls back to NET or SYS; `TIME_SYNC` logged on correction |
| TC-12 | One stored temperature value edited directly | Verifier names the exact record where the chain breaks; OLED code no longer matches cloud |

## 11. Results and Output

**On the unit.** The OLED cycles quietly through status screens and latches to ALERT on a fault, stating the reason, the current value, the safe limit, and the action already taken.

**SMS alert.**

```
ALERT: Vehicle GJ-01-EF-9012
RATE: Probe A rising 1.4C/5min (now 7.4C, limit 8.0C)
Probe B 7.9C | Door CLOSED
Cooling relay restart attempted 11:24
Loc: maps.google.com/?q=23.0225,72.5714
```

**Fleet dashboard.** Vehicle list with status markers, live plot of both probes with the safe band shaded, a ΔT trace beneath it as the compressor-health indicator, live map, and running event log.

**Trip certificate.** Trip and vehicle ID; start and end time and location from GPS; min/max for each probe; maximum ΔT observed; door-open events with count, duration and position; every excursion with start and end time; sensor-integrity result; power continuity; and the chain verification result with the head hash and a verification QR code.

**For the live demonstration:** hold warm water near Probe A for the threshold alert, or warm it slowly by hand for the rate rule; **separate the two probes** for the differential rule — the most convincing moment, because the OLED explains the diagnosis as it happens; unplug Probe B to show graceful degradation; pull the power to show the clean shutdown and bracketed gap; finish by editing one stored value and running the verifier, which names the exact broken record.

## 12. Cost Analysis

| Component | Qty | Total (₹) |
|---|---|---|
| Raspberry Pi 4 Model B, 4 GB | 1 | 6,500 |
| SIM7600 4G/GPS HAT | 1 | 5,500 |
| UPS HAT / power bank | 1 | 1,200 |
| 32 GB high-endurance microSD | 1 | 700 |
| 5 V 3 A USB-C supply | 1 | 600 |
| DS18B20 waterproof probe | 2 | 500 |
| GPIO terminal breakout | 1 | 350 |
| 0.96" I2C OLED display | 1 | 250 |
| 5 V DC fan | 1 | 150 |
| MC-38 reed switch | 1 | 120 |
| Jumper wires | ~25 | 120 |
| Relay module, buzzer, LED, resistors | — | 160 |
| **Hardware total** | | **≈ 16,150** |

Prices are indicative Indian retail figures for 2026. Recurring: SIM data and SMS ₹150–300/month; cloud hosting beyond the prototype ≈ ₹1,500/month shared across a fleet.

Worth buying if budget allows: IP65 enclosure and cable glands (₹650, required before any vehicle mounting), DS3231 RTC (₹150, if the backup unit has none), accelerometer for shock detection (₹200), humidity sensor (₹350). About ₹1,400 for all four.

This build costs roughly 2.7× an equivalent ESP32 design (≈ ₹6,050). The premium buys Python development, a combined 4G/GPS HAT instead of two modules, easy OLED and SQLite support, and headroom for later analytics — the right trade for a prototype that must be built, debugged and demonstrated in one semester, though ESP32 remains the correct choice for fleet production.

## 13. Advantages and Limitations

**Advantages**

- The core safety function works with no internet at all — buzzer, LED, relay and OLED respond in the same control cycle.
- Two probes **diagnose** rather than merely detect, and let the system catch its own sensor failures.
- The rate-of-change rule catches slow compressor failures before a threshold is crossed, and recovery is attempted automatically rather than only notified.
- The driver is informed, not merely alarmed — supporting a correct decision rather than a panicked one.
- Records are tamper-evident and verifiable in the field from the display alone, with timestamps anchored to GPS.
- Outages are bracketed by records, so a gap is accounted for rather than a blind spot.

**Limitations**

- Single point of failure — one Pi, one sensor set; a production unit on a critical route needs redundancy.
- Higher cost and continuous power draw than a microcontroller equivalent, which matters for a vehicle parked with the engine off, and peak-current headroom is thin on the 3 A supply (Section 9).
- Bench-mounted until an enclosure is fitted; not yet vehicle-ready.
- The chain proves the log was not edited but does not bind it to a device identity; key-based signing is the next step. Transport encryption (MQTT over TLS) is specified but not implemented.
- Humidity, shock and fuel level are not measured, so the certificate covers temperature and door integrity only.
- Two probes detect disagreement but cannot always identify which probe is at fault; three would allow majority voting.

## 14. Future Scope

Three-probe majority voting to identify *which* sensor failed; device-key signing to bind records to a specific unit; humidity and shock sensing for full cargo-condition coverage; fuel-level sensing on the reefer's diesel tank to catch siphoning before it becomes a cooling failure; a solenoid door lock on a second relay channel; predictive maintenance from compressor cycling and ΔT trends; a multi-vehicle dashboard with role-based access for drivers, managers and auditors; PMKSY and FSSAI reporting integration so certificates need no manual reformatting; and migration to an ESP32 production variant keeping the identical data model and chain format.

## 15. Conclusion

This project demonstrates that a reliable, tamper-evident cold-chain monitoring system can be built from widely available components, using a Raspberry Pi to trade higher cost and power draw for simpler development and easier debugging. A second temperature probe and a ₹250 display — together about 3% of the build cost — take the system from detection to diagnosis, let it detect its own sensor failures, and put a field-verifiable integrity check in front of the one person who can act on it.

By combining explainable rules with local actuation, driver-facing feedback and remote alerting, the prototype closes the four gaps common to existing systems: it acts without depending on connectivity, it attempts recovery rather than only notifying, it validates its own sensors instead of trusting them blindly, and it produces a record trustworthy enough to serve as evidence. The components, wiring, build sequence and test plan given here are sufficient to reproduce the prototype and extend it toward a field-ready product.

## 16. References

1. "An IoT Smart System for Cold Supply Chain Storage and Transportation Management," Engineering, Technology & Applied Science Research. https://www.etasr.com/index.php/ETASR/article/view/6857
2. C. K. M. Lee, Y. Lv, K. K. H. Ng, W. Ho, K. L. Choy, "Design and application of Internet of things-based warehouse management system for smart logistics," International Journal of Production Research, vol. 56, no. 8, pp. 2753–2768, 2018.
3. M. Humayun, N. Jhanjhi, B. Hamid, G. Ahmed, "Emerging Smart Logistics and Transportation Using IoT and Blockchain," IEEE Internet of Things Magazine, vol. 3, no. 2, pp. 58–62, 2020.
4. "Internet of Things enabled real time cold chain monitoring in a container port," Journal of Shipping and Trade, Springer Nature. https://link.springer.com/article/10.1186/s41072-022-00110-z
5. Ministry of Food Processing Industries, Government of India, "Revised Guidelines for the Integrated Cold Chain and Value Addition Infrastructure Scheme (PMKSY)," 22 May 2025.
6. Analog Devices / Maxim Integrated, "DS18B20 Programmable Resolution 1-Wire Digital Thermometer" (datasheet).
7. Solomon Systech, "SSD1306 — 128 × 64 OLED Driver with Controller" and SIMCom, "SIM7600 Series AT Command Manual" (datasheets).

Prepared by Group 4 — Sky is the Limit · ECE-504 Internet of Things · Monsoon Semester 2026
