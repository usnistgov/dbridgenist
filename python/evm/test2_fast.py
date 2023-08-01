#!/usr/bin/python3
import ADC
import time

REF = 4.774
adc = ADC.ADC(REF, 0)

def int2float(num, REF):
	tmp = 0x100000000
	if num >> 31 == 1:
		return -(tmp-num) * REF / 0x80000000
	else:
		return num * REF / 0x7fffffff

N=2000
fi = open('data.dat','w')
start = time.time()
for i in range(N):
	adc.wait_drdy()
	status, val = adc.read_adc()
	fi.write('{:10.8f}\n'.format(str(int2float(val, REF)))) #, end='\r')
	if i%10==0:
		print('{:10.8f}\n'.format(str(int2float(val, REF)))) #, end='\r')
fi.close()
stop = time.time()
delta=stop-start
print('Taking {0} data took {1} s or {2} s per pt'.format(N,delta,delta/N))
