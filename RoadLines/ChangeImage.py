import cv2 as cv
import numpy as np
import matplotlib.pyplot as plt

def canny(image):
    gray = cv.cvtColor(image, cv.COLOR_RGB2GRAY)
    blur = cv.GaussianBlur(gray,(5,5),0)
    canny = cv.Canny(blur, 50, 150)
    return canny

image = cv.imread('test_image.jpg')
lane_image = np.copy(image)
canny_image = canny(lane_image)

plt.imshow(canny_image)
plt.show()