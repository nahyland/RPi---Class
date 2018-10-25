# Import Libraries#
import time
import RPi.GPIO as gpio

# Define Variables #
Out1 = 14
Out2 = 15
freq = 500


gpio.setmode(gpio.BCM)
gpio.setwarnings(False)
gpio.setup(Out1, gpio.OUT)
gpio.setup(Out2, gpio.OUT)
pwm1 = gpio.PWM(Out1, freq)
#pwm2 = gpio.PWM(Out2, freq)

def cw(t):
	gpio.output(Out1, gpio.HIGH)
	gpio.output(Out2, gpio.LOW)
#	time.sleep(1)
#	pwm1.start(50)
	time.sleep(t)
	gpio.cleanup()

cw(5)

#gpio.output(Out1, gpio.HIGH)
#gpio.output(Out2, gpio.LOW)
#time.sleep(1)
#pwm1.start(50)
#time.sleep(3)
#gpio.cleanup()