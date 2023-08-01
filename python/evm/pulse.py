#!/usr/bin/python3
import ADC
import RPi.GPIO as GPIO
import serial
import threading
import struct

REF = 4.774
START = 6
toread = []
adc = ADC.ADC(REF, 1)
GPIO.setmode(GPIO.BCM)
GPIO.setup(START, GPIO.OUT)
done = False
ser = serial.Serial('/dev/ttyAMA0', 19200, timeout=1)
        
def int2float(num, REF):
    tmp = 0x100000000
    if num >> 31 == 1:
        return -(tmp-num) * REF / 0x80000000
    else:
        return num * REF / 0x7fffffff

def collecting():
    global done
    
    conf = ser.read(4)
    while conf != b'done':
        conf = ser.read(4)
    done = True

while True:
    
    done = False
    conf = ser.read(7)
    while conf != b'pcready':
        conf = ser.read(7)
    ser.write(b'piready')
    t1 = threading.Thread(target=collecting)
    t1.start()
    
    try:
        while not done:
            adc.wait_drdy()
            val = adc.read_adc()
            ret = struct.pack('>l', val)
            ser.write(ret)
            #print(int2float(val, REF), end = '\r')
         
        t1.join()
        
    except Exception as e:
        print(e)
        GPIO.cleanup()
