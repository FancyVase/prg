import pygame
from animations import *
from pygame.locals import *
import numpy as np
import cv2

def projection_setup():
	screen = pygame.display.set_mode((3072,768), pygame.FULLSCREEN)
	x, y = 200, 200
	img_orig = pygame.image.load('img/dropline.png')
	img = img_orig.copy()
	colorkey = img.get_at((0,0))
	img_orig.set_colorkey(colorkey, RLEACCEL)
	img_rect = img.get_rect(center=(x,y))
	angle = 0
	colors = [(255,0,0),(0,255,0),(0,0,255)]
	return screen, x, y, img_orig, img, img_rect, angle, projector_colors

def projection_run(screen, x, y, img_orig, img, img_rect, angle, event):
	screen.fill(0)

	if event == "counterclockwise": angle += 60
	if event == "clockwise": angle -= 60

	img = pygame.transform.rotate(img_orig, angle)
	img_rect = img.get_rect(center=(x,y))
	screen.blit(img, img_rect)

	pygame.display.flip()
	return angle

def projection_end():
	return

def event_handler():
	for Event in pygame.event.get():
		keys = pygame.key.get_pressed()

		if (Event.type == pygame.QUIT or 
			keys[K_ESCAPE] or
			keys[K_q]):   return "quit"
		if keys[K_SPACE]: return "add"
		if keys[K_a]:	  return "counterclockwise"
		if keys[K_d]:	  return "clockwise"	