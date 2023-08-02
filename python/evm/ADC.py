import spidev
import RPi.GPIO as GPIO
import sys

class ADC():
    def __init__(self, REF, mode=0,verbose=0):
        self.verbose = verbose
        self.DRDY = 26
        self.CS = 16
        self.spi = spidev.SpiDev()
        self.setup(mode)
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
    
    def wait_drdy(self,imax=400000):
        i = 0
        while GPIO.input(self.DRDY) != 0:
            i += 1
            if i >= imax:
                if self.verbose: print('timeout on DRDY')
                return i
        return i
    
    def change_channel(self, channel, gnd=0):
        self.set_cs(0)
        inpmux = (0x0a - gnd) | (channel << 4) # First 4 bits are positive input, last 4 are negative input
        self.write_register(0x06, inpmux)
        if self.read_register(0x06)[0] == inpmux:
            #if self.verbose: print("Channel set")
            pass
        else:
            if self.verbose: print("Channel set failed (INPMUX)")
    
    def read_adc(self):
        self.set_cs(0)
        self.spi.writebytes([0x12])
        buf = self.spi.readbytes(6)
        status = buf[0]
        self.set_cs(1)
        read = (buf[1]<<24) & 0xff000000 | (buf[2]<<16) & 0xff0000 | \
        (buf[3]<<8) & 0xff00 | buf[4] & 0xff # Arrange bytes in order
    
        return status, read
    
    def read_adc_pulse(self):
        self.set_cs(0)
        buf = self.spi.readbytes(6)
        self.set_cs(1)
        
        return (buf[1]<<24) & 0xff000000 | (buf[2]<<16) & 0xff0000 |\
        (buf[3]<<8) & 0xff00 | buf[4] & 0xff
        
    def setup(self, mode):  #mode: 1=pulse, 0=continuous
        GPIO.setmode(GPIO.BCM)
        GPIO.setup(self.DRDY, GPIO.IN, pull_up_down=GPIO.PUD_UP)
        GPIO.setup(self.CS, GPIO.OUT)
    
        self.spi.open(0, 1)
        self.spi.max_speed_hz = 4000000
        self.spi.mode = 0b01 # Clock polarity = 0 (clock idles low), 
                             # clock phase = 1 (data sampled on falling edge, shifted on rising edge)
    
        self.spi.writebytes([0x06]) # Send reset command
        self.spi.writebytes([0x0a]) # Send stop command
        
        id = self.get_id()
        if id == 0x01:
        	if self.verbose: print("ID Read success")
        else:
        	if self.verbose: print("ID Read failed")
        	self.exit_clean()
        self.spi.writebytes([0x0A])
        
        GAIN = 0
        mode2= 0x8f | (GAIN << 4) 
        self.write_register(0x05, mode2)
        if self.read_register(0x05)[0] == mode2:
        	if self.verbose: print("DRATE set")
        else:
        	if self.verbose: print("DRATE set failed (MODE2)")
        	self.exit_clean()
        
        refmux = 0x24
        self.write_register(0x0f, refmux)
        if self.read_register(0x0f)[0] == refmux:
        	if self.verbose: print("REF voltage set")
        else:
        	if self.verbose: print("REF voltage set failed (REFMUX)")
        	self.exit_clean()
        
        #mode0 = 0x00 | (mode << 7)
        if mode==0:
            mode0=0
        else:
            mode0=0x40
        self.write_register(0x03, mode0)
        if self.read_register(0x03)[0] == mode0:
        	if self.verbose: print("Delay set")
        else:
        	if self.verbose: print("Delay set failed (MODE0)")
        	self.exit_clean()
        
        mode1 = 0x84
        self.write_register(0x04, mode1)
        if self.read_register(0x04)[0] == mode1:
        	if self.verbose: print("Filter set")
        else:
        	if self.verbose: print("Filter set failed (MODE1)")
        	self.exit_clean()
            
        inpmux = 0x0a
        self.write_register(0x06, inpmux)
        if self.read_register(0x06)[0] == inpmux:
            if self.verbose: print("Channel set")
        else:
            if self.verbose: print("Channel set failed (INPMUX)")
            self.exit_clean()
    
        self.spi.writebytes([0x08])
    
    def exit_clean(self):
        self.spi.close()
        GPIO.cleanup()
        sys.exit()
