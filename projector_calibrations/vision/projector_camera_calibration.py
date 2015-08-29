import pygame
import cv2
import random
import numpy as np
import time
import datetime

NUM_MARKERS = 20
marker = pygame.image.load('img/marker.png')

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
	
	return [sum([v[0] for v in vertices])/len(vertices), sum([v[1] for v in vertices])/len(vertices)]

def find_line(cap):
	height = cap.read()[1].shape[0]
	width = cap.read()[1].shape[1]
	maxcorners = 6

	ret, frame = cap.read()
	gray = cv2.cvtColor(frame, cv2.COLOR_BGR2GRAY)
	gray = cv2.bilateralFilter(gray,9,75,75)

	corners = cv2.goodFeaturesToTrack(gray,15,0.01,10)
	corners = np.int0(corners)
	line_corners = []

	counter = 0
	for i in corners:
		x, y = i.ravel()
		if x > 60 and y > 0 and y < height - 40 and counter < maxcorners:
			cv2.circle(frame,(x,y),1,(0,0,255),-1)
			line_corners.append((x,y))
			counter += 1

	if len(line_corners) == 6:
		# line_corners.sort(key=lambda tup: -tup[0] + tup[1])
		
		vx, vy, x, y = cv2.fitLine(np.array(line_corners),cv2.cv.CV_DIST_L2,0,0.01,0.01)
		line = [float(vx),float(vy),float(x),float(y)]

		left_pt = int((-x*vy/vx) + y)
		right_pt = int(((gray.shape[1]-x)*vy/vx)+y)
		cv2.line(frame,(gray.shape[1]-1,right_pt),(0,left_pt),255,2)
		
		filename = '/tmp/calibration_' + datetime.datetime.now().strftime("%H:%M:%S.%f") + '.jpg'
		cv2.imwrite(filename, frame)
		return line

# def select_marker(x, y, projector):
# 	m = smart_marker.copy()
# 	if (x - projector[0]) > 200 and (projector[2] - x > 200):
# 		if y < 150:
# 			m = pygame.transform.rotate(m, -45)
# 			return m
# 		elif y > 618:
# 			m = pygame.transform.rotate(m, 135)
# 			return m
	
# 	return marker.copy()

def draw_marker(screen, x, y, angle, projector):
	screen.fill(0)
	# m = select_marker(x, y, projector)
	rect = marker.get_rect(center = (x, y))
	rot_marker = pygame.transform.rotate(marker, angle)
	rot_rect = rot_marker.get_rect(center = rect.center)

	screen.blit(rot_marker, rot_rect)
	pygame.display.flip()

def find_marker_coordinate(screen, cap, x, y, projector):
	lines = []
	angle = 0

	for i in range(3):
		draw_marker(screen, x, y, angle, projector)
		angle += 60
		lines.append(find_line(cap))

		if len(lines) > 2:
			try:
				return centroid(lines)
			except:
				break

def find_matches_per_projector(screen, cap, projector):
	radius = marker.get_height()/2
	proj_points = []
	cam_points = []

	for m in range(NUM_MARKERS):
		x = random.randint(projector[0] + radius, projector[2] - radius)
		y = random.randint(projector[1] + radius, projector[3] - radius)
		cam_coords = find_marker_coordinate(screen, cap, x, y, projector)

		if cam_coords is not None:
			proj_points.append([x,y])
			cam_points.append(cam_coords)

	return proj_points, cam_points


def find_marker_matches(bounds):
	screen = pygame.display.set_mode((3072,768), pygame.FULLSCREEN)
	cap = cv2.VideoCapture(0)
	time.sleep(2)

	point_pairs = []
	
	for projector in bounds:
		proj_points, cam_points = find_matches_per_projector(screen, cap, projector)
		point_pairs.append([proj_points, cam_points])

	cap.release()
	return point_pairs

def main():
	bounds = [[0,0,1024,768],[1024,0,2048,768],[2048,0,3072,768]]

	bounds[0][0] += 40
	bounds[0][1] += 80
	bounds[0][2] -= 70
	bounds[1][2] -= 50
	bounds[1][3] -= 90
	bounds[2][1] += 50

	# find projector and camera coordinates for markers
	matches =  find_marker_matches(bounds)
	print matches

if __name__ == '__main__':
	main()