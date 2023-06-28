#!/usr/bin/python
# -*- coding:utf-8 -*-

import time
import ADS1263
import RPi.GPIO as GPIO
import numpy as np
import matplotlib.pyplot as plt
import datetime

REF = 4.66          # Modify according to actual voltage
                    # external AVDD and AVSS(Default), or internal 2.5V

# ADC1 test part
TEST_ADC1       = True
# ADC2 test part
TEST_ADC2       = False
# ADC1 rate test part
TEST_ADC1_RATE   = False
# RTD test part
TEST_RTD        = False

def takeNPoints(N=1024,ch=0):
	progress = 0.0
	ADC = ADS1263.ADS1263()

	if (ADC.ADS1263_init_ADC1('ADS1263_38400SPS') == -1):
		exit()
	ADC.ADS1263_SetMode(0) # 0 is singleChannel, 1 is diffChannel
	data = []
	start_time = time.time()
	for i in range(N):
		ADC_Value = ADC.ADS1263_GetAll([ch])    # get ADC1 value
		if(ADC_Value[0]>>31 ==1):
			data.append(str(REF*2 - ADC_Value[0] * REF / 0x80000000) + ',' + str(time.time()-start_time))
		else:
			data.append(str(ADC_Value[0] * REF / 0x7fffffff) + ',' + str(time.time()-start_time))
		if int(i/N*1000)/10 != progress:
			progress = int(i/N*1000)/10
			print(str(progress) + "% complete", end="\r")
	stop_time = time.time()
	dt = (stop_time-start_time)/(N-1)
	ADC.ADS1263_Exit()
	return data,dt

n = input("n (ks): ")
freq = input("Frequency: ")
amp = input("Amplitude: ")
data_y, dt = takeNPoints(int(float(n)*1000))
data_x =  np.arange(0,len(data_y)) *dt
name = str(n) + '_' + freq + '_' + amp + '_' + str(datetime.datetime.now()) + '.txt'
name = name.replace(':', '-')
with open(name, 'w') as f:
	f.write('# Nch=1, dt={0:8.6f} ms\n'.format(dt*1000))
	for i in data_y:
		#f.write('{0:14.11f}\n'.format(i))
		f.write(i + "\n")
exit()
