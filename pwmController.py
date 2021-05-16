import time
from adafruit_servokit import ServoKit

kit = ServoKit(channels=8)

servo_min = 0
serco_Max = 180

print('Moving servo on channel 0 press Ctrl-C to quit...')
while True:
    x = int(input("servo angle 0-180"))
    kit.servo[0].angle = x
