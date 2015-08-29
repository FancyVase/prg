import cv2
import numpy as np

img = cv2.imread('projector_1.jpg')
gray = cv2.cvtColor(img, cv2.COLOR_BGR2GRAY)
edges = cv2.Canny(gray, 50, 150, apertureSize = 3)
minLineLength = 100
maxLineGap = 1

# lines = cv2.HoughLinesP(edges, 1, np.pi/180, 50,minLineLength,maxLineGap)
lines = cv2.HoughLines(edges, 1, np.pi/180, 200)

# print lines

# for x1,y1,x2,y2 in lines[0]:
# 	cv2.line(img,(x1,y1),(x2,y2),(0,255,0),2)

for rho, theta in lines[0]:
	a = np.cos(theta)
	b = np.sin(theta)
	x0 = a*rho
	y0 = b*rho
	x1 = int(x0 + 1000*(-b))
	y1 = int(y0 + 1000*(a))
	x2 = int(x0 - 1000*(-b))
	y2 = int(y0 - 1000*(a))

	cv2.line(img,(x1,y1),(x2,y2),(0,0,255),2)
	print "(" + str(x1) + "," + str(y1) + ")" + " (" + str(x2) + str(y2) + ")"


cv2.imshow('dst',img)
if cv2.waitKey(0) & 0xff == 27:
	cv2.destroyAllWindows()

# cv2.imwrite('houghlines5.5.jpg',img)