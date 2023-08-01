import ADC

REF = 4.774
adc = ADC.ADC(REF)

def int2float(num, REF):
	if num >> 31 == 1:
		return num * REF / 0x80000000
	else:
		return num * REF / 0x7fffffff

try:
	print("01234567890123456789012345678901234567890")
	while True:
		val = adc.read_adc()
		if val == -1:
			val == "CAN'T READ"
		else:
			#val = int2float(val, REF)
			pass
		print(format(val, '032b') + " " + str(int2float(val, REF)), end='\r')

except KeyboardInterrupt:
	print("\nData collection stopped")
	adc.exit_clean()
