import network
import socket
import time
import dht
import machine
import ujson


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
#=======================================================================================================
UBIDOTS_TOKEN = 'BBUS-KT8bnRLiS4SJd0IcTWYZMPP1k5MTuj'
TEMPERATURE_VARIABLE_ID = '67bcb416aa22bd000e55526d'  # ID variabel untuk suhu
HUMIDITY_VARIABLE_ID = '67bcb44ef56124000d706bd9'     # ID variabel untuk kelembapan

dht_pin = machine.Pin(15)
sensor = dht.DHT11(dht_pin)
#=======================================================================================================
def send_to_ubidots(temperature, humidity):
    # Kirim data suhu
    url_temp = "http://industrial.api.ubidots.com/api/v1.6/variables/{}/values/?token={}".format(TEMPERATURE_VARIABLE_ID, UBIDOTS_TOKEN)
    payload_temp = '{{"value": {}}}'.format(temperature)

    # Kirim data kelembapan
    url_hum = "http://industrial.api.ubidots.com/api/v1.6/variables/{}/values/?token={}".format(HUMIDITY_VARIABLE_ID, UBIDOTS_TOKEN)
    payload_hum = '{{"value": {}}}'.format(humidity)

    try:
        s = socket.socket()
        s.connect(("industrial.api.ubidots.com", 80))

        # Kirim data suhu
        s.send(b"POST " + url_temp.encode() + b" HTTP/1.1\r\n")
        s.send(b"Host: industrial.api.ubidots.com\r\n")
        s.send(b"Content-Type: application/json\r\n")
        s.send(b"Content-Length: " + str(len(payload_temp)).encode() + b"\r\n")
        s.send(b"\r\n")
        s.send(payload_temp.encode())

        # Kirim data kelembapan
        s.send(b"POST " + url_hum.encode() + b" HTTP/1.1\r\n")
        s.send(b"Host: industrial.api.ubidots.com\r\n")
        s.send(b"Content-Type: application/json\r\n")
        s.send(b"Content-Length: " + str(len(payload_hum)).encode() + b"\r\n")
        s.send(b"\r\n")
        s.send(payload_hum.encode())

        s.close()
        print("Data sent to Ubidots")
    except Exception as e:
        print("Failed to send data:", e)
#===========================================================================
while True:
    try:
        sensor.measure()
        temperature = sensor.temperature()
        humidity = sensor.humidity()
        
        print("Temperature: {}°C, Humidity: {}%".format(temperature, humidity))
        
        send_to_ubidots(temperature, humidity)
        
        time.sleep(5)
    except Exception as e:
        print("Error reading sensor:", e)
        time.sleep(5)