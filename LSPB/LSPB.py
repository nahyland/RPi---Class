# ME 5731 Project 2: Part 3
# Author: Harrison Seung and Nicholas Hyland
# Group: 9

# Program Description #
# This code is to ramp the start and end of each movement made, it should be inserted into another program
# This is done by Linear Ssegments with Parabolic Blend


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
#- End Initialize -#


# Variables
#Vm = (end to end travel distance)/2
#V0 = 0
#tf = we define / optimize
#q0 = given (start position/cup position)
#qf = given (cup position/dropoff position)
#tb = (q0-qf+Vm*tf)/(Vm-V0)

# new variables
#pwmfreq = "easy math value"                             # motor PWM cycles per second
#cycles_per_update = 1                                   # number of motor PWM cycles per duty cycle update
#ticktime = cycles_per_update / pwmfreq                  # tick is the PWM update wait time
#ticktotal = tb / ticktime								# total number of ticks
#dcstep = 90/ticktime									# controls rate of acceleration per tick

# check constraints for tf and tb per (13) and (14) or (19) or summary on page 7

# I was thinking code for motion would be in 3 parts like this:



#- Code -#
class LSPB(object):
	def movecontrol(self,rbotposit,rbotwant):
		pread.rbotpos()
		V0 = 0
		Vm = 7.5
		q0 = rbotposit[i]
		qf = rbotwant[i]
		tb = (q0-qf+Vm*tf)/(Vm-V0)
		tf = 2*(qf-q0)/(V0-Vm)

		if tf < 2*tb:
			# bad things
		else:
			# bleh



	return tb
	return tf
#- End Code -#


# OLD GARBAGE

## 3 While loops ##
# Part 1: Ramp up. t <= tb                              # start with some default value like tb = 0.25tf)
while dc < 95:
    dc += dcstep
    time.sleep(ticktime)

# Part 2: Constant Velocity.  tb < t <= (tf-tb)
while tcurr < (tf - tb):
    dc = 95
    time.sleep(ticktime)

# Part 3: Ramp down.  (tf-tb) < t < tf                  # end with equivalent ramp down
while dc > 0:
    dc -= dcstep
    time.sleep(ticktime)

#- End Class -#

#- Code Start -#
pca.start()
pca.set_freq(500)
