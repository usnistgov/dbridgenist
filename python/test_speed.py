# -*- coding: utf-8 -*-
"""
Created on Thu Jun 29 11:15:29 2023

@author: wbalance
"""

import time
import ADS1263
import RPi.GPIO as GPIO

ADC = ADS1263.ADS1263()
if (ADC.ADS1263_init_ADC1('ADS1263_38400SPS') == -1):
    exit()
ADC.ADS1263_SetMode(0)
ADC.SetChannal(0)

times = []
n = input("n: ")

for i in range(int(n)):
    start_time = time.time()
    
    ADC.ADS1263_WaitDRDY()
    Value = ADC.ADS1263_Read_ADC_Data()

    times.append(time.time()-start_time)
    
print(times)
print(sum(times)/len(times))