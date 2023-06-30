#!/usr/bin/python
# -*- coding: utf-8 -*-
"""
Created on Wed Jun 28 13:40:03 2023

@author: wbalance
"""

import time
import ADS1263
import RPi.GPIO as GPIO
import numpy as np
import threading

data = []
temp = []
start_time = time.time()
REF = 4.5
writing = False

def addData(time1, fn):
    global data
    global writing
    global temp

    while time.time() < start_time + time1:
        if data:
<<<<<<< HEAD
            with open(fn, 'a') as f:
                for val in data:
                    f.write('{0:15.5f} {1:14.11f}\n'.format(now,val))
            data = []
=======
            writing = True
            with open(fn, 'a') as f:
                for val in data:
                    f.write('{0:15.5f} {1:14.11f}\n'.format(val[0],val[1]))
            data = temp
            temp = []
            writing = False
>>>>>>> 4613e40beebaa7d844ce9531d962a1adace398a1
            
def getData(time1):
    global data
    global start_time
    global temp

    ADC = ADS1263.ADS1263()
    if (ADC.ADS1263_init_ADC1('ADS1263_38400SPS') == -1):
	    exit()
    ADC.ADS1263_SetMode(0)
    
    start_time = time.time()

    while time.time() < start_time + time1:
        ADC_Value = ADC.ADS1263_GetChannalValue(0)
        if(ADC_Value>>31 ==1):
            val=REF*2 - ADC_Value * REF / 0x80000000
        else:
            val=ADC_Value * REF / 0x7ffffff
        if not writing:
            data.append([time.time()-start_time, val])
        else:
            temp.append([time.time()-start_time, val])


run_time = input("Time (hh:mm:ss): ")
name = run_time
run_time = run_time.split(':')
secs = int(run_time[0])*3600 + int(run_time[1])*60 + int(run_time[2])

t1 = threading.Thread(target=getData, args=(secs,))
t2 = threading.Thread(target=addData, args=(secs, str(name)+'.dat',))

t1.start()
t2.start()

t1.join()
t2.join()
