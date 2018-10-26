# ME 5731 Project 2: Part 3
# Author: Harrison Seung and Nicholas Hyland
# Group: 9

# Program Description #
# This code is to ramp the start and end of each movement made, it should be inserted into another program
# This is done by Linear Ssegments with Parabolic Blend



# Variables
Vm = (end to end travel distance)/2
V0 = 0
tf = we define / optimize
tb = we define / optimize
q0 = given (start position/cup position)
qf = given (cup position/dropoff position)

# new variables
pwmfreq = "easy math value"                             # motor PWM cycles per second
cycles_per_update = 1                                   # number of motor PWM cycles per duty cycle update
ticktime = cycles_per_update / pwmfreq                  # tick is the PWM update wait time
ticktotal = tb / ticktime								# total number of ticks
dcstep = 90/ticktime									# controls rate of acceleration per tick

# check constraints for tf and tb per (13) and (14) or (19) or summary on page 7

# I was thinking code for motion would be in 3 parts like this:


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

#Start Program#

#- Import and setup classes -#
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
#- End Import and setup -#


#- Class and Functions -#
class LSPB(object):
	def rbotpos(self):								# Read ADS values and output voltage
		aziVolt = rbot.readDC(0) * 6.144 / 100
		armVolt = rbot.readDC(0) * 6.144 / 100
		verVolt = rbot.readDC(2) * 6.144 / 100
		rotVolt = rbot.readDC(3) * 6.144 / 100

 	# Convert potValues to actual position
	def verVout(self, verVolt):
		verMax = 4.51 # potValue at max range
		verMin = 2.82 # potValue at min range
		verVRange = verMax - verMin # potValue range
		verLen = 13 # ver range of motion
		verPos = (verMax - verVolt) / verVRange * verLen # ver position in inches
		return verPos

	def aziVout(self, aziVolt):
		aziMax = 4.506 # potValue at max range
		aziMin = 1.685 # potValue at min range
		aziVRange = aziMax - aziMin # potValue range
		aziLen = 380 # azi range of motion
		aziPos = (aziMax - aziVolt) / aziVRange * aziLen # aziPos in degrees
		return aziPos

	def armVout(self, A, V):
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
		return armPos

	def clipVoutself, clipVolt):
		clipMax = 4.506 # potValue at max range
		clipMin = 1.685 # potValue at min range
		clipVRange = clipMax - clipMin # potValue range
		clipLen = 90 # arm range of motion
		clipPos = (clipMax - clipVolt)/ clipVRange * clipLen # clipPos in degrees
	return clipPos


		# Container for questions, Professor's values used to get voltage from ADS
	#	def readvolt(self, channel):
	#		if channel < 4:
	#			config = ads.config_reg(mux = ADS_CONFIG_MUX[channel], gain = ADS_CONFIG_GAIN[1])
	#			value = ads.read_adc(config)
	#			return value

	#	def rbotpos(self):								# Read ADS values and output voltage
	#		aziVolt = readvolt(0) * 0.0048828
	#		armVolt = readvolt(1) * 0.0048828
	#		verVolt = readvolt(2) * 0.0048828
	#		rotVolt = readvolt(3) * 0.0048828
		# End Container

#- End Class -#

#- Code Start -#
pca.start()
pca.set_freq(500)

armc = [-8.838, 8.975, 0.108, -0.115]

#- End Code -#
