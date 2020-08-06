import RPi.GPIO as GPIO
import time
    
servo1 = 7

GPIO.setmode(GPIO.BOARD)

GPIO.setup(servo1,GPIO.OUT)

s1 = GPIO.PWM(servo1,50)
s1.start(6)

while True:
    x = input("enter go or stop")
       
    if x == 'g':
        s1.ChangeDutyCycle(6)
        time.sleep(1)
        s1.ChangeDutyCycle(11)
        time.sleep(1)
        s1.ChangeDutyCycle(3)
        time.sleep(1)
    else:
        GPIO.cleanup()