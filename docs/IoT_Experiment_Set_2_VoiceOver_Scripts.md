# IoT Experiment Set 2 — Voice-Over Scripts

*Arduino UNO · Experiments 14–20 · Narration for the demonstration videos*

Experiments 11–13 (multimeter-only component review and measurements) have no
demonstration video and so no voice-over script. Each script below runs 76–98 words
(~31–41 seconds at ~145 wpm). Numbers are spelled out for narration. Total: 597 words.

---

## Experiment 14 — Blink Rate Follows Potentiometer Position

*88 words · approx. 36 seconds*

> Experiment fourteen replaces a fixed timer with a live sensor. The potentiometer's two outer legs sit across five volts and ground, turning it into a variable voltage divider; the middle leg, the wiper, feeds analog pin A-zero. In code, analog-read samples that pin as a number from zero to one-thousand-twenty-three, ten-bit resolution. That value becomes the delay for the LED on pin thirteen — high, delay, low, delay. Turn the knob toward five volts and the delay grows, so the blink slows down; turn it the other way and the blink speeds up.

---

## Experiment 15 — LED Intensity Follows Potentiometer Position

*84 words · approx. 35 seconds*

> Experiment fifteen keeps the same potentiometer wiring on A-zero but swaps the effect. The LED now sits on pin nine, a PWM-capable pin, because we're using analog-write instead of delay. The code reads the sensor as before, then maps that zero-to-one-thousand-twenty-three range down to zero-to-two-fifty-five, the range analog-write understands. So instead of the LED blinking faster or slower, it now glows dimmer or brighter in real time as the knob turns — no blinking at all, just smoothly varying brightness.

---

## Experiment 16 — Blink Rate Follows Light Intensity

*80 words · approx. 33 seconds*

> Experiment sixteen swaps the potentiometer for a light-dependent resistor. The LDR runs from five volts into a fixed resistor that drops to ground, and the junction between them feeds A-zero — exactly the same divider idea as before, just built from a light sensor instead of a knob. The code itself is untouched from experiment fourteen. Watch what happens when I shade the LDR versus shine a torch on it: more light means lower LDR resistance, a different voltage at A-zero, and a visibly different blink rate.

---

## Experiment 17 — LED Intensity Follows Light Intensity

*76 words · approx. 31 seconds*

> Experiment seventeen combines the last two changes. Hardware-wise it's experiment sixteen's LDR divider feeding A-zero, but the LED has moved to PWM pin nine, and the code maps the sensor reading to analog-write just like experiment fifteen. The result: LED brightness now tracks ambient light directly. Cover the LDR and the LED responds one way; shine a bright light on it and the brightness shifts the other way — a simple light-reactive dimmer built entirely from what we've already wired.

---

## Experiment 18 — Ethernet Shield: Web Page Showing Analog Inputs

*98 words · approx. 41 seconds*

> Experiment eighteen brings networking into the picture. The Ethernet shield stacks directly onto the Arduino, borrowing pins ten through thirteen internally for SPI communication with its W-five-one-double-oh chip, so those pins are off-limits for anything else. In code, Ethernet-dot-begin brings the interface up with a MAC address and an IP address, and a server object listens on port eighty. Every time a browser connects, the sketch loops through all six analog pins and writes their live readings straight into an HTML page. Refresh the browser, and you're watching the Arduino's sensors update over your actual network.

---

## Experiment 19 — Web Page Shows Only Two Labelled Sensors

*79 words · approx. 33 seconds*

> Experiment nineteen trims experiment eighteen's page down to exactly two readings. The LDR divider now feeds A-one and the potentiometer's wiper moves to A-four, and the code drops the loop over all six pins in favor of two explicit, labelled prints: "the current LDR value is," and "the current potentiometer value is." Refresh the page while I change the light on the sensor and turn the knob, and you'll see both labelled numbers update independently, live over the network.

---

## Experiment 20 — Potentiometer to Serial Monitor and ThingSpeak

*92 words · approx. 38 seconds*

> Experiment twenty sends one sensor out to two destinations. The potentiometer stays on A-zero, but the local web server is gone; instead the sketch opens an Ethernet client connection straight to api-dot-thingspeak-dot-com and posts the reading to my channel's write A-P-I key every fifteen seconds, which is ThingSpeak's minimum update interval on the free tier. At the same time, Serial-dot-println writes the same value to the Serial Monitor every loop. Watch both side by side: the Serial Monitor updates instantly as I turn the knob, and the ThingSpeak chart catches up a few seconds later with the logged datapoint.

---
