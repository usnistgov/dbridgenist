import time
import ADS1263
import RPi.GPIO as GPIO
ADC = ADS1263.ADS1263()
if ADC.ADS1263_init_ADC1('ADS1263_38400SPS') == -1:
	exit()
ADC.ADS1263_SetMode(0)
ADC.ADS1263_SetChannal(0)

ADC.ADS1263_WaitDRDY()
times = []
now = time.time()
for i in range(1000):
	meas = ADC.ADS1263_Read_ADC_Data()
	later = time.time()
	times.append(later-now)
	print(meas * 4.6 / 0x7fffffff)
	now = later

with open('test.dat', 'a') as f:
	for val in times:
		f.write("{0}\n".format(val))
