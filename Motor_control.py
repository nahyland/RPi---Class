
import time
import RPi.GPIO as GPIO

In1 = 8
In2 = 10

def init():
	GPIO.setmode(GPIO.BOARD)
	GPIO.setup(In1, GPIO.OUT)
	GPIO.setup(In2, GPIO.OUT)

def cw(t):
	init()
	GPIO.output(In1, GPIO.HIGH)
	GPIO.output(In2, GPIO.LOW)
	time.sleep(t)
	GPIO.cleanup()

def ccw(t):
	init()
	GPIO.output(In1, GPIO.LOW)
	GPIO.output(In2, GPIO.HIGH)
	time.sleep(t)
	GPIO.cleanup()

cw(4)

ccw(4)