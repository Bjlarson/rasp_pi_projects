import picamera

#Setup the camera such that it closes
#when we are done with it
print("Taking a Picture")
with picamera.PiCamera() as camera:
    camera.resolution = (1280,720)
    
    for i in range(10):
        camera.capture("/home/pi/Documents/PiPics/newimage.jpg")
        print(i)
print("pictureTaken.")