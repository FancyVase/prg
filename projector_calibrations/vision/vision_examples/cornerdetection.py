import cv2
import numpy as np

filename = 'img/projector-polygon-5.png'
img = cv2.imread(filename)
gray = cv2.cvtColor(img,cv2.COLOR_BGR2GRAY)

gray = cv2.bilateralFilter(gray,9,75,75)

gray = np.float32(gray)
dst = cv2.cornerHarris(gray,3,3,0.08)


# result is dilated for marking the cornerHarris
dst = cv2.dilate(dst,None)
print dst

# Threshold for an optimal value, it may vary depending on the image.
# index = img[dst>.03*dst.max()]
# x = int(sum([i[0] for i in index])/len(index))
# y = int(sum([i[1] for i in index])/len(index))

img[dst>.03*dst.max()]=(255,255,0)

# cv2.circle(img,(x,y),30,(0,255,255),5)

cv2.imshow('dst',img)
if cv2.waitKey(0) & 0xff == 27:
	cv2.destroyAllWindows()
