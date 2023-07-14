# -*- coding: utf-8 -*-
"""
Created on Fri Jul 14 10:17:05 2023

@author: wbalance
"""

import serial
import threading

def get_data():
    ser = serial.Serial('/dev/ttyAMA0')
    print(ser.name)
    ser.write(b'hello')
    ser.close()
    
timer = threading.Timer(30.0, get_data)
timer.start()