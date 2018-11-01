# ME 5731 Project 2: Part 1
# Author: Harrison Seung and Nicholas Hyland
# Group: 9
# Description: Class PCA9685 functions
# Date: 10/4/2018

# Import required libraries
import time, smbus, math

# --- Define PCA9685 Registers --- #
PCA_ADDR            = 0x40
OUTDRV              = 0x04
ALLCALL             = 0x01
LEDINVRT            = 0x10
SLEEP               = 0x10
RESTART             = 0x80
PRE_SCALE           = 0xFE
PCA_MODE1           = 0x00
PCA_MODE2           = 0x01
LED0_ON_L           = 0x06 # byte0
LED0_ON_H           = 0x07 # byte1
LED0_OFF_L          = 0x08 # byte2
LED0_OFF_H          = 0x09 # byte3
ALL_LED_ON_L        = 0xFA
ALL_LED_ON_H        = 0xFB
ALL_LED_OFF_L       = 0xFC
ALL_LED_OFF_H       = 0xFD

# --- Define PCA9685 Class --- #
class PCA9685(object):
	# Initialize PCA9685 Modules
	def start(self):
		bus = smbus.SMBus(1)
		#set PWM channels to default
		self.set_all_pwm(0, 0)

		#set mode
		bus.write_byte_data(PCA_ADDR, PCA_MODE2, OUTDRV) #Mode2, default Totem-Pole structure
		bus.write_byte_data(PCA_ADDR, PCA_MODE1, ALLCALL) #Mode1, PCA responds to LED All call
		time.sleep(0.005) 	# allow time for oscillator to stabilize

		#Start/Reset active PWM channels
		mode1 = bus.read_byte_data(PCA_ADDR, PCA_MODE1)
		mode1 = mode1 & ~SLEEP		# wake up device
		bus.write_byte_data(PCA_ADDR, PCA_MODE1, mode1)
		time.sleep(0.005)

	# Set frequency of pwm.  Same for all channels
	def set_freq(self, freq): #set_freq(self, frequency)
		bus = smbus.SMBus(1)
		#PWM frequency PRE_SCALE per 7.3.5
		prescaleval = (25000000.0/(4096.0*float(freq)))-1
		prescale = int(math.floor(prescaleval+0.5))

		#update PRE_SCALE register
		defaultMode = bus.read_byte_data(PCA_ADDR, PCA_MODE1)
		lowpowerMode = (defaultMode & 0x7F) | 0x10 # Update SLEEP bit to 1
		bus.write_byte_data(PCA_ADDR, PCA_MODE1, lowpowerMode)
		bus.write_byte_data(PCA_ADDR, PRE_SCALE, prescale)
		bus.write_byte_data(PCA_ADDR, PCA_MODE1, defaultMode)
		time.sleep(0.005)

		#Enable restart
		bus.write_byte_data(PCA_ADDR, PCA_MODE1, defaultMode | 0x80)

	# Set pwm for specified channel
	def set_pwm(self, channel, on, off): #set_pwm(self, on count, off count)
		bus = smbus.SMBus(1)
		bus.write_byte_data(PCA_ADDR, LED0_ON_L + 4*channel, on & 0xFF)
		bus.write_byte_data(PCA_ADDR, LED0_ON_H + 4*channel, on >> 8)
		bus.write_byte_data(PCA_ADDR, LED0_OFF_L + 4*channel, off & 0xFF)
		bus.write_byte_data(PCA_ADDR, LED0_OFF_H + 4*channel, off >> 8)

	# Set pwm for all channels
	def set_all_pwm(self, on, off): #set_all_pwm(self, on count, off count)
		bus = smbus.SMBus(1)
		bus.write_byte_data(PCA_ADDR, ALL_LED_ON_L, on & 0xFF)
		bus.write_byte_data(PCA_ADDR, ALL_LED_ON_H, on >> 8)
		bus.write_byte_data(PCA_ADDR, ALL_LED_OFF_L, off & 0xFF)
		bus.write_byte_data(PCA_ADDR, ALL_LED_OFF_H, off >> 8)

	def setPWMchannel(self, channel, dirVal):		# Set PWM pin and dir
		if channel == 0:	# azimuth
			if dirVal[channel] == 1:
				posPin = 0
				negPin = 1
			elif dirVal[0] == -1:
				posPin = 1
				negPin = 0
		elif channel == 1:	# vertical
			if dirVal[channel] == 1:
				posPin = 2
				negPin = 3
			elif dirVal[channel] == 1:
				posPin = 3
				negPin = 2
		elif channel == 2:	# arm
			if dirVal[channel] == 1:
				posPin = 4
				negPin = 5
			elif dirVal[channel] == 1:
				posPin = 5
				negPin = 4
		elif channel == 3:	# clipper rotation
			if dirVal[channel] == 1:
				posPin = 6
				negPin = 7
			elif dirVal[channel] == 1:
				posPin = 7
				negPin = 6
		return posPin, negPin

	def setMotor(self, channel, dc, dir, leddir): 	# Set PWM duty cycle
		# set count for pwm to turn off in pulse length of 4096
		off_count = int(math.floor((dc/100) * 4095 - 1) + .5)
		# select PWM pins
		posPin, negPin, name = self.setPWMchannel(channel, leddir[channel])
		# Direction 1
		if dir == 1:
			# set direction
			self.set_pwm(posPin, 0, 0) #LED0 pwm is ON/OFF at 0/off_count
			self.set_pwm(negPin, 0, off_count) #LED1 pwm is ON/OFF at 0/off_count
		# Direction 2
		elif dir == -1:
	    		# set direction
			self.set_pwm(posPin, 0, off_count) #LED0 pwm is ON/OFF at 0/off_count
			self.set_pwm(negPin, 0, 0) #LED1 pwm is ON/OFF at 0/off_count

		# Stop mode
		else:
			self.set_all_pwm(0, 0) #LED0 pwm is set off # Update motor

	def dirset(self):								# Direction Setter/verification of direction
		for i in range (4):							# Runs through all 4 motor/sensor sets
			dc_base = readDC(0+i)					# Read current position from sensor
			self.set_pwm(0+2*i ,0 , 2082)			# Use first channel to move motor
			print("PWM {0} initial value recorded".format(0+2*i))
			input("Press Enter to continue...")
			#time.sleep(0.1)

			self.set_pwm(0+2*i ,0 , 0)				# Stops PWM signal to first channel
			dc = readDC(0+i)						# Read new position from sensor

			print("PWM {0} second value recorded".format(0+2*i))
			input("Press Enter to continue...")
			#time.sleep(0.001)

			# send signal to opposite LED out (i.e. LED1)
			self.set_pwm(1+2*i, 0, 2082)				# Activate motor, return to start position at 50% duty cycle
			#time.sleep(0.1)
			self.set_pwm(1+2*i, 0, 0)

			dc_dir = dc - dc_base					# Calc dir of first channel

			if dc_dir < 0:							# Why use abs val and 0.01?
				leddir[i] = -1
			elif dc_dir > 0:
				leddir[i] = 1
			else:
				print("Read error")
		return leddir

	# Stop code
	def exit(self):
		bus = smbus.SMBus(1)
		bus.close()
		self.set_all_pwm(0, 0)
