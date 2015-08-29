import numpy as np
import cv2

cap = cv2.VideoCapture(0)

while(True):
	# Capture frame-by-frame
	ret, frame = cap.read()

	# Our operations on the frame come here
	gray = cv2.cvtColor(frame, cv2.COLOR_BGR2GRAY)

	gray = cv2.bilateralFilter(gray,9,75,75)

	gray = np.float32(gray)
	dst = cv2.cornerHarris(gray,3,3,0.08)

	dst = cv2.dilate(dst,None)

	# Threshold for an optimal value, it may vary depending on the image.
	# frame[dst>0.03*dst.max()]=[0,0,255]

	# Display the resulting frame
	cv2.imshow('frame', frame)
	if cv2.waitKey(1) & 0xFF == ord('q'):
		break

# When everything is done, release the Capture
cap.release()
cv2.destroyAllWindows()