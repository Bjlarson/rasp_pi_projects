import serial
import time
import RPi.GPIO as GPIO
import bluetooth

# Set GPIO mode
GPIO.setmode(GPIO.BOARD)

#Configure UART
ser = serial.Serial('/dev/ttyS0', 9600, timeout=2)

# Define GPIO pins
trigger_pin = 7  # GPIO pin connected to the HC-SR04 trigger pin
echo_pin = 11     # GPIO pin connected to the HC-SR04 echo pin

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
print("Waiting for connection on RFCOMM channel " + port)

# try to connect and start listening to stream
client_socket, client_address = server_socket.accept()
print("Accepted connection from " + client_address)

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
    distance = (pulse_duration * speed_of_sound) / 2

    return distance

print(client_socket.recv(1024))

#Main Loop
while True:
    Distance = measure_distance()

    if(desending):
        if(Distance <= 5):
            motor -= 0.5
        elif(Distance >= last_Distance):
            motor -= .1
    elif(30 <= Distance <= 35):
        timer = time.time()
        if(timer_start == 0.0):
            timer_start = timer
        elif(timer-timer_start >= 30):
            desending = True
            motor -= .1
    elif(Distance <= last_Distance):
        motor += .1

    #Construct the data string to send
    data_string = f"M:{motor},P:{pitch},R:{roll},Y:{yaw}\n"

    ser.write(data_string.encode('utf-8'))

    last_Distance = Distance

    time.sleep(0.2)
        