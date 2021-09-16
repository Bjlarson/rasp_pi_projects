import serial
import time
import string
import pynmea2
import math

TargetLat = 41.808376
TargetLong = -111.793380
beginingLat = 0
beginingLong = 0
currentlat = 0
currentlong = 0
lastLat = 0
LastLong = 0

f = open('gps.txt', 'a')
f.write('\n')
f.close()

def MilesBetweenTwoPoints(lat1,long1,lat2,long2):
	R=6371000                               # radius of Earth in meters
	phi_1=math.radians(lat1)
	phi_2=math.radians(lat2)

	delta_phi=math.radians(lat2-lat1)
	delta_lambda=math.radians(long2-long1)

	a=math.sin(delta_phi/2.0)**2+\
    	math.cos(phi_1)*math.cos(phi_2)*\
        math.sin(delta_lambda/2.0)**2
	c=2*math.atan2(math.sqrt(a),math.sqrt(1-a))
        
	meters = R*c                         # output distance in meters
	km = meters/1000.0              # output distance in kilometers
	miles = meters*0.000621371      # output distance in miles
	feet = miles*5280              # output distance in feet

	return miles

def Feet(miles):
	return miles*5280 

def MilesPerHour(miles,time1,time2):
	return (miles/(time2-time1))*60*60

def DeterminDirectionFromTwoPoints(lat1,long1,lat2,long2):
	y = Math.sin(λ2-λ1) * Math.cos(φ2)
	x = Math.cos(φ1)*Math.sin(φ2) - Math.sin(φ1)*Math.cos(φ2)*Math.cos(λ2-λ1)
	θ = Math.atan2(y, x)
	brng = (θ*180/Math.PI + 360) % 360; # in degrees

while True:
	port="/dev/ttyAMA0"
	ser=serial.Serial(port, baudrate=9600, timeout=0.5)
	dataout = pynmea2.NMEAStreamReader()
	newdata=ser.readline()

	if newdata[0:6] == b"$GPRMC":
		newmsg=pynmea2.parse(newdata.decode("utf-8"))
		lat=newmsg.latitude
		lng=newmsg.longitude


		gps = "Latitude = " + str(lat) + " and Longitude = " + str(lng)
		print(gps)
		f = open('gps.txt', 'a')
		f.write(gps)
		f.write('\n')
		f.close()