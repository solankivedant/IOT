# Experiment Set 1 — Step-by-Step Lab Guide (Arduino UNO)

Submission due: 21/08/2026. Every experiment lists wiring as a list of **direct
component-to-component connections** (e.g. "LED anode — one end of the resistor"). Build each
connection in order. Physically, component legs and jumper wires all plug into the
breadboard's shared strips — any two ends listed as connected just need to end up sharing a
breadboard row (or a power rail) to be electrically joined; exactly which row/column you pick
doesn't matter. Nothing is skipped or referred back to "same as before" — each experiment can
be built from a completely empty breadboard using only its own table.

> This guide tells you **how to build and run** each experiment. The graded report
> questions from the PDF are listed at the end of each experiment as a checklist — answer
> those yourself (they need your own explanation, video, and calculations).

---

## 1. Components Used (from `images/`)

| Component | Photo | Pins / Legs |
|---|---|---|
| Arduino UNO | `images/arduino-uno.jpeg` | Left header: **5V, RESET, 3.3V, 5V, GND, GND, VIN**. Bottom header: **A0–A5**. Right headers: **SCL, SDA, AREF, GND, 13, 12, 11~, 10~, 9~, 8** and **7, 6~, 5~, 4, 3~, 2, TX→1, RX←0**. `~` = PWM-capable pin. Onboard LED labelled **"L"** sits next to pin 13. |
| Breadboard | `images/breadboard.jpeg` | Top/bottom rails: **red `+`**, **blue `−`** (full length). Center terminal strips: rows **A–E** and **F–J**, columns **1–60**. Every column A–E is one electrical node (same for F–J); A–E is NOT connected to F–J (center gap). |
| LED | `images/led-light.jpeg` | **Long leg = anode (+)**, **short leg = cathode (−)**. |
| Resistor | `images/resistor.jpeg` | 2 legs, no polarity. |
| Push button switch | `images/switch.jpeg` | 4 legs: the 2 legs on the same side of the switch body are always internally connected to each other; the 2 sides connect to each other only while pressed. |
| Jumper wires | `images/wire.jpeg` | Male–male wires for every connection below. |
| USB cable | `images/arduino-connector.jpeg` | USB-B end → Arduino, USB-A end → PC. |
| Potentiometer | `images/potentiometer.jpeg` | 3 legs (2 outer + 1 wiper). Not used in Experiments 1–10. |
| LDR module | `images/light-intensity-control-senor.jpeg` | Labelled **DO, GND, VCC**. Not used in Experiments 1–10. |
| Bench power supply | `images/power-supply.jpeg` | Not needed — UNO is powered by USB. |

---

## 2. One-Time Software Setup

| Step | From | To |
|---|---|---|
| 1 | Arduino UNO USB port | USB cable (USB-B end) |
| 2 | USB cable (USB-A end) | PC USB port |
| 3 | IDE menu **Tools → Board** | Select **Arduino AVR Boards → Arduino Uno** |
| 4 | IDE menu **Tools → Port** | Select **COM3 (Arduino UNO)** *(use whichever COM number appears)* |

(Install the Arduino IDE first, from **https://www.arduino.cc/**, if not already installed.)

---

## 3. Breadboard Layout Key (used by every experiment below)

- Every "connection" below is really: plug both ends into the breadboard so they land in the **same row** (or the same power rail) — that's what makes them electrically joined. Use a jumper wire wherever the two ends can't physically reach the same row on their own.
- **Power rails**: red strip = `+`, blue strip = `−`.
- Give each component its own free row/column so nothing touches by accident.

---

## 4. Experiment-by-Experiment Wiring

### Experiment 1 — Blink (Pin 13)

| # | Connection |
|---|---|
| 1 | Power the Arduino UNO from the PC using the USB cable |
| 2 | LED anode (long leg) — one end of the resistor |
| 3 | Resistor — other end to Arduino Digital Pin 13 |
| 4 | LED cathode (short leg) — Arduino GND |

Note: the LED and resistor are wired in series — anode side goes to Pin 13 (through the resistor), cathode side goes to GND. Also watch the onboard LED labelled **"L"** next to pin 13 on the Arduino board — it blinks in sync with the external LED, no separate wiring needed for it.

**Resistor value (Q1.c):** `R_min = (5V − 2V) / 0.02A ≈ 150 Ω` → use 220 Ω or 330 Ω.

**Code — sketch name `Experiment_1`:**
```cpp
void setup() {
  pinMode(13, OUTPUT);
}
void loop() {
  digitalWrite(13, HIGH);
  delay(1000);
  digitalWrite(13, LOW);
  delay(1000);
}
```

**Report checklist:** 1.a (video), 1.b (setup/loop/pinMode/digitalWrite/delay), 1.c (resistor calc, done above), 1.d–1.o (UNO datasheet lookups + Mega/Nano comparison).

---

### Experiment 2 — 40% Duty Cycle (Pin 13)

| # | Connection |
|---|---|
| 1 | Power the Arduino UNO from the PC using the USB cable |
| 2 | LED anode (long leg) — one end of the resistor |
| 3 | Resistor — other end to Arduino Digital Pin 13 |
| 4 | LED cathode (short leg) — Arduino GND |

(Hardware is identical to Experiment 1 — only the code timing changes below.)

**Code:**
```cpp
void setup() {
  pinMode(13, OUTPUT);
}
void loop() {
  digitalWrite(13, HIGH);
  delay(400);   // ON 40% of 1000 ms
  digitalWrite(13, LOW);
  delay(600);   // OFF 60% of 1000 ms
}
```

**Report checklist:** 2.a (video), 2.b (paste code), 2.c (describe delay change), 2.d (400/1000 = 40% calc).

---

### Experiment 3 — Two LEDs, Complementary Duty Cycles (Pin 13, code unchanged from Exp 2)

| # | Connection |
|---|---|
| 1 | Power the Arduino UNO from the PC using the USB cable |
| 2 | LED 1 anode (long leg) — one end of Resistor 1 |
| 3 | Resistor 1 — other end to Arduino Digital Pin 13 |
| 4 | LED 1 cathode (short leg) — Arduino GND |
| 5 | LED 2 anode (long leg) — one end of Resistor 2 |
| 6 | Resistor 2 — other end to Arduino 5V |
| 7 | LED 2 cathode (short leg) — same node as Resistor 1 / Pin 13 (LED 1's anode side) |

Note: step 7 ties LED 2's cathode to LED 1's Pin-13 node, so both circuits are driven by the single wire from Pin 13 (step 3) — no second wire is plugged into the Arduino pin itself.

Circuit behavior: LED 1 conducts (Pin 13 → GND path) when Pin 13 = HIGH → ON 40% / OFF 60%. LED 2 conducts (5V rail → Pin 13 sinking) only when Pin 13 = LOW → ON 60% / OFF 40%.

**Code:** identical to Experiment 2 (re-upload it, or leave it running — no code changes).

**Report checklist:** 3.a (video), 3.b (explain LED 2 was flipped and tied to the 5V rail so it lights on the LOW phase instead of the HIGH phase).

---

### Experiment 4 — Fade (Pin 9, PWM)

| # | Connection |
|---|---|
| 1 | Power the Arduino UNO from the PC using the USB cable |
| 2 | LED anode (long leg) — one end of the resistor |
| 3 | Resistor — other end to Arduino Digital Pin 9 *(marked `9~` on the board)* |
| 4 | LED cathode (short leg) — Arduino GND |

**Code — sketch name `Experiment_4`:**
```cpp
int led = 9;
int brightness = 0;
int fadeAmount = 5;

void setup() {
  pinMode(led, OUTPUT);
}
void loop() {
  analogWrite(led, brightness);
  brightness = brightness + fadeAmount;
  if (brightness <= 0 || brightness >= 255) {
    fadeAmount = -fadeAmount;
  }
  delay(30);
}
```

**Report checklist:** 4.a (video), 4.b (analogWrite), 4.c (explain the boundary-reversal `if`), 4.d (PWM pins are 3, 5, 6, 9, 10, 11 — the `~` marked pins, tied to hardware timers).

---

### Experiment 5 — Blink (Pin 13) + Fade (Pin 9) Simultaneously

| # | Connection |
|---|---|
| 1 | Power the Arduino UNO from the PC using the USB cable |
| 2 | LED A anode (long leg) — one end of Resistor A |
| 3 | Resistor A — other end to Arduino Digital Pin 13 |
| 4 | LED A cathode (short leg) — Arduino GND |
| 5 | LED B anode (long leg) — one end of Resistor B |
| 6 | Resistor B — other end to Arduino Digital Pin 9 |
| 7 | LED B cathode (short leg) — Arduino GND |

**Code:**
```cpp
int led9 = 9, brightness = 0, fadeAmount = 5;
int led13 = 13;
unsigned long previousMillis = 0;
bool led13State = LOW;

void setup() {
  pinMode(led9, OUTPUT);
  pinMode(led13, OUTPUT);
}
void loop() {
  analogWrite(led9, brightness);
  brightness += fadeAmount;
  if (brightness <= 0 || brightness >= 255) fadeAmount = -fadeAmount;

  if (millis() - previousMillis >= 1000) {
    previousMillis = millis();
    led13State = !led13State;
    digitalWrite(led13, led13State);
  }
  delay(30);
}
```

**Report checklist:** 5.a (video), 5.b (paste code), 5.c (added LED B branch on pin 9; pin 13 timing moved from `delay()` to `millis()` so it doesn't block the fade).

---

### Experiment 6 — Blink 4 LEDs Together (Pins 13, 11, 9, 7)

| # | Connection |
|---|---|
| 1 | Power the Arduino UNO from the PC using the USB cable |
| 2 | LED 1 anode (long leg) — one end of Resistor 1 |
| 3 | Resistor 1 — other end to Arduino Digital Pin 13 |
| 4 | LED 1 cathode (short leg) — Arduino GND |
| 5 | LED 2 anode (long leg) — one end of Resistor 2 |
| 6 | Resistor 2 — other end to Arduino Digital Pin 11 |
| 7 | LED 2 cathode (short leg) — Arduino GND |
| 8 | LED 3 anode (long leg) — one end of Resistor 3 |
| 9 | Resistor 3 — other end to Arduino Digital Pin 9 |
| 10 | LED 3 cathode (short leg) — Arduino GND |
| 11 | LED 4 anode (long leg) — one end of Resistor 4 |
| 12 | Resistor 4 — other end to Arduino Digital Pin 7 |
| 13 | LED 4 cathode (short leg) — Arduino GND |

**Code:**
```cpp
int pins[] = {13, 11, 9, 7};

void setup() {
  for (int i = 0; i < 4; i++) pinMode(pins[i], OUTPUT);
}
void loop() {
  for (int i = 0; i < 4; i++) digitalWrite(pins[i], HIGH);
  delay(1000);
  for (int i = 0; i < 4; i++) digitalWrite(pins[i], LOW);
  delay(1000);
}
```

**Report checklist:** 6.a (video), 6.b (paste code), 6.c (describe 4-LED wiring and array-based code).

---

### Experiment 7 — Sequential ON, Then All OFF (Pins 13, 11, 9, 7)

| # | Connection |
|---|---|
| 1 | Power the Arduino UNO from the PC using the USB cable |
| 2 | LED 1 anode (long leg) — one end of Resistor 1 |
| 3 | Resistor 1 — other end to Arduino Digital Pin 13 |
| 4 | LED 1 cathode (short leg) — Arduino GND |
| 5 | LED 2 anode (long leg) — one end of Resistor 2 |
| 6 | Resistor 2 — other end to Arduino Digital Pin 11 |
| 7 | LED 2 cathode (short leg) — Arduino GND |
| 8 | LED 3 anode (long leg) — one end of Resistor 3 |
| 9 | Resistor 3 — other end to Arduino Digital Pin 9 |
| 10 | LED 3 cathode (short leg) — Arduino GND |
| 11 | LED 4 anode (long leg) — one end of Resistor 4 |
| 12 | Resistor 4 — other end to Arduino Digital Pin 7 |
| 13 | LED 4 cathode (short leg) — Arduino GND |

(Hardware identical to Experiment 6 — only the code sequencing changes below.)

**Code:**
```cpp
int pins[] = {13, 11, 9, 7};

void setup() {
  for (int i = 0; i < 4; i++) pinMode(pins[i], OUTPUT);
}
void loop() {
  for (int i = 0; i < 4; i++) {
    digitalWrite(pins[i], HIGH);
    delay(2000);
  }
  for (int i = 0; i < 4; i++) digitalWrite(pins[i], LOW);
  delay(2000);
}
```

**Report checklist:** 7.a (video), 7.b (paste code), 7.c (describe: same wiring as Exp 6, code now staggers the ON sequence 2 s apart, then clears all four together).

---

### Experiment 8 — Rotating Single LED (Pins 13, 11, 9, 7)

| # | Connection |
|---|---|
| 1 | Power the Arduino UNO from the PC using the USB cable |
| 2 | LED 1 anode (long leg) — one end of Resistor 1 |
| 3 | Resistor 1 — other end to Arduino Digital Pin 13 |
| 4 | LED 1 cathode (short leg) — Arduino GND |
| 5 | LED 2 anode (long leg) — one end of Resistor 2 |
| 6 | Resistor 2 — other end to Arduino Digital Pin 11 |
| 7 | LED 2 cathode (short leg) — Arduino GND |
| 8 | LED 3 anode (long leg) — one end of Resistor 3 |
| 9 | Resistor 3 — other end to Arduino Digital Pin 9 |
| 10 | LED 3 cathode (short leg) — Arduino GND |
| 11 | LED 4 anode (long leg) — one end of Resistor 4 |
| 12 | Resistor 4 — other end to Arduino Digital Pin 7 |
| 13 | LED 4 cathode (short leg) — Arduino GND |

(Hardware identical to Experiments 6 & 7 — only the code changes below.)

**Code:**
```cpp
int pins[] = {13, 11, 9, 7};

void setup() {
  for (int i = 0; i < 4; i++) pinMode(pins[i], OUTPUT);
}
void loop() {
  for (int i = 0; i < 4; i++) {
    digitalWrite(pins[i], HIGH);
    delay(2000);
    digitalWrite(pins[i], LOW);
  }
}
```

**Report checklist:** 8.a (video), 8.b (paste code), 8.c (describe changes vs Exp 7), 8.d–8.f (LED datasheet: Green material combo, Red peak forward current, Blue peak wavelength), 8.g (why different materials give different LED colors — bandgap energy vs photon wavelength, with diagram), 8.h (define Luminosity + SI unit: lumen).

---

### Experiment 9 — Push Button Controls LED (Pin 13 LED, Pin 2 button)

| # | Connection |
|---|---|
| 1 | Power the Arduino UNO from the PC using the USB cable |
| 2 | LED anode (long leg) — one end of the resistor |
| 3 | Resistor — other end to Arduino Digital Pin 13 |
| 4 | LED cathode (short leg) — Arduino GND |
| 5 | Switch's Side A legs (its two same-side legs, internally joined) — Arduino 5V |
| 6 | Switch's Side B legs (its two same-side legs, internally joined) — Arduino Digital Pin 2 |
| 7 | Same Side B node — one end of the pull-down resistor |
| 8 | Pull-down resistor — other end to Arduino GND |

Notes: a 4-leg push button has two internally-joined leg pairs — "Side A" and "Side B" — and pressing the button bridges Side A to Side B (see the switch entry in the components table). Side A is tied to 5V; Side B is tied to Pin 2 *and* pulled down to GND through the resistor. So Pin 2 reads LOW until pressed, and HIGH only while pressed (5V flows in through Side A). **Confirm this pull-down circuit with your instructor before wiring, per the slide.**

Logic: button **not pressed** → Pin 2 pulled to GND through the resistor → reads **LOW**. Button **pressed** → Side A (5V) connects to Side B → Pin 2 reads **HIGH**.

**Code — sketch name `Experiment_9`:**
```cpp
const int buttonPin = 2;
const int ledPin = 13;
int buttonState = 0;

void setup() {
  pinMode(ledPin, OUTPUT);
  pinMode(buttonPin, INPUT);
}
void loop() {
  buttonState = digitalRead(buttonPin);
  if (buttonState == HIGH) {
    digitalWrite(ledPin, HIGH);
  } else {
    digitalWrite(ledPin, LOW);
  }
}
```
Note: with this exact code and pull-down wiring, the LED is ON **while pressed**. If the target behavior is "LED OFF while pressed" as worded on the slide, swap the two branches (see Experiment 10) or rewire as a pull-up instead.

**Report checklist:** 9.a (video), 9.b (digitalRead), 9.c (draw the button circuit; explain how it produces logic HIGH/LOW).

---

### Experiment 10 — Push Button Turns LED Off, Otherwise ON

| # | Connection |
|---|---|
| 1 | Power the Arduino UNO from the PC using the USB cable |
| 2 | LED anode (long leg) — one end of the resistor |
| 3 | Resistor — other end to Arduino Digital Pin 13 |
| 4 | LED cathode (short leg) — Arduino GND |
| 5 | Switch's Side A legs (its two same-side legs, internally joined) — Arduino 5V |
| 6 | Switch's Side B legs (its two same-side legs, internally joined) — Arduino Digital Pin 2 |
| 7 | Same Side B node — one end of the pull-down resistor |
| 8 | Pull-down resistor — other end to Arduino GND |

(Hardware identical to Experiment 9 — only the code branches are swapped below.)

**Code:**
```cpp
const int buttonPin = 2;
const int ledPin = 13;
int buttonState = 0;

void setup() {
  pinMode(ledPin, OUTPUT);
  pinMode(buttonPin, INPUT);
}
void loop() {
  buttonState = digitalRead(buttonPin);
  if (buttonState == HIGH) {
    digitalWrite(ledPin, LOW);   // pressed -> LED off
  } else {
    digitalWrite(ledPin, HIGH);  // not pressed -> LED on
  }
}
```

**Report checklist:** 10.a (video), 10.b (paste code), 10.c (describe: wiring unchanged from Exp 9, only the HIGH/LOW branches were swapped).

---

## 5. Quick Pin-Use Summary

| Experiment | Digital pin(s) used | Extra hardware beyond LED+resistor |
|---|---|---|
| 1 | 13 | — |
| 2 | 13 | — |
| 3 | 13 (both LEDs, one reversed) | 2nd LED wired reverse-polarity to 5V rail |
| 4 | 9 (PWM) | — |
| 5 | 13 + 9 | — |
| 6 | 13, 11, 9, 7 | — |
| 7 | 13, 11, 9, 7 | — |
| 8 | 13, 11, 9, 7 | — |
| 9 | 13 (LED) + 2 (button) | Push button + pull-down resistor |
| 10 | 13 (LED) + 2 (button) | Same as Experiment 9 |
