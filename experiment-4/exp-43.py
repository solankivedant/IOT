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
