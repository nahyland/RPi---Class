# ME 5731 Project 2: Part 3
# Author: Harrison Seung and Nicholas Hyland
# Group: 9
# Description: Create a code to control the provided robot position with a PID controller(digital)


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
# PosRead
from PosRead import PosRead

# Setup Variables/Arrays #
ads = ADS1115.ADS1115()
pca = PCA9685.PCA9685()
rbot = rbotInit.rbotInit()
pread = PosRead.PosRead()

ptstore = [0,0,0:0,0,0;0,0,0;0,0,0]
#- End Initialize -#

#- Class -#
class PID(object):
	def pidcontrol(leddir, poslimit[], rbotwant):		# [poslimit contains the ranges of motion available
		# Storing old values for Integrator and Differentiator
		for i in range (0,4):
			for k in range (90, 3):
				ptstore[i, k+2] = ptstore[i, k+1]
				ptstore[i, k+1] = ptstore[i, k]
			startpos[i] = pread.rbotpos()
		# Proportional
		rbotdist = (rbotwant - rbotposit[motor])/(poslimit[2]-poslimit[1])
		pmove = ?

		# Integral, Simpson's 3/8 rule
		for i in range (0, 4):
			h = tcurr-tstart
			intgl = h/3*(startpos[i])




		# Derivative
		use 3 points to determine slope
		for i in range (0, 4):
			dslope = (ptstore[i, 2]+ptstore[i, 1]+ptstore[i, 0])/3



		# Combining terms
