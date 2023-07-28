import spidev
import RPi.GPIO as GPIO
import sys

class ADC():
    def __init__(self, REF):
        self.DRDY = 26
        self.CS = 16
        self.spi = spidev.SpiDev()
        self.setup()
        self.wait_drdy()
        self.REF = REF
    
    def set_cs(self, state):
        if state == 0:
            GPIO.output(self.CS, GPIO.LOW)
        elif state == 1:
            GPIO.output(self.CS, GPIO.HIGH)
        else:
            return
    
    def read_register(self, reg):
        self.set_cs(0)
        self.spi.writebytes([0x20 | reg, 0x00])
        result = self.spi.readbytes(1)
        self.set_cs(1)
        return result
    
    def write_register(self, reg, data):
        self.set_cs(0)
        self.spi.writebytes([0x40 | reg, 0x00, data])
        self.set_cs(1)
    
    def get_id(self):
        return self.read_register(0)[0]>>5
    
    def wait_drdy(self):
        i = 0
        while True:
            i += 1
            if GPIO.input(self.DRDY) == 0:
                break
            if i >= 400000:
                print('timeout on DRDY')
                break
    
    def read_adc(self):
        self.set_cs(0)
        i = 0
        while True:
            i += 1
            self.spi.writebytes([0x12])
    
            if self.spi.readbytes(1)[0] & 0x40 != 0:
                break
            if i >= 400000:
                print('timeout on read')
                return -1
        buf = self.spi.readbytes(4)
        self.set_cs(1)
        read = (buf[0]<<24) & 0xff000000 | (buf[1]<<16) & 0xff0000 | (buf[2]<<8) & 0xff00 | buf[3] & 0xff
    
        return read
    
    def setup(self):
        GPIO.setmode(GPIO.BCM)
        GPIO.setup(self.DRDY, GPIO.IN, pull_up_down=GPIO.PUD_UP)
        GPIO.setup(self.CS, GPIO.OUT)
    
        self.spi.open(0, 1)
        self.spi.max_speed_hz = 2000000
        self.spi.mode = 0b01
    
        self.spi.writebytes([0x06])
        self.spi.writebytes([0x0a])
        
        id = self.get_id()
        if id == 0x01:
        	print("ID Read success")
        else:
        	print("ID Read failed")
        	self.exit_clean()
        self.spi.writebytes([0x0A])
        
        GAIN = 0
        mode2 = 0x80
        mode2 |= (GAIN << 4) | 0xf
        self.write_register(0x05, mode2)
        if self.read_register(0x05)[0] == mode2:
        	print("DRATE set")
        else:
        	print("DRATE set failed (MODE2)")
        	self.exit_clean()
        
        refmux = 0x24
        self.write_register(0x0f, refmux)
        if self.read_register(0x0f)[0] == refmux:
        	print("REF voltage set")
        else:
        	print("REF voltage set failed (REFMUX)")
        	self.exit_clean()
        
        delay = 0x00
        self.write_register(0x03, delay)
        if self.read_register(0x03)[0] == delay:
        	print("Delay set")
        else:
        	print("Delay set failed (MODE0)")
        	self.exit_clean()
        
        mode1 = 0x84
        self.write_register(0x04, mode1)
        if self.read_register(0x04)[0] == mode1:
        	print("Filter set")
        else:
        	print("Filter set failed (MODE1)")
        	self.exit_clean()
            
        inpmux = 0x0a
        self.write_register(0x06, inpmux)
        if self.read_register(0x06)[0] == inpmux:
            print("Channel set")
        else:
            print("Channel set failed (INPMUX)")
            self.exit_clean()
    
        self.spi.writebytes([0x08])
    
    def exit_clean(self):
        self.spi.close()
        GPIO.cleanup()
        sys.exit()
