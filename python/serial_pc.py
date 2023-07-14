# -*- coding: utf-8 -*-
"""
Created on Fri Jul 14 10:38:49 2023

@author: wbalance
"""

import serial
import time
import sys

ser = serial.Serial('COM5', 19200, timeout=1)

while True:
    try:
        ret = ser.read(2)
        ret = int(ret.decode())
    except KeyboardInterrupt:
        break
    
ser.close()