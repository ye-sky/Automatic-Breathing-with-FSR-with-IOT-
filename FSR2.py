import RPi.GPIO as GPIO
import time
GPIO.setmode(GPIO.BOARD)
delayt = .1 
value = 0 # this variable will be used to store the FSR value
fsr = 13 #FSR is connected with pin number 7
led = 11 #led is connected with pin number 11
GPIO.setup(led, GPIO.OUT) # as led is an output device so that’s why we set it to output.
GPIO.output(led, False) # keep led off by default 
def rc_time (fsr):
    count = 0
 
    #Output on the pin for
    GPIO.setup(fsr, GPIO.OUT)
    GPIO.output(fsr, False)
    time.sleep(delayt)
 
    #Change the pin back to input
    GPIO.setup(fsr, GPIO.IN)
 
    #Count until the pin goes high
    while (GPIO.input(fsr) == 0):
        count += 1
 
    return count
 
 
#Catch when script is interrupted, cleanup correctly
try:
    # Main loop
    while True:
        print("FSR Value:")
        value = rc_time(fsr)
       
        print(value)
        if ( value > 100 ):
                print("Lights are ON")
                GPIO.output(led, True)
        if (value <= 0):
                print("Lights are OFF")
                GPIO.output(led, False)
except KeyboardInterrupt:
    pass
finally:
    GPIO.cleanup()