# -*- coding: utf-8 -*-
"""
Created on Fri Jul 14 10:17:05 2023

@author: wbalance
"""

import serial
import threading
import time
import ADS1263

dt = 0.001
data = []
ts = []
done = False
t0 = time.time()

def float2int(num):
    if num>=0:
        ret = int(num*0x7fffffff)
    else:
        ret = int(-num*0x80000000)
    return ret

def encode(num):
    arr = bytearray()
    num = "{0}".format(num)
    for x in num:
        arr.append(int(ord(x)))
    return arr

def reset():
    global data, ts, done, t0
    data = []
    ts = []
    done = False
    t0 = time.time()

def getData():
    global data, ts, done, ADC, t0
    if not done:
        t1 = threading.Timer(dt,getData)
        t1.start()
    now = time.time()
    rt = now - t0
    t1 = time.time()
    meas = ADC.ADS1263_Read_ADC_Data()
    t2 = time.time()
    rt = 0.5*(t1+t2)-t0
    data.append(meas)
    ts.append(rt)

ser = serial.Serial('/dev/ttyAMA0', 19200, timeout=1)    
while True:
    conf = ser.read(7)
    while conf != b'pcready':
        conf = ser.read(7)
    ser.write(b'piready')
    reset()
    t1 = threading.Timer(dt,getData)
    conf = ser.read(4)
    while conf != b'done':
        conf = ser.read(4)
    done = True
    