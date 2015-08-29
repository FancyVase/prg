import pygame
import numpy
import cv2

def draw_line(screen, color, start, end, bounds):
	if end[0] == start[0]:
		m = end[1] - start[1]
	else:
		m = (end[1] - start[1])/(end[0] - start[0])
	b = m*(0 - start[0]) + start[1]

	start_pos = (bounds[0], m*(bounds[0]) + b)
	end_pos = (bounds[2], m*(bounds[2]) + b)

	pygame.draw.line(screen, color, start_pos, end_pos, 2)

def perspective_transform(src, transform):
	v0 = numpy.float32([[src[0][i], src[1][i]] for i in range(len(src[0]))])
	v0 = numpy.array([v0])
	result = cv2.perspectiveTransform(v0, transform).tolist()
	result = [(result[0][i][0], result[0][i][1]) for i in range(len(result[0]))]
	return result

class Grid:
    def __init__(self, color, world_width, world_height, numcells, transform, bounds):
        self.color = color;
        self.numcells = numcells
        self.cw = world_width/float(numcells)
        self.ch = world_height/float(numcells)
        self.transform = transform
        self.bounds = bounds

    def Render(self, screen):
        for i in range(self.numcells): 
            for j in range(self.numcells):
                world_vertices = [[i*self.cw, (1+i)*self.cw, (1+i)*self.cw, i*self.cw],[(1+j)*self.ch, (1+j)*self.ch, j*self.ch, j*self.ch]]
                proj_vertices = perspective_transform(world_vertices, self.transform)

                for i in range(len(proj_vertices)):
		            if i == len(proj_vertices) - 1:
		                draw_line(screen, self.color, proj_vertices[i], proj_vertices[0], self.bounds)
		            else:
		                draw_line(screen, self.color, proj_vertices[i], proj_vertices[i+1], self.bounds)

    def Rainbow(self): # for looping colorful displays
        r, g, b = self.color
        if b == 50 and r < 150:
            r += 1
        if r == 150 and g < 150:
            g += 1
        if g == 150 and b < 150:
            b += 1
        if b == 150 and r > 50:
            r -= 1
        if r == 50 and g > 50:
            g -= 1
        if g == 50 and b > 50:
            b -= 1 

        self.color = (r, g, b)

def run_demo(screen, grids):
	screen.fill(0)

	for e in pygame.event.get():
		if e.type == pygame.QUIT or pygame.key.get_pressed()[pygame.K_ESCAPE]:
			return False

	for grid in grids:
		grid.Render(screen)
		# grid.Rainbow()

	pygame.display.flip()

	return True


def grid_setup(homographies):
	screen = pygame.display.set_mode((3072, 768), pygame.FULLSCREEN)
	bounds = [[0,0,1024,768],[1024,0,2048,768],[2048,0,3072,768]]
	grids = []

	world_width = 177.8
	world_height = 279.4
	numcells = 10

	for i in range(len(homographies)):
		grids.append(Grid((150,150,150), world_width, world_height, numcells, homographies[i], bounds[i]))

	running = True

	while running:
		running = run_demo(screen, grids)

def main(homographies=None):
	if homographies is None:
		print "Missing homography transformations."
	
	else:
		grid_setup(homographies)


if __name__ == '__main__':
	main()