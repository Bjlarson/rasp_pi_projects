from pca9685 import PCA9685
import time
from machine import Pin, I2C
from imu import MPU6050
from servo import Servos

# Define motor pins
FRIndex = 0
FLIndex = 3
BLIndex = 2
BRIndex = 1

pin = Pin("LED", Pin.OUT)

# Initialize PCA9685 Board
id = 0
pcai2c = I2C(id, sda=Pin(0), scl=Pin(1))

pca = PCA9685(pcai2c)
servo = Servos(pcai2c)

# Initialize MPU6050 on I2C 0
mpui2c = I2C(1, sda=Pin(2), scl=Pin(3), freq=400000)
mpu = MPU6050(mpui2c)

# PID controller gains
Kp = 0.5
Ki = 0.1
Kd = 0.1

# Setpoint (target) values
target_pitch = 0.0
target_roll = 0.0
target_yaw = 0.0

# Initialize error and integral variables
error_sum_pitch = 0.0
error_sum_roll = 0.0
error_sum_yaw = 0.0
last_error_pitch = 0.0
last_error_roll = 0.0
last_error_yaw = 0.0
    
# Arm Motors 
servo.position(index=FRIndex, degrees=40)
time.sleep(.1)
servo.position(index=BRIndex, degrees=40)
time.sleep(.1)
servo.position(index=BLIndex, degrees=40)
time.sleep(.1)
servo.position(index=FLIndex, degrees=40)

pin.toggle()
time.sleep(30)
pin.toggle()

# Main loop
while True:
    # Calculate errors
    error_pitch = target_pitch - mpu.accel.y*100
    error_roll = target_roll - mpu.accel.x*100
    error_yaw = target_yaw - mpu.gyro.z

    # Calculate PID control signals
    control_signal_pitch = Kp * error_pitch + Ki * error_sum_pitch + Kd * (error_pitch - last_error_pitch)
    control_signal_roll = Kp * error_roll + Ki * error_sum_roll + Kd * (error_roll - last_error_roll)
    control_signal_yaw = Kp * error_yaw + Ki * error_sum_yaw + Kd * (error_yaw - last_error_yaw)

    # Calculate motor speeds with limits
    motor_speed_1 = min(max(50 + control_signal_pitch - control_signal_roll + control_signal_yaw, 40), 150)
    motor_speed_2 = min(max(50 + control_signal_pitch + control_signal_roll - control_signal_yaw, 40), 150)
    motor_speed_3 = min(max(50 - control_signal_pitch + control_signal_roll + control_signal_yaw, 40), 150)
    motor_speed_4 = min(max(50 - control_signal_pitch - control_signal_roll - control_signal_yaw, 40), 150)

    # Set motor speeds
    servo.position(index=FRIndex, degrees=motor_speed_1)
    servo.position(index=FLIndex, degrees=motor_speed_2)
    servo.position(index=BLIndex, degrees=motor_speed_3)
    servo.position(index=BRIndex, degrees=motor_speed_4)

    # Update error and integral variables
    Fr += error_pitch
    error_sum_roll += error_roll
    error_sum_yaw += error_yaw
    last_error_pitch = error_pitch
    last_error_roll = error_roll
    last_error_yaw = error_yaw

    # Delay before the next iteration
    time.sleep(0.2)