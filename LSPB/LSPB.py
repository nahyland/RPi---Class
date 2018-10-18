# ME 5731 Project 2: Part 3
# Author: Harrison Seung and Nicholas Hyland
# Group: 9

# Program Description #
# This code is to ramp the start and end of each movement made, it should be inserted into another program
# This is done by Linear Ssegments with Parabolic Blend



# Variables
Vm = (end to end travel distance)/2
V0 = 0
tf = we define / optimize
tb = we define / optimize
q0 = given (start position/cup position)
qf = given (cup position/dropoff position)

# new variables
pwmfreq = "easy math value"                             # motor PWM cycles per second
cycles_per_update = 1                                   # number of motor PWM cycles per duty cycle update
ticktime = cycles_per_update / pwmfreq                  # tick is the PWM update wait time
ticktotal = tb / ticktime								# total number of ticks
dcstep = "value"                                        # controls rate of acceleration per tick

# check constraints for tf and tb per (13) and (14) or (19) or summary on page 7

I was thinking code for motion would be in 3 parts like this:


## 3 While loops ##
# Part 1: Ramp up. t <= tb                              # start with some default value like tb = 0.25tf)
while dc < 95:
    dc += dcstep
    time.sleep(ticktime)

# Part 2: Constant Velocity.  tb < t <= (tf-tb)
while tcurr < (tf - tb):
    dc = 95
    time.sleep(ticktime)

# Part 3: Ramp down.  (tf-tb) < t < tf                  # end with equivalent ramp down
while dc > 0:
    dc -= dcstep
    time.sleep(ticktime)


## 2 For, 1 While loops ##
# Part 1: Ramp up. t <= tb                              # start with some default value like tb = 0.25tf)
for i in range (0, ticktotal):
    dc += dcstep
    time.sleep(ticktime)

# Part 2: Constant Velocity.  tb < t <= (tf-tb)
while tcurr < (tf - tb):
    dc = 95
    time.sleep(ticktime)

# Part 3: Ramp down.  (tf-tb) < t < tf                  # end with equivalent ramp down
for i in range (0, ticktotal):
    dc -= dcstep
    time.sleep(ticktime)
