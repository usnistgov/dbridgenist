#!/usr/bin/python3
import ADC
import time
import datetime
import os

REF = 4.774
adc = ADC.ADC(REF, 1)

def int2float(num, REF):
	tmp = 0x100000000
	if num >> 31 == 1:
		return -(tmp-num) * REF / 0x80000000 # invert by subtraction from 2^N
	else:
		return num * REF / 0x7fffffff

bd = '/home/wbalance/data'
Loops=1
N=60000
skip=10000
for j in range(Loops):
	start = time.time()
	now = datetime.datetime.now()
	i=0
	extra=0
	ch1data=[]
	ch2data=[]
	while i<N:
		adc.change_channel(i%2,0) # switch channels
		iwait = adc.wait_drdy()
		status, val = adc.read_adc()
		if status & 0x40!=0x40: # check status byte, second bit 1 = new data
			extra+=1
			continue
		if i>=2:
			if i%2 == 0 :
				ch1data.append(val)
			else:
				ch2data.append(val)
			if i%skip==0:
				print('{4}: {0:10.8f} {1:08b} {2} {3}'.\
			  format(int2float(val, REF),status,extra,iwait,i)) #, end='\r')
		extra=0
		i=i+1
	stop = time.time()
	fn ='data_'+now.strftime('%Y%m%d_%H%M%S')+'.dat'
	fi = open(os.path.join(bd,fn),'w')
	for a,b in zip(ch1data,ch2data):
		fi.write('{:11.9f} '.format(int2float(a, REF))) #, end='\r')	
		fi.write('{:11.9f}\n'.format(int2float(b, REF))) #, end='\r')			
	fi.close()
	delta=stop-start
	print('Taking {0} data took {1:8.3f} s or {2:9.3f} ms per pt cs={3:9.3f} kHz '.\
	   format(N,delta,delta*1000/N,N/delta/1000))
