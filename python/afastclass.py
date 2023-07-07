#!/usr/bin/python
# -*- coding: utf-8 -*-
"""
Created on Wed Jun 28 13:40:03 2023

@author: wbalance
"""

import time
import numpy as np
import threading
import matplotlib.pyplot as plt
import os

done = False
while not done:
    simulate=input("Simulate? ")
    if simulate.lower() == "y" or simulate.lower() == "yes" or simulate.lower() == "true":
        simulate = True
        done  = True
    elif simulate.lower() == "n" or simulate.lower() == "no" or simulate.lower() == "false":
        simulate = False
        done = True
    else:
        print("Invalid")

if not simulate:
    freq = float(input("Frequency: "))
    import ADS1263
    import RPi.GPIO as GPIO
    ADC = ADS1263.ADS1263()
    if (ADC.ADS1263_init_ADC1('ADS1263_38400SPS') == -1):
        exit()
    ADC.ADS1263_SetMode(0)
    ADC.ADS1263_SetChannal(0)
 
data = []
ts   = []
start_time = time.time()
REF = 4.76
writing = False
dt = 0.005
end = False
N =10
minN=5

sim_a = 1
sim_o = 2
sim_p =np.pi/4
sim_f = 1
gco = 1
#1/100/0.0001=
#if simulate:
#    chunkN = 1.0/float(sim_f)/dt
#else:
#    chunkN = 1.0/float(freq)/dt
chunkN = 500
t0= time.time()
sim_vnoise =1e-3

def fit_sine(t,y,T0):
    """
    Assume the base function is A*sin(wt+phi) = Acos(phi)sin(wt)+ Asin(phi)cos(wt)
    Hence C = Asin(phi) and S =A cos(phi)  C/S = tan(phi)
    """
    w= 2*np.pi/T0
    wt = t*w
    O = np.ones(len(y))
    C = np.cos(wt)
    S = np.sin(wt)
    X = np.matrix(np.vstack((O,C,S)).T)
    C = (X.T*X).I    # covariance matrix
    fit_pars=C*X.T*np.matrix(y).T
    fit_vals =np.array( X*fit_pars)[:,0]  
    C2 = np.dot(y-fit_vals,y-fit_vals)
    #Ndf = len(data)-3
    #sigma2 = C2/Ndf
    #CS = C*sigma2   # scaled covariance matrix

    #off = fit_pars[0,0]
    amp = np.sqrt(fit_pars[1,0]**2+fit_pars[2,0]**2)
    phi = np.arctan2(fit_pars[1,0],fit_pars[2,0])
    return amp,phi,C2,fit_vals

def int2float(meas,REF):
    if meas >> 31 == 1: 
        ret =  REF*2  - meas * REF / 0x80000000
    elif meas >> 31 != 1:
        ret =  meas * REF / 0x7fffffff
    return ret

def addData(fn):
    global data, writing, temp, end, gco

    t1 = threading.Timer(N*dt,addData, args=('test.dat',))
    t1.start()
    co=0
    bd = r'./chunks'
    if not os.path.exists(bd):
        os.makedirs(bd)
    
    if len(data)<chunkN+minN:
        return
    while len(data)>chunkN+minN:
        with open(fn, 'a') as f:
            mytime =[]
            mydata =[]
            while co<chunkN:
                co+=1
                if not simulate:
                    meas = int2float(int(data.pop(0)), REF)
                else:
                    meas = data.pop(0)
                mytime.append(ts.pop(0))
                mydata.append(meas)
                #meas=data.pop(0)
            mytime=np.array(mytime)
            mydata=np.array(mydata)
            with open(os.path.join(bd,'test{0:03}.dat'.format(gco)), 'a') as f2:
                for a,b in zip(mytime, mydata):
                    f2.write('{0:.6}{1:10.6f}\n'.format(a,b))            
            gco = gco+1
            if simulate:
                a,phi,c2,vals=fit_sine(mytime,mydata,1.0/sim_f)
            else:
                a, phi, c2,vals = fit_sine(mytime,mydata,1.0/freq)
            meantime = np.mean(mytime)
            s='{0:11.6f} {1:11.8f} {2:9.6f} {3:7.4e}\n'.format(meantime,a,phi,c2)
            f.write(s)
            print(s,end='')
        #print(co)
        #print('datalen={0} dt mean={1:5.4} ms'.format(len(tmp),1000*np.mean(tmp)))

def float2int(meas,REF):
    if meas>=0:
        ret = int(meas/REF*0x7fffffff)
    else:
        ret = int(-meas/REF*0x80000000)
    return ret

def getData():
    t1 = threading.Timer(dt,getData)
    t1.start()
    now = time.time()
    rt = now - t0
    if simulate:
        t1 =  time.time()    
        meas = sim_o+sim_a*np.cos(2*np.pi*sim_f*rt+sim_p)+\
            np.random.normal(scale=sim_vnoise)
        t2 =  time.time()    
        rt = 0.5*(t1+t2)-t0
    else:
        t1 = time.time()
        ADC.ADS1263_WaitDRDY()
        meas = ADC.ADS1263_Read_ADC_Data()
        t2 = time.time()
        rt = 0.5*(t1+t2)-t0
    data.append(meas)
    ts.append(rt)

N=10
now = time.time()
t1 = threading.Timer(dt, getData)
t2 = threading.Timer(N*dt,addData, args=('test.dat',))



t1.start()

t2.start()

t1.join()
t2.join()
