import pygame

class Disk:
	def __init__(self, color, pos, size):
		self.color = color
		self.pos = pos
		self.size = size

	def render(self, screen):
		pygame.draw.circle(screen,self.color,self.pos,self.size, 3)

def main():
	pygame.time.wait(1000)
	screen = pygame.display.set_mode((3072,768),pygame.FULLSCREEN)
	running = True

	diskList = []
	mousePressed = False
	mouseDown = False
	mouseReleased = False
	target = None
	
	while running:
		screen.fill(0)
		pos = pygame.mouse.get_pos()

		for Event in pygame.event.get():
			if Event.type == pygame.QUIT or pygame.key.get_pressed()[pygame.K_ESCAPE]:
				running = False
				break

			if pygame.key.get_pressed()[pygame.K_SPACE]:
				pygame.display.toggle_fullscreen()

			if Event.type == pygame.MOUSEBUTTONDOWN:
				mousePressed = True 
				mouseDown = True 

			if Event.type == pygame.MOUSEBUTTONUP:
				mouseReleased = True
				mouseDown = False

		if mousePressed:
			for disk in diskList:
				if (pos[0] >= (disk.pos[0] - disk.size) and
					pos[0] <= (disk.pos[0] + disk.size) and
					pos[1] >= (disk.pos[1] - disk.size) and
					pos[1] <= (disk.pos[1] + disk.size)):
					target = disk

			if target is None and len(diskList) < 4:
				target = Disk((150, 255, 255), pos, 10)
				diskList.append(target)

		if mouseDown and target is not None:
			target.pos = pos

		if mouseReleased:
			target = None

		vertices = []

		for disk in diskList:
			disk.render(screen)

			if disk.pos not in vertices:
				vertices.append([disk.pos[0], disk.pos[1]])

		if len(vertices) == 4:
			pygame.draw.polygon(screen,(255,255,255),vertices)

		mousePressed = False
		mouseReleased = False

		pygame.display.flip()

	print "vertices: " + str(vertices)
	return vertices

if __name__ == '__main__':
	main()