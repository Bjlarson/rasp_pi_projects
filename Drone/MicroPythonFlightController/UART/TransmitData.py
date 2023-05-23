import serial
import time

# Configure UART
ser = serial.Serial('/dev/ttyAMA0', 9600)  # Replace '/dev/ttyAMA0' with the appropriate UART port
ser.timeout = 1

# Variables to transmit
var1 = 10
var2 = 20
var3 = 30
var4 = 40

# Transmitting loop
while True:
    # Construct the data string to send
    data_string = f"{var1},{var2},{var3},{var4}\n"  # Assuming variables are integers

    # Send data over UART
    ser.write(data_string.encode())

    # Delay before the next transmission
    time.sleep(1)
