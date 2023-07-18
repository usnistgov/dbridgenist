# -*- coding: utf-8 -*-
"""
Created on Fri Jul 14 10:17:05 2023

@author: wbalance
"""

import serial
import threading
import time
import ADS1263

dt = 0.002
N = 10
ADC = ADS1263.ADS1263()
if (ADC.ADS1263_init_ADC1('ADS1263_38400SPS') == -1):
    exit()
ADC.ADS1263_SetMode(0)
ADC.ADS1263_SetChannal(0)
data = []
ts = []
done = False
t0 = time.time()
ser = serial.Serial('/dev/ttyAMA0', 19200, timeout=1)

def int2float(num):
    if num >> 31 == 1: 
        ret = num / 0x80000000
    elif num >> 31 != 1:
        ret =  num / 0x7fffffff
    return round(ret, 6)

def float2int(num):
    if num>=0:
        ret = int(num*0x7fffffff)
    else:
        ret = int(-num*0x80000000)
    return ret

def encode(num):
    arr = bytearray()
    num = str(num)
    for x in num:
        arr.append(int(ord(x)))
    return arr

def reset():
    global data, ts, done, t0
    data = []
    ts = []
    done = False
    t0 = time.time()

def addData():
    global ser
    if not done:
        t2 = threading.Timer(N*dt,addData)
        t2.start()    
    if data:
        meas = int(data.pop(0))
        t = float2int(ts.pop(0))
        s = '{0} {1}'.format(t,meas)
        s = encode(s)
        length = len(s)
        length = encode(length)
        ser.write(length)
        ser.write(s)

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

while True:
    try:
        while True:
            conf = ser.read(7)
            while conf != b'pcready':
                conf = ser.read(7)
            ser.write(b'piready')
            reset()
            length = ser.read(2)
            while length == b'':
                length = ser.read(2)
            dt = ser.read(int(length.decode()))
            while dt == b'':
                dt = ser.read(int(length.decode()))
            dt = int2float(int(dt.decode()))
            t1 = threading.Timer(dt,getData)
            t2 = threading.Timer(N*dt,addData)
            t1.start()
            t2.start()
            conf = ser.read(4)
            while conf != b'done':
                conf = ser.read(4)
            done = True
    except Exception as e:
        e = "From pi: " + e
        ser.write(encode(len(encode(e))))
        ser.write(encode(e))