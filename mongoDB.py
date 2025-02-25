import Adafruit_DHT
import pymongo
import time


DHT_SENSOR = Adafruit_DHT.DHT11
DHT_PIN = 21

SSID = 'Kuro:)'
PASSWORD = 'ny3ny3wj3l3k'


wlan = network.WLAN(network.STA_IF)
wlan.active(True)

print("Connecting to WiFi", end="")
wlan.connect(SSID, PASSWORD)

while not wlan.isconnected():
    print(".", end="")
    time.sleep(0.5)

print(" Connected!")
print("IP Address:", wlan.ifconfig()[0])

mongo_client = pymongo.MongoClient("mongodb+srv://izazn07:<db_password>@kitabisa.ptg0x.mongodb.net/?retryWrites=true&w=majority&appName=KitaBISA")
db = mongo_client["sensor_data"]  # Nama database
collection = db["readings"]  # Nama koleksi

try:
    while True:
        humidity, temperature = Adafruit_DHT.read_retry(DHT_SENSOR, DHT_PIN)

        if humidity is not None and temperature is not None:
            print(f'Temperature={temperature:.1f}°C  Humidity={humidity:.1f}%')

            data = {
                "temperature": temperature,
                "humidity": humidity,
                "timestamp": time.time()
            }
            collection.insert_one(data)
            print("Data saved to MongoDB")

        else:
            print("Failed to retrieve data from humidity sensor")

        time.sleep(5)

except KeyboardInterrupt:
    print("Program dihentikan.")
except Exception as e:
    print(f"Terjadi kesalahan: {e}")