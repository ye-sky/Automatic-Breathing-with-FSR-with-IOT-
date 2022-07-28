import pyaudio
import math
import struct
import wave
import time
import os
import RPi.GPIO as GPIO
import json
import requests


GPIO.setmode(GPIO.BOARD)
delayt = .1 
value = 0 # this variable will be used to store the FSR value
fsr = 13 #FSR is connected with pin number 7
led = 11 #led is connected with pin number 11
GPIO.setup(led, GPIO.OUT) # as led is an output device so that’s why we set it to output.
GPIO.output(led, False) # keep led off by default 

Threshold = 0 #250 is best

SHORT_NORMALIZE = (1.0/32768.0)
chunk = 1024
FORMAT = pyaudio.paInt16
CHANNELS = 1
RATE = 16000
swidth = 2

TIMEOUT_LENGTH = 1

f_name_directory = r'/home/pi/Desktop/project'

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


class Recorder:

    @staticmethod
    def rms(frame):
        count = len(frame) / swidth
        format = "%dh" % (count)
        shorts = struct.unpack(format, frame)

        sum_squares = 0.0
        for sample in shorts:
            n = sample * SHORT_NORMALIZE
            sum_squares += n * n
        rms = math.pow(sum_squares / count, 0.5)

        return rms * 1000

    def __init__(self):
        self.p = pyaudio.PyAudio()
        self.stream = self.p.open(format=FORMAT,
                                  channels=CHANNELS,
                                  rate=RATE,
                                  input=True,
                                  output=True,
                                  frames_per_buffer=chunk)

    def record(self):
        print('Snore detected, recording beginning and Taking initiative')
        rec = []
        current = time.time()
        end = time.time() + TIMEOUT_LENGTH

        while current <= end:

            data = self.stream.read(chunk)
            if rc_time(fsr) <= Threshold: end = time.time() + TIMEOUT_LENGTH

            current = time.time()
            rec.append(data)
        self.write(b''.join(rec))

    def write(self, recording):
        n_files = len(os.listdir(f_name_directory))

        filename = os.path.join(f_name_directory, '{}.wav'.format(n_files))

        wf = wave.open(filename, 'wb')
        wf.setnchannels(CHANNELS)
        wf.setsampwidth(self.p.get_sample_size(FORMAT))
        wf.setframerate(RATE)
        wf.writeframes(recording)
        wf.close()
        print('Written to file: {}'.format(filename))
        print(filename)
        print(n_files)
        print(format(filename))
        print('Returning to listening')
        headers = {"Authorization": "Bearer ya29.a0AfH6SMDIRxrjF_z06LmuQ2bbOz7DM5yHMquUsTUo00OzQ1cqrqtkCsrM-07_WfXH5naQ3cZ-UgMBdp0GIHPafJeiiI2siQSDDvtpsXKFL61DIYWOQeAVrMKF_W98W07DT2ixeu_7GZeC6ZhmsT_kMGfK0xjh"}
        para = {
                 "name": filename.format(filename),
                 "parents": ["16Xqs2DNb9VGj6d9QpJZ79xW17NjWZsMd"]
               }
        files = {
           'data': ('metadata', json.dumps(para), 'application/json; charset=UTF-8'),
           'file': open(filename.format(filename), "rb")
               }
        r = requests.post(
           "https://www.googleapis.com/upload/drive/v3/files?uploadType=multipart",
            headers=headers,
            files=files
                     )
        print(r.text)
        
        
    def listen(self):
        print('Listening beginning')
        input = self.stream.read(chunk)
        rms_val = self.rms(input)
        self.record()
                
                
# def rc_time (fsr):
#         count = 0
#  
#     #Output on the pin for
#         GPIO.setup(fsr, GPIO.OUT)
#         GPIO.output(fsr, False)
#         time.sleep(delayt)
#  
#     #Change the pin back to input
#         GPIO.setup(fsr, GPIO.IN)
#  
#     #Count until the pin goes high
#         while (GPIO.input(fsr) == 0):
#               count += 1
#  
#         return count
 
 
#Catch when script is interrupted, cleanup correctly
try:
    # Main loop
       while True:
         print("FSR Value:")
         value = rc_time(fsr)
         
         print(value)
         time.sleep(3)
         if ( value > 100 ):
                print("Lights are ON and not recording")
                GPIO.output(led, True)
         if (value <= 0):
                print("Lights are OFF and recording")
                GPIO.output(led, False)
                a = Recorder()
                a.listen()

          
except KeyboardInterrupt:
         pass
finally:
         GPIO.cleanup()

#     def listen(self):
#         print('Listening beginning')
#         while True:
#             input = self.stream.read(chunk)
#             rms_val = self.rms(input)
#             if value <= 0:
#                 self.record()
# 
# a = Recorder()
# 
# a.listen()