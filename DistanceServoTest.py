import RPi.GPIO as GPIO
import time

GPIO.setmode(GPIO.BOARD)

TRIG = 7
ECHO = 12

TRIG2 = 13
ECHO2 = 11

SERVO = 15

GPIO.setup(TRIG, GPIO.OUT)
GPIO.output(TRIG,0)
GPIO.setup(TRIG2, GPIO.OUT)
GPIO.output(TRIG2,0)
GPIO.setup(SERVO, GPIO.OUT)

GPIO.setup(ECHO,GPIO.IN)
GPIO.setup(ECHO2,GPIO.IN)

s1 = GPIO.PWM(SERVO,50)
s1.start(6)

while True:
    time.sleep(2)

    print("Starting Measurment White...")

    GPIO.output(TRIG,1)
    time.sleep(0.00001)
    GPIO.output(TRIG,0)

    while GPIO.input(ECHO) == 0:
        pass
    startW = time.time()

    while GPIO.input(ECHO) == 1:
        pass
    stopW = time.time()
    
    distanceW = (stopW - startW) * 17000
    print(distanceW)
    
    time.sleep(2)
        
    if distanceW <=10:
        s1.ChangeDutyCycle(11)

    print("Starting Measurment Red...")

    GPIO.output(TRIG2,1)
    time.sleep(0.00001)
    GPIO.output(TRIG2,0)

    while GPIO.input(ECHO2) == 0:
        pass
    startR = time.time()

    while GPIO.input(ECHO2) == 1:
        pass
    stopR = time.time()
    
    distanceR = (stopR - startR) * 17000

    print(distanceR)
    
    if distanceR <= 10:
        s1.ChangeDutyCycle(4)
    elif distanceR >= 100:
        break

GPIO.cleanup()