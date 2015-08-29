import cv2
import numpy as np
import cv2.cv as cv
from matplotlib import pyplot as plt

img = cv2.imread('img/ellipses-test.png',0)
img = cv2.medianBlur(img,5)
# img = cv2.fastNlMeansDenoising(img)


cimg = cv2.cvtColor(img,cv2.COLOR_GRAY2BGR)

circles = cv2.HoughCircles(img,cv.CV_HOUGH_GRADIENT,1,20,
                            param1=50,param2=30,minRadius=0,maxRadius=0)

circles = np.uint16(np.around(circles))
x = sum([c[0] for c in circles[0]])/len(circles[0])
y = sum([c[1] for c in circles[0]])/len(circles[0])

cv2.circle(cimg, (x, y),2,(255,255,0),3)

for i in circles[0,:]:
    # draw the outer circle
    cv2.circle(cimg,(i[0],i[1]),i[2],(0,255,0),2)
    # draw the center of the circle
    cv2.circle(cimg,(i[0],i[1]),2,(0,0,255),3)

cv2.imshow('detected circles',cimg)
cv2.waitKey(0)
cv2.destroyAllWindows()