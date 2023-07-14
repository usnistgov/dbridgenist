# -*- coding: utf-8 -*-
"""
Created on Fri Jul 14 10:38:49 2023

@author: wbalance
"""

import serial
import time

ser = serial.Serial('COM5', 30000, timeout=1)

ser.read(2)

ser.close()