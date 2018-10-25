# ME 5731 Project 2
# Author: Harrison Seung & Nicholas Hyland
# Objective: Interface RPi with ADS1115() module

# Import libraries
import smbus  #System Management Bus Functions
import time

# ADS1115 Registers
ADS_ADDR	= 0x48
ADS_PT_CONV	= 0x00   # contains results from last conversion
ADS_PT_CONFIG	= 0x01   # change operating modes

### CONFIG Register Operations ###
# Operation status, bit [15]
ADS_CONFIG_OS = {
	0:	0x0000, # R/W: Device IS performing conv/No effect
	1:	0x8000 # R/W: Device is NOT performing conv/Begin single conv
}


# Mux, bit [14:12]
ADS_CONFIG_MUX = {
	000:	0x0000,
	100:	0x4000, 
	101:	0x5000, 
	110:	0x6000, 
	111:	0x7000  
}

# Gain, bit [11:9]
ADS_CONFIG_GAIN = {
	2/3:	0x0000, # +/-6.144V
	1:	0x0200, # +/-4.096V
	2:	0x0500, # +/-2.048V
	4:	0x0600, # +/-1.024V
	8:	0x0800, # +/-0.512V
	16:	0x0A00	 # +/-0.256V
}

# Operating Mode, bit [8]
ADS_CONFIG_MODE = {
	0: 0x0000, # Continuous
	1: 0x0100  # Single
}

# Data Rate in samples per second, bit [7:5]
ADS_CONFIG_DR = {
	8:	0x0000, 
	16:	0x0020, 
	32:	0x0040, 
	64:	0x0060, 
	128:	0x0080, 
	250:	0x00A0, 
	475:	0x00C0, 
	860:	0x00E0  
}

### Functions ###
def config_reg(mux, os=ADS_CONFIG_OS[1], gain=ADS_CONFIG_GAIN[2/3], mode=ADS_CONFIG_MODE[1], DR=ADS_CONFIG_DR[128]):
	config = os # bit[15]
	config |= mux	# bit[14:12]
	config |= gain	# bit[11:9]
	config |= mode	# bit[8]
	config |= DR 	# bit[7:5]
	config |= 0x03 # defaults for bit[4:0]
	return config

# convert raw data
def convert_value(low, high):
    # concatentate high and low values
    value = ((high & 0xFF) << 8 | (low & 0xFF))

    # Get signed value
    if (value > 0x8000):
        value = value - 0x10000 
    return value

def read_adc(config):
	# Send config to ADC
	bus.write_i2c_block_data(ADS_ADDR, ADS_PT_CONFIG, [(config >> 8) & 0xFF, (config & 0xFF)])
	
	# Allow time for sample to be written to pointer conversion register
	time.sleep(1.0/DR) #allow time for sample to be written

	# Read pointer conversion register
	result = bus.read_i2c_block_data(ADS_ADDR, ADS_PT_CONV, 2)
	#print("High = {0}, Low = {1}".format(result[0], result[1]))

	# Convert raw data to decimal format
	value = convert_value(result[1], result[0])
	#print("Raw value = {0}".format(value))

	# Convert value to voltage
	volts = (value/0x8000)*6.144
	print("Voltage = {:.2f}".format(volts))
	
	return(volts)

### Main Code ###

bus = smbus.SMBus(1) #initialize SMbus

DR = ADS_CONFIG_DR[128] #set data rate

# Setup configuration
read_A01 = config_reg(mux = ADS_CONFIG_MUX[000])
#read_A0 = config_reg(mux = ADS_CONFIG_MUX[100])
#read_A1 = config_reg(mux = ADS_CONFIG_MUX[101])
#read_A2 = config_reg(mux = ADS_CONFIG_MUX[110])
#read_A3 = config_reg(mux = ADS_CONFIG_MUX[111])

# Read ADC
try:
	while 1:
		read_adc(read_A01)
		time.sleep(0.1)
#		read_adc(read_A0)
#		time.sleep(1)
#		read_adc(read_A1)
#		time.sleep(1)
#		read_adc(read_A2)
#		time.sleep(1)
#		read_adc(read_A3)
#		time.sleep(1)
except KeyboardInterrupt:
	bus.close()