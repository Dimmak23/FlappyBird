import pygame
import os
from pygame.constants import QUIT, K_ESCAPE, K_DOWN, K_UP, K_LEFT, K_RIGHT
import random


def create_objective(enemy: bool, color: tuple, size: dict,
                     moveRange: tuple) -> dict:

    surface = pygame.Surface(tuple(size.values()))
    surface.fill(color)

    initialPos = {"x": 0, "y": 0}

    if enemy:
        initialPos["x"] = width
        initialPos["y"] = random.randint(0, height - size["height"])
        deltas = {"x": random.randint(*moveRange), "y": 0}
    else:
        initialPos["x"] = random.randint(0, width - size["width"])
        initialPos["y"] = 0
        deltas = {"x": 0, "y": random.randint(*moveRange)}

    rectangle = pygame.Rect(tuple(initialPos.values()), tuple(size.values()))

    # Let's return dictionary, because we can see what kind of object there by keys
    return {"surface": surface, "rectangle": rectangle, "deltas": deltas}


if __name__ == "__main__":

    #  Clean this pygame message
    os.system("CLS")

    pygame.init()

    # Screen properties
    screen = width, height = 800, 600
    # Frame rate
    FPS = pygame.time.Clock()

    BLACK = (0, 0, 0)

    WHITE = (255, 255, 255)
    RED = (255, 0, 0)
    ORANGE = (255, 165, 0)
    YELLOW = (255, 255, 0)
    GREEN = (0, 255, 0)
    BLUE = (0, 0, 255)
    SLATEBLUE = (106, 90, 205)
    ROSYBROWN = (188, 143, 143)

    RANDOM_COLORS = [
        WHITE, RED, ORANGE, YELLOW, GREEN, BLUE, SLATEBLUE, ROSYBROWN
    ]

    mainWindow = pygame.display.set_mode(screen)
    mainWindow.fill((155, 155, 155))

    ballSize = (20, 20)
    ball = pygame.Surface(ballSize)
    ball.fill(WHITE)
    ballRectangle = ball.get_rect()
    ballRectangle = ballRectangle.move((0, 0))
    ballDeltaPos = {"x": 5, "y": 5}

    score: int = 0


    CREATE_ENEMY = pygame.USEREVENT + 1
    pygame.time.set_timer(CREATE_ENEMY, 1500)
    enemies = []
    enemiesSizes = {"width": 20, "height": 20}
    enemyMoveRange = (2, 5)

    CREATE_BONUS = pygame.USEREVENT + 2
    pygame.time.set_timer(CREATE_BONUS, 2500)
    bonuses = []
    bonusesSizes = {"width": 20, "height": 20}
    bonusMoveRange = (4, 7)

    # Game cycle
    running = True
    while running:

        # Frame per second settings
        FPS.tick(60)

        # Event handling
        for event in pygame.event.get():
            if event.type == QUIT:
                running = False
            if event.type == CREATE_ENEMY:
                enemies.append(
                    create_objective(enemy=True, color=RED, size=enemiesSizes, moveRange=enemyMoveRange))
            if event.type == CREATE_BONUS:
                bonuses.append(
                    create_objective(enemy=False, color=GREEN, size=bonusesSizes, moveRange=bonusMoveRange))

        # Redraw main window to black every iteration
        mainWindow.fill(BLACK)
        # Redraw ball on top of the main window
        mainWindow.blit(ball, ballRectangle)
        # Redraw enemy on top of the previous
        for enemy in enemies:
            mainWindow.blit(enemy["surface"], enemy["rectangle"])
        # Redraw bouneses on top of the previous
        for bonus in bonuses:
            mainWindow.blit(bonus["surface"], bonus["rectangle"])

        # User controls
        pressedKeys = pygame.key.get_pressed()
        if pressedKeys[K_DOWN] and ballRectangle.bottom < height:
            ballRectangle = ballRectangle.move([0, ballDeltaPos["y"]])
        if pressedKeys[K_UP] and ballRectangle.top > 0:
            ballRectangle = ballRectangle.move([0, -ballDeltaPos["y"]])
        if pressedKeys[K_LEFT] and ballRectangle.left > 0:
            ballRectangle = ballRectangle.move([-ballDeltaPos["x"], 0])
        if pressedKeys[K_RIGHT] and ballRectangle.right < width:
            ballRectangle = ballRectangle.move([ballDeltaPos["x"], 0])

        # Manipulate enemies
        for enemy in enemies:
            # Move enemies
            enemy["rectangle"] = enemy["rectangle"].move(
                [-enemy["deltas"]["x"], enemy["deltas"]["y"]])
            # Delete enemies
            # NOTE: we assume that enemy should be deleted when it's RIGHT side
            # 		go outside the game field, so it's full body go outside
            if enemy["rectangle"].right < 0:
                enemies.pop(enemies.index(enemy))

            if ballRectangle.colliderect(enemy["rectangle"]):
                running = False

        # Manipulate bonuses
        for bonus in bonuses:
            # Move enemies
            bonus["rectangle"] = bonus["rectangle"].move(
                [-bonus["deltas"]["x"], bonus["deltas"]["y"]])
            # Delete enemies
            # NOTE: we assume that bonus should be deleted when it's TOP side
            # 		go outside the game field, so it's FULL BODY go outside
            if bonus["rectangle"].top > height:
                bonuses.pop(bonuses.index(bonus))

            if ballRectangle.colliderect(bonus["rectangle"]):
                score += 1
                bonuses.pop(bonuses.index(bonus))

        # Show every drawing to screen
        pygame.display.flip()

        # Allow to exit by 'Escape' shortcut
        if pressedKeys[K_ESCAPE]:
            running = False
