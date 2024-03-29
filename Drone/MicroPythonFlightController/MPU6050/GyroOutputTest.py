from imu import MPU6050
from time import sleep
from machine import Pin, I2C

#Shows Pi is on by turning on LED when plugged in
LED = Pin("LED", Pin.OUT)
LED.on()

i2c = I2C(0, sda=Pin(0), scl=Pin(1), freq=400000)
imu = MPU6050(i2c)

while True:
    ax=round(imu.accel.x,2)
    ay=round(imu.accel.y,2)
    az=round(imu.accel.z,2)
    gx=round(imu.gyro.x)
    #gy=round(imu.gyro.y) - offset[1]
    #gz=round(imu.gyro.z) - offset[2]
    #print("ax",ax,"\t","ay",ay,"\t","az",az,"\t","gx",gx,"\t","gy",gy,"\t","gz",gz,"\t","Temperature",tem,"        ",end="\r")
    print("x",gx)
    sleep(0.5) 
