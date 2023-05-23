from pca9685 import PCA9685
import time
from machine import I2C, Pin
from servo import Servos

FRIndex = 0
FLIndex = 3
BLIndex = 2
BRIndex = 1
id = 0
i2c = I2C(id, sda=Pin(0), scl=Pin(1))

pca = PCA9685(i2c)
servo = Servos(i2c)

#This is the auto calibration procedure of a normal ESC
def Calibration(index):
    servo.position(index=index, degrees=0)
    print("make sure to Disconnect the battery and press Enter enter any other key to skip calibration")
    inp = input()
    if inp == '':
        servo.position(index=index, degrees=150)
        print("Connect the battery NOW.. you will here two beeps, then wait for a calibration tones to stop then disconnect the battery and press enter to move to next step")
        inp = input()


Calibration(BRIndex)
Calibration(BLIndex)
Calibration(FLIndex)

servo.position(index=FRIndex, degrees=40)
servo.position(index=BRIndex, degrees=40)
servo.position(index=BLIndex, degrees=40)
servo.position(index=FLIndex, degrees=40)
print("Connect the battery NOW.. you will here two beeps, then wait for a gradual falling tone then press Enter")
inp = input()
x = 50
while(True):
    if(x < 150):
        servo.position(index=FRIndex, degrees=x)
        servo.position(index=BRIndex, degrees=x)
        servo.position(index=BLIndex, degrees=x)
        servo.position(index=FLIndex, degrees=x)
        time.sleep(.5)
        x+=10
        print(x)
    else:
        servo.position(index=FRIndex, degrees=0)
        servo.position(index=BRIndex, degrees=0)
        servo.position(index=BLIndex, degrees=0)
        servo.position(index=FLIndex, degrees=0)
        x=0
        print("stop")
        break
