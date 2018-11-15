# ME 5731 Project 2: Part 1
# Author: Harrison Seung and Nicholas Hyland
# Group: 9
# Description: File for setting waypoints

# Waypoints #
beginpos = [0,0,0]
cuppos = [20,5,5]
droppos = [140,8,7]

# wp = [azimuth, vertical, arm]; measured in degrees and inches
wp1 = [beginpos[0],beginpos[1],beginpos[2]]
wp2 = [cuppos[0],cuppos[1]-1,cuppos[2]-2]
wp3 = [cuppos[0],cuppos[1]-1,cuppos[2]]
wp4 = [cuppos[0],cuppos[1]+1,cuppos[2]]
wp5 = [droppos[0],droppos[1]+1,droppos[2]]
wp6 = [droppos[0],droppos[1]-1,droppos[2]]
wp7 = [droppos[0],droppos[1]-1,droppos[2]-2]
wp8 = [beginpos[0],beginpos[1],beginpos[2]]

# DC for speed
dcwant = 50


#- Class -#
Class Waypoints(self):
	def waypoint(self):
		waypt = [wp1;wp2;wp3;wp4;wp5;wp6;wp7;wp8]
	return waypt
	return dcwant
#- End Class -#
