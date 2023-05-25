import machine
import time

motor = 0
pitch = 0
roll = 0
yaw = 0

uart = machine.UART(0, baudrate=9600, timeout=2)
uart.init(bits=8, parity=None, stop=1, rx=machine.Pin(1), tx=machine.Pin(0))  # Adjust the RX and TX pin numbers as per your Pico setup

def ReadComputer():
    global motor, pitch, roll, yaw  # Declare the variables as global
    
    data = uart.readline()
    print(data)
    if data:
        received_data = str(data, 'utf-8').strip()
        variables = received_data.split(',')
    
        if len(variables) == 4:
            for var in variables:
                if var.startswith('M:'):
                    motor = int(var.split(':')[1])
                elif var.startswith('P:'):
                    pitch = int(var.split(':')[1])
                elif var.startswith('R:'):
                    roll = int(var.split(':')[1])
                elif var.startswith('Y:'):
                    yaw = int(var.split(':')[1])
    

while True:
    ReadComputer()

    print("M", motor, "P", pitch, "R", roll, "Y", yaw)

    time.sleep(0.2)
