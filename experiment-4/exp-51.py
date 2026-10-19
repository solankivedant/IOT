import time
import requests
import board
import adafruit_dht

API_KEY = "YOUR_WRITE_API_KEY"
URL = "https://api.thingspeak.com/update"

dht = adafruit_dht.DHT22(board.D4)        # DATA on physical pin 7 (GPIO4)

try:
    while True:
        try:
            temperature = dht.temperature
            humidity = dht.humidity
        except RuntimeError as e:
            # DHT22 misses a reading now and then, just try again
            print("Reading failed:", e.args[0])
            time.sleep(2)
            continue

        if temperature is None or humidity is None:
            time.sleep(2)
            continue

        print("Temperature: {:.1f} C   Humidity: {:.1f} %".format(temperature, humidity))

        try:
            r = requests.get(URL, params={"api_key": API_KEY,
                                          "field1": temperature,
                                          "field2": humidity}, timeout=10)
            print("Sent to ThingSpeak, entry:", r.text)
        except requests.RequestException as e:
            print("Upload failed:", e)

        time.sleep(15)                    # ThingSpeak free limit
except KeyboardInterrupt:
    pass
finally:
    dht.exit()
