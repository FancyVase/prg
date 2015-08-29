import pygame
import numpy

def bad_demo(screen, grid):
	screen.fill(0)

	for e in pygame.event.get():
		if e.type == pygame.QUIT or pygame.key.get_pressed()[pygame.K_ESCAPE]:
			return False

	screen.blit(grid, (0,0))

	pygame.display.flip()

	return True


def demo_setup():
	screen = pygame.display.set_mode((3072, 768), pygame.FULLSCREEN)
	grid = pygame.image.load('img/grid.png')
	print grid.get_width()
	print grid.get_height()
	grid = pygame.transform.scale(grid, (3072, 768))

	running = True

	while running:
		running = bad_demo(screen, grid)

def main():
	demo_setup()


if __name__ == '__main__':
	main()