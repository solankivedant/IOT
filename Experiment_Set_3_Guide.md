# Experiment Set 3 — Step-by-Step Lab Guide (Arduino UNO)

Submission due: 17/10/2026. This set adds **display output** (7-segment LED, 16x2 LCD),
**serial communication in both directions** (Serial Monitor / Plotter / typed input),
**distance sensing** (HC-SR04 ultrasonic) and **internet data** (ThingSpeak upload, and one
Arduino reading another Arduino's web page). Wiring is given as **direct
component-to-component connections** — build each connection in order, landing both ends of
a "connection" in the same breadboard row (or a power rail) to join them electrically.

> This guide tells you **how to build and run** each experiment. The graded report
> questions from the PDF are listed at the end of each experiment as a checklist — answer
> those yourself (they need your own explanation, photos/video, and measurements).
>
> **Programs for Experiments 21, 26 (partly), 27, 28, 29, 30 and 31 are not printed in the
> slide deck.** The deck prints the code only for Experiments 22, 23, 24 and the Serial Read
> example used by 26. For the others, the slides give just the *task* and the *questions*,
> and refer to sketches named `Experiment_xx` supplied separately by the instructor. The
> code shown below for those is a standard, working Arduino implementation that matches the
> described behaviour and the PDF's own questions — swap in the instructor's exact file if
> it differs; the wiring and concepts stay the same.

---

## 1. Components Used

Same physical kit as Sets 1 and 2 (`component-images/`), plus these items that are now active:

| Component | Photo | Pins / Legs |
|---|---|---|
| Arduino UNO | `component-images/arduino-uno.jpeg` | Left header: **5V, RESET, 3.3V, 5V, GND, GND, VIN**. Bottom header: **A0–A5**. Right headers: **SCL, SDA, AREF, GND, 13, 12, 11~, 10~, 9~, 8** and **7, 6~, 5~, 4, 3~, 2, TX→1, RX←0**. `~` = PWM-capable pin. |
| Breadboard | `component-images/breadboard.jpeg` | Top/bottom rails: **red `+`**, **blue `−`**. Center strips: rows **A–E** / **F–J**, columns **1–60**; A–E not joined to F–J. |
| LED, resistor (220 Ω), jumper wires, USB cable | `led-light.jpeg`, `resistor.jpeg`, `wire.jpeg`, `arduino-connector.jpeg` | LED: **long leg = anode (+)**, **short leg = cathode (−)**. Resistors have no polarity. |
| Potentiometer (10 kΩ) | `component-images/potentiometer.jpeg` | 3 legs: **two outer legs** = fixed ends of the track (across 5V/GND), **middle leg = wiper**. |
| Push button switch | `component-images/switch.jpeg` | 4 legs: the 2 legs on the same side of the body are always joined; the two sides join only while the button is pressed. |
| **7-segment LED display (1 digit)** | `component-images/seven-segment-front.jpeg`, `seven-segment-back.jpeg` | **10 pins** — 5 on the top edge, 5 on the bottom edge. Holding the display with the digit facing you and the decimal point at bottom-right, the pin numbers run **1–5 along the bottom (left → right)** and **6–10 along the top (right → left)**. Standard pin-out: **1 = E, 2 = D, 3 = COM, 4 = C, 5 = DP, 6 = B, 7 = A, 8 = COM, 9 = F, 10 = G**. The two COM pins (3 and 8) are joined inside — use either one. |
| **HC-SR04 ultrasonic sensor** | `component-images/ultrasonic-sensor.jpeg` | 4 pins: **Vcc, Trig, Echo, Gnd**. Vcc = +5 V; **Trig** is an *input* (hold HIGH 10 µs to fire a burst); **Echo** is an *output* (goes HIGH for as long as the echo takes to return). Works at 40 kHz. |
| **16x2 LCD (JHD 162A, HD44780-compatible)** | `component-images/led-screen-front.jpeg`, `led-back.jpeg` | 16 pins, numbered 1–16 on the back: **1 VSS, 2 VDD (VCC), 3 V0 (VEE, contrast), 4 RS, 5 R/W, 6 E, 7–14 DB0–DB7, 15 LED+ (backlight anode), 16 LED− (backlight cathode)**. |
| **Ethernet Shield (W5100)** | *(not in image set)* | Stacks on the UNO. Uses **pins 10, 11, 12, 13** (SPI) internally — those four are **reserved** while the shield is mounted. RJ45 port connects to your router. Needed for Experiments 29 and 31. |
| Second Arduino + Ethernet Shield | *(not in image set)* | Needed only for Experiment 31 — acts as the *server* the first board reads from. |

---

## 2. One-Time Software Setup

| Step | From | To |
|---|---|---|
| 1 | Arduino UNO USB port | USB cable (USB-B end) |
| 2 | USB cable (USB-A end) | PC USB port |
| 3 | IDE menu **Tools → Board** | Select **Arduino AVR Boards → Arduino Uno** |
| 4 | IDE menu **Tools → Port** | Select **COM3 (Arduino UNO)** *(use whichever COM number appears)* |
| 5 (Exp 29, 31) | Ethernet Shield | Push firmly onto the UNO headers, then connect its RJ45 port to your router |
| 6 (Exp 29) | Browser | Use the **ThingSpeak** account and channel created in Experiment 20 (Field 1 = distance) |

Serial Monitor / Plotter (Experiments 22–29): open from **Tools → Serial Monitor** (Ctrl+Shift+M)
or **Tools → Serial Plotter** (Ctrl+Shift+L), and set the baud rate to **9600** at the bottom
right. The two windows cannot be open at the same time — close one before opening the other.

---

## 3. Breadboard Layout Key

- Every "connection" below means: plug both ends into the breadboard so they land in the
  **same row** (or the same power rail).
- **Power rails**: red strip = `+` (tied to Arduino 5V), blue strip = `−` (tied to Arduino GND).
- Always keep a resistor in series with every LED or LED segment (220 Ω) — an Arduino pin can
  safely source only about 20 mA.

---

## 4. Experiment-by-Experiment Build

### Experiment 21 — One 7-Segment Display Counting 0 to 9 (every 2 s)

Each of the 7 segments (a–g) gets its own Arduino pin and its own 220 Ω resistor; the display's
common pin goes to GND. (This wiring is for a **common-cathode** display — see Q21.b to check
which kind you have; a common-anode display needs the change in the note below.)

| # | Connection |
|---|---|
| 1 | Power the Arduino UNO from the PC using the USB cable |
| 2 | Arduino Digital Pin **2** — one end of Resistor 1 |
| 3 | Resistor 1 other end — display pin **7** (segment **a**) |
| 4 | Arduino Digital Pin **3** — one end of Resistor 2 |
| 5 | Resistor 2 other end — display pin **6** (segment **b**) |
| 6 | Arduino Digital Pin **4** — one end of Resistor 3 |
| 7 | Resistor 3 other end — display pin **4** (segment **c**) |
| 8 | Arduino Digital Pin **5** — one end of Resistor 4 |
| 9 | Resistor 4 other end — display pin **2** (segment **d**) |
| 10 | Arduino Digital Pin **6** — one end of Resistor 5 |
| 11 | Resistor 5 other end — display pin **1** (segment **e**) |
| 12 | Arduino Digital Pin **7** — one end of Resistor 6 |
| 13 | Resistor 6 other end — display pin **9** (segment **f**) |
| 14 | Arduino Digital Pin **8** — one end of Resistor 7 |
| 15 | Resistor 7 other end — display pin **10** (segment **g**) |
| 16 | Display pin **3** or **8** (common) — Arduino **GND** |

Segment layout (for reference): `a` = top bar, `b` = top-right, `c` = bottom-right, `d` = bottom
bar, `e` = bottom-left, `f` = top-left, `g` = middle bar, `DP` = decimal point (left unused).

**Code — sketch name `Experiment_21`:**
```cpp
// segments a,b,c,d,e,f,g on Arduino pins 2..8
const int segPins[7] = {2, 3, 4, 5, 6, 7, 8};

// bit 0 = a, bit 1 = b, ... bit 6 = g  (1 = segment ON on a common-cathode display)
const byte digits[10] = {
  0x3F,  // 0
  0x06,  // 1
  0x5B,  // 2
  0x4F,  // 3
  0x66,  // 4
  0x6D,  // 5
  0x7D,  // 6
  0x07,  // 7
  0x7F,  // 8
  0x6F   // 9
};

void setup() {
  for (int i = 0; i < 7; i++) {
    pinMode(segPins[i], OUTPUT);
  }
}

void loop() {
  for (int n = 0; n < 10; n++) {
    for (int s = 0; s < 7; s++) {
      digitalWrite(segPins[s], bitRead(digits[n], s));
    }
    delay(2000);   // change the number every two seconds
  }
}
```

> **Common-anode display?** Wire the common pin to **5V** instead of GND and invert the output:
> change the write to `digitalWrite(segPins[s], !bitRead(digits[n], s));`. Everything else is
> identical.

**Report checklist:** 21.a (video with voice-over showing the display counting 0→9 and repeating), 21.b (how to tell Common Cathode from Common Anode — e.g. with a multimeter in **diode-test** mode, touch the red probe to the common pin and the black probe to a segment pin: if that segment lights, the display is **common anode**; if it only lights with the probes swapped (black on the common pin, red on a segment), it is **common cathode**. Alternatively, without a multimeter: join Arduino 5V → 220 Ω → one segment pin and touch the common pin to GND; the segment lighting means common cathode. If it stays dark, reverse it (common pin to 5V, segment pin through 220 Ω to GND) — lighting then means common anode).

---

### Experiment 22 — Potentiometer Value on Serial Monitor and Serial Plotter

| # | Connection |
|---|---|
| 1 | Power the Arduino UNO from the PC using the USB cable |
| 2 | Potentiometer outer leg A — Arduino **5V** |
| 3 | Potentiometer outer leg B — Arduino **GND** |
| 4 | Potentiometer wiper (middle leg) — Arduino **A0** |

**Code — sketch name `Experiment_22`** (from the slide deck, verbatim):
```cpp
/*
AnalogReadSerial
Reads an analog input on pin 0, prints the result to the Serial Monitor.
Graphical representation is available using Serial Plotter (Tools > Serial Plotter menu).
Attach the center pin of a potentiometer to pin A0, and the outside pins to +5V and ground.
This example code is in the public domain.
http://www.arduino.cc/en/Tutorial/AnalogReadSerial
*/
// the setup routine runs once when you press reset:
void setup() {
  // initialize serial communication at 9600 bits per second:
  Serial.begin(9600);
}

// the loop routine runs over and over again forever:
void loop() {
  // read the input on analog pin 0:
  int sensorValue = analogRead(A0);
  // print out the value you read:
  Serial.println(sensorValue);
  delay(1);        // delay in between reads for stability
}
```

**How to observe it:** upload, open **Tools → Serial Monitor** (9600 baud) and turn the knob —
the numbers run from **0** to **1023**. Close it, open **Tools → Serial Plotter** and the same
values are drawn as a live line graph.

**Report checklist:** 22.a (video with voice-over), 22.b (22.b.1 `Serial.begin(9600);` opens the USB serial port at 9600 bits per second; 22.b.2 `Serial.println(..)` sends the value as readable text followed by a carriage-return + newline).

---

### Experiment 23 — Push Button State on Serial Monitor and Plotter

| # | Connection |
|---|---|
| 1 | Power the Arduino UNO from the PC using the USB cable |
| 2 | Resistor (10 kΩ recommended, 220 Ω also works) — one end to Arduino **5V** |
| 3 | Resistor other end — switch **Side A** (its two same-side legs, internally joined) *(this row is the junction)* |
| 4 | Switch **Side B** (its two same-side legs, internally joined) — Arduino **GND** |
| 5 | Junction of resistor and switch (step 3) — Arduino Digital Pin **2** |

The resistor *pulls pin 2 up to 5V* while the button is open, and pressing the button connects
that junction straight to GND. So the input reads **1 when released** and **0 while pressed**
(the opposite of Experiment 9's wiring).

**Code — sketch name `Experiment_23`** (from the slide deck, verbatim):
```cpp
/*
DigitalReadSerial
Reads a digital input on pin 2, prints the result to the Serial Monitor
This example code is in the public domain.
http://www.arduino.cc/en/Tutorial/DigitalReadSerial
*/
// digital pin 2 has a pushbutton attached to it. Give it a name:
int pushButton = 2;

// the setup routine runs once when you press reset:
void setup() {
  // initialize serial communication at 9600 bits per second:
  Serial.begin(9600);
  // make the pushbutton's pin an input:
  pinMode(pushButton, INPUT);
}

// the loop routine runs over and over again forever:
void loop() {
  // read the input pin:
  int buttonState = digitalRead(pushButton);
  // print out the state of the button:
  Serial.println(buttonState);
  delay(1);        // delay in between reads for stability
}
```

**How to observe it:** Serial Monitor scrolls `1` continuously, and `0` while you hold the
button. In the Serial Plotter you see a flat line at 1 that drops to 0 for as long as the button is pressed.

**Report checklist:** 23.a (video with voice-over — show both the Monitor and the Plotter reacting to the button).

---

### Experiment 24 — Potentiometer → Serial Monitor + LED Brightness (with `map`)

| # | Connection |
|---|---|
| 1 | Power the Arduino UNO from the PC using the USB cable |
| 2 | LED anode (long leg) — one end of the resistor |
| 3 | Resistor other end — Arduino Digital Pin **9** *(`9~`, PWM)* |
| 4 | LED cathode (short leg) — Arduino **GND** |
| 5 | Potentiometer outer leg A — Arduino **5V** |
| 6 | Potentiometer outer leg B — Arduino **GND** |
| 7 | Potentiometer wiper (middle leg) — Arduino **A0** |

**Code — sketch name `Experiment_24`** (from the slide deck, verbatim):
```cpp
/*
Analog input, analog output, serial output
Reads an analog input pin, maps the result to a range from 0 to 255 and uses
the result to set the pulse width modulation (PWM) of an output pin.
Also prints the results to the Serial Monitor.
The circuit:
- potentiometer connected to analog pin 0.
Center pin of the potentiometer goes to the analog pin.
side pins of the potentiometer go to +5V and ground
- LED connected from digital pin 9 to ground
created 29 Dec. 2008
modified 9 Apr 2012
by Tom Igoe
This example code is in the public domain.
http://www.arduino.cc/en/Tutorial/AnalogInOutSerial
*/
// These constants won't change. They're used to give names to the pins used:
const int analogInPin = A0;  // Analog input pin that the potentiometer is attached to
const int analogOutPin = 9;  // Analog output pin that the LED is attached to

int sensorValue = 0;         // value read from the pot
int outputValue = 0;         // value output to the PWM (analog out)

void setup() {
  // initialize serial communications at 9600 bps:
  Serial.begin(9600);
}

void loop() {
  // read the analog in value:
  sensorValue = analogRead(analogInPin);
  // map it to the range of the analog out:
  outputValue = map(sensorValue, 0, 1023, 0, 255);
  // change the analog out value:
  analogWrite(analogOutPin, outputValue);

  // print the results to the Serial Monitor:
  Serial.print("sensor = ");
  Serial.print(sensorValue);
  Serial.print("\t output = ");
  Serial.println(outputValue);

  // wait 2 milliseconds before the next loop for the analog-to-digital
  // converter to settle after the last reading:
  delay(2);
}
```

**Report checklist:** 24.a (video with voice-over — show the LED dimming/brightening *and* the Monitor/Plotter values), 24.b (24.b.1 `map(sensorValue, 0, 1023, 0, 255)` linearly rescales the 10-bit ADC value (0–1023) to the 8-bit PWM range (0–255); 24.b.2 `Serial.print("\t output = ");` prints the text, where `\t` is a tab character, with no line break; 24.b.3 `Serial.println(outputValue);` prints the number and then ends the line).

---

### Experiment 25 — Same as 24, but Without `map()`

Hardware is **identical to Experiment 24** (LED + resistor on pin 9, potentiometer wiper on A0, outer legs on 5V/GND).

| # | Connection |
|---|---|
| 1 | Power the Arduino UNO from the PC using the USB cable |
| 2 | LED anode (long leg) — one end of the resistor |
| 3 | Resistor other end — Arduino Digital Pin **9** *(PWM)* |
| 4 | LED cathode (short leg) — Arduino **GND** |
| 5 | Potentiometer outer leg A — Arduino **5V** |
| 6 | Potentiometer outer leg B — Arduino **GND** |
| 7 | Potentiometer wiper (middle leg) — Arduino **A0** |

**Code** (Experiment 24 with the `map()` line replaced by a plain division — 1023 ÷ 4 ≈ 255, which does the same scaling):
```cpp
const int analogInPin = A0;
const int analogOutPin = 9;

int sensorValue = 0;
int outputValue = 0;

void setup() {
  Serial.begin(9600);
}

void loop() {
  sensorValue = analogRead(analogInPin);
  outputValue = sensorValue / 4;          // 0..1023  ->  0..255, no map()
  analogWrite(analogOutPin, outputValue);

  Serial.print("sensor = ");
  Serial.print(sensorValue);
  Serial.print("\t output = ");
  Serial.println(outputValue);

  delay(2);
}
```
(Integer division makes `outputValue` run 0…255. `analogWrite(pin, sensorValue / 4)` directly, or `sensorValue >> 2`, is equivalent.)

**Report checklist:** 25.a (video with voice-over).

---

### Experiment 26 — Serial Read (Typing to the Arduino)

No extra hardware — only the Arduino on USB. (An LED on pin 13 / the on-board "L" LED can be added if you want a visible response, but it is not required.)

| # | Connection |
|---|---|
| 1 | Power the Arduino UNO from the PC using the USB cable |

**Code — sketch name `Experiment_26`** (the Serial Read example shown on the slides):
```cpp
int incomingByte = 0;   // for incoming serial data

void setup() {
  Serial.begin(9600);     // opens serial port, sets data rate to 9600 bps
}

void loop() {
  // send data only when you receive data:
  if (Serial.available() > 0) {
    // read the incoming byte:
    incomingByte = Serial.read();

    // say what you got:
    Serial.print("I received: ");
    Serial.println(incomingByte, DEC);
  }
}
```

**How to observe it:** open the Serial Monitor at 9600 baud, type a character (for example `A`)
in the input box at the top and press **Send**. The Arduino replies `I received: 65` (the ASCII
code of `A`). With the line-ending box set to **Newline**, it also prints `I received: 10`
because the newline character `\n` is itself a received byte.

**Report checklist:** 26.a (video with voice-over), 26.b (26.b.1 `Serial.available()` returns how many bytes are waiting in the serial receive buffer (0 if none); 26.b.2 `Serial.read()` removes and returns the first waiting byte as an `int`, or **−1** if nothing is available).

---

### Experiment 27 — Typed Number 3, 4 or 5 Lights the LED on That Pin for 2 Seconds

Three LEDs, each with its own resistor, on pins 3, 4 and 5.

| # | Connection |
|---|---|
| 1 | Power the Arduino UNO from the PC using the USB cable |
| 2 | LED 1 anode (long leg) — Resistor 1 one end |
| 3 | Resistor 1 other end — Arduino Digital Pin **3** |
| 4 | LED 1 cathode (short leg) — Arduino **GND** |
| 5 | LED 2 anode (long leg) — Resistor 2 one end |
| 6 | Resistor 2 other end — Arduino Digital Pin **4** |
| 7 | LED 2 cathode (short leg) — Arduino **GND** |
| 8 | LED 3 anode (long leg) — Resistor 3 one end |
| 9 | Resistor 3 other end — Arduino Digital Pin **5** |
| 10 | LED 3 cathode (short leg) — Arduino **GND** |

**Code:**
```cpp
void setup() {
  Serial.begin(9600);
  pinMode(3, OUTPUT);
  pinMode(4, OUTPUT);
  pinMode(5, OUTPUT);
  Serial.println("Enter a number between 3 and 5:");
}

void loop() {
  if (Serial.available() > 0) {
    String text = Serial.readStringUntil('\n');   // read the whole typed line
    text.trim();                                  // drop spaces / '\r'
    if (text.length() == 0) return;               // ignore an empty line

    int number = text.toInt();                    // text -> integer (0 if not a number)

    if (number >= 3 && number <= 5) {
      digitalWrite(number, HIGH);                 // pin number == typed number
      Serial.print("LED on pin ");
      Serial.print(number);
      Serial.println(" is ON for 2 seconds.");
      delay(2000);
      digitalWrite(number, LOW);
    } else {
      Serial.println("Number is out of Range.");
    }
  }
}
```

**How to observe it:** Serial Monitor at 9600 baud, line ending **Newline**. Type `3` → LED on
pin 3 for 2 s; `4` → pin 4; `5` → pin 5; anything else (`2`, `9`, `-1`, `abc`) →
`Number is out of Range.`

**Report checklist:** 27.a (video with voice-over), 27.b (paste the full new sketch), 27.c (describe the changes vs. Experiment 26: Serial.read() byte-by-byte replaced with reading a whole line and converting it with `toInt()`; added three output pins; added a range check 3–5; the typed number doubles as the pin number; the out-of-range message; and `delay(2000)` for the 2-second ON time).

---

### Experiment 28 — Distance Measurement with the HC-SR04 Ultrasonic Sensor

| # | Connection |
|---|---|
| 1 | Power the Arduino UNO from the PC using the USB cable |
| 2 | HC-SR04 **Vcc** — Arduino **5V** |
| 3 | HC-SR04 **Gnd** — Arduino **GND** |
| 4 | HC-SR04 **Trig** — Arduino Digital Pin **7** |
| 5 | HC-SR04 **Echo** — Arduino Digital Pin **8** |

(The slide's picture uses two different digital pins for Trig and Echo. Pins 7 and 8 are used
here so that the same wiring keeps working in Experiment 29, where the Ethernet Shield takes
over pins 10–13. If the instructor's `Experiment_28` sketch defines different pins, either
rewire to match it or change `trigPin` / `echoPin` below.)

**How it works (slides 27–30):** Trig is held HIGH for **10 µs**, the sensor sends an
8-cycle 40 kHz ultrasonic burst, the burst bounces off the object, and Echo stays HIGH for
exactly as long as the round trip took. Sound travels at **340 m/s = 0.034 cm/µs**, and the
wave goes to the object *and back*, so `distance = time × 0.034 / 2`.

**Code — sketch name `Experiment_28`:**
```cpp
const int trigPin = 7;
const int echoPin = 8;

long duration;     // echo pulse length in microseconds
float distance;    // distance in cm

void setup() {
  pinMode(trigPin, OUTPUT);
  pinMode(echoPin, INPUT);
  Serial.begin(9600);
}

void loop() {
  // make sure Trig is LOW, then send a clean 10 microsecond HIGH pulse
  digitalWrite(trigPin, LOW);
  delayMicroseconds(2);
  digitalWrite(trigPin, HIGH);
  delayMicroseconds(10);
  digitalWrite(trigPin, LOW);

  // time (in microseconds) the Echo pin stays HIGH
  duration = pulseIn(echoPin, HIGH);

  // distance = time x speed of sound / 2   (there and back)
  distance = duration * 0.034 / 2;

  Serial.print("Distance: ");
  Serial.print(distance);
  Serial.println(" cm");

  delay(500);
}
```

**How to observe it:** Serial Monitor at 9600 baud — hold a book at 10 cm, 20 cm and 30 cm in
front of the sensor and compare the readings with a ruler. The sensor is reliable roughly from
2 cm to 400 cm.

**Report checklist:** 28.a (video with voice-over), 28.b (`duration = pulseIn(echoPin, HIGH)` waits for Echo to go HIGH, starts a timer, waits for it to go LOW, and returns the HIGH time in **microseconds** — returns 0 if no pulse arrives before the timeout (default 1 s)), 28.c (distance equation `d = t × v / 2`, with `v = 0.034 cm/µs` in air; **under water** the speed of sound is about **1480 m/s ≈ 0.148 cm/µs**, so the formula becomes `d = t × 0.148 / 2` — about 4.35× larger per microsecond. Note the standard HC-SR04 is *not waterproof*; a sealed waterproof transducer would be needed).

---

### Experiment 29 — Send Ultrasonic Distance to ThingSpeak

Experiment 28's sensor wiring plus the Ethernet Shield. Because the shield reserves pins
10–13, the sensor stays on pins 7 and 8 (see note above).

| # | Connection |
|---|---|
| 1 | Seat the **Ethernet Shield** onto the Arduino UNO headers (all pins aligned, pressed flush) |
| 2 | Ethernet Shield RJ45 port — network cable — router with internet access |
| 3 | HC-SR04 **Vcc** — Arduino **5V** |
| 4 | HC-SR04 **Gnd** — Arduino **GND** |
| 5 | HC-SR04 **Trig** — Arduino Digital Pin **7** |
| 6 | HC-SR04 **Echo** — Arduino Digital Pin **8** |
| 7 | Power the Arduino UNO (through the shield) from the PC using the USB cable |

**Code** (Experiment 28's measurement + Experiment 20's ThingSpeak upload):
```cpp
#include <SPI.h>
#include <Ethernet.h>

byte mac[] = { 0xDE, 0xAD, 0xBE, 0xEF, 0xFE, 0xED };
EthernetClient client;
char server[] = "api.thingspeak.com";
String writeAPIKey = "YOUR_THINGSPEAK_WRITE_API_KEY";  // channel's API Keys tab

const int trigPin = 7;
const int echoPin = 8;
unsigned long lastUpdate = 0;

float measureDistanceCm() {
  digitalWrite(trigPin, LOW);
  delayMicroseconds(2);
  digitalWrite(trigPin, HIGH);
  delayMicroseconds(10);
  digitalWrite(trigPin, LOW);
  long duration = pulseIn(echoPin, HIGH);
  return duration * 0.034 / 2;
}

void setup() {
  Serial.begin(9600);
  pinMode(trigPin, OUTPUT);
  pinMode(echoPin, INPUT);
  Ethernet.begin(mac);                 // DHCP
}

void loop() {
  float distance = measureDistanceCm();
  Serial.print("Distance: ");
  Serial.print(distance);
  Serial.println(" cm");

  if (millis() - lastUpdate > 15000) {   // ThingSpeak free tier: 1 update / 15 s minimum
    lastUpdate = millis();
    if (client.connect(server, 80)) {
      String body = "api_key=" + writeAPIKey + "&field1=" + String(distance);
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

**How to observe it:** move an object in front of the sensor; the Serial Monitor shows each
reading, and the ThingSpeak channel's **Field 1** chart gains one new point about every 15 s.

**Report checklist:** 29.a (video with voice-over — show the sensor, the Serial Monitor and the ThingSpeak graph), 29.b (paste the new sketch), 29.c (describe the changes vs. Experiment 28: added `SPI.h`/`Ethernet.h`, a MAC address, `Ethernet.begin(mac)`, an `EthernetClient`, the ThingSpeak host and Write API key; measurement code moved into a function; an HTTP POST to `/update` carrying `field1=<distance>` every 15 s; Experiment 28's Serial printing kept for local viewing).

---

### Experiment 30 — 16x2 LCD Display

Wiring follows the schematic on slide 39 (LiquidCrystal "Hello World" circuit): the LCD runs
in **4-bit mode** (data pins DB4–DB7 only), with the contrast set by a 10 kΩ potentiometer and the backlight fed
through a 220 Ω resistor.

| # | Connection |
|---|---|
| 1 | Power the Arduino UNO from the PC using the USB cable |
| 2 | Arduino **5V** — breadboard `+` rail; Arduino **GND** — breadboard `−` rail |
| 3 | LCD pin **1 (VSS)** — `−` rail (GND) |
| 4 | LCD pin **2 (VDD)** — `+` rail (5V) |
| 5 | Potentiometer outer leg A — `+` rail (5V) |
| 6 | Potentiometer outer leg B — `−` rail (GND) |
| 7 | Potentiometer wiper (middle leg) — LCD pin **3 (V0)** *(contrast)* |
| 8 | LCD pin **4 (RS)** — Arduino Digital Pin **12** |
| 9 | LCD pin **5 (R/W)** — `−` rail (GND) *(write-only)* |
| 10 | LCD pin **6 (E)** — Arduino Digital Pin **11** |
| 11 | LCD pins **7–10 (DB0–DB3)** — *not connected* |
| 12 | LCD pin **11 (DB4)** — Arduino Digital Pin **5** |
| 13 | LCD pin **12 (DB5)** — Arduino Digital Pin **4** |
| 14 | LCD pin **13 (DB6)** — Arduino Digital Pin **3** |
| 15 | LCD pin **14 (DB7)** — Arduino Digital Pin **2** |
| 16 | LCD pin **15 (LED+)** — one end of the 220 Ω resistor |
| 17 | 220 Ω resistor other end — `+` rail (5V) |
| 18 | LCD pin **16 (LED−)** — `−` rail (GND) |

Turn the contrast potentiometer until the characters appear (if you see only solid blocks or
nothing, adjust the knob first).

**Code — sketch name `Experiment_30`, Part 1** (standard LiquidCrystal "Hello World"):
```cpp
#include <LiquidCrystal.h>

// RS, E, D4, D5, D6, D7
LiquidCrystal lcd(12, 11, 5, 4, 3, 2);

void setup() {
  lcd.begin(16, 2);          // 16 columns, 2 rows
  lcd.print("hello, world!");
}

void loop() {
  lcd.setCursor(0, 1);       // column 0, second row
  lcd.print(millis() / 1000); // seconds since reset
}
```

**Code — Part 3 (today's date instead of the greeting):**
```cpp
#include <LiquidCrystal.h>

LiquidCrystal lcd(12, 11, 5, 4, 3, 2);

void setup() {
  lcd.begin(16, 2);
  lcd.setCursor(0, 0);
  lcd.print("Date: 05/10/2026");   // change to today's date
  lcd.setCursor(0, 1);
  lcd.print("IoT Experiment 30");
}

void loop() {
}
```

**Report checklist:** 30.a (one **combined** video with voice-over covering Point 1 *and* Point 3), 30.b (the updated sketch from Point 3), 30.c (describe the change: the text sent with `lcd.print()` was replaced from "hello, world!" to the date, and the running-seconds counter in `loop()` was replaced by a second fixed line).

---

### Experiment 31 — Read Data from Another Arduino's Web Server

Two Arduinos on the same network. **Board A** is the server — it runs the web-page sketch
from Experiment 18 or 19 and is simply left powered. **Board B** (this experiment) is the
client that connects to Board A and prints what it receives.

| # | Connection (Board B) |
|---|---|
| 1 | Seat the **Ethernet Shield** onto Board B's UNO headers |
| 2 | Board B shield RJ45 port — network cable — the same router/switch Board A is connected to |
| 3 | Power Board B from the PC using the USB cable (Serial Monitor shows the received page) |

On Board A, make sure the server's static address is the one you will use below (for the
Experiment 18 sketch that is `192.168.1.177`) and that it is up before starting Board B.

**Code — sketch name `Experiment_31`** (Arduino "WebClient" pattern):
```cpp
#include <SPI.h>
#include <Ethernet.h>

// Board B needs its OWN MAC address (different from Board A's)
byte mac[] = { 0xDE, 0xAD, 0xBE, 0xEF, 0xFE, 0xEE };

IPAddress server(192, 168, 1, 177);   // Board A's IP address (the web-page server)
IPAddress ip(192, 168, 1, 178);       // a free address for Board B on the same network

EthernetClient client;

void setup() {
  Serial.begin(9600);
  Ethernet.begin(mac, ip);
  delay(1000);                         // give the shield time to start
  Serial.println("connecting...");

  if (client.connect(server, 80)) {
    Serial.println("connected");
    client.println("GET / HTTP/1.1");  // ask Board A for its web page
    client.println("Host: 192.168.1.177");
    client.println("Connection: close");
    client.println();
  } else {
    Serial.println("connection failed");
  }
}

void loop() {
  // print everything Board A sends back
  while (client.available()) {
    char c = client.read();
    Serial.print(c);
  }

  if (!client.connected()) {
    Serial.println();
    Serial.println("disconnecting.");
    client.stop();
    while (true);                      // stop here (press reset to fetch again)
  }
}
```

**How to observe it:** Serial Monitor at 9600 baud shows `connecting... connected`, then the
HTTP header lines and the HTML text that Board A produces (e.g. `analog input 0 is 512`, or
`The current LDR value is ...` for the Experiment 19 sketch), then `disconnecting.`.

**Report checklist:** 31.a (video with voice-over — show Board A's sensors changing and Board B's Serial Monitor receiving it), 31.b (31.b.1 `SPI.h` and `Ethernet.h`; 31.b.2 `byte mac[] = {...}` array passed to `Ethernet.begin(mac, ip)`; 31.b.3 an `IPAddress` object (`ip` for this board, `server` for the target board); 31.b.4 raw HTTP text over a TCP connection on port 80 using `EthernetClient`).

---

## 5. Quick Reference Summary

| Experiment | Input pin(s) | Output pin(s) | Extra hardware |
|---|---|---|---|
| 21 | — | 2–8 (segments a–g) | 7-segment display + 7 × 220 Ω |
| 22 | A0 (pot) | — (Serial) | Potentiometer |
| 23 | 2 (button) | — (Serial) | Push button + pull-up resistor |
| 24 | A0 (pot) | 9 (PWM LED) + Serial | Potentiometer + LED |
| 25 | A0 (pot) | 9 (PWM LED) + Serial | Same as 24 (no `map()`) |
| 26 | USB serial in | USB serial out | None |
| 27 | USB serial in | 3, 4, 5 (LEDs) | 3 LEDs + 3 resistors |
| 28 | 8 (Echo) | 7 (Trig) + Serial | HC-SR04 |
| 29 | 8 (Echo) | 7 (Trig); 10–13 reserved | HC-SR04 + Ethernet Shield + ThingSpeak |
| 30 | — | 12 (RS), 11 (E), 5/4/3/2 (D4–D7) | 16x2 LCD + 10 kΩ pot + 220 Ω |
| 31 | Ethernet (client) | Serial | 2 × (Arduino + Ethernet Shield) |
