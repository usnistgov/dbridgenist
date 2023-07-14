# -*- coding: utf-8 -*-
"""
Created on Fri Jul 14 10:38:49 2023

@author: wbalance
"""

import serial
import time
import sys

ser = serial.Serial('COM5', 19200, timeout=1)

try:
    while True:
        try:
            ret = ser.read(2)
            if ret != b'':
                ret = int(ret.decode())
                print(ret)
        except KeyboardInterrupt:
            break
except:
    ser.close()
    
ser.close()