# ME 5731 Project 2: Part 3
# Author: Harrison Seung and Nicholas Hyland
# Group: 9

# Program Description #
# This program is to initialize the robot, and set directions for each pair of PWM outputs


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
ads = ADS1115.ADS1115()

leddir = [-1,-1,-1,-1]								# Creates matrix to store motor direction values
## End Initialize ##


# -- Define rbotInit Class -- #
class rbotInit(object):
	# Read from ADS1115, convert the analog signal pulled from ADS into 0 to 100 range
	def readDC(self, channel):
		if channel < 4:
			config = ads.config_reg(mux = ADS_CONFIG_MUX[channel], gain = ADS_CONFIG_GAIN[1])
			value = ads.read_adc(config)
			value_max = 32768
			dc_max = 100
			dc = (value / value_max) * dc_max
			return int(math.floor(dc))

	# Direction Setter/verification of direction
	def dirset(self):
		for i in range (4):						# Runs through all 4 motor/sensor sets
			dc_base = self.readDC(i)			# Reads initial value at starting position

			# send signal to first LED out (i.e. LED0)
			pca.set_pwm(2 * i ,0 ,2082)			# Activates first channel to move motor
			time.sleep(0.1)
			pca.set_pwm(2 * i ,0 ,0)			# Stops PWM signal to first channel

			dc = self.readDC(i)					# Calculate new position from sensor
			time.sleep(0.001)

			# send signal to opposite LED out (i.e. LED1) return to start position at 50% duty cycle
			pca.set_pwm(2 * i + 1, 0, 2082)
			time.sleep(0.1)
			pca.set_pwm(2 * i + 1, 0, 0)
			dc_post = self.readDC(i)			# Records value after movement cycle to check against initial position

			dc_dir = dc - dc_base
			dc_trav = dc_post - dc_base			# This is the travel distance between initial and final position (should be ~0)

			if abs(dc_trav/dc) < 0.01:			# Check to see if the robot is at the end of travel on an output, in %
				pca.set_pwm(2 * i, 0, 2082)
				time.sleep(0.1)
				dc_base = self.readDC(i)		# Sets new initial, to be consistent with directions
				pca.set_pwm(2 * i, 0, 0)

				dc_dir = dc_base - dc			# Secondary motion is in -initial direction, so end value stays the same

			if(dc_dir > 0):						# sets direction as 1 or -1
				led_dir[i] = 0					# 1 means that first out is positive (i.e. LED0 is forward)
			elif(dc_dir < 0):
				led_dir[i] = 1					# -1 means that second out is positive (i.e. LED 1 is foward)
			else:
				pca.set_pwm(1, 0, 0)
				print("Feedback not responding on motor", i)
			return leddir
# -- End Class -- #

###- Code Needed to start -###

# pca.start()
# pca.set_freq(500)
# dirset()

###- End Code -###
