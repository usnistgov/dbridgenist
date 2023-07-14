# -*- coding: utf-8 -*-
"""
Created on Fri Jul 14 10:17:05 2023

@author: wbalance
"""

import serial

ser = serial.Serial('/dev/ttyS0')
print(ser.name)
ser.write(b'hello')
ser.close()