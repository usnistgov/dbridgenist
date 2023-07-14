# -*- coding: utf-8 -*-
"""
Created on Fri Jul 14 10:17:05 2023

@author: wbalance
"""

import serial
import threading
import time

def get_data():
    ser = serial.Serial('/dev/ttyAMA0')
    
    for i in range(30):
        ret = 30-i
        ret = ret.to_bytes(2, 'big')
        ser.write(ret)
        time.sleep(1)
    
    ser.close()
    
timer = threading.Timer(5.0, get_data)
timer.start()