# -*- coding: utf-8 -*-
"""
Created on Fri Jul 14 10:38:49 2023

@author: wbalance
"""

import serial
import time
import sys
import os

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

ser = serial.Serial('COM5', 19200, timeout=1)
try:
    REF = 4.79
    gain = 1
    ser.write(b'pcready')
    conf = ser.read(7)
    i = 0
    while conf != b'piready':
        conf = ser.read(7)
        i += 1
        if i >= 30:
            raise TimeoutError('Communication failed')
    print("Communication successful")
    #dt = float(input("dt: "))
    #ser.write(encode(len(encode(float2int(dt)))))
    #ser.write(encode(float2int(dt)))
    while True:
        try:
            length = ser.read(2)
            print(length)
            ret = None
            if length != b'':
                ret = ser.read(int(length.decode()))
            if ret != b'' and ret != None and len(ret.decode().split()) == 2:
                ret = ret.decode()
                ret = ret.split()
                with open(os.path.join(r'U:\JordanLove\DATA\202307\19', "test.dat"), 'a') as f:
                    s = '{0:10.6f} {1:10.6f}\n'.format(int2float(int(ret[0])),  int2float2(int(ret[1]), REF)/gain)
                    f.write(s)
                    print(s)
            elif ret != b'' and ret != None and len(ret.decode().split()) != 2:
                err = ret
                while err == b'':
                    err = ser.read(int(length.decode()))
                print(err.decode())
        except KeyboardInterrupt:
            ser.write(b'done')
            ser.close()
            break

except Exception as e:
    print(e)
    ser.write(b'done')
    ser.close()