import time
import ADS1263
import config
import RPi.GPIO as GPIO
ADC = ADS1263.ADS1263()
if ADC.ADS1263_init_ADC1('ADS1263_38400SPS') == -1:
	exit()
ADC.ADS1263_SetMode(0)
ADC.ADS1263_SetChannal(0)

ADC.ADS1263_WaitDRDY()
times = []
cs_pin = 22

now = time.time()
for i in range(1000):
    config.digital_write(cs_pin, GPIO.LOW)
    config.spi_writebyte([0x12])
    buf = config.spi_readbytes(5)
    config.digital_write(cs_pin, GPIO.HIGH)
    read  = (buf[0]<<24) & 0xff000000 | (buf[1]<<16) & 0xff0000 | (buf[2]<<8) & 0xff00 | (buf[3]) & 0xff
    later = time.time()
    times.append(later-now)
    now = later
    time.sleep(0.001)

with open('test.dat', 'a') as f:
	for val in times:
		f.write("{0}\n".format(val))
