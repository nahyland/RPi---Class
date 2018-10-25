# ME 5731 Project 2
# Author: Harrison Seung & Nicholas Hyland
# Objective: Interface RPi with PGA9685 module
# References: PCA9685 documentation by NXP Semiconductors


# Import functions from ADC1115
from ADS1115 import ADS1115
from ADS1115.ADS1115 import ADS_CONFIG_MUX, ADS_CONFIG_GAIN

# Import functions from PCA9685_H
from PCA9685 import PCA9685

# Import libraries
import smbus, time, math


# Name the files
ads = ADS1115.ADS1115()
pca = PCA9685.PCA9685()


## ADS1115 Code ##

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



# Functions to combine boards
def volts_to_dc(volts):
	perc_v = (volts + .13) / 3 + 0.05
	down = 150 * perc_v
	return down


#### Combined Code ####
bus = smbus.SMBus(1) #initialize SMbus

# Setup registries and configurations for each board
## ADS1115 ##
DR = ADS_CONFIG_DR[128] #set data rate
read_A01 = ads.config_reg(mux = ADS_CONFIG_MUX[000])

## PCA9685 ##

# Registers #
PCA_ADDR	= 0x40
OUTDRV		= 0x04
ALLCALL		= 0x01
SLEEP		= 0x10
RESTART		= 0x80
PRE_SCALE	= 0xFE
 
#Mode register
PCA_MODE1	= 0x00
PCA_MODE2	= 0x01

# LED0/PWM channel 0
LED0_ON_L = 	0x06	# byte0
LED0_ON_H = 	0x07	# byte1
LED0_OFF_L = 	0x08	# byte2
LED0_OFF_H = 	0x09	# byte3

#All LED
ALL_LED_ON_L       = 0xFA
ALL_LED_ON_H       = 0xFB
ALL_LED_OFF_L      = 0xFC
ALL_LED_OFF_H      = 0xFD

# Initialize PCA9685
init()

pca.set_freq(60)	#Set initial frequency
up = 4095
down = 150


# Run PWM outputs on channels 1 and 2 of PCA9685
try:
	while 1:
#		for i in range(0, 9):
		ads.read_adc(read_A01)
		volts_to_dc(volts)
		set_pwm(0, 0, up)
		set_pwm(1, 0, down)
		time.sleep(1)
#		for i in range(0, 9):
		ads.read_adc(read_A01)
		volts_to_dc(volts)
		set_pwm(0, 0, down)
		set_pwm(1, 0, up)
		time.sleep(1)
except KeyboardInterrupt:
	bus.close()

