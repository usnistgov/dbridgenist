#!/usr/bin/python3
import spidev
import RPi.GPIO as GPIO

GPIO.setmode(GPIO.BCM)

spi = spidev.SpiDev()
spi.open(0, 1)
spi.max_speed_hz = 2000000
spi.mode = 0b01
CS = 16
GPIO.setup(CS, GPIO.OUT)

result = spi.xfer([0x06])
for reg in range(27):
	GPIO.output(CS, GPIO.LOW)
	spi.writebytes([0x20 | reg, 0x00])
	result2 = spi.readbytes(1)
	print(format(reg, '#04x'), ':', format(result2[0], '#04x'),':', format(result2[0], '#010b'))
	GPIO.output(CS, GPIO.HIGH)

spi.close()
