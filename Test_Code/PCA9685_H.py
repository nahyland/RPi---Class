# ME 5731 Project 2
# Author: Harrison Seung & Nicholas Hyland
# Objective: Interface RPi with PCA9685 module
# References: PCA9685 documentation by NXP Semiconductors

# Import libraries
import smbus  #System Management Bus Functions
import time
import math 

### PCA9685 Registers ###
PCA_ADDR	= 0x40
OUTDRV		= 0x04
ALLCALL		= 0x01
SLEEP		= 0x10
RESTART		= 0x80
PRE_SCALE	= 0xFE
 
#Mode register
PCA_MODE1	= 0x00
PCA_MODE2	= 0x01


# LED0/PWM channel 0
LED0_ON_L = 	0x06	# byte0
LED0_ON_H = 	0x07	# byte1
LED0_OFF_L = 	0x08	# byte2
LED0_OFF_H = 	0x09	# byte3

# LED1/PWM channel 1
LED1_ON_L =	0x0A
LED1_ON_H =	0x0B
LED1_OFF_L =	0x0C
LED1_OFF_H =	0x0D

#All LED
ALL_LED_ON_L       = 0xFA
ALL_LED_ON_H       = 0xFB
ALL_LED_OFF_L      = 0xFC
ALL_LED_OFF_H      = 0xFD

### Functions ###
def init(): #initialize PCA
	#set PWM channels to default
	set_all_pwm(0, 0)
	
	#set mode
	bus.write_byte_data(PCA_ADDR, PCA_MODE2, 0x04) #Mode2, default Totem-Pole structure
	bus.write_byte_data(PCA_ADDR, PCA_MODE1, 0x01) #Mode1, PCA responds to LED All call
	time.sleep(0.005) 	# allow time for oscillator to stabilize

	#Start/Reset active PWM channels
	mode1 = bus.read_byte_data(PCA_ADDR, PCA_MODE1)
	mode1 = mode1 & ~SLEEP		# wake up device
	bus.write_byte_data(PCA_ADDR, PCA_MODE1, mode1)
	time.sleep(0.005)	
	print("PWM Initialized")

def set_freq(freq): #set frequency
	#PWM frequency PRE_SCALE per 7.3.5
	prescaleval = (25000000.0/(4096.0*float(freq)))-1
	prescale = int(math.floor(prescaleval+0.5))

	#update PRE_SCALE register
	oldmode = bus.read_byte_data(PCA_ADDR, PCA_MODE1)
	newmode = (oldmode & 0x7F) | 0x10 # Update SLEEP bit to 1
	bus.write_byte_data(PCA_ADDR, PCA_MODE1, newmode)
	bus.write_byte_data(PCA_ADDR, PRE_SCALE, prescale) 
	bus.write_byte_data(PCA_ADDR, PCA_MODE1, oldmode)
	time.sleep(0.005)
	
	#Enable restart
	bus.write_byte_data(PCA_ADDR, PCA_MODE1, oldmode | 0x80)
	print("Frequency set at {0}".format(freq))

def set_pwm(channel, on, off): #set pwm
	chan_set(channel)
	bus.write_byte_data(PCA_ADDR, LED0_ON_L+4*channel, on & 0xFF)
	bus.write_byte_data(PCA_ADDR, LED0_ON_H+4*channel, on >> 8)
	bus.write_byte_data(PCA_ADDR, LED0_OFF_L+4*channel, off & 0xFF)
	bus.write_byte_data(PCA_ADDR, LED0_OFF_H+4*channel, off >> 8)
	print("channel: {2}, ON count {0}, OFF count {1}]".format(on, off, channel))

def set_all_pwm(on, off): #set all pwm 
	bus.write_byte_data(PCA_ADDR, ALL_LED_ON_L, on & 0xFF)
	bus.write_byte_data(PCA_ADDR, ALL_LED_ON_H, on >> 8)
	bus.write_byte_data(PCA_ADDR, ALL_LED_OFF_L, off & 0xFF)
	bus.write_byte_data(PCA_ADDR, ALL_LED_OFF_H, off >> 8)
	print("All PWM set [{0}, {1}]".format(on, off))

def chan_set(channel):	# Set Pwm/LED channel
	chan_on_l = "LED" + str(channel) + "_ON_L"
	chan_on_h = "LED" + str(channel) + "_ON_H"
	chan_off_l = "LED" + str(channel) + "_OFF_L"
	chan_off_h = "LED" + str(channel) + "_OFF_H"

### Main Code ###
bus = smbus.SMBus(1) #initialize SMbus

init()

#set frequency
set_freq(60)

up = 4095
down = 150

#run motor
try:
	while 1:
		set_pwm(0, 0, up)
		set_pwm(1, 0, down)
		time.sleep(1)
		set_pwm(0, 0, down)
		set_pwm(1, 0, up)
		time.sleep(1)
except KeyboardInterrupt:
	bus.close()