import RPi.GPIO as GPIO
import time

# Set GPIO mode
GPIO.setmode(GPIO.BCM)

# Define GPIO pins
trigger_pin = 23  # GPIO pin connected to the HC-SR04 trigger pin
echo_pin = 24     # GPIO pin connected to the HC-SR04 echo pin

# Set up GPIO pins
GPIO.setup(trigger_pin, GPIO.OUT)
GPIO.setup(echo_pin, GPIO.IN)

def measure_distance():
    # Send a trigger pulse
    GPIO.output(trigger_pin, GPIO.HIGH)
    time.sleep(0.00001)
    GPIO.output(trigger_pin, GPIO.LOW)

    # Wait for the echo pulse
    pulse_start = time.time()
    while GPIO.input(echo_pin) == GPIO.LOW:
        pulse_start = time.time()

    pulse_end = time.time()
    while GPIO.input(echo_pin) == GPIO.HIGH:
        pulse_end = time.time()

    # Calculate distance
    pulse_duration = pulse_end - pulse_start
    speed_of_sound = 343  # meters per second
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
