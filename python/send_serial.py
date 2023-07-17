#!/usr/bin/python
# -*- coding: utf-8 -*-
"""
Created on Wed Jun 28 13:40:03 2023

@author: wbalance
"""

import time
import numpy as np
import threading
import os
import serial

done = False
while not done:
    simulate=input("Simulate? ")
    if simulate.lower() == "y" or simulate.lower() == "yes" or simulate.lower() == "true":
        simulate = True
        done  = True
    elif simulate.lower() == "n" or simulate.lower() == "no" or simulate.lower() == "false":
        simulate = False
        done = True
    else:
        print("Invalid")
        
time1 = input("Time: ")
time1 = time1.split(":")
time1 = 3600*int(time1[0])+60*int(time1[1])+int(time1[2])
print(time1, type(time1))

if not simulate:
    freq = float(input("Frequency: "))
    import ADS1263
    import RPi.GPIO as GPIO
    import config
    
    ADC = ADS1263.ADS1263()
    if (ADC.ADS1263_init_ADC1('ADS1263_38400SPS') == -1):
        exit()
    ADC.ADS1263_SetMode(0)
    ADC.ADS1263_SetChannal(0)
 
done = False
data = []
ts   = []
start_time = time.time()
REF = 4.76
writing = False
dt = 0.0003
end = False
N =10
minN=5
gain = 1.013654
cs_pin = 22
sim_a = 1
sim_o = 1
sim_p =np.pi/4
sim_f = 1
gco = 1
#1/100/0.0001=
#if simulate:
#    chunkN = 1.0/float(sim_f)/dt
#else:
#    chunkN = 1.0/float(freq)/dt
chunkN = 100
t0= time.time()
sim_vnoise =1e-3
sim_anoise = 1e-3
sim_onoise = 1e-3
sim_pnoise = 0
sim_fnoise = 0

def int2float(meas,REF):
    if meas >> 31 == 1: 
        ret =  REF*2  - meas * REF / 0x80000000
    elif meas >> 31 != 1:
        ret =  meas * REF / 0x7fffffff
    return ret

def float2int(meas,REF):
    if meas>=0:
        ret = int(meas/REF*0x7fffffff)
    else:
        ret = int(-meas/REF*0x80000000)
    return ret

def encode(num):
    arr = bytearray()
    num = "{0}".format(num)
    for x in num:
        arr.append(int(ord(x)))
    return arr

def addData(start):
    global data, writing, temp, end, gco, done
    
    if time.time()-start <= time1 and not done:
        t2 = threading.Timer(N*dt, addData2, args=(now,))
        t2.start()
    else:
        done = True
        
    ser = serial.Serial('dev/ttyAMA0', 19200, timeout=1)
    try:
        if not simulate and data:
            #meas = (int2float(int(data.pop(0)), REF)-0.0141172)/gain
            meas = int(data.pop(0))
            t = float2int(ts.pop(0), REF)
            s = '{0} {1}'.format(t,meas)
            s = encode(s)
            length = len(s)
            length = encode(length)
            ser.write(length)
            ser.write(s)
        elif simulate and data:
            meas = float2int(data.pop(0), REF)
            t = float2int(ts.pop(0), REF)
            s = '{0} {1}'.format(t,meas)
            s = encode(s)
            length = len(s)
            length = encode(length)
            ser.write(length)
            ser.write(s)
    except Exception as e:
        #print(e)
        ser.close()
        done = True
    
    ser.close()

def getData():
    global data, writing, temp, end, gco, done
    if not done:
        t1 = threading.Timer(dt,getData)
        t1.start()
    now = time.time()
    rt = now - t0
    if simulate:
        t1 =  time.time()    
        meas = (sim_o+np.random.normal(scale=sim_onoise))+\
            (sim_a+np.random.normal(scale=sim_anoise))*\
            np.cos(2*np.pi*(sim_f+np.random.normal(scale=sim_fnoise))*\
            rt+(sim_p+np.random.normal(scale=sim_pnoise)))+\
            np.random.normal(scale=sim_vnoise)
        t2 =  time.time()    
        rt = 0.5*(t1+t2)-t0
    else:
        t1 = time.time()
        meas = ADC.ADS1263_Read_ADC_Data()
        t2 = time.time()
        rt = 0.5*(t1+t2)-t0
    data.append(meas)
    ts.append(rt)

N=10
ADC.ADS1263_WaitDRDY()
now = time.time()
t1 = threading.Timer(dt, getData)
t2 = threading.Timer(N*dt, addData, args=(now,))


t1.start()

t2.start()

t1.join()
t2.join()
