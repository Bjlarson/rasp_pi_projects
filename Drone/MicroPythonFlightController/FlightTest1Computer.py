import serial
import time
import RPi.GPIO as GPIO
import bluetooth
import smbus
import adafruit_mpl3115a2

# Define GPIO pins
trigger_pin = 7  # GPIO pin connected to the HC-SR04 trigger pin
echo_pin = 12     # GPIO pin connected to the HC-SR04 echo pin

#Variables to transmit
motor = 40
pitch = 0
roll = 0
yaw = 0

#Distance Variables
last_Distance = 0.0
Distance = 0.0
timer_start = 0.0
timer = 0.0
desending = False
Go = False
average_alt = 0
last_alt = 0
target_alt = 0

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

# Set GPIO mode
GPIO.setmode(GPIO.BOARD)

#Configure UART
ser = serial.Serial('/dev/ttyS0', 9600, timeout=2)

# Set up GPIO pins
GPIO.setup(trigger_pin, GPIO.OUT)
GPIO.setup(echo_pin, GPIO.IN)

GPIO.output(trigger_pin, GPIO.LOW)
time.sleep(2)

# setup connection with bluetooth
server_socket = bluetooth.BluetoothSocket(bluetooth.RFCOMM)
server_socket.bind(("", bluetooth.PORT_ANY))
server_socket.listen(1)

port = server_socket.getsockname()[1]
print("Waiting for connection on RFCOMM channel ", port)

# try to connect and start listening to stream
client_socket, client_address = server_socket.accept()
print("Accepted connection from ", client_address)

class MPL3115A2():
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

def measure_distance():
    # Send a trigger pulse
    GPIO.output(trigger_pin, GPIO.HIGH)
    time.sleep(0.00001)
    GPIO.output(trigger_pin, GPIO.LOW)

    # Wait for the echo pulse
    while GPIO.input(echo_pin) == 0:
        pulse_start = time.time()

    while GPIO.input(echo_pin) == 1:
        pulse_end = time.time()

    # Calculate distance
    pulse_duration = pulse_end - pulse_start
    speed_of_sound = 360  # meters per second
    distance = (round((pulse_duration * speed_of_sound) / 2)*100)

    return distance

#gets a rolling average for altimeter to mitigate the variation in altitude readings
def rolling_average(value, window, current):
     #removes the oldest value from the current average
     current -= current / window

     #adds the new value to the current average
     current += value / window

     return round(current, 2)
     
#waits for a message from bluetooth and prints the string revived by the bluetooth connection
print(client_socket.recv(1024))

#sets up the alimeter sensor
mpl3115a2 = MPL3115A2()
mpl3115a2.control_alt_config()
mpl3115a2.data_config()
time.sleep(1)

#sets the target altitude for the test
taralt = mpl3115a2.read_alt_temp()
target_alt = taralt['a'] + 5

#Main Loop
try:
    while True:
        #Gets distance from the ultra sonic sensor
        Distance = measure_distance()


        alt = mpl3115a2.read_alt_temp()
        average_alt = rolling_average(alt['a'] * 3.281,5,average_alt)

        if(desending):
            if(Distance <= 5):
                motor -= 0.5
            elif(average_alt >= last_alt):
                motor -= .1
        elif(average_alt >= target_alt):
            timer = time.time()

            if(average_alt > target_alt + 1.5):
                motor -= .1
            if(average_alt < last_alt + .5):
                motor += .1
    
            if(timer_start == 0.0):
                timer_start = timer
            elif(timer-timer_start >= 30):
                desending = True
                motor -= .1
        elif(average_alt <= target_alt):
            motor += .1

        #Construct the data string to send
        data_string = f"M:{motor},P:{pitch},R:{roll},Y:{yaw}\n"

        ser.write(data_string.encode('utf-8'))

        last_Distance = Distance
        last_alt = average_alt

        time.sleep(0.2)
        
except KeyboardInterrupt:
    # Handle Keyboard Interrupt
    motor = 40
    data_string = f"M:{motor},P:{pitch},R:{roll},Y:{yaw}\n"
    ser.write(data_string.encode('utf-8')) 