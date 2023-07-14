# -*- coding: utf-8 -*-
"""
Created on Fri Jul 14 10:38:49 2023

@author: wbalance
"""

import serial
import time

ser = serial.Serial('COM5')
start = time.time()

while ser.read(5) != 0 and time.time()-start<30:
    print(ser.read(5))

print(ser.read(5))
ser.close()