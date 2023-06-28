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

def takeNPoints(N=1024,ch=0,fn='test.dat'):
	ADC = ADS1263.ADS1263()

	if (ADC.ADS1263_init_ADC1('ADS1263_38400SPS') == -1):
		exit()
	ADC.ADS1263_SetMode(0) # 0 is singleChannel, 1 is diffChannel
	start_time = time.time()
	for i in range(N):
		ADC_Value = ADC.ADS1263_GetChannalValue(ch)    # get ADC1 value
		now =time.time()-start_time   
		if(ADC_Value>>31 ==1):
			val=REF*2 - ADC_Value * REF / 0x80000000
		else:
			val=ADC_Value * REF / 0x7fffffff
		print(now,val)	
		fi = open(fn,'a')
		fi.write('{0:15.5f} {1:14.11f}\n'.format(now,val))
		fi.close()
	ADC.ADS1263_Exit()
	return 

n = input("n (ks): ")
takeNPoints(int(float(n)*1000))
exit()
