#  This program is for concatenating a string #

pre_val = "LED"		# string to be used before variable
post_val = "_ON_H"	# string to be used after variable

chan_pwm = 1		# integer to be added to string



# Adding together pre_val, the integer, and _post_val
fin_string = pre_val + str(chan_pwm) + post_val

print(fin_string)	# Showing the user the newly formed string
