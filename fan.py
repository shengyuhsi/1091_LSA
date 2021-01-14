import os
import Adafruit_DHT
import time
DHT_SENSOR = Adafruit_DHT.DHT22
DHT_PIN = 4
while True:
    humidity,temperature =  Adafruit_DHT.read_retry(DHT_SENSOR,DHT_PIN)
    if(temperature >= 30):
        os.system('sudo ./uhubctl -l 1-1 -p 2 -a on')
    if(temperature <= 25):
        os.system('sudo ./uhubctl -l 1-1 -p 2 -a off')
time.sleep(5000)