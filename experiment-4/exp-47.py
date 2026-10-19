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
