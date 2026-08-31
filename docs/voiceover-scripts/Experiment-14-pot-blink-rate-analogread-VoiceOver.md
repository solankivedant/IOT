# Experiment 14 — Blink Rate Follows Potentiometer Position

## Voice-Over Script

**Word count:** 88  |  **Approx. read time:** 36 seconds (~145 wpm)

> Experiment fourteen replaces a fixed timer with a live sensor. The potentiometer's two outer legs sit across five volts and ground, turning it into a variable voltage divider; the middle leg, the wiper, feeds analog pin A-zero. In code, analog-read samples that pin as a number from zero to one-thousand-twenty-three, ten-bit resolution. That value becomes the delay for the LED on pin thirteen — high, delay, low, delay. Turn the knob toward five volts and the delay grows, so the blink slows down; turn it the other way and the blink speeds up.
