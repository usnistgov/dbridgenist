# -*- coding: utf-8 -*-
"""
Created on Wed Jul  5 11:18:59 2023

@author: wbalance
"""
import threading
import time

global last
global dT
dT=1

def hello(n,last):
    now=time.time()
    n=n+1
    t = threading.Timer(dT, hello,args=(n,now))
    t.start()
    print(n,now-last)
    last =now

last = time.time()
n=0
t = threading.Timer(dT, hello,args=(n,last))
t.start()  # after 30 seconds, "hello, world" will