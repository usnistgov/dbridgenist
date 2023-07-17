# -*- coding: utf-8 -*-
"""
Created on Fri Jul 14 10:38:49 2023

@author: wbalance
"""

import serial
import time
import sys

ser = serial.Serial('COM5', 19200, timeout=1)
REF = 4.76

def int2float(num):
    if num >> 31 == 1: 
        ret = num / 0x80000000
    elif num >> 31 != 1:
        ret =  num / 0x7fffffff
    return round(ret, 6)

def int2float2(num, REF):
    if num >> 31 == 1: 
        ret = num * REF / 0x80000000
    elif num >> 31 != 1:
        ret =  num * REF / 0x7fffffff
    return round(ret, 6)

try:
    while True:
        try:
            ret = ser.read(23)
            print(ret)
            if ret != b'':
                ret = int(ret.decode())
                ret = ret.split()
                with open("U:\JordanLove\DATA\202307\17\test.dat", 'a') as f:
                    f.write('{0:.6}{1:10.6f}'.format(int2float(ret[0]),  int2float2(ret[1], REF)))
        except KeyboardInterrupt:
            break

except Exception as e:
    print(e)
    ser.close()
    
ser.close()