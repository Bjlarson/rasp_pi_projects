import socket
import RPi.GPIO as GPIO
import time
from adafruit_servokit import ServoKit

kit = ServoKit(channels = 8)

elevator = 1
rudder = 0
motor1 = 2
motor2 = 3

s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
s.bind(("192.168.1.13",1234))
s.listen(5)

while True:
    clientsocket, address = s.accept()
    print(f"Connection from {address} has been established!")
    
    msg = "Welcome to the server!"
    
    clientsocket.send(bytes(msg, "utf-8"))

    #arm ESC
    kit.servo[motor1].angle = 0
    kit.servo[motor2].angle = 0

    msg = "Connect Battery"
    clientsocket.send(bytes(msg, "utf-8"))
    
    while True:
        incomeing = clientsocket.recv(6).decode()
        print (incomeing)
        
        if(incomeing[0:3] == "ser"):
            print("servo command")
            clientsocket.send(bytes("servo command", "utf-8"))

            turnAngle = int(incomeing[3:len(incomeing)])
            kit.servo[rudder].angle = turnAngle
            
        elif(incomeing[0:3] == "elv"):
            print("servo command")
            clientsocket.send(bytes("servo command", "utf-8"))

            elevatorAngle = int(incomeing[3:len(incomeing)])
            kit.servo[elevator].angle = elevatorAngle
            
        elif(incomeing[0:3] == "mtr"):
            print("Motor command")
            clientsocket.send(bytes("Motor command", "utf-8"))
            
            x = incomeing[3:len(incomeing)]
            
            if x== 'stp':
                print("Stop")
                clientsocket.send(bytes("Stop", "utf-8"))
                kit.servo[motor1].angle = 0
                kit.servo[motor2].angle = 0
                x = 'z'
    
            elif x== 'ext':
                GPIO.cleanup()
                print("GPIO clean up")
                clientsocket.send(bytes("GPIO clean up", "utf-8"))
                break
            else:
                try:
                    motor_val = int(x)
                    print("User assigned speed")
                    clientsocket.send(bytes("User assigned speed", "utf-8"))
                    kit.servo[motor1].angle = motor_val
                    kit.servo[motor2].angle = motor_val
                    x = 'z'
        
                except ValueError:
                    print("<<< wrong data >>>")
                    print("Please enter the defined data to continue.")
                    clientsocket.send(bytes("<<< wrong data >>>", "utf-8"))
                    clientsocket.send(bytes("Please enter the defined data to continue.", "utf-8"))
            
            
            
            
           