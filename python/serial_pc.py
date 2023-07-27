# -*- coding: utf-8 -*-
"""
Created on Fri Jul 14 10:38:49 2023

@author: wbalance
"""

import serial
import time
import sys
import os
import struct
import linecache

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

def float2int(num):
    if num>=0:
        ret = int(num*0x7fffffff)
    else:
        ret = int(-num*0x80000000)
    return ret

def encode(num):
    arr = bytearray()
    num = str(num)
    for x in num:
        arr.append(int(ord(x)))
    return arr

def PrintException():
    exc_type, exc_obj, tb = sys.exc_info()
    f = tb.tb_frame
    lineno = tb.tb_lineno
    filename = f.f_code.co_filename
    linecache.checkcache(filename)
    line = linecache.getline(filename, lineno, f.f_globals)
    print('EXCEPTION IN ({}, LINE {} "{}"): {}'.format(filename, lineno, line.strip(), exc_obj))

ser = serial.Serial('COM5', 19200, timeout=1)
try:
    REF = 4.79
    gain = 1.0205
    ser.write(b'pcready')
    conf = ser.read(7)
    i = 0
    while conf != b'piready':
        conf = ser.read(7)
        i += 1
        if i >= 30:
            raise TimeoutError('Communication failed')
    print("Communication successful")
    while True:
        try:
            length = ser.in_waiting
            ret = ser.read(length)
            if length%4 != 0 or length == 0:
                continue
            ret2 = struct.iter_unpack('>l',ret)
            dts = []
            vals = []
            ns = []
            for i in range(int(length/12)):
                dts.append(next(ret2)[0])
                vals.append(next(ret2)[0])
                ns.append(next(ret2)[0])
            with open(os.path.join(r'U:\JordanLove\DATA\202307\24', "test.dat"), 'a') as f:
                for a,b,c in zip(dts, vals, ns):
                    s = '{0:10.6f} {1:10.6f} {2}\n'.format(int2float2(int(a), 5),  int2float2(int(b), REF)/gain, c)
                    f.write(s)
                    print(s)
        except KeyboardInterrupt:
            ser.write(b'done')
            ser.close()
            break

except:
    PrintException()
    ser.write(b'done')
    ser.close()