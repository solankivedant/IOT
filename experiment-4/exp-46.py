import RPi.GPIO as GPIO
import time

LEDS = [11, 13, 15]

GPIO.setwarnings(False)
GPIO.setmode(GPIO.BOARD)
GPIO.setup(LEDS, GPIO.OUT, initial=GPIO.LOW)

try:
    while True:
        for pin in LEDS:                  # 11, then 13, then 15
            GPIO.output(pin, GPIO.HIGH)   # this LED stays ON
            time.sleep(2)
        GPIO.output(LEDS, GPIO.LOW)       # all OFF together
        time.sleep(2)
except KeyboardInterrupt:
    pass
finally:
    GPIO.cleanup()
