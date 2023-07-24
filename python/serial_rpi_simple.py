# -*- coding: utf-8 -*-
"""
Created on Fri Jul 14 10:17:05 2023

@author: wbalance
"""

import serial
import threading
import time
import ADS1263
import struct

dt = 0.0012
N = 10
n = 0
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

def float2int(num, REF):
    if num>=0:
        ret = int(num / REF * 0x7fffffff)
    else:
        ret = int(-num / REF * 0x80000000)
    return ret

def reset():
    global data, ts, done, dt
    data = []
    ts = []
    done = False
    dt = 0.006

def getData():
    global data, ts, done, ADC, t0, ser, n
    if not done:
        t1 = threading.Timer(dt,getData)
        t1.start()
    now = time.time()
    rt = now - t0
    t1 = time.time()
    meas = int(ADC.ADS1263_Read_ADC_Data())
    t2 = time.time()
    rt = 0.5*(t1+t2)-t0
    t0 += rt
    t = float2int(rt, 5)
    ret = struct.pack('>l', t) + struct.pack('>l', meas) + struct.pack('>l', n)
    n += 1
    ser.write(ret)

while True:
    try:
        while True:
            conf = ser.read(7)
            while conf != b'pcready':
                conf = ser.read(7)
            ser.write(b'piready')
            reset()
            t0 = time.time()
            t1 = threading.Timer(dt,getData)
            t1.start()
            conf = ser.read(4)
            while conf != b'done':
                conf = ser.read(4)
            done = True
    except Exception as e:
        print(e)
        break
