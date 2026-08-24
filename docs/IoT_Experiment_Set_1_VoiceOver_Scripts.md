# IoT Experiment Set 1 — Voice-Over Scripts

*Arduino UNO · Experiments 1–10 · Narration for the demonstration videos*

Each script runs 70–80 words (~30 seconds at a natural pace). Numbers are spelled out for narration. Total: 726 words.

---

## Experiment 1 — Blink (Pin 13)

*74 words · approx. 31 seconds*

> Experiment one: the classic blink. A single LED sits in series with a two-twenty ohm resistor, anode side going to digital pin thirteen, cathode straight to ground. The resistor limits current to about twenty milliamps, protecting the LED. In code, setup runs once and sets pin thirteen as an output. Loop then repeats forever: drive the pin high, wait one second, drive it low, wait again. Notice the onboard L LED blinking in step.

---

## Experiment 2 — 40% Duty Cycle (Pin 13)

*78 words · approx. 32 seconds*

> Experiment two: a forty percent duty cycle. The wiring is unchanged from experiment one — LED and resistor in series on pin thirteen. Only the timing moves. Instead of a symmetric one second on, one second off, the pin now stays high for four hundred milliseconds and low for six hundred. The period is still one second, so duty cycle equals four hundred over one thousand — forty percent. The blink now looks noticeably shorter on than off.

---

## Experiment 3 — Two LEDs, Complementary Duty Cycles

*73 words · approx. 30 seconds*

> Experiment three: complementary duty cycles from one pin. The code is untouched. LED one still runs from pin thirteen to ground, lighting on the high phase — forty percent. LED two is reversed: its anode goes through a resistor to five volts, and its cathode ties to the same pin thirteen node. It only conducts when pin thirteen sinks current, that is when the pin is low — so it lights sixty percent.

---

## Experiment 4 — Fade (Pin 9, PWM)

*72 words · approx. 30 seconds*

> Experiment four: fading with PWM. The LED moves to pin nine, marked with a tilde, because only the timer-backed pins three, five, six, nine, ten and eleven support analogWrite. Each loop writes the current brightness, then adds five. When brightness reaches zero or two fifty-five, the sign of fadeAmount flips, so the value bounces between the limits. A thirty millisecond delay makes the ramp smooth rather than instant. The LED breathes continuously.

---

## Experiment 5 — Blink and Fade Simultaneously

*71 words · approx. 30 seconds*

> Experiment five: blinking and fading at the same time. Two branches now — LED A on pin thirteen, LED B on pin nine, each with its own resistor to ground. The key change is in software. Pin thirteen no longer uses delay, which would freeze the fade. Instead millis is compared against a stored timestamp, and the state toggles every thousand milliseconds while the fade keeps stepping smoothly on pin nine.

---

## Experiment 6 — Blink 4 LEDs Together

*73 words · approx. 30 seconds*

> Experiment six: four LEDs blinking together. Each LED gets its own resistor and its own pin — thirteen, eleven, nine and seven — with all four cathodes returning to ground. In code the pins live in an array, so a single for loop sets every pin as an output in setup. The loop then drives all four high, waits a second, drives all four low, and waits again. They blink in perfect unison.

---

## Experiment 7 — Sequential ON, Then All OFF

*70 words · approx. 29 seconds*

> Experiment seven: a staggered switch-on. The hardware is identical to experiment six — same four LEDs on pins thirteen, eleven, nine and seven. Only the sequencing changes. The first for loop now turns each LED on one at a time, pausing two seconds between them, so they accumulate until all four are lit. A second loop then clears every pin together, and after another two second pause the cycle restarts.

---

## Experiment 8 — Rotating Single LED

*72 words · approx. 30 seconds*

> Experiment eight: a single travelling light. Wiring is unchanged again — four LEDs on pins thirteen, eleven, nine and seven. The difference is that the turn-off now happens inside the same loop iteration. Each pass drives one pin high, waits two seconds, then immediately drives it low before moving to the next. Only one LED is ever lit, so the light appears to rotate across the row continuously, a classic chaser pattern.

---

## Experiment 9 — Push Button Controls LED

*70 words · approx. 29 seconds*

> Experiment nine: reading a push button. The LED stays on pin thirteen. The button's side A legs go to five volts, side B goes to pin two and also through a pull-down resistor to ground. That resistor holds pin two at a defined LOW when nothing is pressed. Pressing bridges the sides, so five volts reaches pin two and digitalRead returns HIGH. The code mirrors that state onto the LED.

---

## Experiment 10 — Push Button Turns LED Off, Otherwise ON

*73 words · approx. 30 seconds*

> Experiment ten: inverting the button logic. Not a single wire changes from experiment nine — same LED on pin thirteen, same button and pull-down resistor on pin two. Only the two branches of the if statement are swapped. Now a HIGH reading, meaning the button is pressed, writes LOW and switches the LED off; releasing it returns pin two to LOW and the LED comes back on. A software-only inversion of the behaviour.

---

