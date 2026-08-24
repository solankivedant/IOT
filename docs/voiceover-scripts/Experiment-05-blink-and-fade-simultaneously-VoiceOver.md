# Experiment 5 — Blink and Fade Simultaneously

## Voice-Over Script

**Word count:** 71  |  **Approx. read time:** 30 seconds (~145 wpm)

> Experiment five: blinking and fading at the same time. Two branches now — LED A on pin thirteen, LED B on pin nine, each with its own resistor to ground. The key change is in software. Pin thirteen no longer uses delay, which would freeze the fade. Instead millis is compared against a stored timestamp, and the state toggles every thousand milliseconds while the fade keeps stepping smoothly on pin nine.
