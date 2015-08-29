import numpy as np
import cv2

def intersection(a, b):
	m1 = a[1]/a[0]
	c1 = a[3] - m1*a[2]
	m2 = b[1]/b[0]
	c2 = b[3] - m2*b[2]
	x = (c2 - c1)/(m1 - m2)
	y = m1*x + c1
	return (x, y)

def centroid(points):
	vertices = []
	for i in range(len(points)):
		if i < len(points) - 1:
			vertices.append(intersection(points[i],points[i+1]))
		else:
			vertices.append(intersection(points[i],points[0]))
	
	return (sum([v[0] for v in vertices])/len(vertices), sum([v[1] for v in vertices])/len(vertices))

cap = cv2.VideoCapture(0)
height = cap.read()[1].shape[0]
width = cap.read()[1].shape[1]
maxcorners = 6
points = []
while(True):
	# Capture frame-by-frame
	ret, frame = cap.read()
	gray = cv2.cvtColor(frame, cv2.COLOR_BGR2GRAY)
	gray = cv2.bilateralFilter(gray,9,75,75)

	corners = cv2.goodFeaturesToTrack(gray,15,0.01,10)
	corners = np.int0(corners)
	line_corners = []

	counter = 0
	for i in corners:
		x,y = i.ravel()
		if x > 40 and x < width - 70 and y > 20 and y < height - 20 and counter < maxcorners:
			cv2.circle(frame,(x,y),1,(0,0,255),-1)

			line_corners.append((x,y))
			counter += 1

	if len(line_corners) == 6:
		line_corners.sort(key=lambda tup: -tup[0] + tup[1])
		
		vx, vy, x, y = cv2.fitLine(np.array(line_corners),cv2.cv.CV_DIST_L2,0,0.01,0.01)
		point = [float(vx),float(vy),float(x),float(y)]

		left_pt = int((-x*vy/vx) + y)
		right_pt = int(((gray.shape[1]-x)*vy/vx)+y)
		cv2.line(frame,(gray.shape[1]-1,right_pt),(0,left_pt),255,2)
	
	k = cv2.waitKey(33)
	if k == 27 or k == 113:
		break
	if k == 10:
		print "ADDED"
		points.append([float(vx),float(vy),float(x),float(y)])

	if len(points) > 2:
		print centroid(points)
		cv2.circle(frame,centroid(points),3,(255,0,255),-1)

	cv2.imshow('frame', frame)

# When everything is done, release the Capture
cap.release()
cv2.destroyAllWindows()