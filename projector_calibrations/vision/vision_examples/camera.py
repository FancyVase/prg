import numpy as np
import cv2

cap = cv2.VideoCapture(0)

while(True):
	# Capture frame-by-frame
	ret, frame = cap.read()
	# frame = cv2.fastNlMeansDenoisingColored(frame,None,10,10,7,21)

	# Our operations on the frame come here
	gray = cv2.cvtColor(frame, cv2.COLOR_BGR2GRAY)

	ret, thresh = cv2.threshold(gray,127,255,0)
	contours, hierarchy = cv2.findContours(thresh,cv2.RETR_TREE,cv2.CHAIN_APPROX_SIMPLE)

	(x, y), radius = cv2.minEnclosingCircle(contours[1])
	center = (int(x),int(y))
	cv2.circle(gray,center,0,(255,255,0),2)

	for i in range(len(contours) - 1):
		if hierarchy[0][i][1] < 100:
			cv2.drawContours(gray, contours, i, (0,255,0), 2) 

	# Display the resulting frame
	cv2.imshow('frame', gray)
	if cv2.waitKey(1) & 0xFF == ord('q'):
		break

# When everything is done, release the Capture
cap.release()
cv2.destroyAllWindows()