import time
from board import SCL,SDA
import busio
import adafruit_pca9685

i2c_bus = busio.I2C(SCL,SDA)
pwm = adafruit_pca9685.PCA9685(i2c_bus)

pwm.frequency = 50

# Demo using LED on of the PCA9685
# Wire up the LED  on such that 
#    Shortleg of LED goes to GND and
#    Long leg goes to PWM pin 

pwm.set_pwm(3,0,4095)   # Full bright
pwm.set_pwm(4,0,4095)   # Full bright
pwm.set_pwm(5,0,4095)   # Full bright
time.sleep(5)

pwm.set_pwm(3,1024,3072)
pwm.set_pwm(4,1024,3072)
pwm.set_pwm(5,1024,3072) # half bright
time.sleep(5)

pwm.set_pwm(3,0,0)  #off
pwm.set_pwm(4,0,0)  #off
pwm.set_pwm(5,0,0)  #off
time.sleep(5)

lowlevel = 0
highlevel = 0
while lowlevel < 1024:
    pwm.set_pwm(3,lowlevel,highlevel)
    pwm.set_pwm(4,lowlevel,highlevel)
    pwm.set_pwm(5,lowlevel,highlevel)
    lowlevel +=1
    highlevel +=3

while highlevel < 4095:
    pwm.set_pwm(3,lowlevel,highlevel)
    pwm.set_pwm(4,lowlevel,highlevel)
    pwm.set_pwm(5,lowlevel,highlevel)
    lowlevel +=1
    highlevel +=1

while highlevel > 3072:
    pwm.set_pwm(3,lowlevel,highlevel)
    pwm.set_pwm(4,lowlevel,highlevel)
    pwm.set_pwm(5,lowlevel,highlevel)
    lowlevel +=1
    highlevel -=1

while highlevel > 0:
    while lowlevel > 0:
        pwm.set_pwm(3,lowlevel,highlevel)
        pwm.set_pwm(4,lowlevel,highlevel)
        pwm.set_pwm(5,lowlevel,highlevel)
        lowlevel +=1
        highlevel -=2
    highlevel-=1
