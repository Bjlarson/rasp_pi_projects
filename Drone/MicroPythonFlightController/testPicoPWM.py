import time
from machine import Pin, I2C
from imu import MPU6050

# Initialize MPU6050 on I2C 0
i2c = I2C(1, sda=Pin(2), scl=Pin(3), freq=400000)
mpu = MPU6050(i2c)

# Define motor pins
motor_pin_1 = Pin(6, Pin.OUT)
motor_pin_2 = Pin(7, Pin.OUT)
motor_pin_3 = Pin(2, Pin.OUT)
motor_pin_4 = Pin(3, Pin.OUT)

# PID controller gains
Kp = 0.05
Ki = 0.01
Kd = 0.01

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

# Main loop
while True:
    # Read gyroscope and accelerometer data from MPU6050
    gyro_data = mpu.gyro
    accel_data = mpu.accel

    # Calculate errors
    error_pitch = target_pitch - accel_data[1]
    error_roll = target_roll - accel_data[0]
    error_yaw = target_yaw - gyro_data[2]

    # Calculate PID control signals
    control_signal_pitch = Kp * error_pitch + Ki * error_sum_pitch + Kd * (error_pitch - last_error_pitch)
    control_signal_roll = Kp * error_roll + Ki * error_sum_roll + Kd * (error_roll - last_error_roll)
    control_signal_yaw = Kp * error_yaw + Ki * error_sum_yaw + Kd * (error_yaw - last_error_yaw)

    # Calculate motor speeds
    motor_speed_1 = 1000 + control_signal_pitch + control_signal_roll + control_signal_yaw
    motor_speed_2 = 1000 + control_signal_pitch - control_signal_roll - control_signal_yaw
    motor_speed_3 = 1000 - control_signal_pitch - control_signal_roll + control_signal_yaw
    motor_speed_4 = 1000 - control_signal_pitch + control_signal_roll - control_signal_yaw

    # Set motor speeds
    #motor_pin_1.duty_u16(int(motor_speed_1))
    #motor_pin_2.duty_u16(int(motor_speed_2))
    #motor_pin_3.duty_u16(int(motor_speed_3))
    #motor_pin_4.duty_u16(int(motor_speed_4))
    print(motor_speed_1)
    print(motor_speed_2)
    print(motor_speed_3)
    print(motor_speed_4)

    # Update error and integral variables
    error_sum_pitch += error_pitch
    error_sum_roll += error_roll
    error_sum_yaw += error_yaw
    last_error_pitch = error_pitch
    last_error_roll = error_roll
    last_error_yaw = error_yaw

    # Delay before the next iteration
    time.sleep(0.01)

