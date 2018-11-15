# ME 5731 Project 2: Part 3
# Author: Harrison Seung and Nicholas Hyland
# Group: 9
# Description: Create a code to control the provided robot position with a "Bang Bang" controller


#- Initialize -#
import RPi.GPIO as gpio
import os, time, math, smbus

# ADS1115
from ADS1115 import ADS1115
from ADS1115.ADS1115 import ADS_CONFIG_MUX
from ADS1115.ADS1115 import ADS_CONFIG_GAIN
# PCA9685
from PCA9685 import PCA9685
# PosRead
from PosRead import PosRead

# Setup Variables/Matrices #
# Variables
ads = ADS1115.ADS1115()
pca = PCA9685.PCA9685()
rbot = rbotInit.rbotInit()

# Matrices(lists)
ptstore = [0,0,0]
#- End Initialize -#


#- Class -#
class PID(object):
	def bangbang(leddir, rbotwant, dcspeed):
		dcin = math.floor(dcspeed * 4096 - 1)
		# Loop continues until all positions are at rbotwant positions
		while ptstore[i, 0]!=rbotwant[0] & ptstore[i, 1]!=rbotwant[1] & ptstore[i, 2]!=rbotwant[2]
			for i in range (0,2):
				# Measure current position
				ptstore[i] = ads.convertALL()

				# Moving and Stopping
				if rbotwant[i] == ptstore[i]:
					pca.set_pwm(i, 0, dcin)
				else:
					pca.set_pwm(i, 0, 0)

				time.sleep(0.002)			# 500Hz operating frequency
#- End Class -#
