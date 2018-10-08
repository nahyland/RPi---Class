

## Variable setup ##
min_posit = 0		# Lower extreme position, from input voltage
max_posit = 5		# Upper extreme position position, from input voltage
des_posit = 3		# Desired position, based on voltage
dc = 0			# Duty cycle of PWM output to motor

# Range calculation
posit_range = max_posit - min_posit


#- Loop for speed control -#
while 1:
	# Check position relative to lower extreme
	dist_check = (curr_posit - des_posit) / posit_range

	if dist_check > 0.5:	# If motor has 1/ of the max distance to cover
		dc = 95		# Sets speed high to cover more distance
	elif dist_check > 0.25 & dist_check <= 0.5	# Slowing on approach
		dc -= 10
	elif dist_check <= 0.25 & dist_check =/= 0	# Tapering velocity to 0
		dc -= 5
	else

#- End Loop -#