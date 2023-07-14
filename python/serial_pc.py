# -*- coding: utf-8 -*-
"""
Created on Fri Jul 14 10:38:49 2023

@author: wbalance
"""

import serial
import time
import sys

ser = serial.Serial('COM5', 19200, timeout=1)

ret = ser.read(2)
arr = []

for i in range(50):
    ret = ser.read(1)
    if ret != b'':
        arr.append(ret)
    i += 1
    
print(arr)

ser.close()