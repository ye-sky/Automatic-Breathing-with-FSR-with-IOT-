import time
import board
import adafruit_dht
import Adafruit_DHT

import urllib.request
import requests
import threading
import json

sensor = Adafruit_DHT.DHT11
pin = 22 #GPIO 22

humidity, temperature = Adafruit_DHT.read_retry(sensor, pin)
dhtDevice = adafruit_dht.DHT11(board.D4, use_pulseio=False)
 
while True:
    try:
        # Print the values to the serial port
        temperature_c = dhtDevice.temperature
        temperature_f = temperature_c * (9 / 5) + 32
        humidity = dhtDevice.humidity
        print(
            "Body Temp: {:.1f} F / {:.1f} C Body Humidity: {}% ".format(
                temperature_f, temperature_c, humidity
            )
        )
     
    except RuntimeError as error:
        print(error.args[0])
        time.sleep(3.0)
        continue
    except Exception as error:
        dhtDevice.exit()
        raise error
 
    time.sleep(3.0)
    def thingspeak_post():
             threading.Timer(15,thingspeak_post).start()
             #val=random.randint(1,30)
             URl='https://api.thingspeak.com/update?api_key='
             KEY='HJQU6XZATJ4ODVWQ'
             HEADER='&field1={}&field2={}'.format(temperature_c,humidity)
             NEW_URL=URl+KEY+HEADER
             print(NEW_URL)
             data=urllib.request.urlopen(NEW_URL)
             print(data)
             
    if __name__ == '__main__':
               thingspeak_post() 