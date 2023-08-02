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
		return -(tmp-num) * REF / 0x80000000
	else:
		return num * REF / 0x7fffffff

bd = '/home/wbalance/data'
N=20000
skip=1000
for j in range(3):
	start = time.time()
	now = datetime.datetime.now()
	i=0
	extra=0
	ch1data=[]
	ch2data=[]
	while i<N:
		#adc.change_channel(i%2, (i%2)*3)
		adc.change_channel(i%2,0)
		iwait = adc.wait_drdy()
		status, val = adc.read_adc()
		if status & 0x40!=0x40:
			extra+=1
			continue
		if i>=2:
			if i%2 == 0 :
				ch1data.append(val)
			else:
				ch2data.append(val)
			if i%skip==0:
				print('{0:10.8f} {1:08b} {2} {3}'.format(int2float(val, REF),status,extra,iwait)) #, end='\r')
		extra=0
		i=i+1
	fn ='data_'+now.strftime('%Y%m%d_%H%M%S')+'.dat'
	fi = open(os.path.join(bd,fn),'w')
	for a,b in zip(ch1data,ch2data):
		fi.write('{:11.9f} '.format(int2float(a, REF))) #, end='\r')	
		fi.write('{:11.9f}\n'.format(int2float(b, REF))) #, end='\r')			
	fi.close()
	stop = time.time()
	delta=stop-start
	print('Taking {0} data took {1} s or {2} s per pt'.format(N,delta,delta/N))
