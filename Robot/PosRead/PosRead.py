# ME 5731 Project 2: Part 3
# Author: Harrison Seung and Nicholas Hyland
# Group: 9

# Program Description #
# This code is to read the potentiometer voltages and output the position of each segment of the robot

#- Initialize -#
import RPi.GPIO as gpio
import os, time, math, smbus

# ADS1115
from ADS1115 import ADS1115
from ADS1115.ADS1115 import ADS_CONFIG_MUX
from ADS1115.ADS1115 import ADS_CONFIG_GAIN

# PCA9685
from PCA9685 import PCA9685

# rbotInit
from Initialization import rbotInit

# Setup Variables/Arrays #
ads = ADS1115.ADS1115()
pca = PCA9685.PCA9685()
rbot = rbotInit.rbotInit()
#- End Initialize -#


#- Class -#
class LSPB(object):
	def rbotpos(self):								# Read ADS values and output voltage
		aziVolt = rbot.readDC(0) * 6.144 / 100
		armVolt = rbot.readDC(0) * 6.144 / 100
		verVolt = rbot.readDC(2) * 6.144 / 100
		rotVolt = rbot.readDC(3) * 6.144 / 100

 		# Convert potValues to actual position
		# Azimuth Position
		aziMax = 4.506 # potValue at max range
		aziMin = 1.685 # potValue at min range
		aziVRange = aziMax - aziMin # potValue range
		aziLen = 380 # azi range of motion
		aziPos = (aziMax - aziVolt) / aziVRange * aziLen # aziPos in degrees

		# Vertical Position
		verMax = 4.51 # potValue at max range
		verMin = 2.82 # potValue at min range
		verVRange = verMax - verMin # potValue range
		verLen = 13 # ver range of motion
		verPos = (verMax - verVolt) / verVRange * verLen # ver position in inches

		# Arm Position
		# Define potValues at min/max range
		AL1 = 4.57
		AL2 = 2.95
		AH1 = 2.87
		AH2 = 1.31
		VL = 4.51
		VH = 2.82
		# Calculate constants
		C = np.array([[AL1, VL, AL1*AL1, VL*VL],
					[AL2, VL, AL2*AL2, VL*VL],
					[AH1, VH, AH1*AH1, VH*VH],
					[AH2, VH, AH2*AH2, VH*VH]])
				R = np.array([[0], [13.75], [0], [13.75]])
		invC = np.linalg.inv(C)
		# Calculate X constants
		X = np.matmul(invC, R)
		armPos = X[0]*A + X[1]*V + X[2]*A*A + X[3]*V*V # armPos in inches

		# Clip Position
		clipMax = 4.506 # potValue at max range
		clipMin = 1.685 # potValue at min range
		clipVRange = clipMax - clipMin # potValue range
		clipLen = 90 # arm range of motion
		clipPos = (clipMax - clipVolt)/ clipVRange * clipLen # clipPos in degrees

	rbotposit = [azipos, verpos, armpos, clippos]
	return rbotposit
#- End Class -#

#- Code Start -#
#pca.start()
#pca.set_freq(500)

#- End Code -#
