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
start_time = time.time()
REF = 4.73

def addData(time1, fn):
    global data
    
    while time.time() < start_time + time1:
        now = time.time()-start_time
        if data:
            with open(fn, 'a') as f:
                for val in data:
                    f.write('{0:15.5f} {1:14.11f}\n'.format(now,val))
            data = []
            
def getData(time1):
    global data
    ADC = ADS1263.ADS1263()
    if (ADC.ADS1263_init_ADC1('ADS1263_38400SPS') == -1):
	    exit()
    ADC.ADS1263_SetMode(0)
    
    while time.time() < start_time + time1:
        ADC_Value = ADC.ADS1263_GetChannalValue(0)
        if(ADC_Value>>31 ==1):
            val=REF*2 - ADC_Value * REF / 0x80000000
        else:
            val=ADC_Value * REF / 0x7fffffff
        data = []
        data.append(val)
        

run_time = input("Time (hh:mm:ss): ")
run_time = run_time.split(':')
secs = int(run_time[0])*3600 + int(run_time[1])*60 + int(run_time[2])

t1 = threading.Thread(target=getData, args=(secs,))
t2 = threading.Thread(target=addData, args=(secs, str(run_time)+'.dat',))

t1.start()
t2.start()

t1.join()
t2.join()