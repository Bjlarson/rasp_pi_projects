from pca9685 import PCA9685
from machine import I2C, Pin
from servo import Servos

sda = Pin(0)
slc = Pin(1)
id = 0
i2c = I2C(id=id, sda=sda, slc=slc)

pca = PCA9685(i2c)
servo = Servos(i2c)
servo.position(index=0, degrees=180)