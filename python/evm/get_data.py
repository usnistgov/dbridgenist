import spidev
import RPi.GPIO as GPIO
import sys

def read_register(reg):
	spi.writebytes([0x20 | reg, 0x00])
	result = spi.readbytes(1)
	return result

def write_register(reg, data):
	spi.writebytes([0x40 | reg, 0x00, data])

def get_id():
	return read_register(0)[0]>>5

def setup():
    id = get_id()
    if id == 0x01:
    	print("ID Read success")
    else:
    	print("ID Read failed")
    	sys.exit()
    spi.writebytes([0x0A])
    
    GAIN = 0
    mode2 = 0x80
    mode2 |= (GAIN << 4) | 0xf
    write_register(0x05, mode2)
    if read_register(0x05)[0] == mode2:
    	print("DRATE set")
    else:
    	print("DRATE set failed (MODE2)")
    	sys.exit()
    
    refmux = 0x24
    write_register(0x0f, refmux)
    if read_register(0x0f)[0] == refmux:
    	print("REF voltage set")
    else:
    	print("REF voltage set failed (REFMUX)")
    	sys.exit()
    
    delay = 0x00
    write_register(0x03, delay)
    if read_register(0x03)[0] == delay:
    	print("Delay set")
    else:
    	print("Delay set failed (MODE0)")
    	sys.exit()
    
    mode1 = 0x84
    write_register(0x04, mode1)
    if read_register(0x04)[0] == mode1:
    	print("Filter set")
    else:
    	print("Filter set failed (MODE1)")
    	sys.exit()

GPIO.setmode(GPIO.BCM)

spi = spidev.SpiDev()
spi.open(0, 1)
spi.max_speed_hz = 2000000

result = spi.xfer([0x06])
setup()