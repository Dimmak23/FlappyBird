import pygame
import os
from pygame.constants import QUIT, K_ESCAPE, K_DOWN, K_UP, K_LEFT, K_RIGHT
import random


def create_enemy():
	
	enemySize = (20, 20)	
	enemy = pygame.Surface(enemySize)
	enemy.fill(RED)
	enemyRectangle = pygame.Rect(width, random.randint(0, height), *enemySize)
	enemyDeltaPos = {"x": random.randint(2, 5), "y": 0}

	# Let's return dictionary, because we can see what kind of object there by keys
	return {"enemySurface": enemy, "enemyRectangle": enemyRectangle, "enemyDeltaPos": enemyDeltaPos}


if __name__ == "__main__":

	#  Clean this pygame message
	os.system('CLS')

	pygame.init()
	
	# Screen properties
	screen = width, height = 800, 600
	# Frame rate
	FPS = pygame.time.Clock()
	
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
	
	DELTAS_ENEMY = [0.2, 0.3, 0.4, 0.5]
 
 
	mainWindow = pygame.display.set_mode(screen)
	mainWindow.fill((155, 155, 155))
	
	ballSize = (20, 20)
	ball = pygame.Surface(ballSize)
	ball.fill(WHITE)
	ballRectangle = ball.get_rect()
	ballRectangle = ballRectangle.move((0, 0))
	# ballSpeed = [1, 1]
	ballDeltaPos = {"x": 5, "y": 5}
 
	# enemySize = (20, 20)	
	# enemy = pygame.Surface(enemySize)
	# enemy.fill(RED)
	# enemyRectangle = pygame.Rect(width, 100, *enemySize)
	# enemyDeltaPos = {"x":1, "y":1}

	CREATE_ENEMY = pygame.USEREVENT + 1
	pygame.time.set_timer(CREATE_ENEMY, 1500)

	enemies = []
	
	running = True
	while running:
		
		FPS.tick(60)
		
		for event in pygame.event.get():
			if event.type == QUIT:
				running = False
			if event.type == CREATE_ENEMY:
				enemies.append(create_enemy())		
		
		pressedKeys = pygame.key.get_pressed()
  
		# Redraw main window to black every iteration
		mainWindow.fill(BLACK)
		# Redraw ball on top of the main window
		mainWindow.blit(ball, ballRectangle)
  		# Redraw enemy on top of the main window
		for enemy in enemies:
			mainWindow.blit(enemy["enemySurface"], enemy["enemyRectangle"])

		# User controls
		if pressedKeys[K_DOWN]:
			ballRectangle = ballRectangle.move([0,ballDeltaPos["y"]])
		if pressedKeys[K_UP]:
			ballRectangle = ballRectangle.move([0,-ballDeltaPos["y"]])
		if pressedKeys[K_LEFT]:
			ballRectangle = ballRectangle.move([-ballDeltaPos["x"],0])
		if pressedKeys[K_RIGHT]:
			ballRectangle = ballRectangle.move([ballDeltaPos["x"],0])

		# Manipulate enemies
		for enemy in enemies:
			# Move enemies
			enemy["enemyRectangle"] = enemy["enemyRectangle"].move([-enemy["enemyDeltaPos"]["x"], enemy["enemyDeltaPos"]["y"]])
			# Delete enemies
			# NOTE: we assume that enemy should be deleted when it's RIGHT side
			# 		go outside the game field, so it's full body go outside
			if enemy["enemyRectangle"].right < 0:
				enemies.pop(enemies.index(enemy))

		# Show every drawing to screen
		pygame.display.flip()
  
		# Allow to exit by 'Escape' shortcut
		if pressedKeys[K_ESCAPE]:
			running = False
