import serial
import time

#Configure UART
ser = serial.Serial('/dev/ttyS0', 9600, timeout=2)

#Variables to transmit
motor = 0
pitch = 0
roll = 0
yaw = 0

#Main Loop
while True:
    #Construct the data string to send
    data_string = f"M:{motor},P:{pitch},R:{roll},Y:{yaw}\n"

    ser.write(data_string.encode('utf-8'))

    time.sleep(0.2)
        