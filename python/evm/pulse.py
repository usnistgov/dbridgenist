import ADC
import RPi.GPIO as GPIO
import time

REF = 4.774
START = 6
toread = []
adc = ADC.ADC(REF, 1)
GPIO.setmode(GPIO.BCM)
GPIO.setup(START, GPIO.OUT)

def sleep(duration, get_now=time.perf_counter):
    now = get_now()
    end = now + duration
    while now < end:
        now = get_now()
        
def int2float(num, REF):
    tmp = 0x100000000
    if num >> 31 == 1:
        return -(tmp-num) * REF / 0x80000000
    else:
        return num * REF / 0x7fffffff
        
try:
    while True:
        GPIO.output(START, GPIO.HIGH)
        val = adc.read_adc_pulse()
        GPIO.output(START, GPIO.LOW)
        print(int2float(val), end = '\r')
        sleep(0.1)
        
except KeyboardInterrupt:
    pass