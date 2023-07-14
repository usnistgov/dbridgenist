# -*- coding: utf-8 -*-
"""
Created on Fri Jul 14 10:38:49 2023

@author: wbalance
"""

import serial
import time
import sys

ser = serial.Serial('COM5', 19200, timeout=1)

def int2float(meas,REF):
    if meas >> 31 == 1: 
        ret = - meas / 0x80000000
    elif meas >> 31 != 1:
        ret =  meas / 0x7fffffff
    return ret

try:
    while True:
        try:
            ret = ser.read(2)
            if ret != b'':
                ret = int(ret.decode())
                print(int2float(ret))
        except KeyboardInterrupt:
            break
except:
    ser.close()
    
ser.close()