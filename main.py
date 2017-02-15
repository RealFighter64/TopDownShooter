import pygame
from asteroid import Asteroid
from bullet import Bullet
from random import randint
pygame.init()
mainFont = pygame.font.Font("assets/PrStart.ttf", 30)
controlFont = pygame.font.Font("assets/PrStart.ttf", 24)

titleFont = pygame.font.Font("assets/m12.ttf", 60)
spaceIcon = pygame.image.load("assets/spaceicon.png")
wasdIcon = pygame.image.load("assets/wasdicon.png")

pygame.key.set_repeat(True)

bg = pygame.image.load("assets/bg.png")
backgroundY = -600

score = 0
difficulty = 0

bulletImg = pygame.image.load("assets/bullet.png")

asteroidSmall = pygame.image.load("assets/asteroid-small.png")
asteroidMedium = pygame.image.load("assets/asteroid-medium.png")
asteroidLarge = pygame.image.load("assets/asteroid-large.png")

spaceship = pygame.image.load("assets/spaceship.png")
spaceship = pygame.transform.scale(spaceship, (50, 50))
spaceshipRect = spaceship.get_rect().move((175, 500))
spaceshipSpeed = 5
spaceshipCurrentSpeed = [0, 0]


size = (400, 600)
screen = pygame.display.set_mode(size)
screenRect = screen.get_rect()
pygame.display.set_caption("Random Game Thing")

BLUE = (0, 0, 255)
WHITE = (255, 255, 255)

clock = pygame.time.Clock()
isRunning = True
gameStarted = False

asteroidArray = []
bulletArray = []
keyNowUp = True
randconst = 0

def getInputs():
    global keyNowUp, isRunning, gameStarted, spaceshipCurrentSpeed
    spaceshipCurrentSpeed = [0, 0]
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            isRunning = False
        if event.type == pygame.KEYDOWN:
            if gameStarted:
                getPlayerControls(event)
            else:
                getMenuControls(event)
        if event.type == pygame.KEYUP:
            if event.key == pygame.K_SPACE:
                keyNowUp = True

def spawnAsteroid(randnum, randx):
    global difficulty
    if randnum > 1999:
        asteroidArray.append(Asteroid(3, asteroidLarge, (randx, 0), screen))
    elif randnum > 1996:
        asteroidArray.append(Asteroid(2, asteroidMedium, (randx, 0), screen))
    else:
        asteroidArray.append(Asteroid(1, asteroidSmall, (randx, 0), screen))
    difficulty += 10

def getPlayerControls(event):
    global keyNowUp, spaceshipCurrentSpeed
    speed = [0, 0]
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

    spaceshipCurrentSpeed = speed

def getMenuControls(event):
    global keyNowUp, gameStarted
    if event.key == pygame.K_SPACE and keyNowUp:
        print("lol")
        gameStarted = True
        keyNowUp = False

def renderingLoop():
    global backgroundY
    # -- rendering logic
    screen.fill(BLUE)

    # -- scroll and render the background
    backgroundY += 2
    if backgroundY > 0 :
        backgroundY = -600
    screen.blit(bg, (0,backgroundY))

    if gameStarted:
        renderGameElements()
    else:
        renderMenuScreen()

    # -- update screen
    pygame.display.flip()
    
def renderGameElements():
    # -- render the bullets
    for bullet in bulletArray:
        bullet.draw()
    # -- render the asteroids
    for asteroid in asteroidArray:
        asteroid.draw()
    # -- blit the spaceship to the screen
    screen.blit(spaceship, spaceshipRect)
    # -- render the score
    screen.blit(mainFont.render("Score: "+str(score), True, WHITE), (0,0))

def renderMenuScreen():
    screen.blit(titleFont.render("SPACE", True, WHITE), (50,30))
    screen.blit(titleFont.render("RUSH", True, WHITE), (78,100))
    screen.blit(wasdIcon, (50, 200))
    screen.blit(spaceIcon, (50, 300))
    screen.blit(controlFont.render("to move", True, WHITE), (175, 220))
    screen.blit(controlFont.render("to shoot", True, WHITE), (175, 305))
    screen.blit(controlFont.render("Press [SPACE]", True, WHITE), (50, 400))
    screen.blit(controlFont.render("to start", True, WHITE), (100, 430))
    screen.blit(spaceship, spaceshipRect)


def logicLoop():
    global spaceshipRect, score
    # -- move spaceship
    spaceshipRect = spaceshipRect.move(spaceshipCurrentSpeed)
    spaceshipRect = spaceshipRect.clamp(screenRect)

    # -- spawn a random asteroid
    randnum = randint(difficulty, 2000)
    randx = randint(0, size[0])
    if randnum > 1990:
        spawnAsteroid(randnum, randx)
    
    # -- move the bullets
    for bullet in bulletArray:
        bullet.move()
        if bullet.rect.bottom < 0:
            bulletArray.remove(bullet)

    
    # -- move the asteroids, check for collisions
    for asteroid in asteroidArray:
        asteroid.move()
        # -- check if asteroid is out of bounds
        asteroid.rect = asteroid.rect.clamp(screenRect)
        if asteroid.rect.bottom >= size[1]:
            isRunning = False
        # -- check if asteroid is colliding with a bullet
        bulletIndex = asteroid.rect.collidelist(bulletArray)
        if bulletIndex != -1:
            score += 1
            # -- split asteroid into smaller asteroids
            if asteroid.size == 2:
                asteroidArray.append(Asteroid(1, asteroidSmall, (asteroid.rect.left - 10, asteroid.rect.top), screen))
                asteroidArray.append(Asteroid(1, asteroidSmall, (asteroid.rect.right + 10, asteroid.rect.top), screen))
            elif asteroid.size == 3:
                asteroidArray.append(Asteroid(2, asteroidMedium, (asteroid.rect.left, asteroid.rect.top), screen))
                asteroidArray.append(Asteroid(2, asteroidMedium, (asteroid.rect.right, asteroid.rect.top), screen))
            asteroidArray.remove(asteroid)

# -- main game loop
while isRunning:
    getInputs()
    renderingLoop()
    if gameStarted:
        logicLoop()

    # -- limit to 60fps
    clock.tick(60)

# -- quit the game
pygame.quit()

