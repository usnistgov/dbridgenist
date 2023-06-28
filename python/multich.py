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

def takeNPoints(N=1024,chs=[0]):
	progress = 0.0
	ADC = ADS1263.ADS1263()

	if (ADC.ADS1263_init_ADC1('ADS1263_38400SPS') == -1):
		exit()
	ADC.ADS1263_SetMode(0) # 0 is singleChannel, 1 is diffChannel
	data = []
	start_time = time.time()
	for i in range(N):
		ADC_Value = ADC.ADS1263_GetAll(chs)    # get ADC1 value
		temp = []
		for j in ADC_Value:
			if(j>>31 ==1):
				temp.append(REF*2 - j * REF / 0x80000000)
			else:
				temp.append(j * REF / 0x7fffffff)
		data.append(temp)
		if int(i/N*1000)/10 != progress:
			progress = int(i/N*1000)/10
			print(str(progress) + "% complete", end="\r")
	stop_time = time.time()
	dt = (stop_time-start_time)/(N-1)
	ADC.ADS1263_Exit()
	return data,dt

n = input("n (ks): ")
chs = input("Channels: ")
chs = chs.split(',')
for i in range(len(chs)):
	chs[i] = chs[i].strip()
	chs[i] = int(chs[i])

settings = []
for i in range(len(chs)):
	freq = input("Frequency for channel {}: ".format(i))
	amp = input("Amplitude for channel {}: ".format(i))
	off = input("Offset for channel {}: ".format(i))
	settings.append([freq, amp, off, i])

data_y, dt = takeNPoints(int(float(n)*1000), chs)
data_x =  np.arange(0,len(data_y)) *dt

for j in settings:
	name = '{0}_{1}.txt'.format(str(n), str(datetime.datetime.now()))
	name = name.replace(':', '-')
	with open(name, 'w') as f:
		f.write('# Nch={0}, dt={1:8.6f} ms\n'.format(len(chs), dt*1000))
		for k in chs:
			f.write('#Channel {0}: {1}, {2}, {3}\n'.format(k, settings[k][0], settings[k][1], settings[k][2]))
		for i in data_y:
			vals = ''
			for val in i:
				vals += '{0:14.11f}, '.format(val)
			f.write(vals[:-2] + '\n')
exit()
