# This program will let you test your ESC and brushless motor.
# Make sure your battery is not connected if you are going to calibrate it at first.
# Since you are testing your motor, I hope you don't have your propeller attached to it otherwise you are in trouble my friend...?
# This program is made by AGT @instructable.com. DO NOT REPUBLISH THIS PROGRAM... actually the program itself is harmful                                             pssst Its not, its safe.

import time   #importing time library to make Rpi wait because its too impatient 
import RPi.GPIO as gpio #importing GPIO library

ESC=12  #Connect the ESC in this GPIO pin 

gpio.setmode(gpio.BOARD)
gpio.setup(ESC, gpio.OUT)

pwm = gpio.PWM(ESC,50)
pwm.start(0)

max_value = 10 #change this if your ESC's max value is different or leave it be
min_value = 5.5  #change this if your ESC's min value is different or leave it be
print ("For first time launch, select calibrate")
print ("Type the exact word for the function you want")
print ("calibrate OR manual OR control OR arm OR stop")

def manual_drive(): #You will use this function to program your ESC if required
    print ("You have selected manual option so give a value between 5 and 10")    
    while True:
        inp = input()
        if inp == "stop":
            stop()
            break
        elif inp == "control":
            control()
            break
        elif inp == "arm":
            arm()
            break
        else:
            if inp >=5 and inp <=10:
                pwm.ChangeDutyCycle(inp)   
            
                
def calibrate():   #This is the auto calibration procedure of a normal ESC
    pwm.ChangeDutyCycle(0)
    print("Disconnect the battery and press Enter")
    inp = input()
    if inp == '':
        pwm.ChangeDutyCycle(max_value)
        print("Connect the battery NOW.. you will here two beeps, then wait for a gradual falling tone then press Enter")
        inp = input()
        if inp == '':
            pwm.ChangeDutyCycle(min_value)            
            print ("Wierd eh! Special tone")
            time.sleep(7)
            print ("Wait for it ....")
            time.sleep (5)
            print ("Im working on it, DONT WORRY JUST WAIT.....")
            pwm.ChangeDutyCycle(0)   
            time.sleep(2)
            print ("Arming ESC now...")
            pwm.ChangeDutyCycle(min_value)   
            time.sleep(1)
            print ("See.... uhhhhh")
            control() # You can change this to any other function you want
            
def control(): 
    print ("I'm Starting the motor, I hope its calibrated and armed, if not restart by giving 'x'")
    time.sleep(1)
    speed = 7.5    # change your speed if you want to.... it should be between 5 - 10
    print ("Controls - a to decrease speed & d to increase speed OR m to decrease a lot of speed & e to increase a lot of speed")
    while True:
        pwm.ChangeDutyCycle(speed)   
        inp = input()
        
        if inp == "m" and speed >= 5:
            speed -= .1    # decrementing the speed like hell
            print ("speed = %d") % speed
        elif inp == "e":    
            speed += .1    # incrementing the speed like hell
            print ("speed = %d") % speed
        elif inp == "d":
            speed += .01     # incrementing the speed 
            print ("speed = %d") % speed
        elif inp == "a":
            speed -= .01     # decrementing the speed
            print ("speed = %d") % speed
        elif inp == "stop":
            stop()          #going for the stop function
            break
        elif inp == "manual":
            manual_drive()
            break
        elif inp == "arm":
            arm()
            break
        else:
            print ("WHAT DID I SAY!! Press a,q,d or e")
            
def arm(): #This is the arming procedure of an ESC 
    print("Connect the battery and press Enter")
    inp = input()    
    if inp == '':
        pwm.ChangeDutyCycle(0)   
        time.sleep(1)
        pwm.ChangeDutyCycle(max_value)   
        time.sleep(1)
        pwm.ChangeDutyCycle(min_value)   
        time.sleep(1)
        control() 
        
def stop(): #This will stop every action your Pi is performing for ESC ofcourse.
    pwm.ChangeDutyCycle(0) 
    pwm.stop()

#This is the start of the program actually, to start the function it needs to be initialized before calling... stupid python.    
inp = input()
if inp == "manual":
    manual_drive()
elif inp == "calibrate":
    calibrate()
elif inp == "arm":
    arm()
elif inp == "control":
    control()
elif inp == "stop":
    stop()
else :
    print ("Thank You for not following the things I'm saying... now you gotta restart the program STUPID!!")