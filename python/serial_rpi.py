# -*- coding: utf-8 -*-
"""
Created on Fri Jul 14 10:17:05 2023

@author: wbalance
"""

import serial
import threading
import time

def float2int(num):
    if num>=0:
        ret = int(num*0x7fffffff)
    else:
        ret = int(-num*0x80000000)
    return ret

def encode(num, nbytes):
    arr = bytearray()
    num = "{0:0{1}}".format(num, nbytes)
    for x in num:
        arr.append(int(ord(x)))
    return arr

def get_data():
    ser = serial.Serial('/dev/ttyAMA0', 19200, timeout=1)
    
    for i in range(300):
        ret = float2int((300-i)/10)
        ret = encode(ret, 8)
        ser.write(ret)
        time.sleep(0.1)
    
    ser.close()
    
timer = threading.Timer(5.0, get_data)
timer.start()