#!/usr/bin/python
# -*- coding:utf-8 -*-

import time
import ADS1263
import RPi.GPIO as GPIO
import numpy as np
import matplotlib.pyplot as plt
import datetime

REF = 4.73          # Modify according to actual voltage
                    # external AVDD and AVSS(Default), or internal 2.5V

# ADC1 test part
TEST_ADC1       = True
# ADC2 test part
TEST_ADC2       = False
# ADC1 rate test part
TEST_ADC1_RATE   = False
# RTD test part
TEST_RTD        = False

def appendData(filename, data):
	with open(filename, 'a') as f:
		f.write('{0:14.11f}\n'.format(data))

def takeNPoints(freq, amp, N=1024,ch=0):
	progress = 0.0
	ADC = ADS1263.ADS1263()
	ADC_value_arr = [None]

	if (ADC.ADS1263_init_ADC1('ADS1263_38400SPS') == -1):
		exit()
	ADC.ADS1263_SetMode(0) # 0 is singleChannel, 1 is diffChannel
	data = []
	start_time = time.time()
	name = '{0}_{1}_{2}_{3}.txt'.format(str(n),freq,amp,str(datetime.datetime.now()))
	name = name.replace(':', '-')
	for i in range(N):
		ADC_Value = ADC.ADS1263_GetAll([ch])    # get ADC1 value
		if(ADC_Value[0]>>31 ==1):
			x = REF*2 - ADC_Value[0] * REF / 0x80000000
			appendData(name, x)
		else:
			x = ADC_Value[0] * REF / 0x7fffffff
			appendData(name, x)

		if int(i/N*1000)/10 != progress:
			progress = int(i/N*1000)/10
			print(str(progress) + "% complete", end="\r")

	stop_time = time.time()
	dt = (stop_time-start_time)/(N-1)
	ADC.ADS1263_Exit()
	return name, dt

n = input("n (ks): ")
freq = input("Frequency: ")
amp = input("Amplitude: ")
name, dt = takeNPoints(freq, amp, int(float(n)*1000))
with open(name, 'a') as f:
	f.write('# Nch=1, dt={0:8.6f} ms\n'.format(dt*1000))
exit()
