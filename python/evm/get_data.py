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

def wait_drdy():
    i = 0
    while True:
        i += 1
        if GPIO.input(DRDY) == 0:
            break
        if i >= 400000:
            print('timeout')
            break

def read_adc():
    i = 0
    while True:
        i += 1
        spi.writebytes([0x12])

        if spi.readbytes(1)[0] & 0x40 != 0:
            break
        if i >= 400000:
            print('timeout')
            return -1
    buf = spi.readbytes(4)
    read = (buf[0]<<24) & 0xff000000 | (buf[1]<<16) & 0xff0000 | (buf[2]<<8) & 0xff00 | buf[3] & 0xff

    return read

def setup():
    GPIO.setmode(GPIO.BCM)
    GPIO.setup(DRDY, GPIO.IN, pull_up_down=GPIO.PUD_UP)

    spi.open(0, 1)
    spi.max_speed_hz = 2000000
    spi.mode = 0b01

    spi.writebytes([0x06])
    spi.writebytes([0x0a])
    
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
        
    inpmux = 0x0a
    write_register(0x06, inpmux)
    if read_register(0x06)[0] == inpmux:
        print("Channel set")
    else:
        print("Channel set failed (INPMUX)")
        sys.exit()

    spi.writebytes([0x08])

DRDY = 26
spi = spidev.SpiDev()
setup()
wait_drdy()
REF = 4.9

try:
    while True:
        val = read_adc()
        if val == -1:
            val = "CAN'T READ"
        else:
            val = val * REF / 0x7fffffff
        print(str(val) + '          ', end='\r')

except KeyboardInterrupt:
    print("Data collection stopped")
    sys.exit()
