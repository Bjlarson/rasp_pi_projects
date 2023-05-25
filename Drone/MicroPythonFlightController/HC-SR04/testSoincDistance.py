import RPi.GPIO as GPIO
import time

# Set GPIO mode
GPIO.setmode(GPIO.BOARD)

# Define GPIO pins
trigger_pin = 7  # GPIO pin connected to the HC-SR04 trigger pin
echo_pin = 11     # GPIO pin connected to the HC-SR04 echo pin

# Set up GPIO pins
GPIO.setup(trigger_pin, GPIO.OUT)
GPIO.setup(echo_pin, GPIO.IN)

GPIO.output(trigger_pin, GPIO.LOW)
time.sleep(2)

def measure_distance():
    # Send a trigger pulse
    GPIO.output(trigger_pin, GPIO.HIGH)
    time.sleep(0.00001)
    GPIO.output(trigger_pin, GPIO.LOW)

    # Wait for the echo pulse
    while GPIO.input(echo_pin) == 0:
        pulse_start = time.time()

    while GPIO.input(echo_pin) == 1:
        pulse_end = time.time()

    # Calculate distance
    pulse_duration = pulse_end - pulse_start
    speed_of_sound = 360  # meters per second
    distance = (pulse_duration * speed_of_sound) / 2

    return distance

# Main loop
try:
    while True:
        distance = measure_distance()
        print("Distance: {:.2f} cm".format(distance * 100))  # Convert to centimeters
        time.sleep(1)

except KeyboardInterrupt:
    pass

finally:
    GPIO.cleanup()
