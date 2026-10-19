# Experiment Set 4 — Step-by-Step Lab Guide (Raspberry Pi)

Submission due: 20/11/2026. This set moves from the Arduino UNO to the **Raspberry Pi**, and
every program is now written in **Python** instead of C. It starts with setting up the Pi
itself, then repeats the LED / duty-cycle / push-button work of Set 1 on the Pi's GPIO header,
and ends with three **ThingSpeak** uploads (ultrasonic distance, DHT22 temperature + humidity,
IR obstacle sensor). Wiring is given as **direct component-to-component connections** — build
each connection in order, landing both ends of a "connection" in the same breadboard row (or a
power rail) to join them electrically.

> This guide tells you **how to build and run** each experiment. The graded report
> questions from the PDF are listed at the end of each experiment as a checklist — answer
> those yourself (they need your own explanation, photos/video, and measurements).
>
> **The slide deck does not print any programs for this set.** It gives only the task and the
> questions. The Python programs below are standard, working RPi.GPIO implementations that
> match the described behaviour; the same files are saved in `experiment-4/` as
> `exp-42.py` … `exp-52.py`. Swap in the instructor's exact file if it differs; the wiring and
> concepts stay the same.

---

## 1. Components Used

| Component | Photo | Pins / Legs |
|---|---|---|
| **Raspberry Pi (3B+ / 4B / 5)** | *(not in image set)* | 40-pin GPIO header. Pin **1** is the one with the square solder pad, nearest the corner of the board (by the microSD side). **Odd pins (1, 3, 5 … 39) are the inner row, even pins (2, 4 … 40) the outer row** (the row closest to the board edge). |
| microSD card (16 GB or more) + card reader | *(not in image set)* | Holds the operating system. |
| Power supply | *(not in image set)* | Pi 4: **5 V 3 A USB-C**. Pi 5: **5 V 5 A USB-C** (27 W official supply). Pi 3B+: 5 V 2.5 A micro-USB. |
| Monitor + micro-HDMI/HDMI cable, USB keyboard, USB mouse | *(not in image set)* | Needed only for first set-up; afterwards SSH/VNC from the laptop is enough. |
| Breadboard | `component-images/breadboard.jpeg` | Top/bottom rails: **red `+`**, **blue `−`**. Center strips: rows **A–E** / **F–J**, columns **1–60**; A–E not joined to F–J. |
| LED, resistor (220 Ω), jumper wires | `led-light.jpeg`, `resistor.jpeg`, `wire.jpeg` | LED: **long leg = anode (+)**, **short leg = cathode (−)**. Use **female-to-male** jumpers from the Pi header to the breadboard. |
| Push button switch (×2) + 10 kΩ resistor (×2) | `component-images/switch.jpeg` | 4 legs: the 2 legs on the same side of the body are always joined; the two sides join only while the button is pressed. |
| **HC-SR04 ultrasonic sensor** | `component-images/ultrasonic-sensor.jpeg` | **Vcc, Trig, Echo, Gnd**. Runs on **5 V**, so its Echo output is **5 V** — it must go through a **1 kΩ / 2 kΩ voltage divider** before it reaches the Pi (Pi GPIO pins are 3.3 V only). |
| **DHT22 (AM2302) temperature & humidity sensor** | *(not in image set)* | Bare sensor: 4 pins, left to right with the grille facing you: **1 VCC, 2 DATA, 3 NC, 4 GND** (needs a 10 kΩ pull-up from DATA to VCC). 3-pin module: **+, OUT, −** (pull-up already on the board). |
| **IR obstacle sensor module (FC-51 type)** | `component-images/infrared-sensor.jpeg` | 3 pins: **VCC, GND, OUT**. OUT goes **LOW when an object is in front** of it. The blue trimmer sets the detection distance (about 2–30 cm). |

> **3.3 V rule.** Raspberry Pi GPIO pins work at **3.3 V** and are **not 5 V tolerant**. Never
> connect a 5 V signal directly to a GPIO pin — it can permanently damage the Pi. Each pin
> should not supply more than about **16 mA**.

---

## 2. Raspberry Pi Header — Pins Used in This Set

The PDF numbers pins by their **physical position** on the header (Pin 11, 13, 15 …), so every
program uses `GPIO.setmode(GPIO.BOARD)`. The BCM (GPIO) names are given only for reference.

| Physical pin | Name | Used in |
|---|---|---|
| 1 | **3.3 V** | Exp 44 (LED 2), 48–49 (switches), 51 (DHT22), 52 (IR) |
| 2 | **5 V** | Exp 50 (HC-SR04 Vcc) |
| 6 | **GND** | All experiments |
| 7 | GPIO4 | Exp 51 (DHT22 DATA) |
| 9, 14, 20, 25, 30, 34, 39 | GND | Extra ground pins |
| **11** | GPIO17 | LED 1 (Exp 42–49) |
| 12 | GPIO18 | Exp 52 (IR OUT) |
| **13** | GPIO27 | LED 2 (Exp 45–49) |
| **15** | GPIO22 | LED 3 (Exp 45–49) |
| 16 | GPIO23 | Exp 50 (HC-SR04 Trig) |
| 17 | 3.3 V | Second 3.3 V pin |
| 18 | GPIO24 | Exp 50 (HC-SR04 Echo, via divider) |
| **29** | GPIO5 | Switch 1 (Exp 48–49) |
| **31** | GPIO6 | Switch 2 (Exp 48–49) |

Breadboard rails: Pi **pin 6 (GND)** → blue `−` rail, Pi **pin 1 (3.3 V)** → red `+` rail
(only when the experiment needs 3.3 V on the breadboard). **Do not put 5 V on the same rail.**

---

## 3. One-Time Software Set-up (this is also Experiment 41)

See Experiment 41 below for the full step list. After set-up, every program in this set is run
the same way:

| Step | From | To |
|---|---|---|
| 1 | Raspberry Pi desktop | Open **Thonny** (Menu → Programming → Thonny) |
| 2 | Thonny | Paste the program and **Save** as e.g. `exp-42.py` in `/home/<user>/iot/` |
| 3 | Thonny | Press **Run** (F5). The output (prints) appears in the **Shell** pane at the bottom |
| 4 | Thonny | Press **Stop** (Ctrl+F2) to end the program — `GPIO.cleanup()` then turns all pins off |

Or from a terminal: `python3 exp-42.py`, and **Ctrl+C** to stop.

---

## 4. Experiment-by-Experiment Build

### Experiment 41 — Set-up of the Raspberry Pi

No circuit. These steps take a new Pi to a working desktop with Python and GPIO ready.

| # | Step |
|---|---|
| 1 | On the laptop, install **Raspberry Pi Imager** from `raspberrypi.com/software` |
| 2 | Put the microSD card into the card reader and plug it into the laptop |
| 3 | In Imager: **Choose Device** → your Pi model; **Choose OS** → *Raspberry Pi OS (64-bit)* (with desktop); **Choose Storage** → the microSD card |
| 4 | Click **Next → Edit Settings** (OS customisation): set the **hostname** (e.g. `iotpi`), **username + password**, **Wi-Fi SSID + password + country (IN)**, **time zone (Asia/Kolkata)** and keyboard layout. On the **Services** tab tick **Enable SSH** (password authentication) |
| 5 | Click **Save → Yes → Yes** to write the card. Wait for *Write Successful*, then eject the card |
| 6 | Insert the microSD card into the Pi's card slot (underside of the board) |
| 7 | Connect the monitor (HDMI / micro-HDMI port 0), the USB keyboard and the USB mouse. Connect a LAN cable if you are not using Wi-Fi |
| 8 | Connect the power supply **last**. The red LED stays on and the green LED flickers while it boots; the first boot takes a few minutes and may reboot once by itself (it expands the file system) |
| 9 | The desktop appears. If you skipped customisation, the **Welcome to Raspberry Pi** wizard asks for country, user, password and Wi-Fi now |
| 10 | Open a **Terminal** and update the system: `sudo apt update` then `sudo apt full-upgrade -y`, then `sudo reboot` |
| 11 | Find the Pi's IP address with `hostname -I` (needed for SSH/VNC) |
| 12 | Run `sudo raspi-config` → **Interface Options** → enable **SSH** and **VNC** if you want to use the Pi from the laptop. (Or use Menu → Preferences → Raspberry Pi Configuration → Interfaces) |
| 13 | Check Python: `python3 --version` (Python 3 is already installed) and that **Thonny** is in Menu → Programming |
| 14 | Check the GPIO library: `python3 -c "import RPi.GPIO"` should print nothing (no error). On a **Pi 5** run `sudo apt install python3-rpi-lgpio` first — it is a drop-in replacement, so the same `import RPi.GPIO as GPIO` programs work |
| 15 | Install the libraries for Experiments 50–52: `sudo apt install python3-requests` |
| 16 | For the DHT22 (Experiment 51) make a virtual environment, because new Raspberry Pi OS blocks system-wide `pip`: `python3 -m venv --system-site-packages ~/iot-env`, then `source ~/iot-env/bin/activate`, then `pip install adafruit-circuitpython-dht`. In Thonny select this interpreter via **Run → Configure interpreter → Python executable → `~/iot-env/bin/python3`** |
| 17 | Test the header: run `pinout` in the terminal — it prints the 40-pin map of your exact board |
| 18 | Shut down properly before unplugging: `sudo shutdown -h now` (wait for the green LED to stop) |

From the laptop you can now log in with `ssh <user>@iotpi.local` (or the IP from step 11) or
use **RealVNC Viewer** to see the desktop.

**Report checklist:** 41.a (describe all the set-up steps in detail — use the table above, and add screenshots of the Imager settings and the first desktop).

---

### Experiment 42 — Blink One LED on Pin 11 (1 s ON, 1 s OFF)

| # | Connection |
|---|---|
| 1 | Pi physical pin **11** (GPIO17) — one end of the 220 Ω resistor |
| 2 | Resistor other end — LED **anode** (long leg) |
| 3 | LED **cathode** (short leg) — Pi physical pin **6** (GND) |
| 4 | Power the Pi and open Thonny |

(LED current = (3.3 V − 2 V) / 220 Ω ≈ 6 mA, well inside the Pi pin limit.)

**Code — `experiment-4/exp-42.py`:**
```python
import RPi.GPIO as GPIO
import time

LED_PIN = 11                     # physical pin 11 (GPIO17)

GPIO.setwarnings(False)
GPIO.setmode(GPIO.BOARD)         # use physical pin numbers
GPIO.setup(LED_PIN, GPIO.OUT, initial=GPIO.LOW)

try:
    while True:
        GPIO.output(LED_PIN, GPIO.HIGH)   # LED ON
        time.sleep(1)
        GPIO.output(LED_PIN, GPIO.LOW)    # LED OFF
        time.sleep(1)
except KeyboardInterrupt:
    pass
finally:
    GPIO.cleanup()
```

**Report checklist:** 42.a (video with voice-over), 42.b (paste the code).

---

### Experiment 43 — 20 % Duty Cycle on Pin 11

Hardware is **identical to Experiment 42**.

| # | Connection |
|---|---|
| 1 | Pi pin **11** — 220 Ω resistor — LED anode |
| 2 | LED cathode — Pi pin **6** (GND) |

**Code — `experiment-4/exp-43.py`** (period kept at 1 s: ON 0.2 s, OFF 0.8 s):
```python
import RPi.GPIO as GPIO
import time

LED_PIN = 11                     # physical pin 11 (GPIO17)

GPIO.setwarnings(False)
GPIO.setmode(GPIO.BOARD)
GPIO.setup(LED_PIN, GPIO.OUT, initial=GPIO.LOW)

try:
    while True:
        GPIO.output(LED_PIN, GPIO.HIGH)   # ON for 20% of the 1 s period
        time.sleep(0.2)
        GPIO.output(LED_PIN, GPIO.LOW)    # OFF for 80% of the 1 s period
        time.sleep(0.8)
except KeyboardInterrupt:
    pass
finally:
    GPIO.cleanup()
```

Duty cycle = ON time / (ON + OFF) = 0.2 / 1.0 = **20 %**.

**Report checklist:** 43.a (video with voice-over), 43.b (paste the program), 43.c (changes vs. 42: `time.sleep(1)` after HIGH changed to `0.2`, and `time.sleep(1)` after LOW changed to `0.8`; the period stays 1 s, nothing else changed).

---

### Experiment 44 — Two LEDs, 20 % and 80 %, Same Program as 43

The program of Experiment 43 is **not changed** — run `exp-43.py` again. Only the hardware
changes: LED 2 is connected **upside down** to the same pin 11, between 3.3 V and the pin. When
pin 11 is HIGH (3.3 V) both ends of LED 2 are at 3.3 V, so it is OFF; when pin 11 is LOW (0 V)
current flows from 3.3 V through LED 2 *into* pin 11, so it is ON. LED 2 therefore does exactly
the opposite of LED 1: ON for 80 %, OFF for 20 %.

| # | Connection |
|---|---|
| 1 | *(LED 1, unchanged)* Pi pin **11** — Resistor 1 — LED 1 **anode** |
| 2 | *(LED 1, unchanged)* LED 1 **cathode** — Pi pin **6** (GND) |
| 3 | Pi pin **1** (3.3 V) — one end of Resistor 2 (220 Ω) |
| 4 | Resistor 2 other end — LED 2 **anode** (long leg) |
| 5 | LED 2 **cathode** (short leg) — Pi pin **11** (same row as Resistor 1's pin-11 end) |
| 6 | Run `exp-43.py` without editing it |

> Use **3.3 V (pin 1), not 5 V**, for LED 2. With 5 V, LED 2 would push 5 V into pin 11 while it
> is HIGH, which can damage the Pi.

**Report checklist:** 44.a (video with voice-over — show both LEDs: LED 1 short flash, LED 2 long ON), 44.b (describe the hardware changes: second LED + 220 Ω added between 3.3 V and pin 11, with its cathode on pin 11, so it lights when the pin is LOW — "active-low" connection; program untouched).

---

### Experiment 45 — Blink LEDs on Pins 11, 13 and 15 Together

| # | Connection |
|---|---|
| 1 | Pi pin **6** (GND) — breadboard blue `−` rail |
| 2 | Pi pin **11** — Resistor 1 (220 Ω) — LED 1 anode; LED 1 cathode — `−` rail |
| 3 | Pi pin **13** — Resistor 2 (220 Ω) — LED 2 anode; LED 2 cathode — `−` rail |
| 4 | Pi pin **15** — Resistor 3 (220 Ω) — LED 3 anode; LED 3 cathode — `−` rail |

(If LED 2 from Experiment 44 is still connected to pin 11 and 3.3 V, remove it first.)

**Code — `experiment-4/exp-45.py`:**
```python
import RPi.GPIO as GPIO
import time

LEDS = [11, 13, 15]              # GPIO17, GPIO27, GPIO22

GPIO.setwarnings(False)
GPIO.setmode(GPIO.BOARD)
GPIO.setup(LEDS, GPIO.OUT, initial=GPIO.LOW)

try:
    while True:
        GPIO.output(LEDS, GPIO.HIGH)      # all three ON together
        time.sleep(1)
        GPIO.output(LEDS, GPIO.LOW)       # all three OFF together
        time.sleep(1)
except KeyboardInterrupt:
    pass
finally:
    GPIO.cleanup()
```

`GPIO.setup()` and `GPIO.output()` accept a **list** of pins, so one call switches all three at once.

**Report checklist:** 45.a (video with voice-over), 45.b (paste the program).

---

### Experiment 46 — Turn On 11 → 13 → 15 One After Another (2 s), Then All OFF

Hardware is **identical to Experiment 45**.

| # | Connection |
|---|---|
| 1 | Pi pin **6** (GND) — `−` rail |
| 2 | Pi pins **11 / 13 / 15** — each through its own 220 Ω — LED anode; each cathode — `−` rail |

**Code — `experiment-4/exp-46.py`:**
```python
import RPi.GPIO as GPIO
import time

LEDS = [11, 13, 15]

GPIO.setwarnings(False)
GPIO.setmode(GPIO.BOARD)
GPIO.setup(LEDS, GPIO.OUT, initial=GPIO.LOW)

try:
    while True:
        for pin in LEDS:                  # 11, then 13, then 15
            GPIO.output(pin, GPIO.HIGH)   # this LED stays ON
            time.sleep(2)
        GPIO.output(LEDS, GPIO.LOW)       # all OFF together
        time.sleep(2)
except KeyboardInterrupt:
    pass
finally:
    GPIO.cleanup()
```

Timeline: 0 s LED 11 ON → 2 s LED 13 ON → 4 s LED 15 ON → 6 s all OFF → 8 s repeat.

**Report checklist:** 46.a (video with voice-over), 46.b (paste the program).

---

### Experiment 47 — Rotating Single LED (11 → 13 → 15 → 11 …), 2 s Each

Hardware is **identical to Experiment 45**.

| # | Connection |
|---|---|
| 1 | Pi pin **6** (GND) — `−` rail |
| 2 | Pi pins **11 / 13 / 15** — each through its own 220 Ω — LED anode; each cathode — `−` rail |

**Code — `experiment-4/exp-47.py`:**
```python
import RPi.GPIO as GPIO
import time

LEDS = [11, 13, 15]

GPIO.setwarnings(False)
GPIO.setmode(GPIO.BOARD)
GPIO.setup(LEDS, GPIO.OUT, initial=GPIO.LOW)

try:
    while True:
        for pin in LEDS:
            GPIO.output(LEDS, GPIO.LOW)   # turn every LED off
            GPIO.output(pin, GPIO.HIGH)   # then turn only this one on
            time.sleep(2)
except KeyboardInterrupt:
    pass
finally:
    GPIO.cleanup()
```

**Report checklist:** 47.a (video with voice-over), 47.b (paste the program — save it as a new file).

---

### Experiment 48 — Two Push Buttons (Pins 29, 31) Control the LEDs

Pressing a switch must send **logic 1** to the Pi, so each switch goes between **3.3 V** and
the input pin, and a **10 kΩ pull-down** resistor holds the pin at 0 V while the switch is open.
(The program also turns on the Pi's internal pull-down, `PUD_DOWN`, as a backup.)

| # | Connection |
|---|---|
| 1 | Pi pin **6** (GND) — blue `−` rail; Pi pin **1** (3.3 V) — red `+` rail |
| 2 | LEDs as in Experiment 45: pins **11 / 13 / 15** — 220 Ω — LED anode; cathodes — `−` rail |
| 3 | Switch 1 **Side A** — `+` rail (3.3 V) |
| 4 | Switch 1 **Side B** — Pi pin **29** (GPIO5) *(this row is the junction)* |
| 5 | Switch 1 junction (step 4) — 10 kΩ resistor — `−` rail (GND) |
| 6 | Switch 2 **Side A** — `+` rail (3.3 V) |
| 7 | Switch 2 **Side B** — Pi pin **31** (GPIO6) *(junction)* |
| 8 | Switch 2 junction (step 7) — 10 kΩ resistor — `−` rail (GND) |

> Use **3.3 V, never 5 V**, for the switches.

**Code — `experiment-4/exp-48.py`:**
```python
import RPi.GPIO as GPIO
import time

LED1, LED2, LED3 = 11, 13, 15
SW1, SW2 = 29, 31                # GPIO5, GPIO6

GPIO.setwarnings(False)
GPIO.setmode(GPIO.BOARD)
GPIO.setup([LED1, LED2, LED3], GPIO.OUT, initial=GPIO.LOW)
# switch gives 3.3 V (logic 1) when pressed, pull-down keeps it at 0 otherwise
GPIO.setup([SW1, SW2], GPIO.IN, pull_up_down=GPIO.PUD_DOWN)

try:
    while True:
        s1 = GPIO.input(SW1)
        s2 = GPIO.input(SW2)

        GPIO.output(LED1, s1)             # SW1 pressed -> LED on pin 11
        GPIO.output(LED2, s2)             # SW2 pressed -> LEDs on 13 and 15
        GPIO.output(LED3, s2)

        time.sleep(0.05)
except KeyboardInterrupt:
    pass
finally:
    GPIO.cleanup()
```

| Switch 29 | Switch 31 | LED 11 | LED 13 | LED 15 |
|---|---|---|---|---|
| released | released | OFF | OFF | OFF |
| **pressed** | released | **ON** | OFF | OFF |
| released | **pressed** | OFF | **ON** | **ON** |
| **pressed** | **pressed** | **ON** | **ON** | **ON** |

**Report checklist:** 48.a (video with voice-over — press each switch, then both), 48.b (paste the program).

---

### Experiment 49 — Inverted: All LEDs ON, Pressed Switch Turns Them OFF

Hardware is **identical to Experiment 48**.

| # | Connection |
|---|---|
| 1 | Same LEDs on pins **11 / 13 / 15** and same switches on pins **29 / 31** (3.3 V + 10 kΩ pull-down) as Experiment 48 |

**Code — `experiment-4/exp-49.py`:**
```python
import RPi.GPIO as GPIO
import time

LED1, LED2, LED3 = 11, 13, 15
SW1, SW2 = 29, 31

GPIO.setwarnings(False)
GPIO.setmode(GPIO.BOARD)
GPIO.setup([LED1, LED2, LED3], GPIO.OUT, initial=GPIO.HIGH)   # all ON at start
GPIO.setup([SW1, SW2], GPIO.IN, pull_up_down=GPIO.PUD_DOWN)

try:
    while True:
        s1 = GPIO.input(SW1)
        s2 = GPIO.input(SW2)

        # pressed (1) -> LED OFF, released (0) -> LED ON
        GPIO.output(LED1, GPIO.LOW if s1 else GPIO.HIGH)
        GPIO.output(LED2, GPIO.LOW if s2 else GPIO.HIGH)
        GPIO.output(LED3, GPIO.LOW if s2 else GPIO.HIGH)

        time.sleep(0.05)
except KeyboardInterrupt:
    pass
finally:
    GPIO.cleanup()
```

**Report checklist:** 49.a (video with voice-over), 49.b (paste the program), 49.c (changes vs. 48: `initial=GPIO.LOW` → `initial=GPIO.HIGH` so all LEDs start ON; each `GPIO.output(LED, s)` replaced by `GPIO.output(LED, GPIO.LOW if s else GPIO.HIGH)`, i.e. the switch value is inverted before it is written; hardware unchanged).

---

### Experiment 50 — Ultrasonic Sensor → ThingSpeak

The HC-SR04 needs 5 V, and its Echo pin outputs 5 V, so Echo goes through a **voltage divider**
(1 kΩ on top, 2 kΩ to ground) which gives 5 × 2 / (1 + 2) ≈ **3.3 V** at the Pi pin. If you
have no 2 kΩ resistor, use two 1 kΩ in series.

| # | Connection |
|---|---|
| 1 | Pi pin **6** (GND) — blue `−` rail |
| 2 | HC-SR04 **Vcc** — Pi pin **2** (5 V) |
| 3 | HC-SR04 **Gnd** — `−` rail |
| 4 | HC-SR04 **Trig** — Pi pin **16** (GPIO23) *(3.3 V from the Pi is enough to trigger it)* |
| 5 | HC-SR04 **Echo** — one end of the **1 kΩ** resistor |
| 6 | 1 kΩ other end — a free breadboard row *(the divider junction)* |
| 7 | Junction — **2 kΩ** resistor — `−` rail (GND) |
| 8 | Junction — Pi pin **18** (GPIO24) |
| 9 | Pi connected to the internet (Wi-Fi or LAN) |

**ThingSpeak:** log in at `thingspeak.mathworks.com` → **Channels → New Channel** → name it
(e.g. *Pi Ultrasonic*), tick **Field 1 = Distance (cm)** → Save. Copy the **Write API Key**
from the **API Keys** tab into `API_KEY` below.

**Code — `experiment-4/exp-50.py`:**
```python
import RPi.GPIO as GPIO
import time
import requests

API_KEY = "YOUR_WRITE_API_KEY"            # ThingSpeak channel -> API Keys tab
URL = "https://api.thingspeak.com/update"

TRIG = 16                                 # GPIO23
ECHO = 18                                 # GPIO24 (through the 1k/2k divider)

GPIO.setwarnings(False)
GPIO.setmode(GPIO.BOARD)
GPIO.setup(TRIG, GPIO.OUT, initial=GPIO.LOW)
GPIO.setup(ECHO, GPIO.IN)
time.sleep(2)                             # let the sensor settle


def get_distance():
    # 10 microsecond pulse on Trig starts one measurement
    GPIO.output(TRIG, GPIO.HIGH)
    time.sleep(0.00001)
    GPIO.output(TRIG, GPIO.LOW)

    timeout = time.time() + 0.05
    start = time.time()
    while GPIO.input(ECHO) == 0:          # wait for Echo to go HIGH
        start = time.time()
        if start > timeout:
            return None
    end = time.time()
    while GPIO.input(ECHO) == 1:          # wait for Echo to go LOW again
        end = time.time()
        if end > timeout:
            return None

    duration = end - start                # round trip time in seconds
    return round(duration * 34300 / 2, 2) # speed of sound 34300 cm/s


last_upload = 0

try:
    while True:
        distance = get_distance()
        if distance is None:
            print("No echo received")
        else:
            print("Distance:", distance, "cm")

            if time.time() - last_upload >= 15:   # free ThingSpeak: 1 update / 15 s
                try:
                    r = requests.get(URL, params={"api_key": API_KEY,
                                                  "field1": distance}, timeout=10)
                    print("Sent to ThingSpeak, entry:", r.text)
                    last_upload = time.time()
                except requests.RequestException as e:
                    print("Upload failed:", e)
        time.sleep(1)
except KeyboardInterrupt:
    pass
finally:
    GPIO.cleanup()
```

**How to observe it:** Thonny's Shell prints the distance every second; every 15 s it also
prints `Sent to ThingSpeak, entry: N` (N = entry number; **0 means the update was rejected**,
usually a wrong API key or sending faster than 15 s). Open the channel's **Private View** — the
Field 1 chart gains one point every 15 s. Move a book closer / farther to see the line change.

**Report checklist:** 50.a (video with voice-over — sensor, Shell output and the ThingSpeak chart), 50.b (paste the program).

---

### Experiment 51 — DHT22 Temperature & Humidity → ThingSpeak

| # | Connection (bare 4-pin DHT22) |
|---|---|
| 1 | DHT22 pin **1 (VCC)** — Pi pin **1** (3.3 V) |
| 2 | DHT22 pin **2 (DATA)** — Pi pin **7** (GPIO4) |
| 3 | 10 kΩ resistor between DHT22 pin **2 (DATA)** and pin **1 (VCC)** *(pull-up)* |
| 4 | DHT22 pin **3** — *not connected* |
| 5 | DHT22 pin **4 (GND)** — Pi pin **6** (GND) |

*(3-pin module: **+** → pin 1, **OUT** → pin 7, **−** → pin 6; no extra resistor.)*

**Library:** the virtual environment from Experiment 41 step 16
(`adafruit-circuitpython-dht`). Run the program with that interpreter.

**ThingSpeak:** new channel (e.g. *Pi DHT22*) with **Field 1 = Temperature (°C)** and
**Field 2 = Humidity (%)**.

**Code — `experiment-4/exp-51.py`:**
```python
import time
import requests
import board
import adafruit_dht

API_KEY = "YOUR_WRITE_API_KEY"
URL = "https://api.thingspeak.com/update"

dht = adafruit_dht.DHT22(board.D4)        # DATA on physical pin 7 (GPIO4)

try:
    while True:
        try:
            temperature = dht.temperature
            humidity = dht.humidity
        except RuntimeError as e:
            # DHT22 misses a reading now and then, just try again
            print("Reading failed:", e.args[0])
            time.sleep(2)
            continue

        if temperature is None or humidity is None:
            time.sleep(2)
            continue

        print("Temperature: {:.1f} C   Humidity: {:.1f} %".format(temperature, humidity))

        try:
            r = requests.get(URL, params={"api_key": API_KEY,
                                          "field1": temperature,
                                          "field2": humidity}, timeout=10)
            print("Sent to ThingSpeak, entry:", r.text)
        except requests.RequestException as e:
            print("Upload failed:", e)

        time.sleep(15)                    # ThingSpeak free limit
except KeyboardInterrupt:
    pass
finally:
    dht.exit()
```

**How to observe it:** the Shell prints temperature and humidity every 15 s (an occasional
`Reading failed: Checksum did not validate` is normal for the DHT22 — the program just retries).
Breathe on the sensor or hold it in your hand: humidity and temperature rise on both charts.

**Report checklist:** 51.a (video with voice-over — show both Field 1 and Field 2 charts), 51.b (paste the program).

---

### Experiment 52 — IR Obstacle Sensor → ThingSpeak

| # | Connection |
|---|---|
| 1 | IR module **VCC** — Pi pin **1** (3.3 V) *(powering it from 3.3 V keeps its OUT signal at 3.3 V)* |
| 2 | IR module **GND** — Pi pin **6** (GND) |
| 3 | IR module **OUT** — Pi pin **12** (GPIO18) |

Turn the blue trimmer on the module until its **obstacle LED** lights when your hand is about
10 cm away and goes off when you take it away.

**ThingSpeak:** new channel (e.g. *Pi IR Sensor*) with **Field 1 = Object detected (1/0)**.

**Code — `experiment-4/exp-52.py`:**
```python
import RPi.GPIO as GPIO
import time
import requests

API_KEY = "YOUR_WRITE_API_KEY"
URL = "https://api.thingspeak.com/update"

IR_PIN = 12                               # GPIO18, module OUT pin

GPIO.setwarnings(False)
GPIO.setmode(GPIO.BOARD)
GPIO.setup(IR_PIN, GPIO.IN)

last_upload = 0

try:
    while True:
        # module output is LOW when an object is in front of it
        detected = 1 if GPIO.input(IR_PIN) == GPIO.LOW else 0
        print("Object detected" if detected else "No object")

        if time.time() - last_upload >= 15:
            try:
                r = requests.get(URL, params={"api_key": API_KEY,
                                              "field1": detected}, timeout=10)
                print("Sent to ThingSpeak, entry:", r.text)
                last_upload = time.time()
            except requests.RequestException as e:
                print("Upload failed:", e)

        time.sleep(0.5)
except KeyboardInterrupt:
    pass
finally:
    GPIO.cleanup()
```

**How to observe it:** the Shell prints `Object detected` / `No object` twice a second. The
ThingSpeak chart is a step graph that sits at **1** while an object is in front of the sensor
during an upload and at **0** otherwise (hold your hand there for at least 15 s to be sure it
is caught).

**Report checklist:** 52.a (video with voice-over), 52.b (paste the program).

---

## 5. Quick Reference Summary

| Experiment | Input pin(s) | Output pin(s) | Extra hardware |
|---|---|---|---|
| 41 | — | — | microSD, power supply, monitor, keyboard, mouse |
| 42 | — | 11 | 1 LED + 220 Ω |
| 43 | — | 11 (20 % duty) | Same as 42 |
| 44 | — | 11 (drives LED 1 high-side, LED 2 low-side from 3.3 V) | 2 LEDs + 2 × 220 Ω |
| 45 | — | 11, 13, 15 (together) | 3 LEDs + 3 × 220 Ω |
| 46 | — | 11 → 13 → 15, then all off | Same as 45 |
| 47 | — | 11 → 13 → 15 (one at a time) | Same as 45 |
| 48 | 29, 31 (switches, active HIGH) | 11 / 13 + 15 | 3 LEDs + 2 switches + 2 × 10 kΩ |
| 49 | 29, 31 | 11 / 13 + 15 (inverted) | Same as 48 |
| 50 | 18 (Echo via 1k/2k divider) | 16 (Trig) + ThingSpeak | HC-SR04 |
| 51 | 7 (DHT22 DATA) | ThingSpeak (Field 1 + 2) | DHT22 + 10 kΩ pull-up |
| 52 | 12 (IR OUT, active LOW) | ThingSpeak | IR obstacle module |
