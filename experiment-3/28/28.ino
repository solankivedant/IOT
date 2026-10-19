import RPi.GPIO as GPIO
import time

LED_PIN = 11                     # physical pin 11 (GPIO17)

GPIO.setwarnings(False)
GPIO.setmode(GPIO.BOARD)         # use physical pin numbers
GPIO.setup(LED_PIN, GPIO.OUT, initial=GPIO.LOW)

try:
    while True:
        GPIO.output(LED_PIN, GPIO.HIGH)   # LED ON
        time.sleep(1)
        GPIO.output(LED_PIN, GPIO.LOW)    # LED OFF
        time.sleep(1)
except KeyboardInterrupt:
    pass
finally:
    GPIO.cleanup()
