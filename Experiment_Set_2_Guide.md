# Experiment Set 2 — Step-by-Step Lab Guide (Arduino UNO)

Submission due: 18/09/2026. This set moves from LEDs-only circuits into **measurement**
(multimeter), **analog sensing** (potentiometer, LDR) and **networking** (Ethernet Shield).
Wiring is still given as **direct component-to-component connections** — build each
connection in order, landing both ends of a "connection" in the same breadboard row (or a
power rail) to join them electrically. Nothing is skipped or referred back to "same as
before" beyond what's explicitly noted; each experiment can be built starting from the
previous one's hardware exactly as stated.

> This guide tells you **how to build and run** each experiment. The graded report
> questions from the PDF are listed at the end of each experiment as a checklist — answer
> those yourself (they need your own explanation, photos/video, and calculations).
>
> **Experiments 18–20 (Ethernet Shield) reference sketches named `Experiment_18` /
> `Experiment_19` / `Experiment_20`** that are supplied separately by the instructor (not
> printed in the slide deck — only their *behavior* and the questions about them are). The
> code shown for those three below is a standard, working Arduino Ethernet implementation
> that matches the described behavior and the PDF's own questions (11.b.1–4, library used,
> mac/IP setup, analog pins on a web page, ThingSpeak upload) — swap in the instructor's
> exact file if it differs, but the wiring and concepts are the same either way.

---

## 1. Components Used

Same physical kit as Experiment Set 1 (`component-images/`), plus three items that were
listed but unused in Set 1 and are now active, plus one new item:

| Component | Photo | Pins / Legs |
|---|---|---|
| Arduino UNO | `component-images/arduino-uno.jpeg` | Left header: **5V, RESET, 3.3V, 5V, GND, GND, VIN**. Bottom header: **A0–A5**. Right headers: **SCL, SDA, AREF, GND, 13, 12, 11~, 10~, 9~, 8** and **7, 6~, 5~, 4, 3~, 2, TX→1, RX←0**. `~` = PWM-capable pin. |
| Breadboard | `component-images/breadboard.jpeg` | Top/bottom rails: **red `+`**, **blue `−`**. Center strips: rows **A–E** / **F–J**, columns **1–60**; A–E not joined to F–J. |
| LED | `component-images/led-light.jpeg` | **Long leg = anode (+)**, **short leg = cathode (−)**. |
| Resistor | `component-images/resistor.jpeg` | 2 legs, no polarity. |
| Jumper wires | `component-images/wire.jpeg` | Male–male, for every connection below. |
| USB cable | `component-images/arduino-connector.jpeg` | USB-B end → Arduino, USB-A end → PC. |
| **Potentiometer** | `component-images/potentiometer.jpeg` | 3 legs: **two outer legs** are the fixed ends of the resistive track (connect across 5V/GND to form a divider), **middle leg = wiper** (variable voltage output — read this one). |
| **LDR module / bare LDR** | `component-images/light-intensity-control-senor.jpeg` | 2 legs, no polarity — a light-dependent resistor: resistance **drops** as light **increases**. |
| **Digital multimeter** | *(not in image set — any bench/handheld DMM)* | Set to the **Ω (resistance)** range for Experiments 11–13's resistor/LDR checks, and to **DC Voltage (V⎓)** range for the voltage measurements in Experiments 12–13. Red probe = `+`, black probe = `COM/−`. |
| **Ethernet Shield (W5100-based)** | *(not in image set)* | Stacks directly on top of the Arduino UNO — its header pins plug straight into the UNO's headers, pin-for-pin. Internally uses **pins 10, 11, 12, 13** (SPI: SS/MOSI/MISO/SCK) to talk to the W5100 chip — those four pins are reserved and unavailable for LEDs while the shield is mounted. Has an **RJ45 Ethernet port** — connect it to your router/PC with a network cable for Experiments 18–20. |

---

## 2. One-Time Software Setup

| Step | From | To |
|---|---|---|
| 1 | Arduino UNO USB port | USB cable (USB-B end) |
| 2 | USB cable (USB-A end) | PC USB port |
| 3 | IDE menu **Tools → Board** | Select **Arduino AVR Boards → Arduino Uno** |
| 4 | IDE menu **Tools → Port** | Select **COM3 (Arduino UNO)** *(use whichever COM number appears)* |
| 5 (Exp 18–20 only) | IDE menu **Sketch → Include Library → Manage Libraries** | Confirm **Ethernet** library is installed (bundled with the IDE by default) |
| 6 (Exp 18–20 only) | Ethernet Shield | Push firmly onto the UNO's headers so every pin row is seated, *then* plug in an Ethernet cable from the shield's RJ45 port to your router |
| 7 (Exp 20 only) | Browser | Create a free account at **thingspeak.com** (see Q20.d) before running Experiment 20 |

(Install the Arduino IDE first, from **https://www.arduino.cc/**, if not already installed.)

---

## 3. Breadboard / Measurement Layout Key

- Every "connection" below is: plug both ends into the breadboard so they land in the
  **same row** (or the same power rail) — that's what makes them electrically joined.
- **Power rails**: red strip = `+`, blue strip = `−`.
- For Experiments 11–13, the **Arduino only supplies 5V and GND** — it is not running any
  sketch, so any USB connection (PC or a phone charger) that powers the board is enough.
- When measuring **voltage** with the multimeter, probe *across* the two nodes you're
  measuring between — do not break the circuit to insert the meter. When measuring
  **resistance**, the component must be *isolated* from the powered circuit (multimeter
  pushes its own tiny test current through it).

---

## 4. Experiment-by-Experiment Build

### Experiment 11 — Review of Components (Multimeter)

No Arduino sketch — the board (powered over USB) is only used as a convenient 5V/GND source
for Task 11.c; Tasks 11.a and 11.b use the multimeter standalone.

| # | Step |
|---|---|
| 1 | Set the multimeter dial to the **Ω (resistance)** range |
| 2 | **Task 11.a:** touch one probe to each leg of a resistor (off the breadboard, not powered) and read the value; repeat for **at least 3 different resistors** |
| 3 | **Task 11.b:** place the potentiometer's two outer legs across the meter probes *(or just probe outer-leg-to-wiper)* and read resistance; turn the knob to **3 different positions**, recording the value at each |
| 4 | **Task 11.c:** probe across the LDR's two legs; take a reading, then change the light falling on it (cover it with your hand, shine a phone torch on it, etc.) and take **at least 5 readings** across a range of light levels |

**Report checklist:** 11.a (3 photos, resistor readings), 11.b (3 photos, pot readings at 3 settings), 11.c (5 photos + a graph of Light Intensity vs. LDR resistance + explanation of *why* resistance drops as light rises — photoconductivity: more incident photons free more charge carriers in the semiconductor), 11.d–11.h (from the LDR datasheet: material, power dissipation at 30 °C, operating temperature range, minimum dark resistance, peak spectral-response wavelength).

---

### Experiment 12 — Building a Potential Divider Circuit

| # | Connection |
|---|---|
| 1 | Power the Arduino UNO from the PC using the USB cable *(sketch not required — just used as a 5V/GND source)* |
| 2 | Resistor 1 — one end to Arduino **5V** |
| 3 | Resistor 1 other end — Resistor 2 one end (same breadboard row) |
| 4 | Resistor 2 other end — Resistor 3 one end |
| 5 | Resistor 3 other end — Resistor 4 one end |
| 6 | Resistor 4 other end — Resistor 5 one end |
| 7 | Resistor 5 other end — Arduino **GND** |

This gives you 5 resistors in one series chain from 5V down to GND, with **4 accessible
junction nodes** between them (call them N1 after R1, N2 after R2, N3 after R3, N4 after R4).

**Task 12.b — measuring:** set the multimeter to **DC Voltage**, put the black probe on
GND, and touch the red probe to each junction node in turn (and across individual resistors,
node-to-node) to read several different combinations, e.g. `V(5V→N1)` across R1 alone,
`V(N1→GND)` across R2+R3+R4+R5 together, etc.

**Report checklist:** 12.a (1 photo of the wired chain), 12.b (3 photos of voltage measurements across 3 different resistor combinations, each clearly showing the reading), 12.c (write the voltage-divider equation for one resistor in a 5-resistor series chain: `V_Rn = V_total × (R_n / (R1+R2+R3+R4+R5))`).

---

### Experiment 13 — LDR in a Potential Divider

| # | Connection |
|---|---|
| 1 | Power the Arduino UNO from the PC using the USB cable |
| 2 | LDR leg 1 — Arduino **5V** |
| 3 | LDR leg 2 — one end of the resistor (same row = this is your measurement node) |
| 4 | Resistor other end — Arduino **GND** |

**Task 13.b — measuring:** multimeter on **DC Voltage**, black probe on GND, red probe on
the LDR–resistor junction node. Take a reading, then vary the light on the LDR (shade it /
torch it) and take readings at **3 different light intensities**.

**Report checklist:** 13.a (1 photo of the wiring), 13.b (3 photos of voltage readings at 3 light levels), 13.c (write the divider equation for the node voltage: `V_node = V_supply × R / (R_LDR + R)` — note this is voltage across the *fixed resistor*; swap the ratio if you measured across the LDR instead).

---

### Experiment 14 — Blink Rate Follows Potentiometer Position

| # | Connection |
|---|---|
| 1 | Power the Arduino UNO from the PC using the USB cable |
| 2 | LED anode (long leg) — one end of the resistor |
| 3 | Resistor — other end to Arduino Digital Pin **13** |
| 4 | LED cathode (short leg) — Arduino **GND** |
| 5 | Potentiometer outer leg A — Arduino **5V** |
| 6 | Potentiometer outer leg B — Arduino **GND** |
| 7 | Potentiometer wiper (middle leg) — Arduino **A0** |

**Code — sketch name `Experiment_14`** (from the slide deck, verbatim):
```cpp
int sensorPin = A0;   // select the input pin for the potentiometer
int ledPin = 13;      // select the pin for the LED
int sensorValue = 0;  // variable to store the value coming from the sensor

void setup() {
  pinMode(ledPin, OUTPUT);
}
void loop() {
  sensorValue = analogRead(sensorPin);
  digitalWrite(ledPin, HIGH);
  delay(sensorValue);   // 0–1023 ms, so blink rate slows as sensorValue rises
  digitalWrite(ledPin, LOW);
  delay(sensorValue);
}
```

**Report checklist:** 14.a (video with voice-over showing the LED's blink rate changing as you turn the pot), 14.b (explain `analogRead`: 10-bit ADC, returns 0–1023 for 0–5V), 14.c (draw the potentiometer's internal resistive-track + wiper diagram and explain how sliding the wiper changes the divider ratio), 14.d (ATmega328P 28-pin DIP diagram: mark A0–A5, all digital I/O pins, and all PWM `~` pins against their physical DIP pin numbers), 14.e (analog input is enabled by the chip's internal **ADC / analog-to-digital converter** multiplexed across A0–A5), 14.f (PWM pins are driven by the chip's **Timer0/Timer1/Timer2** hardware timers in fast-PWM/phase-correct mode, toggling the pin automatically without CPU intervention each cycle).

---

### Experiment 15 — LED Intensity Follows Potentiometer Position

(Hardware from Experiment 14, with **one change**: the LED must move to a PWM pin since
`analogWrite` needs one — pin 13 isn't PWM-capable.)

| # | Connection |
|---|---|
| 1 | Power the Arduino UNO from the PC using the USB cable |
| 2 | LED anode (long leg) — one end of the resistor |
| 3 | Resistor — other end to Arduino Digital Pin **9** *(marked `9~`, PWM)* |
| 4 | LED cathode (short leg) — Arduino **GND** |
| 5 | Potentiometer outer leg A — Arduino **5V** |
| 6 | Potentiometer outer leg B — Arduino **GND** |
| 7 | Potentiometer wiper (middle leg) — Arduino **A0** |

**Code:**
```cpp
int sensorPin = A0;
int ledPin = 9;         // moved to a PWM-capable pin
int sensorValue = 0;
int brightness = 0;

void setup() {
  pinMode(ledPin, OUTPUT);
}
void loop() {
  sensorValue = analogRead(sensorPin);           // 0–1023
  brightness = map(sensorValue, 0, 1023, 0, 255); // scale to analogWrite's 8-bit range
  analogWrite(ledPin, brightness);
}
```

**Report checklist:** 15.a (video with voice-over), 15.b (paste the new code), 15.c (describe the change: swapped `delay(sensorValue)` blinking on pin 13 for `analogWrite` brightness control on PWM pin 9, with `map()` rescaling the 10-bit ADC reading to the 8-bit PWM range).

---

### Experiment 16 — Blink Rate Follows Light Intensity (LDR replaces Potentiometer)

(Hardware from Experiment 14, with the potentiometer's divider swapped for an LDR divider —
same idea as Experiment 13, but now tapped into A0 instead of just measured.)

| # | Connection |
|---|---|
| 1 | Power the Arduino UNO from the PC using the USB cable |
| 2 | LED anode (long leg) — one end of the resistor |
| 3 | Resistor — other end to Arduino Digital Pin **13** |
| 4 | LED cathode (short leg) — Arduino **GND** |
| 5 | LDR leg 1 — Arduino **5V** |
| 6 | LDR leg 2 — one end of a second resistor (same row = this is your A0 tap node) |
| 7 | Second resistor's other end — Arduino **GND** |
| 8 | Same LDR/resistor junction node (step 6/7) — Arduino **A0** |

**Code:** identical to Experiment 14 (`Experiment_14` sketch, unchanged) — only the hardware feeding A0 changed from a potentiometer's wiper to an LDR divider's junction.

**Report checklist:** 16.a (video with voice-over showing blink rate change as you vary light on the LDR — cover it, shine a torch on it, etc.).

---

### Experiment 17 — LED Intensity Follows Light Intensity

(Hardware from Experiment 16, with the LED moved to PWM pin 9 exactly as in Experiment 15.)

| # | Connection |
|---|---|
| 1 | Power the Arduino UNO from the PC using the USB cable |
| 2 | LED anode (long leg) — one end of the resistor |
| 3 | Resistor — other end to Arduino Digital Pin **9** *(PWM)* |
| 4 | LED cathode (short leg) — Arduino **GND** |
| 5 | LDR leg 1 — Arduino **5V** |
| 6 | LDR leg 2 — one end of a second resistor (A0 tap node) |
| 7 | Second resistor's other end — Arduino **GND** |
| 8 | Same LDR/resistor junction node — Arduino **A0** |

**Code:** identical to Experiment 15 (`analogRead(A0)` → `map()` → `analogWrite(9, brightness)`) — only the sensor divider changed from potentiometer to LDR.

**Report checklist:** 17.a (video with voice-over), 17.b (paste the code — same as Exp 15), 17.c (describe: same brightness-control code as Experiment 15, input swapped from potentiometer wiper to LDR divider node, so brightness now tracks ambient light instead of knob position).

---

### Experiment 18 — Ethernet Shield: Web Page Showing Analog Inputs

| # | Connection |
|---|---|
| 1 | Seat the **Ethernet Shield** onto the Arduino UNO headers (all pins aligned, pressed flush) |
| 2 | Ethernet Shield RJ45 port — network cable — router/switch with internet/LAN access |
| 3 | Potentiometer outer leg A — Arduino **5V** *(on the shield's passthrough header)* |
| 4 | Potentiometer outer leg B — Arduino **GND** |
| 5 | Potentiometer wiper — Arduino **A0** |
| 6 | *(repeat a similar 3-leg divider for any other analog sensor you want on A1–A5, e.g. the LDR divider from Experiment 16/17 into A1)* |
| 7 | Power the Arduino UNO (through the shield) from the PC using the USB cable |

**Code — sketch name `Experiment_18`** (standard Arduino Ethernet "analog inputs on a web
page" example — matches the PDF's Q18.b about library/mac/IP and Q18.d function list):
```cpp
#include <SPI.h>
#include <Ethernet.h>

byte mac[] = { 0xDE, 0xAD, 0xBE, 0xEF, 0xFE, 0xED };  // any locally-administered MAC
IPAddress ip(192, 168, 1, 177);                        // pick a free address on your LAN

EthernetServer server(80);

void setup() {
  Serial.begin(9600);
  Ethernet.begin(mac, ip);
  Serial.print("Hardware status: ");
  Serial.println(Ethernet.hardwareStatus());
  Serial.print("Link status: ");
  Serial.println(Ethernet.linkStatus());
  server.begin();
  Serial.print("Server is at ");
  Serial.println(Ethernet.localIP());
}

void loop() {
  EthernetClient client = server.available();
  if (client) {
    boolean blankLine = true;
    while (client.connected()) {
      if (client.available()) {
        char c = client.read();
        if (c == '\n' && blankLine) {
          client.println("HTTP/1.1 200 OK");
          client.println("Content-Type: text/html");
          client.println("Connection: close");
          client.println();
          client.println("<!DOCTYPE HTML><html>");
          for (int a = 0; a < 6; a++) {
            client.print("analog input ");
            client.print(a);
            client.print(" is ");
            client.print(analogRead(a));
            client.println("<br />");
          }
          client.println("</html>");
          break;
        }
        blankLine = (c == '\n') ? true : (c == '\r') ? blankLine : false;
      }
    }
    delay(1);
    client.stop();
  }
}
```

**Report checklist:** 18.a (video with voice-over showing you browse to the board's IP and see the page update), 18.b (18.b.1: `SPI.h` + `Ethernet.h`; 18.b.2: `byte mac[] = {...}` array passed to `Ethernet.begin`; 18.b.3: an `IPAddress` object passed the same call, or left out entirely for DHCP; 18.b.4: data goes out as raw HTTP text over TCP port 80 via `EthernetClient`/`EthernetServer`), 18.c (shield uses UNO pins **10 (SS), 11 (MOSI), 12 (MISO), 13 (SCK)** for SPI to the W5100 — map these to their ATmega328P DIP pins and explain the chip's hardware SPI peripheral enables this), 18.d (explain each listed function: `Serial.begin` opens the serial port at a baud rate; `Ethernet.begin` configures the network interface; `hardwareStatus()`/`linkStatus()` report shield presence/cable-link state; `server.begin()` starts listening; `EthernetServer server(80)` constructs a server object bound to HTTP port 80; `Serial.print`/`println` write to the USB serial monitor; `client.print`/`println` write bytes back to the connected browser).

---

### Experiment 19 — Web Page Shows Only Two Labelled Sensors

(Hardware builds on Experiment 18 — keep the potentiometer on A0, add the LDR divider from
Experiment 16/17 wired into **A1**, and move the potentiometer's wiper tap from A0 to **A4**.)

| # | Connection |
|---|---|
| 1–2 | Ethernet Shield seated + networked, as in Experiment 18 |
| 3 | LDR leg 1 — Arduino **5V** |
| 4 | LDR leg 2 — one end of a resistor (junction = A1 tap) |
| 5 | Resistor other end — Arduino **GND** |
| 6 | LDR/resistor junction (step 4/5) — Arduino **A1** |
| 7 | Potentiometer outer leg A — Arduino **5V** |
| 8 | Potentiometer outer leg B — Arduino **GND** |
| 9 | Potentiometer wiper — Arduino **A4** |

**Code:** same as Experiment 18, with the reporting loop replaced:
```cpp
          client.println("<!DOCTYPE HTML><html>");
          client.print("The current LDR value is ");
          client.print(analogRead(A1));
          client.println("<br />");
          client.print("The current Potentiometer value is ");
          client.print(analogRead(A4));
          client.println("<br />");
          client.println("</html>");
```

**Report checklist:** 19.a (video with voice-over — change light on the LDR and turn the pot, show both labelled values update on the page), 19.b (paste the full new sketch), 19.c (describe the change: restricted the `for` loop over all 6 analog pins down to two explicit, labelled reads at A1 and A4).

---

### Experiment 20 — Potentiometer to Serial Monitor *and* ThingSpeak

(Hardware builds on Experiment 19 — this experiment only needs the **potentiometer on A0**;
the LDR/A1 wiring from Experiment 19 can stay in place but isn't required.)

| # | Connection |
|---|---|
| 1–2 | Ethernet Shield seated + networked, as in Experiment 18 |
| 3 | Potentiometer outer leg A — Arduino **5V** |
| 4 | Potentiometer outer leg B — Arduino **GND** |
| 5 | Potentiometer wiper — Arduino **A0** |

**Code — sketch name `Experiment_20`** (adds a ThingSpeak upload alongside the existing
Serial + local web page output):
```cpp
#include <SPI.h>
#include <Ethernet.h>

byte mac[] = { 0xDE, 0xAD, 0xBE, 0xEF, 0xFE, 0xED };
EthernetClient client;
char server[] = "api.thingspeak.com";
String writeAPIKey = "YOUR_THINGSPEAK_WRITE_API_KEY";  // from your channel's API Keys tab
unsigned long lastUpdate = 0;

void setup() {
  Serial.begin(9600);
  Ethernet.begin(mac);   // DHCP; use Ethernet.begin(mac, ip) if your router has none
}

void loop() {
  int potValue = analogRead(A0);
  Serial.print("Potentiometer value: ");
  Serial.println(potValue);

  if (millis() - lastUpdate > 15000) {   // ThingSpeak free tier: 1 update / 15 s minimum
    lastUpdate = millis();
    if (client.connect(server, 80)) {
      String body = "api_key=" + writeAPIKey + "&field1=" + String(potValue);
      client.println("POST /update HTTP/1.1");
      client.println("Host: api.thingspeak.com");
      client.println("Connection: close");
      client.println("Content-Type: application/x-www-form-urlencoded");
      client.print("Content-Length: ");
      client.println(body.length());
      client.println();
      client.println(body);
      client.stop();
    }
  }
  delay(1000);
}
```

**Report checklist:** 20.a (video with voice-over — turn the pot, show the Serial Monitor value change *and* the ThingSpeak channel graph update), 20.b (paste the sketch), 20.c (describe changes vs. Exp 19: dropped the local web server entirely, added an `EthernetClient` that POSTs the pot reading to ThingSpeak's `/update` endpoint every 15 s, plus a `Serial.println` for local viewing), 20.d (ThingSpeak account steps: sign up at thingspeak.com → create a new Channel → note Channel ID → open its **API Keys** tab → copy the **Write API Key**), 20.e (how data reaches ThingSpeak: the sketch opens a TCP connection to `api.thingspeak.com:80` and sends an HTTP POST to `/update` with `api_key` and `field1=<value>` in the request body — ThingSpeak logs each POST as one datapoint on Field 1's chart), 20.f (how data reaches the Serial Monitor: `Serial.println(potValue)` writes the ADC reading to the USB serial connection each loop, viewable via IDE **Tools → Serial Monitor** at 9600 baud).

---

## 5. Quick Reference Summary

| Experiment | Analog pin(s) | Digital / PWM pin(s) | Extra hardware beyond Set 1's LED+resistor |
|---|---|---|---|
| 11 | — | — | Multimeter only (resistors, potentiometer, LDR) |
| 12 | — | — | 5 resistors in series + multimeter (voltage) |
| 13 | — | — | LDR + resistor divider + multimeter (voltage) |
| 14 | A0 (pot) | 13 | Potentiometer |
| 15 | A0 (pot) | 9 (PWM) | Potentiometer |
| 16 | A0 (LDR) | 13 | LDR + resistor divider |
| 17 | A0 (LDR) | 9 (PWM) | LDR + resistor divider |
| 18 | A0–A5 (any sensors) | 10/11/12/13 (SPI, reserved by shield) | Ethernet Shield |
| 19 | A1 (LDR) + A4 (pot) | 10/11/12/13 (SPI, reserved) | Ethernet Shield + LDR divider + potentiometer |
| 20 | A0 (pot) | 10/11/12/13 (SPI, reserved) | Ethernet Shield + ThingSpeak account |
