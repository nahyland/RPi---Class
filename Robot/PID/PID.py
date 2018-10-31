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

# Setup Variables/Matrices #
# Variables
ads = ADS1115.ADS1115()
pca = PCA9685.PCA9685()
rbot = rbotInit.rbotInit()
pread = PosRead.PosRead()

# Matrices(lists)
ptstore = [0,0,0:0,0,0;0,0,0;0,0,0]
loopcount = 0
startpos[0,0,0,0]
rbotdist = [0,0,0,0]
sumval = [0,0,0,0]
intgl = [0,0,0,0]
dslope = [0,0,0,0]
#- End Initialize -#

#- Class -#
class PID(object):
	def pidcontrol(leddir, rbotwant, holdt):		#  holdt is the time to hold end position *500
		# Loop continues until all positions are at rbotwant positions
		while ptstore[i, 0]!=rbotwant[0] & ptstore[i, 1]!=rbotwant[1] & ptstore[i, 2]!=rbotwant[2] & ptstore[i, 3]!=rbotwant[3]
			loopcount += 1
			# Storing old values for Integrator and Differentiator, 0 is current, 1 is last, 2 is oldest
			for i in range (0,4):
				for k in range (0, 3):
					ptstore[i, k+2] = ptstore[i, k+1]
					ptstore[i, k+1] = ptstore[i, k]
					# Record new position values
					ptstore[i] = pread.rbotpos()

					# Record initial position on first loop
					if loopcount = 1:
						startpos[i] = pread.rbotpos()
					else:

					# Proportional
					for i in range (0, 4):
						rbotdist[i] = (rbotwant - ptstore[i, 0])/(poslimit[2]-poslimit[1])

					# Integral, Simpson's Composite Rule
					if loopcount > 2
					h = tcurr-tstart / loopcount
					for i in range (0, 4):
						sumval[i] += 3*ptstore[i, 1] +ptstore[i, 0]
						intgl[i] = h/3*(sumval)
					else:
						sumval[i] += ptstore[i, 0]




					# Derivative, use 3 points to determine slope
					for i in range (0, 4):
						dslope[i] = (ptstore[i, 2]+ptstore[i, 1]+ptstore[i, 0])/3

					# Combining terms
					for i in range (0, 4):
						moveout[i] = (rbotdist[i] +intgl[i] +dslope[i])*4096 -1
						pca.set_pwm(i, 0, moveout[i])

					time.sleep(0.002)			# 500Hz operating frequency
#- End Class -#
