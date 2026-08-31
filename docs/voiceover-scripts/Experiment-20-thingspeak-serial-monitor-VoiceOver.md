# Experiment 20 — Potentiometer to Serial Monitor and ThingSpeak

## Voice-Over Script

**Word count:** 92  |  **Approx. read time:** 38 seconds (~145 wpm)

> Experiment twenty sends one sensor out to two destinations. The potentiometer stays on A-zero, but the local web server is gone; instead the sketch opens an Ethernet client connection straight to api-dot-thingspeak-dot-com and posts the reading to my channel's write A-P-I key every fifteen seconds, which is ThingSpeak's minimum update interval on the free tier. At the same time, Serial-dot-println writes the same value to the Serial Monitor every loop. Watch both side by side: the Serial Monitor updates instantly as I turn the knob, and the ThingSpeak chart catches up a few seconds later with the logged datapoint.
