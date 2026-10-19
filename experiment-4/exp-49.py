import RPi.GPIO as GPIO
import time

LED1, LED2, LED3 = 11, 13, 15
SW1, SW2 = 29, 31

GPIO.setwarnings(False)
GPIO.setmode(GPIO.BOARD)
GPIO.setup([LED1, LED2, LED3], GPIO.OUT, initial=GPIO.HIGH)   # all ON at start
GPIO.setup([SW1, SW2], GPIO.IN, pull_up_down=GPIO.PUD_DOWN)

try:
    while True:
        s1 = GPIO.input(SW1)
        s2 = GPIO.input(SW2)

        # pressed (1) -> LED OFF, released (0) -> LED ON
        GPIO.output(LED1, GPIO.LOW if s1 else GPIO.HIGH)
        GPIO.output(LED2, GPIO.LOW if s2 else GPIO.HIGH)
        GPIO.output(LED3, GPIO.LOW if s2 else GPIO.HIGH)

        time.sleep(0.05)
except KeyboardInterrupt:
    pass
finally:
    GPIO.cleanup()
