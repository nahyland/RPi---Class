# ME 5731 Project 2: Part 3
# Author: Harrison Seung and Nicholas Hyland
# Group: 9
# Description: Class ADS1115 functions

# Import required libraries
import time, smbus
import numpy as np

# --- Define ADS1115 Registers --- #
ADS_ADDR =			0x48
ADS_PT_CONV =		0x00	# contains results from last conversion
ADS_PT_CONFIG =		0x01	# change operating modes

# Define ADS_PT_CONFIG Register Operations
# Operation status, bit [15]
ADS_CONFIG_OS =		{
			0:		0x0000,	# R/W: Device IS performing conv/No effect
			1:		0x8000	# R/W: Device is NOT performing conv/Begin single conv
			}

# Mux, bit [14:12]
ADS_CONFIG_MUX =	{
			0:		0x4000,	# A0
			1:		0x5000, # A1
			2:		0x6000, # A2
			3:		0x7000  # A3
				}

# Gain, bit [11:9]
ADS_CONFIG_GAIN =	{
			2/3:	0x0000,	# +/-6.144V
			1:		0x0200,	# +/-4.096V
			2:		0x0500,	# +/-2.048V
			4:		0x0600,	# +/-1.024V
			8:		0x0800,	# +/-0.512V
			16:		0x0A00	# +/-0.256V
			}

# Operating Mode, bit [8]
ADS_CONFIG_MODE =	{
			0:		0x0000, # Continuous
			1:		0x0100  # Single
			}

# Data Rate in samples per second, bit [7:5]
ADS_CONFIG_DR =	{
			8:		0x0000,
			16:		0x0020,
			32:		0x0040,
			64:		0x0060,
			128:	0x0080,
			250:	0x00A0,
			475:	0x00C0,
			860:	0x00E0
			}

# --- Define ADS1115 Class --- #
class ADS1115(object):

	def config_reg(self, mux,
		os=ADS_CONFIG_OS[1], gain=ADS_CONFIG_GAIN[2/3],
		mode=ADS_CONFIG_MODE[1], DR=ADS_CONFIG_DR[128]):	# Builds byte data to send to ADS_PT_CONFIG register
		config = os	# bit[15]
		config |= mux	# bit[14:12]
		config |= gain	# bit[11:9]
		config |= mode	# bit[8]
		config |= DR	# bit[7:5]
		config |= 0x03	# defaults for bit[4:0]
		return config

	def convert_value(self, low, high):	# Converts raw byte data to decimal format
		value = ((high & 0xFF) << 8 | (low & 0xFF))	# concatentate high and low values
		if (value > 0x8000):	# Get signed value
			value = value - 0x10000
		return value

	def read_adc(self, config):	# Reads value from ADS1115 given config value
		bus = smbus.SMBus(1)
		DR = 128 # defined data rate
		bus.write_i2c_block_data(ADS_ADDR, ADS_PT_CONFIG, [(config >> 8) & 0xFF, (config & 0xFF)])	# Send config to ADC
		time.sleep(1.0/DR) 	# Allow time for sample to be written
		result = bus.read_i2c_block_data(ADS_ADDR, ADS_PT_CONV, 2)	# Read pointer conversion register
		value = self.convert_value(result[1], result[0])	# Convert raw data to decimal format
		return(value)

	def readAnalog(self, channel):	# Read current potValue in voltage
		# Set ADS_Pointer_Config byte and read analog signal from channel
		config = self.config_reg(mux = ADS_CONFIG_MUX[channel], gain = ADS_CONFIG_GAIN[2/3])
		value = self.read_adc(config)
		value_max = 32768 # 16 bit max
		Gain = 6.144 # voltage value for [2/3] gain
		voltage = (value / value_max) * Gain
		return voltage

	def verVout(self, verVolt, verMin, verMax, verLen): # Convert verVolt to inches
		verPos = (verVolt-verMin) / (verMax-verMin) * verLen # ver position in inches
		return verPos

	def aziVout(self, aziVolt, aziMin, aziMax, aziLen): # Convert aziVolt to degrees
		aziPos = (aziVolt - aziMin) / (aziMax-aziMin) * aziLen # aziPos in degrees
		return aziPos

	def armVout(self, A, V, AL1, AL2, AH1, AH2, VL, VH, armLen): # Convert armVolt to inches
		C = np.array([[AL1, VL, AL1*AL1, VL*VL], # Calculate constants
					[AL2, VL, AL2*AL2, VL*VL],
					[AH1, VH, AH1*AH1, VH*VH],
					[AH2, VH, AH2*AH2, VH*VH]])
		R = np.array([[0], [armLen], [0], [armLen]]) # End points
		invC = np.linalg.inv(C)
		# Calculate X constants
		X = np.matmul(invC, R)
		armPos = X[0]*A + X[1]*V + X[2]*A*A + X[3]*V*V # armPos in inches
		return armPos[0]

	def clipVout(self, clipVolt, clipMin, clipMax, clipLen): # Convert clipVolt to degrees
		clipPos = (clipVolt - clipMin)/ (clipMax - clipMin) * clipLen # clipPos in degrees
		return clipPos

	def readALL(self): # Read all positions and return in physical units
		# Read ADS for potentiometer voltage
		azi_potVal = self.readAnalog(0)
		ver_potVal = self.readAnalog(1)
		arm_potVal = self.readAnalog(2)
		clip_potVal = self.readAnalog(3)

		position = [azi_potVal, ver_potVal, arm_potVal, clip_potVal]
		return position # returns units in Volts

	def convertALL(self, posVolt, posRange): # Read all positions and return in physical units
		# Calculate current position of joints
		aziRange = posRange[0]
		verRange = posRange[1]
		armRange = posRange[2]
		clipRange = posRange[3]

		aziPos = self.aziVout(aziVolt=posVolt[0], aziMin=aziRange[0], aziMax=aziRange[1], aziLen=aziRange[2])
		verPos = self.verVout(verVolt=posVolt[1], verMin=verRange[0], verMax=verRange[1], verLen=verRange[2])
		armPos = self.armVout(A=posVolt[2], V=posVolt[1], AL1=armRange[0], AL2=armRange[1], AH1=armRange[2], AH2=armRange[3], VL=armRange[4], VH=armRange[5], armLen = armRange[6])
		clipPos = self.clipVout(clipVolt=posVolt[3], clipMin=clipRange[0], clipMax=clipRange[1], clipLen=clipRange[2])

		position = [aziPos, verPos, armPos, clipPos] # [deg, inches, inches, degrees]
		return position
