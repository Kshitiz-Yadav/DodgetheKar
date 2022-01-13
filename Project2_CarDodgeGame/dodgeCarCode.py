import os
os.environ['PYGAME_HIDE_SUPPORT_PROMPT'] = "hide"
import pygame
from pygame.locals import *
from time import sleep
import random
import sys

# Global Variables:
# --Images--
IMAGES = {}

# --Sounds--
SOUNDS = {}
pygame.mixer.init()
channel1 = pygame.mixer.Channel(0)  #Music
channel2 = pygame.mixer.Channel(1)  #Background
channel3 = pygame.mixer.Channel(2)  #Begin / Milestone
channel4 = pygame.mixer.Channel(3)  #GameOver

# --Texts--
TEXTS = {}

# --Dimensions and Positions--
gameAreaSize = (723,750)
introPageSize = (723,450)
screenPos = ((1505 - introPageSize[0])//2 ,50)
carSize = (60,125)
offset = 200
LANES = [94, 152, 214, 273, 334, 393, 453, 512, 572, 630]   #List storing midpoints of lanes
playerPos = [LANES[4]-carSize[0]/2,620]
CARS = []

#--Movements--
playerVelocity = 5
playerAcc = 0.5
carVelocity = 4
carAcc = 1

# --Car Class--
class Car:
    carType = 2
    carLane = 5
    y = -carSize[1]

#--Others--
os.environ['SDL_VIDEO_WINDOW_POS']='{},{}'.format(screenPos[0], screenPos[1])
clock = pygame.time.Clock()
FPS = 32
level = 1
score = 0
carCount = 1
CPinc = 5

def showIntroPage():
    screen = pygame.display.set_mode(introPageSize)

    channel1.play(SOUNDS['IntroPage'], loops = -1)
    channel3.set_volume(0.1)
    channel3.play(SOUNDS['Horn'], loops = 1)
    while True:
        for event in pygame.event.get():
            if event.type == pygame.QUIT or (event.type == KEYDOWN and event.key == K_ESCAPE):
                pygame.quit()
                sys.exit()
            if event.type == KEYDOWN and event.key == K_SPACE:
                channel3.set_volume(1)
                channel1.stop()
                channel3.stop()
                return
        
        screen.blit(IMAGES['IntroPage'], (0,0))
        screen.blit(IMAGES['DevName'], ((screen.get_width() - IMAGES['DevName'].get_width())/2,50))
        screen.blit(IMAGES['GameName'], ((screen.get_width() - IMAGES['GameName'].get_width())/2,100))
        screen.blit(IMAGES['BeginMsg'], ((screen.get_width() - IMAGES['BeginMsg'].get_width())/2,screen.get_height() - 50))
        
        pygame.display.update()

def showGameArea():
    screen = pygame.display.set_mode(gameAreaSize)

    channel1.play(SOUNDS['GameArea'], loops = -1)
    channel2.play(SOUNDS['DrivingCar'], loops = -1)
    channel3.play(SOUNDS['Ignition'], loops = 0)

    global level, score, offset

    y = -50
    nextCP = 5
    while True:
        # Managing user input
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                sys.exit()
        keys = pygame.key.get_pressed()
        if keys[K_LEFT] and playerPos[0] > 67:
            playerPos[0] -= playerVelocity
        if keys[K_RIGHT] and (playerPos[0] + carSize[0]) < 657:
            playerPos[0] += playerVelocity
        if keys[K_ESCAPE]:
            channel1.stop()
            channel2.stop()
            channel3.stop()
            channel4.stop()
            reset()
            return
        
        # Blitting permanent images
        y = y + carVelocity//2
        if y > 750:
            y = -50
        elif y > -50:
            screen.blit(IMAGES['GameArea'], (0,y))
            screen.blit(IMAGES['GameArea'], (0,y-800))
        screen.blit(IMAGES['Player'], (playerPos))

        # Getting and blitting obstacle cars
        caller = True
        for car in CARS:
            if car.y < offset:
                caller = False
            elif car.y > gameAreaSize[1] + 10:
                CARS.pop(CARS.index(car))
                score += 1
        if caller:
            modifyCars()

        for car in CARS:
            car.y += carVelocity
            if car.carType == 1:
                screen.blit(IMAGES['Car1'],(LANES[car.carLane] - carSize[0]/2,car.y))
            elif car.carType == 2:
                screen.blit(IMAGES['Car2'],(LANES[car.carLane] - carSize[0]/2,car.y))
            elif car.carType == 3:
                screen.blit(IMAGES['Car3'],(LANES[car.carLane] - carSize[0]/2,car.y))

        # Blitting score and level
        if score == nextCP:
            increaseLevel()
            nextCP += CPinc
        TEXTS['ScoreValue'] = font.render(str(score), True, 'white')
        TEXTS['LevelValue'] = font.render(str(level), True, 'white')
        screen.blit(TEXTS['ScoreTitle'], (10,10))
        screen.blit(TEXTS['ScoreValue'], (45,40))
        screen.blit(TEXTS['LevelTitle'], (gameAreaSize[0]-TEXTS['LevelTitle'].get_width()-10,10))
        screen.blit(TEXTS['LevelValue'], (gameAreaSize[0]-60,40))

        # Checking Collision
        if checkCollision():
            channel4.play(SOUNDS['GameOver'], loops = 0)
            sleep(2)
            reset()
            return

        pygame.display.update()
        clock.tick(FPS)

def checkCollision():
    for car in CARS:
        if (playerPos[0]>LANES[car.carLane]-1.5*carSize[0]+10 and playerPos[0]<LANES[car.carLane]+0.5*carSize[0]-10) and (playerPos[1]>car.y-carSize[1]+10 and playerPos[1]<car.y+carSize[1]-10):
            return True
    return False

def modifyCars():
    global carCount, score
    laneCheck = [0] * 10
    temp = carCount
    while temp != 0:
        newCar = Car()
        newCar.carLane = random.randint(0, 9)
        if laneCheck[newCar.carLane] == 1:
            continue
        laneCheck[newCar.carLane] = 1
        newCar.carType = random.randint(1, 3)
        newCar.y = random.randint(-2*carSize[1],-carSize[1])
        CARS.append(newCar)
        temp -= 1

    for car in CARS:
        if car.y > gameAreaSize[1] + carSize[1] + 10:
            CARS.pop(CARS.index(car))

def increaseLevel():
    global level, carVelocity, carCount, playerVelocity, playerAcc, carVelocity, carAcc, CPinc, offset
    channel3.play(SOUNDS['Achievement'], loops = 0)
    level += 1
    if level % 5 == 0 and carCount < 8:
        carCount += 1
        CPinc += level
    else:
        carVelocity += carAcc
        playerVelocity += playerAcc
    
    if level % 10 == 0:
        offset += 50
    
def reset():
    global playerPos, CARS, level, score, carCount, playerVelocity, playerAcc, carVelocity, carAcc, CPinc
    playerPos = [LANES[4]-carSize[0]/2,620]
    CARS = []
    level = 1
    score = 0
    carCount = 1
    playerVelocity = 5
    playerAcc = 0.5
    carVelocity = 2
    carAcc = 0.5
    CPinc = 5
    offset = 200

if __name__ == "__main__":

    pygame.init()

    #Adding resources to IMAGES dictionary
    introPageImage = pygame.image.load("Images\IntroPage.png")
    IMAGES['IntroPage'] = pygame.transform.scale(introPageImage, (introPageSize[0], introPageSize[1]))
    gameAreaImage = pygame.image.load("Images\Background.png")
    IMAGES['GameArea'] = pygame.transform.scale(gameAreaImage, (gameAreaSize[0], gameAreaSize[1] + 50))
    playerImage = pygame.image.load("Images\car.png")
    IMAGES['Player'] = pygame.transform.scale(playerImage, (carSize[0], carSize[1]))
    car1Image = pygame.image.load("Images\car1.png")
    IMAGES['Car1'] = pygame.transform.scale(car1Image, (carSize[0], carSize[1]))
    car2Image = pygame.image.load("Images\car2.png")
    IMAGES['Car2'] = pygame.transform.scale(car2Image, (carSize[0], carSize[1]))
    car3Image = pygame.image.load("Images\car3.png")
    IMAGES['Car3'] = pygame.transform.scale(car3Image, (carSize[0], carSize[1]))
    gameNameImage = pygame.image.load("Images\GameName.png")
    IMAGES['GameName'] = pygame.transform.scale(gameNameImage, (500,100))
    devNameImage = pygame.image.load("Images\DevName.png")
    IMAGES['DevName'] = pygame.transform.scale(devNameImage, (150,30))
    beginMsgImage = pygame.image.load("Images\Message.png")
    IMAGES['BeginMsg'] = pygame.transform.scale(beginMsgImage, (200,30))

    #Adding resources to SOUNDS dictionary
    SOUNDS['IntroPage'] = pygame.mixer.Sound("Sounds\IntroPage.mp3") 
    SOUNDS['GameArea'] = pygame.mixer.Sound("Sounds\GameArea.mp3")
    SOUNDS['Horn'] = pygame.mixer.Sound("Sounds\Horn.mp3")
    SOUNDS['Ignition'] = pygame.mixer.Sound("Sounds\Ignition.mp3")
    SOUNDS['DrivingCar'] = pygame.mixer.Sound("Sounds\DrivingCar.mp3")
    SOUNDS['Achievement'] = pygame.mixer.Sound("Sounds\Achievement.mp3")
    SOUNDS['GameOver'] = pygame.mixer.Sound("Sounds\GameOver.mp3")

    # Adding resources to TEXTS dictionary
    font = pygame.font.Font('freesansbold.ttf', 32)
    TEXTS['ScoreTitle'] = font.render("Score", True, 'white')
    TEXTS['ScoreValue'] = font.render(str(score), True, 'white')
    TEXTS['LevelTitle'] = font.render("Level", True, 'white')
    TEXTS['LevelValue'] = font.render(str(level), True, 'white')

    #GameFlow
    pygame.display.set_caption("Dodge the Kar")
    while True:
        showIntroPage()
        showGameArea()
