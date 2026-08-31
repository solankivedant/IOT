# Experiment 15 — LED Intensity Follows Potentiometer Position

## Voice-Over Script

**Word count:** 84  |  **Approx. read time:** 35 seconds (~145 wpm)

> Experiment fifteen keeps the same potentiometer wiring on A-zero but swaps the effect. The LED now sits on pin nine, a PWM-capable pin, because we're using analog-write instead of delay. The code reads the sensor as before, then maps that zero-to-one-thousand-twenty-three range down to zero-to-two-fifty-five, the range analog-write understands. So instead of the LED blinking faster or slower, it now glows dimmer or brighter in real time as the knob turns — no blinking at all, just smoothly varying brightness.
