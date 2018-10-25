# ME 5731 Project 2
# Author: Harrison Seung & Nicholas Hyland
# Objective: Interface RPi with PGA9685 module
# References: PCA9685 documentation by NXP Semiconductors

# Import libraries
import smbus  #System Management Bus Functions
import time
import math

## PGA9685 Registers ##
PCA_ADDR =	0x40	 # 0x70 addresses entire board
ALLCALL = 	0x01
RESTART =	0x80
PRE_SCALE =	0xFE


# Mode Registers
PCA_MODE1 = 	0x00
PCA_MODE2 = 	0x01
OUTDRV =	0x04
SLEEP = 	0x10

# PWM channel 0
LED0_ON_L =	0x06
LED0_ON_H =	0x07
LED0_OFF_L = 	0x08
LED0_OFF_H =	0x09

# PWM channel 1
LED1_ON_L =	0x0A
LED1_ON_H =	0x0B
LED1_OFF_L =	0x0C
LED1_OFF_H =	0x0D

# All PWM channels
ALL_LED_ON_L	= 0xFA
ALL_LED_ON_H	= 0xFB
ALL_LED_OFF_L	= 0xFC
ALL_LED_OFF_H	= 0xFD


## Functions Defined ##
def init():	# initialize PCA9685
	# set PWM channels to default
	set_all_pwm(0, 0)

	# set mode
	bus.write_byte_data(PCA_ADDR, PCA_MODE2, 0x04)	# Mode2, default Totem-pole structure
	bus.write_byte_data(PCA_ADDR, PCA_MODE1, 0x01)	# Mode1, PCA responds to LED All call
	time.sleep(0.005) 	# allow time for oscillator to stabilize

	#Start/Reset active PWM channels
	mode1 = bus.read_byte_data(PCA_ADDR, PCA_MODE1)
	mode1 = mode1 & ~SLEEP
	bus.write_byte_data(PCA_ADDR, PCA_MODE1, mode1)
	time.sleep(0.005)	

def set_freq(freq):
	prescaleval = (25000000/(4096.0 * float(freq)))-1
	prescale = int(math.floor(prescaleval+0.5))

	#update PRE_SCALE register
	oldmode = bus.read_byte_data(PCA_ADDR, PCA_MODE1)
	newmode = (oldmode & 0x7F) | 0x10	#Update sleep bit to 1
	bus.write_byte_data(PCA_ADDR, PCA_MODE1, newmode)
	bus.write_byte_data(PCA_ADDR, PRE_SCALE, prescale)
	bus.write_byte_data(PCA_ADDR, PCA_MODE1, oldmode)
	time.sleep(0.005)

	#Enable restart
	bus.write_byte_data(PCA_ADDR, PCA_MODE1, oldmode | 0x80)
	print("Frequency set at {0}".format(freq))

def set_pwm(on, off):	#set pwm 
	bus.write_byte_data(PCA_ADDR, LED0_ON_L, on & 0xFF)
	bus.write_byte_data(PCA_ADDR, LED0_ON_H, on >> 8)
	bus.write_byte_data(PCA_ADDR, LED0_OFF_L, off & 0xFF)
	bus.write_byte_data(PCA_ADDR, LED0_OFF_H, off >> 8)

	bus.write_byte_data(PCA_ADDR, LED1_ON_L, on & 0xFF)
	bus.write_byte_data(PCA_ADDR, LED1_ON_H, on >> 8)
	bus.write_byte_data(PCA_ADDR, LED1_OFF_L, off & 0xFF)
	bus.write_byte_data(PCA_ADDR, LED1_OFF_H, off >> 8)

def set_all_pwm(on, off):	#set all pwm 
	bus.write_byte_data(PCA_ADDR, ALL_LED_ON_L, on & 0xFF)
	bus.write_byte_data(PCA_ADDR, ALL_LED_ON_H, on >> 8)
	bus.write_byte_data(PCA_ADDR, ALL_LED_OFF_L, off & 0xFF)
	bus.write_byte_data(PCA_ADDR, ALL_LED_OFF_H, off >> 8)


## Main Code ##
bus = smbus.SMBus(1)	# initialize SMbus

init()

set_freq(100)	# Set output frequency

up = 4095
down = 150

# Run motor
try:
	while True:
		set_pwm(0, up)
		time.sleep(1)
		set_pwm(0, down)
		time.sleep(1)
except KeyboardInterrupt:
	bus.close()