# -*- coding: utf-8 -*-
"""
Created on Fri Jul 14 10:38:49 2023

@author: wbalance
"""

import serial
import time
import sys

ser = serial.Serial('COM5', 19200, timeout=1)

def int2float(num):
    if num >> 31 == 1: 
        ret = -num / 0x80000000
    elif num >> 31 != 1:
        ret =  num / 0x7fffffff
    return ret

try:
    while True:
        try:
            ret = ser.read(11)
            if ret != b'':
                ret = int(ret.decode())
                print(int2float(ret))
        except KeyboardInterrupt:
            break
except Exception as e:
    #print(e)
    ser.close()
    
ser.close()