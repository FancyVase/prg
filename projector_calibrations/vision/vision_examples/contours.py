import cv2
import numpy as np

img = cv2.imread('img/ellipses-test-5.png')
imgray = cv2.cvtColor(img,cv2.COLOR_BGR2GRAY)
ret,thresh = cv2.threshold(imgray,127,255,0)
contours, hierarchy = cv2.findContours(thresh,cv2.RETR_TREE,cv2.CHAIN_APPROX_SIMPLE)

(x, y), radius = cv2.minEnclosingCircle(contours[1])
center = (int(x),int(y))
cv2.circle(img,center,0,(255,255,0),2)
print "(" + str(x) + ", " + str(y) + ")"

for i in range(len(contours) - 1 ):
	cv2.drawContours(img, contours, i+1, (0,255,0), 2)

cv2.imshow('Contours',img)
cv2.waitKey(0)
cv2.destroyAllWindows()