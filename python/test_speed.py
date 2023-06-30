# -*- coding: utf-8 -*-
"""
Created on Thu Jun 29 11:15:29 2023

@author: wbalance
"""

import time
import ADS1263
import config
import RPi.GPIO as GPIO

ADC = ADS1263.ADS1263()
if (ADC.ADS1263_init_ADC1('ADS1263_38400SPS') == -1):
    exit()
ADC.ADS1263_SetMode(0)
ADC.ADS1263_SetChannal(0)

times = []
values = []
n = input("n: ")

for i in range(int(n)):
    start_time = time.time()
    
    ADC.ADS1263_WaitDRDY()

    config.digital_write(22, GPIO.LOW)
    while(1):
        config.spi_writebyte([0x12])
        if(config.spi_readbytes(1)[0] & 0x40 != 0):
            break
    buf = config.spi_readbytes(5)
    config.digital_write(22, GPIO.HIGH)

    read = (buf[0]<<16) & 0xff000000 | (buf[1]<<8) & 0xff0000 | (buf[2]) & 0xff00 | (buf[3]) & 0xff
    values.append(read)

    times.append(time.time()-start_time)
    
print(values)
print(sum(times)/len(times))
print(len(times)/sum(times))
