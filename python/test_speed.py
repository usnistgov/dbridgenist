# -*- coding: utf-8 -*-
"""
Created on Thu Jun 29 11:15:29 2023
Modified now
@author: wbalance
"""


import time
import ADS1263
import config
import RPi.GPIO as GPIO

ADC = ADS1263.ADS1263()
if (ADC.ADS1263_init_ADC1('ADS1263_38400SPS') == -1):
    exit()
ADC.ADS1263_SetMode(0)
ADC.ADS1263_SetChannal(0)

times = []
values = []
n = input("n: ")

for i in range(int(n)):
    start_time = time.time()
    
    ADC.ADS1263_WaitDRDY()
    REF =4.73
    ADC_Value = ADC.ADS1263_Read_ADC_Data()
    if(ADC_Value>>31 ==1):
        val=REF*2 - ADC_Value * REF / 0x80000000
    else:
        val=ADC_Value * REF / 0x7fffffff
    values.append(val)

    times.append(time.time()-start_time)
    
print(values)
print(sum(times)/len(times))
print(len(times)/sum(times))