import RPi.GPIO as GPIO
import time

LEDS = [11, 13, 15]              # GPIO17, GPIO27, GPIO22

GPIO.setwarnings(False)
GPIO.setmode(GPIO.BOARD)
GPIO.setup(LEDS, GPIO.OUT, initial=GPIO.LOW)

try:
    while True:
        GPIO.output(LEDS, GPIO.HIGH)      # all three ON together
        time.sleep(1)
        GPIO.output(LEDS, GPIO.LOW)       # all three OFF together
        time.sleep(1)
except KeyboardInterrupt:
    pass
finally:
    GPIO.cleanup()
