import serial
import time
import string
import pynmea2
import math

TargetLat = 41.808376
TargetLong = -111.793380
beginingLat = 0
beginingLong = 0
beginingDirection = 0
currentlat = 0
currentlong = 0
currentTime = 0
currentDirection = 0
lastLat = 0
LastLong = 0
lastTime = 0
lastDirection = 0
miles = 0
mph = 0
fps = 0
turnAmount = 90

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

def FeetPerSecond(miles,time1,time2):
	return ((miles*5280)/(time2-time1))

def MilesPerHour(miles,time1,time2):
	return (miles/(time2-time1))*60*60

def DeterminDirectionFromTwoPoints(lat1,long1,lat2,long2):
	y = math.sin(long2-long1) * math.cos(lat2)
	x = math.cos(lat1) * math.sin(lat2) - math.sin(lat1) * math.cos(lat2) * math.cos(long2-long1)
	θ = math.atan2(y, x)
	return (θ*180/math.PI + 360) % 360; # in degrees

def DeterminBestTurnToPoint(currentDirection, TargetDirection):
	a = TargetDirection-currentDirection
	b = TargetDirection - currentDirection + 360
	c = TargetDirection - currentDirection - 360
	
	list = [abs(a),abs(b),abs(c)]

	if(min(list) == abs(a)):
		return (a/2)+90
	if(min(list) == abs(b)):
		return (b/2)+90
	if(min(list) == abs(c)):
		return (c/2)+90
	

while True:
	port="/dev/ttyAMA0"
	ser=serial.Serial(port, baudrate=9600, timeout=0.5)
	dataout = pynmea2.NMEAStreamReader()
	newdata=ser.readline()

	if newdata[0:6] == b"$GPRMC":
		newmsg=pynmea2.parse(newdata.decode("utf-8"))
		lat=newmsg.latitude
		lng=newmsg.longitude

		if(beginingLat == 0):
			beginingLat = lat
			currentTime = time.time()
		else:
			lastLat = currentlat
			lastTime = currentTime
			currentlat = lat
			currentTime = time.time()
			
		if(beginingLong == 0):
			beginingLong = lng
		else:
			lastlong = currentlong
			currentlong = lng

		if(lastLat != 0 and lastlong != 0):
			currentDirection = DeterminDirectionFromTwoPoints(lastLat,lastlong,currentlat,currentlong)
			turnAmount = DeterminBestTurnToPoint(currentDirection,DeterminDirectionFromTwoPoints(currentlat,currentlong,TargetLat,TargetLong))
			miles = MilesBetweenTwoPoints(lastLat,lastlong,currentlat,currentlong)

		if(beginingDirection == 0 and currentlat != 0 and currentlong != 0):
			beginingDirection = DeterminDirectionFromTwoPoints(beginingLat,beginingLong,currentlat,currentlong)
			miles = MilesBetweenTwoPoints(beginingLat,beginingLong,currentlat,currentlong)

		if(lastTime != 0):
			mph = MilesPerHour(miles,lastTime,currentTime)
			fps = FeetPerSecond(miles,lastTime,currentTime)

		gps = "Latitude = " + str(lat) + " and Longitude = " + str(lng)
		print(gps)
		f = open('gps.txt', 'a')
		f.write(gps + " CurrentDirection = " + str(currentDirection) + " MPH = " + str(mph) + " FPS = " + str(fps) + " TurnAmount = " + str(turnAmount) + " Takeoff/LandingDirection = " + str(beginingDirection))
		f.write('\n')
		f.close()