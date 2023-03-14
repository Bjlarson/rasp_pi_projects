import socket
import RPi.GPIO as GPIO
import time
from adafruit_servokit import ServoKit
import adafruit_mpl3115a2
import serial
import string
import pynmea2
import math
import smbus

#Setup servo
kit = ServoKit(channels = 8)

#Setup Speed, Altitude and Direction Variables
targetAltitude = input() 
targetAltDist = input("Feet from Target") #should be in feet from target
speed = input("Feet per min")
currentTime = 0
currentAlt = 0
lastTime = 0
lastAlt = 0
c_s_rate = 0
TargetLat = 0
TargetLong = 0
beginingLat = 0
beginingLong = 0
beginingDirection = 0

#Setup Controls locations
elevator = 1
rudder = 0
motor1 = 2
motor2 = 3

selfControlled = False        

# Get I2C bus
bus = smbus.SMBus(3)
 
# I2C address of the device
MPL3115A2_DEFAULT_ADDRESS			= 0x60
# MPL3115A2 Regster Map
MPL3115A2_REG_STATUS				= 0x00 # Sensor status Register
MPL3115A2_REG_PRESSURE_MSB			= 0x01 # Pressure data out MSB
MPL3115A2_REG_PRESSURE_CSB			= 0x02 # Pressure data out CSB
MPL3115A2_REG_PRESSURE_LSB			= 0x03 # Pressure data out LSB
MPL3115A2_REG_TEMP_MSB				= 0x04 # Temperature data out MSB
MPL3115A2_REG_TEMP_LSB				= 0x05 # Temperature data out LSB
MPL3115A2_REG_DR_STATUS				= 0x06 # Data Ready status registe
MPL3115A2_OUT_P_DELTA_MSB			= 0x07 # Pressure data out delta MSB
MPL3115A2_OUT_P_DELTA_CSB			= 0x08 # Pressure data out delta CSB
MPL3115A2_OUT_P_DELTA_LSB			= 0x09 # Pressure data out delta LSB
MPL3115A2_OUT_T_DELTA_MSB			= 0x0A # Temperature data out delta MSB
MPL3115A2_OUT_T_DELTA_LSB			= 0x0B # Temperature data out delta LSB
MPL3115A2_REG_WHO_AM_I				= 0x0C # Device Identification Register
MPL3115A2_PT_DATA_CFG				= 0x13 # PT Data Configuration Register
MPL3115A2_CTRL_REG1					= 0x26 # Control Register-1
MPL3115A2_CTRL_REG2					= 0x27 # Control Register-2
MPL3115A2_CTRL_REG3					= 0x28 # Control Register-3
MPL3115A2_CTRL_REG4					= 0x29 # Control Register-4
MPL3115A2_CTRL_REG5					= 0x2A # Control Register-5
 
# MPL3115A2 PT Data Configuration Register
MPL3115A2_PT_DATA_CFG_TDEFE			= 0x01 # Raise event flag on new temperature data
MPL3115A2_PT_DATA_CFG_PDEFE			= 0x02 # Raise event flag on new pressure/altitude data
MPL3115A2_PT_DATA_CFG_DREM			= 0x04 # Generate data ready event flag on new pressure/altitude or temperature data
 
# MPL3115A2 Control Register-1 Configuration
MPL3115A2_CTRL_REG1_SBYB			= 0x01 # Part is ACTIVE
MPL3115A2_CTRL_REG1_OST				= 0x02 # OST Bit ACTIVE
MPL3115A2_CTRL_REG1_RST				= 0x04 # Device reset enabled
MPL3115A2_CTRL_REG1_OS1				= 0x00 # Oversample ratio = 1
MPL3115A2_CTRL_REG1_OS2				= 0x08 # Oversample ratio = 2
MPL3115A2_CTRL_REG1_OS4				= 0x10 # Oversample ratio = 4
MPL3115A2_CTRL_REG1_OS8				= 0x18 # Oversample ratio = 8
MPL3115A2_CTRL_REG1_OS16			= 0x20 # Oversample ratio = 16
MPL3115A2_CTRL_REG1_OS32			= 0x28 # Oversample ratio = 32
MPL3115A2_CTRL_REG1_OS64			= 0x30 # Oversample ratio = 64
MPL3115A2_CTRL_REG1_OS128			= 0x38 # Oversample ratio = 128
MPL3115A2_CTRL_REG1_RAW				= 0x40 # RAW output mode
MPL3115A2_CTRL_REG1_ALT				= 0x80 # Part is in altimeter mod
MPL3115A2_CTRL_REG1_BAR				= 0x00 # Part is in barometer mode

mpl3115a2 = MPL3115A2()
mpl3115a2.control_alt_config()
mpl3115a2.data_config()

def control_alt_config(self):
	"""Select the Control Register-1 Configuration from the given provided value"""
	CONTROL_CONFIG = (MPL3115A2_CTRL_REG1_SBYB | MPL3115A2_CTRL_REG1_OS128 | MPL3115A2_CTRL_REG1_ALT)
	bus.write_byte_data(MPL3115A2_DEFAULT_ADDRESS, MPL3115A2_CTRL_REG1, CONTROL_CONFIG)
    
def data_config(self):
    """Select the PT Data Configuration Register from the given provided value"""
    DATA_CONFIG = (MPL3115A2_PT_DATA_CFG_TDEFE | MPL3115A2_PT_DATA_CFG_PDEFE | MPL3115A2_PT_DATA_CFG_DREM)
    bus.write_byte_data(MPL3115A2_DEFAULT_ADDRESS, MPL3115A2_PT_DATA_CFG, DATA_CONFIG)
 
def read_alt_temp(self):
    """Read data back from MPL3115A2_REG_STATUS(0x00), 6 bytes
    status, tHeight MSB, tHeight CSB, tHeight LSB, temp MSB, temp LSB"""
    data = bus.read_i2c_block_data(MPL3115A2_DEFAULT_ADDRESS, MPL3115A2_REG_STATUS, 6)

    # Convert the data to 20-bits
    tHeight = ((data[1] * 65536) + (data[2] * 256) + (data[3] & 0xF0)) / 16
    temp = ((data[4] * 256) + (data[5] & 0xF0)) / 16

    altitude = tHeight / 16.0
    cTemp = temp / 16.0
    fTemp = cTemp * 1.8 + 32
 
    return {'a' : altitude, 'c' : cTemp, 'f' : fTemp}
 
def control_pres_config(self):
    """Select the Control Register-1 Configuration from the given provided value"""
    CONTROL_CONFIG = (MPL3115A2_CTRL_REG1_SBYB | MPL3115A2_CTRL_REG1_OS128)
    bus.write_byte_data(MPL3115A2_DEFAULT_ADDRESS, MPL3115A2_CTRL_REG1, CONTROL_CONFIG)
 
def read_pres(self):
    """Read data back from MPL3115A2_REG_STATUS(0x00), 4 bytes
    status, pres MSB, pres CSB, pres LSB"""
    data = bus.read_i2c_block_data(MPL3115A2_DEFAULT_ADDRESS, MPL3115A2_REG_STATUS, 4)

    # Convert the data to 20-bits
    pres = ((data[1] * 65536) + (data[2] * 256) + (data[3] & 0xF0)) / 16
    pressure = (pres / 4.0) / 1000.0

    return {'p' : pressure}

def CalculateDensityAltitude(altitude, temperature):
	standardTemp = (altitude/1000)*2
	
	return altitude+(120(temperature - standardTemp))

def FeetPerMin(CurrentAltimeter,LastAltimeter,curTime,lastT):
	return ((LastAltimeter - CurrentAltimeter)/(curTime-lastT))*60

def DetermineClimbDesentRate():
	targetFPM = (targetAltitude - currentAlt)/(speed/targetAltDist)
	if(targetFPM > 500):
		return 500
	else:
		return targetFPM

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
	return (θ*180/math.pi + 360) % 360; # in degrees

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


s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
s.bind(("192.168.1.13",1234))
s.listen(5)

clientsocket, address = s.accept()
print(f"Connection from {address} has been established!")
    
msg = "Welcome to the server!"
    
clientsocket.send(bytes(msg, "utf-8"))

f = open('Altimeter.txt', 'w')
f.close()
f = open('SpeedAndDirection.txt', 'a')
f.write('\n')
f.close()

#arm ESC
kit.servo[motor1].angle = 0
kit.servo[motor2].angle = 0

msg = "Connect Battery"
clientsocket.send(bytes(msg, "utf-8"))

while True:
    incomeing = clientsocket.recv(8).decode()
    print (incomeing)
        
    if(incomeing[0:4] == "prep"):
        print("servo command")
        clientsocket.send(bytes("servo command", "utf-8"))

        turnAngle = int(incomeing[3:len(incomeing)])
        kit.servo[rudder].angle = turnAngle
            
    elif(incomeing[0:4] == "endd"):
        print("servo command")
        clientsocket.send(bytes("servo command", "utf-8"))

        elevatorAngle = int(incomeing[3:len(incomeing)])
        kit.servo[elevator].angle = elevatorAngle

    elif(incomeing[0:4] == "stop"):
        print("Stop")
        clientsocket.send(bytes("Stop", "utf-8"))
        kit.servo[motor1].angle = 0
        kit.servo[motor2].angle = 0
        x = 'z'

    elif(incomeing[0:4] == "strt"):
        print("Motor command")
        clientsocket.send(bytes("Motor command", "utf-8"))
            
        x = incomeing[3:len(incomeing)]
		
		alt = mpl3115a2.read_alt_temp()
		lasttime = currentTime
		currentTime = time.time()
		lastAlt = currentAlt
		currentAlt = (alt['a'] * 3.2808399)
		print("Altitude : %.2f Meeters"%(alt['a']))
		print("Altitude : %.2f Feet"%(alt['a'] * 3.2808399))
		print("Temperature in Celsius : %.2f C"%(alt['c']))
		print("Temperature in Fahrenheit : %.2f F"%(alt['f']))
		mpl3115a2.control_pres_config()
		time.sleep(1)
		pres = mpl3115a2.read_pres()
		print("Pressure : %.2f kPa"%(pres['p']))
		densityAltitude = CalculateDensityAltitude(currentAlt,alt['c'])
		print(densityAltitude)


		if(currentTime != 0 and lastTime != 0):
			c_s_rate = FeetPerMin(currentAlt,lastAlt,currentTime,lastTime)
			print("Feet per Min: " + c_s_rate)
		else:
			currenttime = time.time()
			print("Feet per Min: 0")


		if(c_s_rate > DetermineClimbDesentRate()):
			print("Nose Down")
		elif(c_s_rate < DetermineClimbDesentRate()):
			print("Nose Up")

		print(" ************************************* ")



		f = open('Altimeter.txt', 'a')
		f.write("Altitude : %.2f Feet"%(alt['a'] * 3.2808399))
		f.write('\n')
		f.write("Temperature in Fahrenheit : %.2f F"%(alt['f']))
		f.write('\n')
		f.write("Pressure : %.2f kPa"%(pres['p']))
		f.write('\n')
		f.write(densityAltitude)
		f.write('\n')
		f.write(" *********")
		f.write('\n')
		f.close()




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
			f = open('SpeedAndDirection.txt', 'a')
			f.write(gps + " CurrentDirection = " + str(currentDirection) + " MPH = " + str(mph) + " FPS = " + str(fps) + " TurnAmount = " + str(turnAmount) + " Takeoff/LandingDirection = " + str(beginingDirection))
			f.write('\n')
			f.close()