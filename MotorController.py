import RPi.GPIO as GPIO
import time

in1 = 11
in2 = 13
en = 15
temp1 = 1

GPIO.setmode(GPIO.BOARD)
GPIO.setup(in1, GPIO.OUT)
GPIO.setup(in2, GPIO.OUT)
GPIO.setup(en, GPIO.OUT)
GPIO.output(in1, GPIO.LOW)
GPIO.output(in2, GPIO.LOW)
p = GPIO.PWM(en, 1000)

p.start(25)

while True:
    
    x = input()
    
    if x== 'r':
        print("Run")
        if(temp1 == 1):
            GPIO.output(in1,GPIO.LOW)
            GPIO.output(in2,GPIO.HIGH)
            print("Forward")
            x = 'z'
        else:
            GPIO.output(in1,GPIO.HIGH)
            GPIO.output(in2,GPIO.LOW)
            print("Backward")
            x = 'z'
            
    elif x == 's':
            print("Stop")
            GPIO.output(in1,GPIO.LOW)
            GPIO.output(in2,GPIO.LOW)
            x = 'z'
            
    elif x == 'f':
        print("Forward")
        GPIO.output(in1,GPIO.HIGH)
        GPIO.output(in2,GPIO.LOW)
        temp1 = 1
        x = 'z'
        
    elif x == 'b':
        print("Backward")
        GPIO.output(in1,GPIO.LOW)
        GPIO.output(in2,GPIO.HIGH)
        temp1 = 0
        x = 'z'
        
    elif x == 'l':
        print("Low")
        p.ChangeDutyCycle(15)
        x = 'z'
        
    elif x == 'm':
        print("medium")
        p.ChangeDutyCycle(25)
        x = 'z'
        
    elif x == 'h':
        print("High")
        p.ChangeDutyCycle(50)
        x = 'z'
    
    elif x == 'e':
        GPIO.cleanup()
        print("GPIO clean up")
        break
    
    else:
        try:
            val = int(x)
            print("User assigned speed")
            p.ChangeDutyCycle(val)
            x = 'z'
        
        except ValueError:
            print("<<< wrong data >>>")
            print("Please enter the defined data to continue.")