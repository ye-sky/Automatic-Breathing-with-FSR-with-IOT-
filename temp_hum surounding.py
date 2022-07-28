
import Adafruit_DHT

sensor = Adafruit_DHT.DHT11
pin = 4 #GPIO 4

humidity, temperature = Adafruit_DHT.read_retry(sensor, pin)
import time
import board
import adafruit_dht
 
# Initial the dht device, with data pin connected to:
# dhtDevice = adafruit_dht.DHT22(board.D4)
 
# you can pass DHT22 use_pulseio=False if you wouldn't like to use pulseio.
# This may be necessary on a Linux single board computer like the Raspberry Pi,
# but it will not work in CircuitPython.
dhtDevice = adafruit_dht.DHT11(board.D4, use_pulseio=False)
 
while True:
    try:
        # Print the values to the serial port
        temperature_c = dhtDevice.temperature
        temperature_f = temperature_c * (9 / 5) + 32
        humidity = dhtDevice.humidity
        print(
            "Room Temp: {:.1f} F / {:.1f} C Room Humidity: {}% ".format(
                temperature_f, temperature_c, humidity
            )
        )

    except RuntimeError as error:
        # Errors happen fairly often, DHT's are hard to read, just keep going
        print(error.args[0])
        time.sleep(3.0)
        continue
    except Exception as error:
        dhtDevice.exit()
        raise error
 
    time.sleep(3.0)