# Import Libraries#
import time
import RPi.GPIO as gpio

# Define Vairables #
Out1 = 23
Out2 = 24
freq = 500
dc_start = 5


#def init():
gpio.setmode(gpio.BCM)
gpio.setup(Out1, gpio.OUT)
gpio.setup(Out2, gpio.OUT)

pwm1 = gpio.PWM(Out1, freq)
pwm2 = gpio.PWM(Out2, freq)

def cw(t):
#	init()
	gpio.output(Out1, gpio.HIGH)
#	gpio.output(Out2, gpio.LOW)
	time.sleep(1)
	gpio.output(Out1, gpio.LOW)
	time.sleep(1)
	rampit(t)
#	time.sleep(t)
	gpio.cleanup()

def ccw(t):
#	init()
#	gpio.output(Out1, gpio.Low)
#	gpio.output(Out2, gpio.HIGH)
#	rampit(t, divs)
#	time.sleep(t)
	gpio.cleanup()

def rampit(t):
	pauseme =t / 10
	pwm1.start(5)
	time.sleep(0.5)
	sickle = dc_start
	for i in range (0, 9):
		time.sleep(pauseme)
		sickle += 10
		pwm1.ChangeDutyCycle(sickle)
		print("Duty Cycle:", sickle)
	for i in range (0, 9):
		time.sleep(pauseme)
		sickle -= 10
		pwm1.ChangeDutyCycle(sickle)
		print("Duty Cycle:", sickle)

cw(4)

#ccw(10)



