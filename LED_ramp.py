
import time
import RPi.GPIO as gpio

Out1 = 23
Out2 = 24
freq = 1000
dc_start = 5

gpio.setmode(gpio.BCM)
gpio.setup(Out1, gpio.OUT)
gpio.setup(Out2, gpio.OUT)

pwm1 = gpio.PWM(Out1, freq)

def pulse(t):
	gpio.output(Out1, gpio.HIGH)
	gpio.output(Out2, gpio.LOW)
	time.sleep(1)
	rampit(t)
	gpio.cleanup()

def rampit(t):
	pauseme =t / 10
	pwm1.start(50)
	time.sleep(0.5)
	sickle = dc_start
	for i in range (0, 9):
		time.sleep(pauseme)
		pwm1.ChangeDutyCycle(sickle)
		sickle += 10
		print("Duty Cycle:", sickle)
	for i in range (0, 9):
		time.sleep(pauseme)
		sickle -= 10
		pwm1.ChangeDutyCycle(sickle)
		print("Duty Cycle:", sickle)

pulse(3)