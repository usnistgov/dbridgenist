# -*- coding: utf-8 -*-
"""
Created on Fri Jul 28 14:43:35 2023

@author: wbalance
"""

import ADC

REF = 4.913

adc = ADC.ADC(REF)

try:
    while True:
        val = adc.read_adc()
        if val == -1:
            val = "CAN'T READ"
        else:
            val = val * REF / 0x7fffffff
        print(str(val) + '          ', end='\r')
except KeyboardInterrupt:
    print("Data collection stopped")
    adc.exit_clean()
