import pygame
pygame.init()

pygame.key.set_repeat(True)

bg = pygame.image.load("assets/bg.png")
backgroundY = -600

spaceship = pygame.image.load("assets/spaceship.png")
spaceship = pygame.transform.scale(spaceship, (50, 50))
spaceshipRect = spaceship.get_rect()
spaceshipSpeed = 5


size = (400, 600)
screen = pygame.display.set_mode(size)
pygame.display.set_caption("Random Game Thing")

BLUE = (0, 0, 255)

clock = pygame.time.Clock()
isRunning = True

while isRunning:
    speed = [0, 0]
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            isRunning = False
        if event.type == pygame.KEYDOWN:
            if event.key == pygame.K_UP:
                speed[1] = -1 * spaceshipSpeed
                print("up")
            if event.key == pygame.K_DOWN:
                speed[1] = 1 * spaceshipSpeed
                print("down")
            if event.key == pygame.K_RIGHT:
                speed[0] = 1 * spaceshipSpeed
                print("right")
            if event.key == pygame.K_LEFT:
                speed[0] = -1 * spaceshipSpeed
                print("left")
    spaceshipRect = spaceshipRect.move(speed)

    # -- game logic
    backgroundY += 2
    if backgroundY > 0 :
        backgroundY = -600
    # -- rendering logic
    screen.fill(BLUE)
    screen.blit(bg, (0,backgroundY))
    screen.blit(spaceship, spaceshipRect)

    pygame.display.flip()

    clock.tick(60)

pygame.quit()

