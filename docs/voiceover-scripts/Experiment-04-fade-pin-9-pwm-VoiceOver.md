# Experiment 4 — Fade (Pin 9, PWM)

## Voice-Over Script

**Word count:** 72  |  **Approx. read time:** 30 seconds (~145 wpm)

> Experiment four: fading with PWM. The LED moves to pin nine, marked with a tilde, because only the timer-backed pins three, five, six, nine, ten and eleven support analogWrite. Each loop writes the current brightness, then adds five. When brightness reaches zero or two fifty-five, the sign of fadeAmount flips, so the value bounces between the limits. A thirty millisecond delay makes the ramp smooth rather than instant. The LED breathes continuously.
