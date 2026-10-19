import RPi.GPIO as GPIO
import time
import requests

API_KEY = "YOUR_WRITE_API_KEY"            # ThingSpeak channel -> API Keys tab
URL = "https://api.thingspeak.com/update"

TRIG = 16                                 # GPIO23
ECHO = 18                                 # GPIO24 (through the 1k/2k divider)

GPIO.setwarnings(False)
GPIO.setmode(GPIO.BOARD)
GPIO.setup(TRIG, GPIO.OUT, initial=GPIO.LOW)
GPIO.setup(ECHO, GPIO.IN)
time.sleep(2)                             # let the sensor settle


def get_distance():
    # 10 microsecond pulse on Trig starts one measurement
    GPIO.output(TRIG, GPIO.HIGH)
    time.sleep(0.00001)
    GPIO.output(TRIG, GPIO.LOW)

    timeout = time.time() + 0.05
    start = time.time()
    while GPIO.input(ECHO) == 0:          # wait for Echo to go HIGH
        start = time.time()
        if start > timeout:
            return None
    end = time.time()
    while GPIO.input(ECHO) == 1:          # wait for Echo to go LOW again
        end = time.time()
        if end > timeout:
            return None

    duration = end - start                # round trip time in seconds
    return round(duration * 34300 / 2, 2) # speed of sound 34300 cm/s


last_upload = 0

try:
    while True:
        distance = get_distance()
        if distance is None:
            print("No echo received")
        else:
            print("Distance:", distance, "cm")

            if time.time() - last_upload >= 15:   # free ThingSpeak: 1 update / 15 s
                try:
                    r = requests.get(URL, params={"api_key": API_KEY,
                                                  "field1": distance}, timeout=10)
                    print("Sent to ThingSpeak, entry:", r.text)
                    last_upload = time.time()
                except requests.RequestException as e:
                    print("Upload failed:", e)
        time.sleep(1)
except KeyboardInterrupt:
    pass
finally:
    GPIO.cleanup()
