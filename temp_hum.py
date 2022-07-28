import time
import board
import adafruit_dht
import Adafruit_DHT
# import thingspeak

# channel_id = 1369355 # put here the ID of the channel you created before
# write_key = 'HJQU6XZATJ4ODVWQ' # update the "WRITE KEY"
 
sensor = Adafruit_DHT.DHT11
pin = 22 #GPIO 22

humidity, temperature = Adafruit_DHT.read_retry(sensor, pin)

 
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
            "Body Temp: {:.1f} F / {:.1f} C Body Humidity: {}% ".format(
                temperature_f, temperature_c, humidity
            )
        )
     #   response = channel.update({'field1': temperature_c, 'field2': humidity})
    
     
    except RuntimeError as error:
        # Errors happen fairly often, DHT's are hard to read, just keep going
        print(error.args[0])
        time.sleep(3.0)
        continue
    except Exception as error:
        dhtDevice.exit()
        raise error
 
    time.sleep(3.0)
# if __name__ == "__main__":
#         channel = thingspeak.Channel(id=channel_id, write_key=write_key)
#         while True:
#             measure(channel)
#         #free account has a limitation of 15sec between the updates
#             time.sleep(15)    