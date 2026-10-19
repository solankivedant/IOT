import RPi.GPIO as GPIO
import time
import requests

API_KEY = "YOUR_WRITE_API_KEY"
URL = "https://api.thingspeak.com/update"

IR_PIN = 12                               # GPIO18, module OUT pin

GPIO.setwarnings(False)
GPIO.setmode(GPIO.BOARD)
GPIO.setup(IR_PIN, GPIO.IN)

last_upload = 0

try:
    while True:
        # module output is LOW when an object is in front of it
        detected = 1 if GPIO.input(IR_PIN) == GPIO.LOW else 0
        print("Object detected" if detected else "No object")

        if time.time() - last_upload >= 15:
            try:
                r = requests.get(URL, params={"api_key": API_KEY,
                                              "field1": detected}, timeout=10)
                print("Sent to ThingSpeak, entry:", r.text)
                last_upload = time.time()
            except requests.RequestException as e:
                print("Upload failed:", e)

        time.sleep(0.5)
except KeyboardInterrupt:
    pass
finally:
    GPIO.cleanup()
