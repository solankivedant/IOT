import RPi.GPIO as GPIO
import time

LED1, LED2, LED3 = 11, 13, 15
SW1, SW2 = 29, 31                # GPIO5, GPIO6

GPIO.setwarnings(False)
GPIO.setmode(GPIO.BOARD)
GPIO.setup([LED1, LED2, LED3], GPIO.OUT, initial=GPIO.LOW)
# switch gives 3.3 V (logic 1) when pressed, pull-down keeps it at 0 otherwise
GPIO.setup([SW1, SW2], GPIO.IN, pull_up_down=GPIO.PUD_DOWN)

try:
    while True:
        s1 = GPIO.input(SW1)
        s2 = GPIO.input(SW2)

        GPIO.output(LED1, s1)             # SW1 pressed -> LED on pin 11
        GPIO.output(LED2, s2)             # SW2 pressed -> LEDs on 13 and 15
        GPIO.output(LED3, s2)

        time.sleep(0.05)
except KeyboardInterrupt:
    pass
finally:
    GPIO.cleanup()
