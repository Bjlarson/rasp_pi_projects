import bluetooth
import datetime
import smbus
import datetime
import time
import serial
import pynmea2
import math
import PiCamera
import json
import RPi.GPIO as GPIO
from adafruit_servokit import ServoKit

#region global variables
#Location Variables
portNumber = 1
pictureLocation = "/home/blake/Documents/FlightPics/"
gpsPort="/dev/ttyS0"
elevatorPort = 1
rudderPort = 0
motorPort = 2
motorMax = 180
motorMin = 20
mode = "stop"
takeoffSpeed = 20.0
currentWaypoint = 0
pathpoints = []
#endregion


#region Airplane class
#airplane Data Class
class Airplane:
    def __init__(self, elevatorAngle, rudderAngle, motorSpeed, startingAlt, lastPitch, lastAlt, LastLat, LastLong, lastRate, lastSpeed, lastTime, landDirection, mode):
        self.elevatorAngle = elevatorAngle
        self.rudderAngle = rudderAngle
        self.motorSpeed = motorSpeed
        self.startingAlt = startingAlt
        self.lastPitch = lastPitch
        self.lastAlt = lastAlt
        self.lastLat = LastLat
        self.lastLong = LastLong
        self.lastRate = lastRate
        self.lastSpeed = lastSpeed
        self.lastTime = lastTime
        self.landDirection = landDirection
        self.mode = mode
#endregion

#region altimeter setup - Variables
# set I2C address of MPL3115A2 sensor
MPL3115A2_DEFAULT_ADDRESS = 0x60

# define MPL3115A2 register map
MPL3115A2_REG_STATUS = 0x00  # Sensor status Register
MPL3115A2_REG_PRESSURE_MSB = 0x01  # Pressure data out MSB
MPL3115A2_REG_PRESSURE_CSB = 0x02  # Pressure data out CSB
MPL3115A2_REG_PRESSURE_LSB = 0x03  # Pressure data out LSB
MPL3115A2_REG_TEMP_MSB = 0x04  # Temperature data out MSB
MPL3115A2_REG_TEMP_LSB = 0x05  # Temperature data out LSB
MPL3115A2_REG_DR_STATUS = 0x06  # Data Ready status register
MPL3115A2_OUT_P_DELTA_MSB = 0x07  # Pressure data out delta MSB
MPL3115A2_OUT_P_DELTA_CSB = 0x08  # Pressure data out delta CSB
MPL3115A2_OUT_P_DELTA_LSB = 0x09  # Pressure data out delta LSB
MPL3115A2_OUT_T_DELTA_MSB = 0x0A  # Temperature data out delta MSB
MPL3115A2_OUT_T_DELTA_LSB = 0x0B  # Temperature data out delta LSB
MPL3115A2_REG_WHO_AM_I = 0x0C  # Device Identification Register
MPL3115A2_PT_DATA_CFG = 0x13  # PT Data Configuration Register
MPL3115A2_CTRL_REG1 = 0x26  # Control Register-1
MPL3115A2_CTRL_REG2 = 0x27  # Control Register-2
MPL3115A2_CTRL_REG3 = 0x28  # Control Register-3
MPL3115A2_CTRL_REG4 = 0x29  # Control Register-4
MPL3115A2_CTRL_REG5 = 0x2A  # Control Register-5

# define MPL3115A2 PT Data Configuration Register values
MPL3115A2_PT_DATA_CFG_TDEFE = 0x01  # Raise event flag on new temperature data
MPL3115A2_PT_DATA_CFG_PDEFE = 0x02  # Raise event flag on new pressure/altitude data
MPL3115A2_PT_DATA_CFG_DREM = 0x04  # Generate data ready event flag on new pressure/altitude or temperature data

# MPL3115A2 Control Register-1 Configuration
MPL3115A2_CTRL_REG1_SBYB = 0x01  # Part is ACTIVE
MPL3115A2_CTRL_REG1_OST = 0x02  # OST Bit ACTIVE
MPL3115A2_CTRL_REG1_RST = 0x04  # Device reset enabled
MPL3115A2_CTRL_REG1_OS1 = 0x00  # Oversample ratio = 1
MPL3115A2_CTRL_REG1_OS2 = 0x08  # Oversample ratio = 2
MPL3115A2_CTRL_REG1_OS4 = 0x10  # Oversample ratio = 4
MPL3115A2_CTRL_REG1_OS8 = 0x18  # Oversample ratio = 8
MPL3115A2_CTRL_REG1_OS16 = 0x20  # Oversample ratio = 16
MPL3115A2_CTRL_REG1_OS32 = 0x28  # Oversample ratio = 32
MPL3115A2_CTRL_REG1_OS64 = 0x30  # Oversample ratio = 64
MPL3115A2_CTRL_REG1_OS128 = 0x38  # Oversample ratio = 128
MPL3115A2_CTRL_REG1_RAW = 0x40  # RAW output mode
MPL3115A2_CTRL_REG1_ALT = 0x80  # Part is in altimeter mod
MPL3115A2_CTRL_REG1_BAR = 0x00  # Part is in barometer mode
#endregion

#region Gyro - Variables
#some MPU6050 Registers and their Address
PWR_MGMT_1   = 0x6B
SMPLRT_DIV   = 0x19
CONFIG       = 0x1A
GYRO_CONFIG  = 0x1B
INT_ENABLE   = 0x38
ACCEL_XOUT_H = 0x3B
ACCEL_YOUT_H = 0x3D
ACCEL_ZOUT_H = 0x3F
GYRO_XOUT_H  = 0x43
GYRO_YOUT_H  = 0x45
GYRO_ZOUT_H  = 0x47
#endregion
 
#region altimeter class - Methods
class MPL3115A2:
    def control_alt_config(self):
        """Select the Control Register-1 Configuration from the given provided value"""
        CONTROL_CONFIG = MPL3115A2_CTRL_REG1_SBYB | MPL3115A2_CTRL_REG1_OS128 | MPL3115A2_CTRL_REG1_ALT
        bus.write_byte_data(MPL3115A2_DEFAULT_ADDRESS, MPL3115A2_CTRL_REG1, CONTROL_CONFIG)
 
    def data_config(self):
        """Select the PT Data Configuration Register from the given provided value"""
        DATA_CONFIG = MPL3115A2_PT_DATA_CFG_TDEFE | MPL3115A2_PT_DATA_CFG_PDEFE | MPL3115A2_PT_DATA_CFG_DREM
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
 
        return {"a": altitude, "c": cTemp, "f": fTemp}
    
    def read_alt(self):
        """Read data back from MPL3115A2_REG_STATUS(0x00), 6 bytes
        status, tHeight MSB, tHeight CSB, tHeight LSB, temp MSB, temp LSB"""
        data = bus.read_i2c_block_data(MPL3115A2_DEFAULT_ADDRESS, MPL3115A2_REG_STATUS, 6)
 
        # Convert the data to 20-bits
        tHeight = ((data[1] * 65536) + (data[2] * 256) + (data[3] & 0xF0)) / 16
 
        altitude = tHeight / 16.0
 
        return altitude

    def read_pres(self):
        """Read data back from MPL3115A2_REG_STATUS(0x00), 4 bytes
        status, pres MSB, pres CSB, pres LSB"""
        data = self.bus.read_i2c_block_data(self.address, adafruit_mpl3115a2.REG_STATUS, 4)

        # Convert the data to 20-bits
        pres = ((data[1] * 65536) + (data[2] * 256) + (data[3] & 0xF0)) / 16
        pressure = (pres / 4.0) / 1000.0

        return {'p': pressure}
#endregion

#region GPS Methods
#Gets Latitude and Longitude
def Get_Cordinates():
    ser = serial.Serial(gpsPort, baudrate=9600, timeout=0.5)
    dataout = pynmea2.NMEAStreamReader()
    newdata = ser.readline()

    if newdata[0:6] == b"$GPRMC":
        newmsg = pynmea2.parse(newdata.decode("utf-8"))
        lat = newmsg.latitude
        lng = newmsg.longitude
        
        return (lat, lng)

    return (0.0,0.0)

#determin the amount of miles based on two latitudes and longitudes
def miles_between_two_points(lat1, long1, lat2, long2):
    """Calculate distance in miles between two points on Earth."""
    R = 6371000
    phi_1 = math.radians(lat1)
    phi_2 = math.radians(lat2)
    delta_phi = math.radians(lat2 - lat1)
    delta_lambda = math.radians(long2 - long1)
    a = math.sin(delta_phi/2.0)**2 + math.cos(phi_1)*math.cos(phi_2) * math.sin(delta_lambda/2.0)**2
    c = 2*math.atan2(math.sqrt(a), math.sqrt(1-a))
    meters = R * c
    miles = meters * 0.000621371
    return miles

#determin the speed in feet per second based on the distance traveled and start and end time
def feet_per_second(miles, time1, time2):
    """Calculate feet per second given miles and time difference."""
    return ((miles * 5280) / (time2 - time1))

#determin the speed based on the distance traveled in miles and the start and end time
def miles_per_hour(miles, time1, time2):
    """Calculate miles per hour given miles and time difference."""
    return (miles / (time2 - time1)) * 60 * 60

#determon the current direction from two directions
def determin_direction_from_two_points(lat1, long1, lat2, long2):
    """Determine the direction in degrees from one point to another."""
    y = math.sin(long2 - long1) * math.cos(lat2)
    x = math.cos(lat1) * math.sin(lat2) - math.sin(lat1) * math.cos(lat2) * math.cos(long2 - long1)
    theta = math.atan2(y, x)
    return (theta * 180 / math.pi + 360) % 360

#determin the best turn to get to a point on the compus
def determin_best_turn_to_point(current_direction, target_direction):
    """Determine the best turn amount from current direction to target direction."""
    a = target_direction - current_direction
    b = target_direction - current_direction + 360
    c = target_direction - current_direction - 360
    lst = [abs(a), abs(b), abs(c)]
    if min(lst) == abs(a):
        return (a / 2) + 90
    elif min(lst) == abs(b):
        return (b / 2) + 90
    elif min(lst) == abs(c):
        return (c / 2) + 90
#endregion

#region Gyro - Methods
#Initialize the gyro
def MPU_Init():
	#write to sample rate register
	bus.write_byte_data(Device_Address, SMPLRT_DIV, 7)
	
	#Write to power management register
	bus.write_byte_data(Device_Address, PWR_MGMT_1, 1)
	
	#Write to Configuration register
	bus.write_byte_data(Device_Address, CONFIG, 0)
	
	#Write to Gyro configuration register
	bus.write_byte_data(Device_Address, GYRO_CONFIG, 24)
	
	#Write to interrupt enable register
	bus.write_byte_data(Device_Address, INT_ENABLE, 1)

#read data output from gyro raw data
def read_raw_data(addr):
	#Accelero and Gyro value are 16-bit
        high = bus.read_byte_data(Device_Address, addr)
        low = bus.read_byte_data(Device_Address, addr+1)
    
        #concatenate higher and lower value
        value = ((high << 8) | low)
        
        #to get signed value from mpu6050
        if(value > 32768):
                value = value - 65536
        return value

def get_x_acceleration():
    #Read Accelerometer raw value
	acc_x = read_raw_data(ACCEL_XOUT_H)
	
	#Full scale range +/- 250 degree/C as per sensitivity scale factor
	return acc_x / 16384.0

def get_y_acceleration():
    #Read Accelerometer raw value
    acc_y = read_raw_data(ACCEL_YOUT_H)

    #Full scale range +/- 250 degree/C as per sensitivity scale factor
    return acc_y / 16384.0

def get_z_acceleration():
    #Read Accelerometer raw value
    acc_z = read_raw_data(ACCEL_ZOUT_H)
    
    #Full scale range +/- 250 degree/C as per sensitivity scale factor
    return acc_z / 16384.0

def get_x_pitch():
    # Read Gyroscope raw value
    gyro_x = read_raw_data(GYRO_XOUT_H)

    # Convert raw data to degrees per second
    return gyro_x / 131.0

def get_y_pitch():
    #Read Gyroscope raw value
    gyro_y = read_raw_data(GYRO_YOUT_H)

    #Convert raw data to degrees per second
    return gyro_y / 131.0

def get_z_pitch():
    #Read Gyroscope raw value
    gyro_z = read_raw_data(GYRO_ZOUT_H)

    return gyro_z / 131.0
#endregion

#region MISC Methods
# Logging Method
def log_message(message):
    current_time = datetime.datetime.now()

    with open(current_time.strftime("%Y-%m-%d")+'FlightLog.txt', 'a') as log_file:
        log_file.write('Time: ' + current_time.strftime("%Y-%m-%d %H:%M:%S") + '  message: ' + message + '\n')

#take a picture
def take_Pic_and_save(camera, FileName):
    fileLocationAndName = pictureLocation + FileName + current_time.strftime("%Y-%m-%d-%H-%M-%S") + ".jpg"
    camera.capture(fileLocationAndName)
    log_message("Picture Taken: " + FileName + current_time.strftime("%Y-%m-%d %H:%M:%S"))

#sends a message to the client 
def send_message(client_socket, message):
    client_socket.send(message)

#waits for a message from the clienadded comments
def receive_message(client_socket):
    return client_socket.recv(1024)

#decerialize path points from message
def decerialize_points(client_socket):
    points = receive_message(client_socket)
    return json.loads(points)
     
#endregion

#region preflight methods
#Calibrate the ESCMotor
def Calibrate(client_socket, kit):
    kit.servo[motorPort].angle = 0
    send_message(client_socket, "Disconnect the battery and send c input when ready")
    recipt = receive_message(client_socket)
    if recipt == 'c':
        kit.servo[motorPort].angle = motorMax
        send_message(client_socket, 'Connect the battery NOW.. you will here two beeps, then wait for a gradual falling tone then send c input')
        recipt = receive_message(client_socket)
        if recipt == 'c':
            kit.servo[motorPort].angle = motorMin          
            send_message(client_socket, "its working")
            time.sleep(7)
            send_message(client_socket, "its working")
            time.sleep (5)
            send_message(client_socket,"Im working on it, DONT WORRY JUST WAIT.....")
            kit.servo[motorPort].angle = 0 
            time.sleep(2)
            send_message(client_socket, "Arming ESC now...")
            kit.servo[motorPort].angle = motorMin   
            time.sleep(1)
            send_message(client_socket, "Calibration Complete")

#This is the arming procedure of an ESC 
def arm(client_socket, kit): 
    send_message(client_socket, 'Connect the battery and send c input')
    recipt = receive_message(client_socket)
    if recipt == 'c':
        kit.servo[motorPort].angle = 0   
        time.sleep(1)
        kit.servo[motorPort].angle = motorMax 
        time.sleep(1)
        kit.servo[motorPort].angle = motorMin  
        time.sleep(1) 

#Preflight test gets Latitude and Longitude and altitude and send that back to the user it also checks that all flight controls are able to move the full range of motion
def Preflight_Check(client_socket, altimeter, kit, airplane):
    Latitude, Longitude = Get_Cordinates()
    Altitude, Celceus, Farenheight = altimeter.read_alt_temp()

    log_message(str(Latitude) + ", " + str(Longitude) + " - Alt: " + str(Altitude) + " temp: " + str(Celceus) + "C, " + str(Farenheight) + "F")  
    send_message(client_socket, str(Latitude) + ", " + str(Longitude) + " - Alt: " + str(Altitude) + " temp: " + str(Celceus) + "C, " + str(Farenheight) + "F")

    send_message(client_socket, 'Be awair motor will start block wheels and send c input to continue')
    recipt = receive_message(client_socket)
    if (recipt == 'c'):
        i = 0
        while True:
            if(i < 180):
                Set_Elevator(kit, i, airplane)
                Set_Rudder(kit, i, airplane)
                if(i > 20):
                    Set_throttle(kit, i, airplane)
            else:
                Set_Elevator(kit, 0, airplane)
                Set_Rudder(kit, 90, airplane)
                Set_throttle(kit, 0, airplane)
                break


#This will stop every action your Pi is performing for ESC ofcourse.
def stop(client_socket, kit): 
    log_message("stoped")
    kit.servo[motorPort].angle = 0
    kit.servo[elevatorPort].angle = 90
    kit.servo[rudderPort].angle = 90
#endregion

#region takeoff Methods
#determins if we can takeoff at current speed
def check_can_takeoff(speed, airplane):
    airplane.lastSpeed = speed
    log_message("speed: " + str(speed))
    return speed > takeoffSpeed

#checks if we have a higher altitude than starting point
def Check_has_takenoff(altitude, speed ,airplane):
    global mode
    if(altitude > startingAlt + 1):
        mode = "normal"

        airplane.mode = "normal"
        airplane.lastSpeed = speed

        log_message("Took Off at speed of " + str(speed))
#endregion

#region stall methods
#Checks if speed has gone up to see if we should continue to go down or start to pull up
def Has_Speed_Increased(currentSpeed, lastSpeed, airplane):
    airplane.lastSpeed = currentSpeed
    
    return currentSpeed > lastSpeed

#change elevator and motor to get out of a stall CanGoUp is for trying to go up(true) or down(False)
def Recover(airplane, kit, CanGoUp):
    if(CanGoUp == True ):
        log_message("Can increase pitch")
        Set_Elevator(kit, airplane.elevator + .02, airplane)
    else:
        log_message("Need to decrease pitch")
        Set_Elevator(kit, airplane.elevator - .02, airplane)

#Has recovered from a stall to go back to normal flight
def Has_Recoverd(lastSpeed, currentSpeed, pitch, airplane):
    global mode
    airplane.lastPitch = pitch

    log_message("pitch: " + str(pitch) + " Speed: " + str(currentSpeed))

    if(currentSpeed >= lastSpeed & pitch >= 0):
        log_message("recovered from stall")
        mode = airplane.mode
        return True
    
    log_message("Last Speed: " + str(lastSpeed) + " Current Speed: " + str(currentSpeed) + " Pitch: " + str(pitch))
    return False

#estimates if we are close to or on the ground during a stall and if we should start the landing shut down process
def Should_Emergency_Land(altitude, TargetAlt, startingAlt, airplane):
    global mode
    if( altitude <= startingAlt + 10 or altitude < TargetAlt - 150):
        airplane.mode = "land"
        mode = "land"
        log_message("Emergancy Landing - Alt: " + str(altitude) + " Starting Altitude: " + str(startingAlt) + " Target Altitude: " + str(TargetAlt))
        return True
    
    return False

#endregion

#region Normal flight methods
def FeetPerMin(CurrentAltimeter,LastAltimeter,curTime,lastT):
	return ((LastAltimeter - CurrentAltimeter)/(curTime-lastT))*60

#get the climb or decent rate
def DetermineClimbDesentRate(endAlt, startAlt, MPH, MilesToAlt):
    targetFPM = (endAlt - startAlt)/(MPH/MilesToAlt)
    return targetFPM
    
#set Elevators and engine to meet the rate of climb
def Set_Elevators_Engine_To_ROC(lastAlt, currentAlt, targetAlt, MPH, milesToAlt, distLastTraveled, airplane, kit):
    currentRate = DetermineClimbDesentRate(currentAlt, lastAlt, MPH, distLastTraveled)
    targetRate = DetermineClimbDesentRate(targetAlt, currentAlt, MPH, milesToAlt)

    log_message("target feet per min: " + str(targetRate) + " current feet per min: " + str(currentRate))

    airplane.lastRate = currentRate
    airplane.lastAlt = currentAlt

    if (currentRate < targetRate):
        if(currentRate >= 800):
            return
        
        if(abs(currentRate - targetRate) < 100):
            log_message("Slow Incline: " + str(abs(currentRate - targetRate)))
            Set_Elevator(kit, (airplane.elevatorAngle + .05), airplane)
            Set_throttle(kit, (airplane.motorSpeed + 5), airplane)
        else:
            log_message("Large Incline: " + str(abs(currentRate - targetRate)))
            Set_Elevator(kit, (airplane.elevatorAngle + .1), airplane)
            Set_throttle(kit, (airplane.motorSpeed + 10), airplane)
    elif(currentRate > targetRate):
        if(abs(currentRate - targetRate) < 100):
            log_message("Slow Decline: " + str(abs(currentRate - targetRate)))
            Set_Elevator(kit, (airplane.elevatorAngle - .05), airplane)
            Set_throttle(kit, (airplane.motorSpeed - 5), airplane)
        else:
            log_message("Large Decline: " + str(abs(currentRate - targetRate)))
            Set_Elevator(kit, (airplane.elevatorAngle - .1), airplane)
            Set_throttle(kit, (airplane.motorSpeed - 10), airplane)


#set a speed between 20 - 180 or 0
def Set_throttle(kit, speed, airplane):
    if(speed > 180):
        speed = 180
    elif(speed < 0):
        speed = 0
    kit.servo[motorPort].angle(speed)
    log_message("motor speed set to " + str(speed))
    airplane.motorSpeed = speed

#set a rudder location between 0 and 180
def Set_Rudder(kit, angle, airplane):
    if(angle > 180):
        angle = 180
    elif(angle < 0):
        angle = 0
    kit.servo[rudderPort].angle(angle)
    log_message("set rudder to " + str(angle))
    airplane.rudderAngle = angle 

#set a elevator postition between -1 or 1
def Set_Elevator(kit, angle, airplane):
    if(angle > 1):
        angle = 1
    elif(angle < -1):
        angle = -1

    if(angle <= 0):
        kit.servo[elevatorPort].angle(abs(angle) * 90)
    else:
        kit.servo[elevatorPort].angle((angle*90) + 90)  
    log_message("set elevator to " + str((abs(angle) * 90)))
    airplane.elevatorAngle = angle

#Check out current direction and move towards point
def Move_Towards_target(TargetLat, TargetLong, CurrentLat, CurrentLong, LastLat, LastLong, kit, airplane):
    CurrentDirection = determin_direction_from_two_points(LastLat, LastLong, CurrentLat, CurrentLong)
    targetDirection = determin_direction_from_two_points(CurrentLat, CurrentLong, TargetLat, TargetLong)

    turnAngle = determin_best_turn_to_point(CurrentDirection, targetDirection)

    airplane.lastLat = CurrentLat
    airplane.lastLong = CurrentLong

    log_message("Turn Angle: " + str(turnAngle) + "Current Direction: " + str(CurrentDirection) + "Target Direction" + str(targetDirection))
    Set_Rudder(kit, turnAngle, airplane)

#Check if we are in a stall
def Check_If_Stalling(currentRate, LastRate, TargetRate, pitch):
    global mode
    if(pitch > 45 & currentRate < LastRate & currentRate < TargetRate):
        log_message("Stall with values - Current: " + str(currentRate) + " Last: " + str(LastRate) + " Target: " + str(TargetRate) + " pitch: " + str(pitch))
        mode = "stall"
        return True


#Check if we have reacehed a waypoint to determin if we are within 1ft from the destination
def Have_Reached_Waypoint(TargetLat, TargetLong, currentLat, currentLong, altitude, targetAltitude):
    global currentWaypoint
    miles = miles_between_two_points(TargetLat, TargetLong, currentLat, currentLong)

    if ((miles*5280) <= 1 & abs(altitude - targetAltitude) < 10):
        log_message("Reached Waypoint")
        currentWaypoint += 1  
        return True
    return False

#check if we are on final
def On_Final(airplane):
    global mode
    if(len(pathpoints) - 1 == currentWaypoint):
        mode = "slow"
        airplane.Mode = "slow"
        log_message("Slow Flight")
        return True

    return False
        
#endregion

#region Slow Flight
#control speed with pitch
def Slow_Flight_Speed(currentSpeed, targetSpeed, kit, airplane):
    airplane.lastSpeed = currentSpeed
    if(currentSpeed < targetSpeed):
        log_message("Slow Flight decreasing angle at speed: " + str(currentSpeed))
        Set_Elevator(kit, airplane.elevatorAngle - .01, airplane)
    elif(currentSpeed > targetSpeed):
        log_message("Slow Flight increasing angle at speed: " + str(currentSpeed))
        Set_Elevator(kit, airplane.elevatorAngle + .01, airplane)

#control decent rate with motor speed
def Slow_Flight_Decent(CurrentAlt, LastAlt, MPH, targetRate, distToTarget, kit, airplane):
    currentRate = DetermineClimbDesentRate(CurrentAlt, LastAlt, MPH, distToTarget)
    
    airplane.lastRate = currentRate
    airplane.lastspeed = MPH
    airplane.LastAlt = CurrentAlt

    if(currentRate > targetRate):
        log_message("Slow Flight increasing motor speed. Rate of Change: " + str(currentRate))
        Set_throttle(kit, airplane.motorSpeed + 5, airplane)
    elif(currentRate < targetRate):
        log_message("Slow Flight decreasing motor speed. Rate of Change: " + str(currentRate))
        Set_throttle(kit, airplane.motorSpeed - 1, airplane)

#checks if we are close enough to the landing point to start the landing and shutdown process
def Should_Land(currentAlt, DistToTarget, TargetAlt, airplane):
    global mode
    if(currentAlt <= TargetAlt + 2 & DistToTarget <= 10):
        mode = "land"
        airplane.mode = "land"
        log_message("Switch to Landing")
        return True
    
    return False

#endregion

#region Landing Methods
#Keep pitch level
def Keep_Pitch_Level(Pitch, kit, airplane):
    airplane.lastPitch = Pitch
    if (Pitch > 0):
        log_message("Lower Elevator to level out - Pitch: " + str(Pitch))
        Set_Elevator(kit, airplane.elevatorAngle - .01)
    elif(Pitch < 0):
        log_message("Raise Elevator to level out - Pitch: " + str(Pitch))
        Set_Elevator(kit, airplane.elevatorAngle + .01)

#keep Landing heading
def Keep_Landing_Heading(currentDirection, landingDirection, kit, airplane):
    turnAngle = determin_best_turn_to_point(currentDirection, landingDirection)
    Set_Rudder(kit, turnAngle, airplane)

#Has Landed
def Has_Landed(altitude, targetAltitude):
    return (abs(altitude - targetAltitude) <= 1)

#endregion

#region Initialize Boards
#setup camera
camera = PiCamera()
camera.resolution = (3280, 2464)

#setup altimeter board
mpl3115a2 = MPL3115A2()
 
#setup servo kit board with 8 channels
kit = ServoKit(channels = 8)

# initialize I2C bus for altimeter
Altbus = smbus.SMBus(3)

#initialize Gyro
Gyrobus = smbus.SMBus(2)
MPU_Init()

#initialize airplane variables
plane = Airplane(0, 90, 0, mpl3115a2.read_alt(), get_x_pitch(), mpl3115a2.read_alt(), Get_Cordinates().lat, Get_Cordinates().lng, 0, 0, datetime.datetime.now(), 0, "stop")
#endregion

# setup connection with bluetooth
server_socket = bluetooth.BluetoothSocket(bluetooth.RFCOMM)
server_socket.bind(("", bluetooth.PORT_ANY))
server_socket.listen(portNumber)

port = server_socket.getsockname()[1]
log_message("Waiting for connection on RFCOMM channel " + port)

# try to connect and start listening to stream
client_socket, client_address = server_socket.accept()
log_message("Accepted connection from " + client_address)

send_message(client_socket, "Send Flight Path")
pathpoints = decerialize_points(client_socket)

send_message(client_socket, "Send Mode: stop, calibrate, arm, preflight, takeoff")
mode = receive_message(client_socket)

while True:
    if(mode == "calibrate"):
        Calibrate(client_socket, kit)
        send_message(client_socket, "Send Mode: stop, calibrate, arm, preflight, takeoff")
        mode = receive_message(client_socket)
    elif(mode == "arm"):
        arm(client_socket, kit)
        send_message(client_socket, "Send Mode: stop, calibrate, arm, preflight, takeoff")
        mode = receive_message(client_socket)
    elif(mode == "preflight"):
        Preflight_Check(client_socket, mpl3115a2, kit, plane)()
        send_message(client_socket, "Send Mode: stop, calibrate, arm, preflight, takeoff")
        mode = receive_message(client_socket)
    elif(mode == "takeoff"):
        Set_throttle(kit, 180, plane)
        cLat, cLng = Get_Cordinates()
        Move_Towards_target(pathpoints[currentWaypoint].lat, pathpoints[currentWaypoint].lng, cLat, cLng, plane.lastLat, plane.lastLong, kit, plane)
        if(check_can_takeoff(miles_per_hour(miles_between_two_points(cLat, cLng, plane.lastLat, plane.lastLong), datetime.datetime.now(), plane.lastTime), plane)):
            Set_Elevator(kit, 0, plane)
            
        take_Pic_and_save(camera, pictureLocation)
        Check_has_takenoff(mpl3115a2.read_alt(),miles_per_hour(miles_between_two_points(cLat, cLng, plane.lastLat, plane.lastLong), datetime.datetime.now(), plane.lastTime))
    elif(mode == "normal"):
        Set_throttle(kit, 150, plane)
        take_Pic_and_save(camera, pictureLocation)
        cLat, cLng = Get_Cordinates()
        Set_Elevators_Engine_To_ROC(
            plane.lastAlt, 
            mpl3115a2.read_alt(), 
            pathpoints[currentWaypoint].alt, 
            miles_per_hour(miles_between_two_points(cLat, cLng, plane.lastLat, plane.lastLong), datetime.datetime.now(), plane.lastTime), 
            miles_between_two_points(cLat, cLng, pathpoints[currentWaypoint].lat, pathpoints[currentWaypoint].lng), 
            miles_between_two_points(plane.lastLat, plane.lastLong, cLat, cLng), 
            plane)
        Move_Towards_target(pathpoints[currentWaypoint].lat, pathpoints[currentWaypoint].lng, cLat, cLng, plane.lastLat, plane.lastLong, kit, plane)
        Have_Reached_Waypoint(pathpoints[currentWaypoint].lat, pathpoints[currentWaypoint].lng, cLat, cLng, mpl3115a2.read_alt(), pathpoints[currentWaypoint].alt)
        Check_If_Stalling(
            DetermineClimbDesentRate(
                mpl3115a2.read_alt(), 
                plane.lastAlt, 
                miles_per_hour(miles_between_two_points(cLat, cLng, plane.lastLat, plane.lastLong), datetime.datetime.now(), plane.lastTime), 
                miles_between_two_points(plane.lastLat, plane.lastLong, cLat, cLng)), 
            plane.lastRate,
            DetermineClimbDesentRate(
                pathpoints[currentWaypoint].alt, 
                mpl3115a2.read_alt(), 
                miles_per_hour(miles_between_two_points(cLat, cLng, plane.lastLat, plane.lastLong), datetime.datetime.now(), plane.lastTime), 
                miles_between_two_points(cLat, cLng, pathpoints[currentWaypoint].lat, pathpoints[currentWaypoint].lng)), 
            get_y_pitch())
        On_Final(plane)
    elif(mode == "slow"):
        Set_throttle(kit, 120, plane)
        cLat, cLng = Get_Cordinates()
        Move_Towards_target(pathpoints[currentWaypoint].lat, pathpoints[currentWaypoint].lng, cLat, cLng, plane.lastLat, plane.lastLong, kit, plane)
        Slow_Flight_Decent(
            mpl3115a2.read_alt(),
            plane.lastAlt,
            miles_per_hour(miles_between_two_points(cLat, cLng, plane.lastLat, plane.lastLong), datetime.datetime.now(), plane.lastTime),
            DetermineClimbDesentRate(
                pathpoints[currentWaypoint].alt, 
                mpl3115a2.read_alt(), 
                miles_per_hour(miles_between_two_points(cLat, cLng, plane.lastLat, plane.lastLong), datetime.datetime.now(), plane.lastTime), 
                miles_between_two_points(cLat, cLng, pathpoints[currentWaypoint].lat, pathpoints[currentWaypoint].lng)),
            kit,
            plane
        )
        Slow_Flight_Speed(
            miles_per_hour(miles_between_two_points(cLat, cLng, plane.lastLat, plane.lastLong), datetime.datetime.now(), plane.lastTime),
            50,
            kit,
            plane
        )
        Should_Land(
            mpl3115a2.read_alt(),
            miles_between_two_points(cLat, cLng, pathpoints[currentWaypoint].lat, pathpoints[currentWaypoint].lng),
            pathpoints[currentWaypoint].alt,
            plane
        )
    elif(mode == "land"):
        Set_throttle(kit, plane.motorSpeed - 5, plane)
        cLat, cLng = Get_Cordinates()
        Keep_Landing_Heading(
            determin_direction_from_two_points(plane.lastLat, plane.lastLong, cLat, cLng),
            determin_direction_from_two_points(pathpoints[currentWaypoint-1].lat, pathpoints[currentWaypoint-1].lng, pathpoints[currentWaypoint].lat, pathpoints[currentWaypoint].lng),
            kit,
            plane
        )
        Keep_Pitch_Level(get_x_pitch, kit, plane)
        Has_Landed(mpl3115a2.read_alt(), pathpoints[currentWaypoint].alt)
    elif(mode == "stall"):
            take_Pic_and_save(camera, pictureLocation)
            Recover(
                plane, 
                kit, 
                Has_Speed_Increased(
                    miles_per_hour(miles_between_two_points(cLat, cLng, plane.lastLat, plane.lastLong), datetime.datetime.now(), plane.lastTime),
                    plane.lastSpeed,
                    plane
                    )
                )
            Has_Recoverd(
                plane.lastSpeed, 
                miles_per_hour(miles_between_two_points(cLat, cLng, plane.lastLat, plane.lastLong), datetime.datetime.now(), plane.lastTime), 
                get_y_pitch, 
                plane)
            Should_Emergency_Land(mpl3115a2.read_alt(), pathpoints[currentWaypoint].alt, plane.startingAlt, plane)
    elif(mode == "stop"):
        Set_throttle(kit, 0, plane)
        Set_Elevator(kit, 90, plane)
        Set_Rudder(kit, 90, plane)
        break
