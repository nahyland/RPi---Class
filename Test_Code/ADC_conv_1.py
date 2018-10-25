### ADS1115 16-bit ADC reading code ###

## SETUP ##
# Import Libraries #
import time
import smbus

# I2C Bus #
bus = smbus.SMBus(1)

# Register Assignments #
adr = 0x48		# ADR -> GND
adr_in = 0x01
adr_out = 0x00
data = [0x84, 0x83]


# Assign Functions #
#def write_i2c():		# Block write transcaction-Writes an array of registers
bus.write_i2c_block_data(0x48, 0x01, data)	# (destination address, char cmd, array transferred)
		# This sends to the configuration register

#def read_i2c():			# Block read transaction-Reads data from output address (0x00) as voltage
data = bus.read_i2c_block_data(0x48, 0x00, 2)	# (destination address, char cmd, # of bytes)
# 	return data
		# This reads 2 bytes of data from 0x00


## Main Code ##
raw_adc = 0
#write_i2c()
time.sleep(0.5)

#read_i2c()
	
# Converting data
raw_adc = data[0] * 256 + data[1]
if raw_adc > 32767:
	raw_adc -= 65535
while True:
	print("Digital value of analog input:", raw_adc)
	time.sleep(0.1)
#time.sleep (0.5)