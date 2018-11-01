# ME 5731 Project 2: Part 3
# Author: Harrison Seung and Nicholas Hyland
# Group: 9

# Test Code #

## Initialize ##
import RPi.GPIO as gpio
import os, time, math, smbus

# Import classes #
# ADS1115
from ADS1115 import ADS1115
from ADS1115.ADS1115 import ADS_CONFIG_MUX
from ADS1115.ADS1115 import ADS_CONFIG_GAIN

# PCA9685
from PCA9685 import PCA9685

# rbotInit
from Initialization import rbotInit


# Setup
ads = ADS1115.ADS1115()
pca = PCA9685.PCA9685()
rbot = rbotInit.rbotInit()


pca.start()
pca.set_freq(500)
#time.sleep(1)
leddir = rbot.dirset()
print(leddir)
