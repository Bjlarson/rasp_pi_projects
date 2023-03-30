#get the climb or decent rate
import datetime


def DetermineClimbDesentRate(targetAlt, currentAlt, speed, targetAltDist):
    targetFPM = (targetAlt - currentAlt)/(speed/targetAltDist)
    if(targetFPM > 500):
        return 500
    else:
        return targetFPM
    
targetAlt = input("Target Atltitude ")
targetAltDist = input("Target Distance in feet ")
speed = input("Speed ")
currentAlt = input("Current Atltitude ")

def log_message(message):
    current_time = datetime.datetime.now()

    with open(str(current_time.hour) + 'FlightLog.txt', 'a') as log_file:
        log_file.write('Time: ' + current_time.strftime("%Y-%m-%d %H:%M:%S") + '  message: ' + message + '\n')

log_message("FPM:" + str(DetermineClimbDesentRate(float(targetAlt), float(currentAlt), float(speed), float(targetAltDist))))
input("any key to end")