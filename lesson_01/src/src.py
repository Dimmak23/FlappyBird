import pygame
import os
from pygame.constants import QUIT
import random


if __name__ == "__main__":

	#  Clean this pygame message
	os.system('CLS')

	pygame.init()
	
	screen = width, height = 800, 600
	
	BLACK = (0,0,0)

	WHITE = (255,255,255)
	RED = (255,0,0)
	ORANGE = (255,165,0)
	YELLOW = (255,255,0)
	GREEN = (0,255,0)
	BLUE = (0,0,255)
	SLATEBLUE = (106,90,205)
	ROSYBROWN = (188,143,143)

	RANDOM_COLORS = [WHITE, RED, ORANGE, YELLOW, GREEN, BLUE, SLATEBLUE, ROSYBROWN]
	
	mainWindow = pygame.display.set_mode(screen)
	mainWindow.fill((155, 155, 155))
	
	ballSize = (20, 20)
	ball = pygame.Surface(ballSize)
	ball.fill(WHITE)
	ballRectangle = ball.get_rect()
	ballRectangle = ballRectangle.move((0, 0))
	ballSpeed = [1, 1]
	
	running = True
	while running:
		for event in pygame.event.get():
			if event.type == QUIT:
				running = False

		ballRectangle = ballRectangle.move(ballSpeed)
		
		# Keep ball inside box 
		if ballRectangle.right > width or ballRectangle.left < 0:
			ballSpeed[0] *= -1
			ball.fill(random.choice(RANDOM_COLORS))
		if ballRectangle.bottom > height or ballRectangle.top < 0:
			ballSpeed[1] *= -1
			ball.fill(random.choice(RANDOM_COLORS))

		mainWindow.fill(BLACK)
		mainWindow.blit(ball, ballRectangle)
		pygame.display.flip()
