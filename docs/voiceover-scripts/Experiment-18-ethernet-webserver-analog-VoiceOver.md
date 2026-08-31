# Experiment 18 — Ethernet Shield: Web Page Showing Analog Inputs

## Voice-Over Script

**Word count:** 98  |  **Approx. read time:** 41 seconds (~145 wpm)

> Experiment eighteen brings networking into the picture. The Ethernet shield stacks directly onto the Arduino, borrowing pins ten through thirteen internally for SPI communication with its W-five-one-double-oh chip, so those pins are off-limits for anything else. In code, Ethernet-dot-begin brings the interface up with a MAC address and an IP address, and a server object listens on port eighty. Every time a browser connects, the sketch loops through all six analog pins and writes their live readings straight into an HTML page. Refresh the browser, and you're watching the Arduino's sensors update over your actual network.
