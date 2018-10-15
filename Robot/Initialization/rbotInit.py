# ME 5731 Project 2: Part 3
# Author: Harrison Seung and Nicholas Hyland
# Group: 9

# Program Description #
# This program is to initialize the robot, and set directions for each PWM output


## Initialize ##
import RPi.GPIO as gpio
import os, time, math, smbus

# Import classes #
# ADS1115
from ADS1115 import ADS1115
from ADS1115.ADS1115 import ADS_CONFIG_MUX
from ADS1115.ADS1115 import ADS_CONFIG_GAIN

# PCA9685
from PCA9685 import PCA9685

# Setup Variables/Arrays
leddir = [0,0,0,0]



# -- Define Functions -- #
# Read from ADS1115
def readAnalog(channel):
	if channel < 5:
		config = ads.config_reg(mux = ADS_CONFIG_MUX[channel], gain = ADS_CONFIG_GAIN[1])
		value = ads.read_adc(config)
	return value

# Convert Analog signal from ADS to 0 to 100 range
def calcDC(value):
	value_max = 32768
	dc_max = 100
	dc = (value / value_max) * dc_max
	return int(math.floor(dc))

# Direction Setter
def dirset():
	for i in range (1, 4):
		value = readAnalog(i)	# Baseline
		dc_base = calcDC(value)

		setMotor(50)
		time.sleep(0.1)
	
		value = readAnalog(led#)	# new value, in direction
		dc = calcDC(value)

		setMotor(dc)
		time.sleep(0.1)
		setMotor(0)

		dc_dir = dc - dc_base		# Sets direction as 1 or -1
		if(dc_dir > 0):
			led_dir[i] = 1
		elif(dc_dir < 0):
			led_dir[i] = -1
		else:
			pca.set_pwm(1, 0, 0)
			break
		return led_dir





###- Main Code -###

pca.start()
pca.set_freq(500)
