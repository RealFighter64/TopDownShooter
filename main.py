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

heartIcon = pygame.image.load("assets/heart.png")

pygame.key.set_repeat(True)

bg = pygame.image.load("assets/bg.png")
backgroundY = -600

score = 0
difficulty = 750

bulletImg = pygame.image.load("assets/bullet.png")

asteroidSmall = pygame.image.load("assets/asteroid-small.png")
asteroidMedium = pygame.image.load("assets/asteroid-medium.png")
asteroidLarge = pygame.image.load("assets/asteroid-large.png")

spaceship = pygame.image.load("assets/spaceship.png")
spaceship = pygame.transform.scale(spaceship, (50, 50))
spaceshipRect = spaceship.get_rect().move((175, 500))
spaceshipSpeed = 5
spaceshipCurrentSpeed = [0, 0]
# -- powerups:
# 0 = no powerup
# 1 = machine gun
# 2 = penetration gun
# 3 = rocket
powerup = 0


size = (400, 600)
screen = pygame.display.set_mode(size)
screenRect = screen.get_rect()
pygame.display.set_caption("Random Game Thing")
frameCount = 0
lives = 3

BLUE = (0, 0, 255)
WHITE = (255, 255, 255)

clock = pygame.time.Clock()
isRunning = True
gameState = 0

asteroidArray = []
bulletArray = []
keyNowUp = True

def getInputs():
    global keyNowUp, isRunning, gameState, spaceshipCurrentSpeed
    spaceshipCurrentSpeed = [0, 0]
    pressedKeys = pygame.key.get_pressed()
    if gameState == 1:
        getPlayerControls(pressedKeys)
    elif gameState == 0:
        getMenuControls(pressedKeys)
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            isRunning = False
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
    if difficulty < 1800:
        difficulty += 10

def getPlayerControls(pressedKeys):
    global keyNowUp, spaceshipCurrentSpeed, powerup
    speed = [0, 0]
    if pressedKeys[pygame.K_UP]:
        speed[1] = -1 * spaceshipSpeed
        powerup = 1
    if pressedKeys[pygame.K_DOWN]:
        speed[1] = 1 * spaceshipSpeed
        powerup = 2
    if pressedKeys[pygame.K_RIGHT]:
        speed[0] = 1 * spaceshipSpeed
    if pressedKeys[pygame.K_LEFT]:
        speed[0] = -1 * spaceshipSpeed
    # -- shoot a bullet
    if (pressedKeys[pygame.K_SPACE] and keyNowUp) or (pressedKeys[pygame.K_SPACE] and powerup == 1 and frameCount == 5):
        bulletArray.append(Bullet(bulletImg, spaceshipRect.midtop, screen))
        keyNowUp = False

    spaceshipCurrentSpeed = speed

def getMenuControls(pressedKeys):
    global keyNowUp, gameState
    if pressedKeys[pygame.K_SPACE]:
        gameState = 1

def renderingLoop():
    global backgroundY
    # -- rendering logic
    screen.fill(BLUE)

    # -- scroll and render the background
    backgroundY += 2
    if backgroundY > 0 :
        backgroundY = -600
    screen.blit(bg, (0,backgroundY))

    if gameState == 1:
        renderGameElements()
    elif gameState == 0:
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
    screen.blit(mainFont.render("Score: "+str(score), True, WHITE), (5,5))
    # -- render the lives remaining
    if lives >= 1:
        screen.blit(heartIcon, (365, 5))
    if lives >= 2:
        screen.blit(heartIcon, (330, 5))
    if lives == 3:
        screen.blit(heartIcon, (295, 5))

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

def renderGameOverScreen():
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
    global spaceshipRect, score, difficulty, asteroidArray, bulletArray, size, isRunning, lives
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

        if asteroid.rect.colliderect(spaceshipRect) or asteroid.rect.bottom >= size[1]:
            lives -= 1
            asteroidArray.remove(asteroid)

        asteroid.rect = asteroid.rect.clamp(screenRect)
        if lives == 0:
            gameOver()
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
            if powerup != 2:
                bulletArray.pop(bulletIndex)

def gameOver():
    global gameState, asteroidArray, difficulty, lives, score
    gameState = 0
    asteroidArray = []
    bulletArray = []
    difficulty = 1000
    spaceshipRect.topleft = (175, 500)
    lives = 3
    score = 0

# -- main game loop
while isRunning:
    getInputs()
    renderingLoop()
    if gameState == 1:
        logicLoop()

    if frameCount == 5:
        frameCount = 0
    
    frameCount += 1
    # -- limit to 60fps
    clock.tick(60)

# -- quit the game
pygame.quit()

