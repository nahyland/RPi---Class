# ME 5731 Project 2
# Author: Harrison Seung & Nicholas Hyland
# Objective: Interface RPi with PGA9685() module

# Import libraries
import smbus  #System Management Bus Functions
import time

# PGA9685 Registers
ADS_ADDR	= 0x40	 # 2 addresses appear from "sudo i2cdetect -y 1" 0x40 and 0x70
ADS_PT_CONV	= 0x00   # contains results from last conversion
ADS_PT_CONFIG	= 0x01   # change operating modes

### Control Register Operations ###
# LED0 control, bits [15:12]
PGA_CONFIG_LED0 = {
	NL:	0x06h	# LED0_ON_L	bit[7:0]
	NH:	0x07h	# LED0_ON_H	bit[7:5], [4], 3:0]
	FL:	0x08h	# LED0_OFF_L	bit[7:0]
	FH:	0x09h	# LED0_OFF_H	bit[7:5], [4], [3:0]
}

# LED All-call I2C-bus address, bits [15:13]
PGA_CONFIG_allcall = {
	1:	0x05h	# ALLCALLADR	bit[7:1], [0]
}

# Intermediates are for other LEDs, LED1-LED15, 4 per LED

# I2C subaddress, bits [1:0]
PGA_CONFIG_subadr = {
	1:	0x02h	# SUBADR1	bit[7:1], [0]
	2:	0x03h	# SUBADR2	bit[7:1], [0]
	3:	0x04h	# SUBADR3	bit[7:1], [0]
}

# Mode register 1 or 2, bit [0]
PGA_CONFIG_mode = {
	0:	0x00	# MODE1
	1:	0x01	# MODE2
}

### Mode Register Operations ###



### Functions ###
def control_reg(alcl, LED0=PGA_CONFIG_LED0[NH], os=ADS_CONFIG_OS[1], gain=ADS_CONFIG_GAIN[2/3], mode=ADS_CONFIG_MODE[1], DR=ADS_CONFIG_DR[128]):
	config = LED0	# bit[15:12]
	config |= alcl	# bit[15]
	config |= gain	# bit[11:9]
	config |= mode	# bit[8]
	config |= DR 	# bit[7:5]
	config |= 0x03	# defaults for bit[4:0]
return config