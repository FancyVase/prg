from affine import *
import numpy
import pygame
import cv2

### Helper functions ###

def matrix_to_list(m):
	l = m.tolist()
	l.pop()
	result = []
	for i in range(len(l[0])):
		result.append((l[0][i], l[1][i]))
	return result

def list_to_matrix(l):
	top = [elt[0] for elt in l]
	mid = [elt[1] for elt in l]
	bot = [1] * len(top)
	return numpy.asarray([top, mid, bot])

def projector_to_world(p, transform): # converts projector coordinates to world coordinates
	a = numpy.float32([[coord[0], coord[1]] for coord in p])
	a = numpy.array([a])
	result = cv2.perspectiveTransform(a, transform).tolist()
	return [[elt[0] for elt in result[0]],[elt[1] for elt in result[0]]]

def coords_to_list(coords):
	return [[coord[0] for coord in coords],[coord[1] for coord in coords]]

def draw_line(screen, color, start, end, bounds):
	if end[0] == start[0]:
		m = end[1] - start[1]
	else:
		m = (end[1] - start[1])/(end[0] - start[0])
	b = m*(0 - start[0]) + start[1]

	start_pos = (bounds[0][0], m*(bounds[0][0]) + b)
	end_pos = (bounds[1][0], m*(bounds[1][0]) + b)

	pygame.draw.line(screen, color, start_pos, end_pos, 2)

def get_transform_matrix(v0, v1):
	src = []
	des = []
	for i in range(len(v0[0])):
		src.append([v0[0][i], v0[1][i]])
		des.append([v1[0][i], v1[1][i]])
	src = numpy.float32(src)
	des = numpy.float32(des)
	return cv2.findHomography(src, des)[0], cv2.findHomography(des, src)[0]

def perspective_transform(src, transform):
	a = numpy.float32([[src[0][i], src[1][i]] for i in range(len(src[0]))])
	a = numpy.array([a])
	result = cv2.perspectiveTransform(a, transform).tolist()
	result = [(result[0][i][0],result[0][i][1]) for i in range(len(result[0]))]
	return result

#### Projector 1 : Leftmost in pygame, closest to Kinect ####
# p1v0 = [[84.5, 104.5, 104.5, 84.5], [129.79999999999816, 129.79999999999816, 109.79999999999816, 109.79999999999816]]
# p1v1 = [[631, 758.0, 748.892578125, 623.999755859375], [634.0, 637.0, 750.322265625, 747.0]]
p1v0 = [[28.0,42.0,56.0,70.0,84.0,98.0,112.0,126.0,140.0,28.0,42.0,56.0,70.0,84.0,98.0,112.0,126.0,140.0,28.0,42.0,56.0,70.0,84.0,98.0,112.0,126.0,140.0],[154.0,154.0,154.0,154.0,154.0,154.0,154.0,154.0,154.0,132.0,132.0,132.0,132.0,132.0,132.0,132.0,132.0,132.0,110.0,110.0,110.0,110.0,110.0,110.0,110.0,110.0,110.0]]
p1v1 = [[271, 358, 450, 545, 639, 732, 826, 915, 1001, 270, 356, 446, 538, 630, 722, 812, 900, 983, 268, 355, 443, 531, 621, 710, 798, 885, 975], [481, 479, 481, 482, 484, 485, 487, 491, 490, 609, 609, 611, 614, 617, 620, 622, 624, 625, 732, 734, 740, 742, 746, 749, 753, 754, 760]]
p1transform, p1transform_reverse = get_transform_matrix(p1v0, p1v1)
print p1transform
print ""

#### Projector 2 : Middle in pygame, closest to computer ####
p2v0 = [[0,64,64,0],[40,40,0,0]]
p2v1 = [[1079, 1493, 1486, 1067], [443, 455, 711, 702]]
p2transform, p2transform_reverse = get_transform_matrix(p2v0, p2v1)
print p2transform
print ""

#### Projector 3 : Rightmost in pygame, side one ####
# p3v0 = [[25,138,138,25],[110,110,25,25]]
# p3v1 = [[2475.0, 2473.0, 3062.0, 3062.0], [751.0, 22.99995231628418, 6.000042915344238, 744.0]]
p3v0 = [[28.0,42.0,56.0,70.0,84.0,98.0,112.0,126.0,140.0,28.0,42.0,56.0,70.0,84.0,98.0,112.0,126.0,140.0,28.0,42.0,56.0,70.0,84.0,98.0,112.0,126.0,28.0,42.0,56.0,70.0,84.0,98.0,112.0,126.0],[110.0,110.0,110.0,110.0,110.0,110.0,110.0,110.0,110.0,88.0,88.0,88.0,88.0,88.0,88.0,88.0,88.0,88.0,66.0,66.0,66.0,66.0,66.0,66.0,66.0,66.0,44.0,44.0,44.0,44.0,44.0,44.0,44.0,44.0]]
p3v1 = [[2476, 2475, 2476, 2475, 2475, 2474, 2473, 2474, 2473, 2622, 2624, 2623, 2623, 2623, 2623, 2622, 2622, 2622, 2774, 2773, 2774, 2773, 2774, 2774, 2774, 2773, 2928, 2928, 2927, 2926, 2926, 2926, 2927, 2927], [731, 641, 553, 465, 379, 291, 200, 106, 6, 729, 639, 550, 464, 376, 287, 197, 102, 2, 727, 635, 548, 462, 374, 284, 193, 98, 724, 634, 546, 457, 372, 281, 190, 96]]
p3v1 = [[2475, 2476, 2476, 2476, 2475, 2475, 2474, 2474, 2472, 2624, 2624, 2624, 2624, 2624, 2623, 2623, 2622, 2622, 2774, 2774, 2774, 2775, 2775, 2775, 2774, 2775, 2929, 2929, 2927, 2927, 2927, 2927, 2928, 2927], [731, 640, 553, 466, 379, 290, 200, 106, 6, 729, 639, 551, 464, 376, 288, 197, 103, 0, 727, 636, 549, 461, 375, 285, 193, 100, 725, 634, 547, 458, 371, 282, 190, 96]]
p3transform, p3transform_reverse = get_transform_matrix(p3v0, p3v1)
print p3transform

#### World coordinates for different shapes ####
tcmb_p3 = [[84.5, 104.5, 104.5, 84.5], [97.5, 97.5, 77.5, 77.5]]
tcmb_p2 = [[0,20,20,0],[20,20,0,0]]
sixty_cm_box_p2 = [[0,60,60,0],[60,60,0,0]]
pentagon = [[64.5,78.5,92.5,87.5,71.5],[90.5,106.54,90.5,71,71]]
triangle = [[62.5, 78.5, 94.5],[90.5,115.5,90.5]]
sixtyfour = [[0, 64, 64, 0], [40, 40, 0, 0]]
forty = [[0,40,40,0],[60,60,0,0]]
tcmb_p1 = [[120.68452887, 99.38741793, 99.11605498, 120.41316596], [166.50074153, 165.21811204, 186.87026005, 188.15288954]]
black = [[10,99,99,10],[71.4,71.4,11.4,11.4]]
big_p3 = [[25,138,138,25],[110,110,25,25]]

## Testing/Debugging ## 

# matrix_to_list(p3affine.dot(tcmb_p3))
# print p3affine_reverse.dot(tcmb_p3_p1)
# print p2affine_reverse.dot(tcmb_p2_p3)
# print p2affine.dot(tcmb_p3)
# print matrix_to_list(p2affine.dot(tcmb_p3))
# print list_to_matrix(matrix_to_list(p2affine.dot(tcmb_p3)))

#### TODO ####
# Callibrate first projector with more than 4 points
# Hough transform