import socket
import RPi.GPIO as GPIO
import time

servo1 = 7
in1 = 11
in2 = 13
en = 15
temp1 = 1

GPIO.setmode(GPIO.BOARD)

GPIO.setup(servo1,GPIO.OUT)
GPIO.setup(in1, GPIO.OUT)
GPIO.setup(in2, GPIO.OUT)
GPIO.setup(en, GPIO.OUT)
GPIO.output(in1, GPIO.LOW)
GPIO.output(in2, GPIO.LOW)
p = GPIO.PWM(en, 1000)

p.start(25)

s1 = GPIO.PWM(servo1,50)
s1.start(7)

s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
s.bind(("192.168.1.14",1234))
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
            
            servo_val = float(incomeing[3:len(incomeing)])
            
            print(str(servo_val))
            clientsocket.send(bytes(str(servo_val), "utf-8"))
            
            s1.ChangeDutyCycle(servo_val)
        
        elif(incomeing[0:3] == "mtr"):
            print("Motor command")
            clientsocket.send(bytes("Motor command", "utf-8"))
            
            x = incomeing[3:len(incomeing)]
    
            if x== 'run':
                print("Run")
                clientsocket.send(bytes("Run", "utf-8"))
                
                if(temp1 == 1):
                    GPIO.output(in1,GPIO.LOW)
                    GPIO.output(in2,GPIO.HIGH)
                    print("Forward")
                    clientsocket.send(bytes("Forward", "utf-8"))
                    x = 'z'
                else:
                    GPIO.output(in1,GPIO.HIGH)
                    GPIO.output(in2,GPIO.LOW)
                    print("Backward")
                    clientsocket.send(bytes("Backward", "utf-8"))
                    x = 'z'
            
            elif x== 'stp':
                print("Stop")
                clientsocket.send(bytes("Stop", "utf-8"))
                GPIO.output(in1,GPIO.LOW)
                GPIO.output(in2,GPIO.LOW)
                x = 'z'
            
            elif x== 'for':
                print("Forward")
                clientsocket.send(bytes("Forward", "utf-8"))
                GPIO.output(in1,GPIO.HIGH)
                GPIO.output(in2,GPIO.LOW)
                temp1 = 1
                x = 'z'
        
            elif x== 'bac':
                print("Backward")
                clientsocket.send(bytes("Backward", "utf-8"))
                GPIO.output(in1,GPIO.LOW)
                GPIO.output(in2,GPIO.HIGH)
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
            
            
            
            
           