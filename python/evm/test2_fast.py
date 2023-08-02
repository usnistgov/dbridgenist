#!/usr/bin/python3
import ADC
import time

REF = 4.774
adc = ADC.ADC(REF, 1)

def int2float(num, REF):
	tmp = 0x100000000
	if num >> 31 == 1:
		return -(tmp-num) * REF / 0x80000000
	else:
		return num * REF / 0x7fffffff

N=20000
skip=1000
fi = open('data.dat','w')
start = time.time()
i=0
extra=0
while i<N:
	adc.wait_drdy()
	status, val = adc.read_adc()
	if status & 0x40!=0x40:
		extra+=1
		continue
	i=i+1
	fi.write('{:10.8f}\n'.format(int2float(val, REF))) #, end='\r')
	if i%skip==0:
		print('{0:10.8f} {1:08b} {2}'.format(int2float(val, REF),status,extra)) #, end='\r')
	extra=0
fi.close()
stop = time.time()
delta=stop-start
print('Taking {0} data took {1} s or {2} s per pt'.format(N,delta,delta/N))
