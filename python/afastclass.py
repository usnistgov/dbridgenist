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

simulate=True
if not simulate:
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
REF = 4.73
writing = False
dt = 0.01
end = False
N =10
minN=5

sim_a = 1
sim_o = 2
sim_p =np.pi/4
sim_f = 1
chunkN = 1.0/float(sim_f)/dt
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
    return amp,phi,C2

def find_f(data,dt,t,T0guess=0.1,dT=0,plot=False):
    if dT==0:
        dT = T0guess/10
    #print(T0guess, dT)
    C2a=[]
    TT = np.linspace(T0guess-dT,T0guess+dT)
    for T in TT:
        _,_,C2 = fit_sine(data, t, T)
        C2a.append(C2)
    C2a= np.array(C2a)
    minC2 = np.min(C2a)
    pf = np.polyfit(TT,C2a,2)
    minT = -pf[1]/(2*pf[0])
    miny =np.poly1d(pf)(minT)
    if plot:
        fig,ax = plt.subplots(1)
        ax.plot(TT,C2a,'ro')
        ax.plot(minT,miny,'ks')
        ax.plot(TT[np.argmin(C2a)],minC2,'bD')
    
    if miny> minC2:
        minT = TT[np.argmin(C2a)]
        return find_f(data,dt,t,minT,dT/2,plot)
   
    if minT>T0guess+dT or minT<T0guess-dT:
        return find_f(data,dt,t,minT,dT,plot)
    if dT>1e-3:
        return find_f(data,dt,t,minT,dT/2,plot)
    if minT<0:
        return find_f(data,dt,t,-minT,dT/2,plot)
    return minT


def int2float(meas,REF):
    if meas >> 31 == 1: 
        ret =  REF*2  - meas * REF / 0x80000000
    elif meas >> 31 != 1:
        ret =  meas * REF / 0x7fffffff
    return ret

def addData(fn):
    global data, writing, temp, end

    t1 = threading.Timer(N*dt,addData, args=('test.dat',))
    t1.start()
    co=0
    

    if len(data)<chunkN+minN:
        return
    while len(data)>chunkN+minN:
        with open(fn, 'a') as f:
            mytime =[]
            mydata =[]
            while co<chunkN:
                co+=1
                meas = int2float(int(data.pop(0)), REF)
                mytime.append(ts.pop(0))
                mydata.append(meas)
                #meas=data.pop(0)
            mytime=np.array(mytime)
            mydata=np.array(mydata)
            if simulate:
                a,phi,c2=fit_sine(mytime,mydata,1.0/sim_f)
            else:
                a, phi, c2 = fit_sine(mytime,mydata, find_f(mydata, mytime[-1]/len(mytime), mytime))
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
    if simulate:
        t1 =  time.time()    
        meas = sim_o+sim_a*np.cos(2*np.pi*sim_f*rt+sim_p)+\
            np.random.normal(scale=sim_vnoise)
        meas = float2int(meas,REF)
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
