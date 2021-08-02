import socket
import RPi.GPIO as GPIO
from adafruit_servokit import ServoKit
import time

kit = ServoKit(channels = 8)

servo_min = 0
servo_Max = 180

in1 = 11
in2 = 13
en = 15

in3 = 36
in4 = 26
enb = 40
temp1 = 1

GPIO.setmode(GPIO.BOARD)

GPIO.setup(in1, GPIO.OUT)
GPIO.setup(in2, GPIO.OUT)
GPIO.setup(en, GPIO.OUT)
GPIO.output(in1, GPIO.LOW)
GPIO.output(in2, GPIO.LOW)
p = GPIO.PWM(en, 1000)

GPIO.setup(in3, GPIO.OUT)
GPIO.setup(in4, GPIO.OUT)
GPIO.setup(enb, GPIO.OUT)
GPIO.output(in3, GPIO.LOW)
GPIO.output(in4, GPIO.LOW)
pb = GPIO.PWM(enb, 1000)

p.start(25)

s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
s.bind(("192.168.1.13",1234))
s.listen(5)

while True:
    clientsocket, address = s.accept()
    print(f"Connection from {address} has been established!")
    
    msg = "Welcome to the server!"
    
    clientsocket.send(bytes(msg, "utf-8"))
    
    while True:
        incomeing = clientsocket.recv(6).decode()
        print (incomeing)
        
        if(incomeing[0:3] == "ser"):
            print("servo command")
            clientsocket.send(bytes("servo command", "utf-8"))

            turnAngle = int(incomeing[3:len(incomeing)])
            kit.servo[0].angle = turnAngle
            
        elif(incomeing[0:3] == "elv"):
            print("servo command")
            clientsocket.send(bytes("servo command", "utf-8"))

            elevatorAngle = int(incomeing[3:len(incomeing)])
            kit.servo[1].angle = elevatorAngle
            
        elif(incomeing[0:3] == "mtr"):
            print("Motor command")
            clientsocket.send(bytes("Motor command", "utf-8"))
            
            x = incomeing[3:len(incomeing)]
    
            if x== 'run':
                print("Run")
                clientsocket.send(bytes("Run", "utf-8"))
                
                if(temp1 == 1):
                    GPIO.output(in1,False)
                    GPIO.output(in2,True)
                    GPIO.output(in3,True)
                    GPIO.output(in4,False)
                    print("Forward")
                    clientsocket.send(bytes("Forward", "utf-8"))
                    x = 'z'
                else:
                    GPIO.output(in1,True)
                    GPIO.output(in2,False)
                    GPIO.output(in3,False)
                    GPIO.output(in4)
                    print("Backward")
                    clientsocket.send(bytes("Backward", "utf-8"))
                    x = 'z'
            
            elif x== 'stp':
                print("Stop")
                clientsocket.send(bytes("Stop", "utf-8"))
                GPIO.output(in1,False)
                GPIO.output(in2,False)
                GPIO.output(in3,False)
                GPIO.output(in4,False)
                x = 'z'
            
            elif x== 'for':
                print("Forward")
                clientsocket.send(bytes("Forward", "utf-8"))
                GPIO.output(in1,True)
                GPIO.output(in2,False)
                GPIO.output(in3,False)
                GPIO.output(in4,True)
                temp1 = 1
                x = 'z'
        
            elif x== 'bac':
                print("Backward")
                clientsocket.send(bytes("Backward", "utf-8"))
                GPIO.output(in1,False)
                GPIO.output(in2,True)
                GPIO.output(in3,True)
                GPIO.output(in4,False)
                temp1 = 0
                x = 'z'
        
            elif x== 'low':
                print("Low")
                clientsocket.send(bytes("Low", "utf-8"))
                p.ChangeDutyCycle(15)
                x = 'z'
        
            elif x== 'med':
                print("Medium")
                clientsocket.send(bytes("Medium", "utf-8"))
                p.ChangeDutyCycle(25)
                x = 'z'
        
            elif x== 'hig':
                print("High")
                clientsocket.send(bytes("High", "utf-8"))
                p.ChangeDutyCycle(50)
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
                    p.ChangeDutyCycle(motor_val)
                    x = 'z'
        
                except ValueError:
                    print("<<< wrong data >>>")
                    print("Please enter the defined data to continue.")
                    clientsocket.send(bytes("<<< wrong data >>>", "utf-8"))
                    clientsocket.send(bytes("Please enter the defined data to continue.", "utf-8"))
            
            
            
            
           