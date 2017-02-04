import pygame
from asteroid import Asteroid
from bullet import Bullet
from random import randint
pygame.init()
scoreFont = pygame.font.Font("assets/bariol_regular-webfont.ttf", 36)

pygame.key.set_repeat(True)

bg = pygame.image.load("assets/bg.png")
backgroundY = -600

score = 0

bulletImg = pygame.image.load("assets/bullet.png")

asteroidSmall = pygame.image.load("assets/asteroid-small.png")
asteroidMedium = pygame.image.load("assets/asteroid-medium.png")
asteroidLarge = pygame.image.load("assets/asteroid-large.png")

spaceship = pygame.image.load("assets/spaceship.png")
spaceship = pygame.transform.scale(spaceship, (50, 50))
spaceshipRect = spaceship.get_rect().move((175, 400))
spaceshipSpeed = 5


size = (400, 600)
screen = pygame.display.set_mode(size)
screenRect = screen.get_rect()
pygame.display.set_caption("Random Game Thing")

BLUE = (0, 0, 255)
WHITE = (255, 255, 255)

clock = pygame.time.Clock()
isRunning = True

asteroidArray = []
bulletArray = []
keyNowUp = True
randconst = 0
# -- main game loop
while isRunning:
    # -- set spaceship speed
    speed = [0, 0]
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            isRunning = False
        if event.type == pygame.KEYDOWN:
            if event.key == pygame.K_UP:
                speed[1] = -1 * spaceshipSpeed
            if event.key == pygame.K_DOWN:
                speed[1] = 1 * spaceshipSpeed
            if event.key == pygame.K_RIGHT:
                speed[0] = 1 * spaceshipSpeed
            if event.key == pygame.K_LEFT:
                speed[0] = -1 * spaceshipSpeed
            # -- shoot a bullet
            if event.key == pygame.K_SPACE and keyNowUp:
                bulletArray.append(Bullet(bulletImg, spaceshipRect.midtop, screen))
                keyNowUp = False
        if event.type == pygame.KEYUP:
            if event.key == pygame.K_SPACE:
                keyNowUp = True
    spaceshipRect = spaceshipRect.move(speed)

    # -- game logic

    # -- scroll the background
    backgroundY += 2
    if backgroundY > 0 :
        backgroundY = -600

    # -- spawn a random asteroid
    randnum = randint(randconst, 2000)
    randx = randint(0, size[0])
    if randnum > 1990:
        if randnum > 1999:
            asteroidArray.append(Asteroid(3, asteroidLarge, (randx, 0), screen))
        elif randnum > 1996:
            asteroidArray.append(Asteroid(2, asteroidMedium, (randx, 0), screen))
        else:
            asteroidArray.append(Asteroid(1, asteroidSmall, (randx, 0), screen))
        randconst += 10
    
    # -- make sure that the spaceship is on the screen
    spaceshipRect = spaceshipRect.clamp(screenRect)

    # -- rendering logic
    screen.fill(BLUE)
    # -- render the background
    screen.blit(bg, (0,backgroundY))
    # -- move and draw the bullets
    for bullet in bulletArray:
        bullet.move()
        bullet.draw()
        if bullet.rect.bottom < 0:
            bulletArray.remove(bullet)
    # -- move and draw the asteroids, check for collisions
    for asteroid in asteroidArray:
        asteroid.move()
        asteroid.draw()
        # -- check if asteroid is out of bounds
        asteroid.rect = asteroid.rect.clamp(screenRect)
        if asteroid.rect.bottom >= size[1]:
            isRunning = False
        # -- check if asteroid is colliding with a bullet
        bulletIndex = asteroid.rect.collidelist(bulletArray)
        if bulletIndex != -1:
            score += 1
            if asteroid.size == 2:
                asteroidArray.append(Asteroid(1, asteroidSmall, (asteroid.rect.left - 10, asteroid.rect.top), screen))
                asteroidArray.append(Asteroid(1, asteroidSmall, (asteroid.rect.right + 10, asteroid.rect.top), screen))
            elif asteroid.size == 3:
                asteroidArray.append(Asteroid(2, asteroidMedium, (asteroid.rect.left, asteroid.rect.top), screen))
                asteroidArray.append(Asteroid(2, asteroidMedium, (asteroid.rect.right, asteroid.rect.top), screen))
            asteroidArray.remove(asteroid)
    # -- blit the spaceship to the screen
    screen.blit(spaceship, spaceshipRect)
    # -- render the score
    screen.blit(scoreFont.render("Score: "+str(score), True, WHITE), (0,0))

    # -- update screen
    pygame.display.flip()
    clock.tick(60)

# -- quit the game
pygame.quit()

