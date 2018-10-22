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
leddir = [0,0,0,0]					# Creates matrix to store motor direction values



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

# Direction Setter/verification of direction
def dirset():
	for i in range (0, 3):			# Runs through all 4 motor/sensor sets
		value = readAnalog(i)		# Baseline
		dc_base = calcDC(value)

		# send signal to first LED out (i.e. LED0)	(needs work)
		pca.set_pwm(i ,0 ,2082)		# Use first channel to move motor
		time.sleep(0.1)
		pca.set_pwm(i ,0 ,0)		# Stops PWM signal to first channel

		value = readAnalog(i)	# new value, in direction
		dc = calcDC(value)			# calculate new position from sensor
		time.sleep(0.001)

		# send signal to opposite LED out (i.e. LED1)
		pca.set_pwm(i + 1, 0, 2082)			# Activate motor, return to start position at 50% duty cycle
		time.sleep(0.1)
		pca.set_pwm(i + 1, 0, 0)

		dc_dir = dc - dc_base
		if abs(dc_dir) < 0.01:
			dc_base = dc
			value = readAnalog(i)
			dc = calcDC(value)
			dc_dir = dc_base - dc

			pca.set_pwm(i, 0, 2082)
			time.sleep(0.1)
			pca.set_pwm(i, 0, 2082)

		if(dc_dir > 0.01):			# sets direction as 1 or -1
			led_dir[i] = 1			# 1 means that first out is positive (i.e. LED0 is forward)
		elif(dc_dir < -0.01):
			led_dir[i] = -1			# -1 means that second out is positive (i.e. LED 1 is foward)
		else:
			value = readAnalog(i)
			dc_post = calcDC(value)
			pca.set_pwm(1, 0, 0)
			pca.set_pwm(i, 0, 2082)
			time.sleep(0.1)
			pca.set_pwm(i, 0, 2082)
		return led_dir





###- Main Code -###

pca.start()
pca.set_freq(500)


dirset()


def set_pwm(self, channel, on, off): #set pwm
		bus = smbus.SMBus(1)
		bus.write_byte_data(PCA_ADDR, LED0_ON_L + 4*channel, on & 0xFF)
		bus.write_byte_data(PCA_ADDR, LED0_ON_H + 4*channel, on >> 8)
		bus.write_byte_data(PCA_ADDR, LED0_OFF_L + 4*channel, off & 0xFF)
		bus.write_byte_data(PCA_ADDR, LED0_OFF_H + 4*channel, off >> 8)
