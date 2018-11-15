# ME 5731 Project 2: Part 3
# Author: Harrison Seung and Nicholas Hyland
# Group: 9
# Description: Create a code to move to waypoints via a "bang bang" controller


#- Initialize -#
import RPi.GPIO as gpio
import os, time, math, smbus

# ADS1115
from ADS1115 import ADS1115
from ADS1115.ADS1115 import ADS_CONFIG_MUX
from ADS1115.ADS1115 import ADS_CONFIG_GAIN
# PCA9685
from PCA9685 import PCA9685
# rbotInit
from Initialization import rbotInit
# BangBang
from BangBang import BangBang
# Waypoints
from Waypoints import Waypoint

# Setup Variables/Matrices #
# Variables
ads = ADS1115.ADS1115()
pca = PCA9685.PCA9685()
rbot = rbotInit.rbotInit()
bbcon = BangBang.BangBang()
wpts = Waypoints.Waypoints()
