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
REF = 4.73
writing = False

def addData(time1, fn):
    global data
    global writing
    global temp

    while time.time() < start_time + time1:
        if data:
            writing = True
            with open(fn, 'a') as f:
                for val in data:
                    ACC_Value=val[1]
                    if(ADC_Value>>31 ==1):
                        val_fl=REF*2 - ADC_Value * REF / 0x80000000
                    else:
                        val_fl=ADC_Value * REF / 0x7fffffff

                    f.write('{0:15.5f} {1:14.11f}\n'.format(val[0],val_fl))
            data = temp
            temp = []
            writing = False
            
def getData(time1):
    global data
    global start_time
    global temp

    ADC = ADS1263.ADS1263()
    if (ADC.ADS1263_init_ADC1('ADS1263_38400SPS') == -1):
	    exit()
    ADC.ADS1263_SetMode(0)
    ADC.ADS1263_SetChannal(0)

    
    start_time = time.time()

    while time.time() < start_time + time1:
        ADC.ADS1263_WaitDRDY()
        REF =4.73
        ADC_Value = ADC.ADS1263_Read_ADC_Data()
        if not writing:
            data.append([time.time()-start_time, ADC_Value])
        else:
            temp.append([time.time()-start_time, ADC_Value])


run_time = input("Time (hh:mm:ss): ")
name = run_time
name = name.replace(':', '-')
run_time = run_time.split(':')
secs = int(run_time[0])*3600 + int(run_time[1])*60 + int(run_time[2])

t1 = threading.Thread(target=getData, args=(secs,))
t2 = threading.Thread(target=addData, args=(secs, str(name)+'.dat',))

t1.start()
t2.start()

t1.join()
t2.join()
