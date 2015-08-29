import numpy as np
import cv2

img = cv2.imread('img/projector-polygon-6.png')
gray = cv2.cvtColor(img,cv2.COLOR_BGR2GRAY)
img = cv2.bilateralFilter(img,9,75,75)

corners = cv2.goodFeaturesToTrack(gray,6,0.01,10)
corners = np.int0(corners)

x_center = []
y_center = []

for i in corners:
	x_center.append(i.ravel()[0])
	y_center.append(i.ravel()[1])
	x,y = i.ravel()
	print "(",x,",",y,")"
	cv2.circle(img,(x,y),3,(0,0,255),-1)

x = int(sum(x_center)/len(x_center))
y = int(sum(y_center)/len(y_center))

cv2.circle(img,(x,y),3,(255,0,0),-1)

cv2.imshow('Shi-Tomasi (' + str(x) + ', ' + str(y) + ')',img)
cv2.waitKey(0)
cv2.destroyAllWindows()