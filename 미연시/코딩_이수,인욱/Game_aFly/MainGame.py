__author__ = 'hahaha'

import pygame as py
import random
## sleep = 잠깐 멈춤
from time import sleep

WHITE = (255,255,255)
RED = (255,0,0)

pad_width = 1024
pad_height = 512

background_width = 1024

aircraft_width = 90
aircraft_height = 55

bat_width = 110
bat_height = 67

fireball1_width = 140
fireball1_height = 60
fireball2_width = 86
fireball2_height = 60

def drawScore(count, HP):
    global gamepad

    font = py.font.Font('Game_aFly/Font/Galmuri11-Bold.ttf', 25)
    text = font.render('갯수: ' + str(count) + '체력' + str(HP), True, WHITE)
    gamepad.blit(text,(0,0))

def gameOver():
    global gamepad
    dispMessage('실패')

def gameComplte():
    global gamepad
    dispMessage('실패')

def textObj(text, font):
    textSurface = font.render(text, True, RED)
    return textSurface, textSurface.get_rect()

def dispMessage(text):
    global gamepad

    largeText = py.font.Font('Game_aFly/Font/Galmuri11-Bold.ttf', 115)
    TextSurf, TextRect = textObj(text, largeText)
    TextRect.center = ((pad_width/2),(pad_height/2))
    gamepad.blit(TextSurf, TextRect)
    py.display.update()
    ##py.mixer.music.pause()
    sleep(2)
    ##py.mixer.unpause()
    runGame()

def crash():
    global gamepad, explosion_sound
    ##py.mixer.music.stop() ## or pause
    ##py.mixer.Sound.play(explosion_sound)
    dispMessage('GAME OVER!')

def drawObject(obj, x, y):
    global gamepad
    gamepad.blit(obj,(x, y))

def runGame():
    global gamepad, aircraft, clock, background1, background2
    global bat, fires, bullet, boom, shot_sound

    Player_HP = 100

    isShotBat = False
    boom_count = 0

    bat_passed = 0

    bullet_xy = []

    x = pad_width * 0.05
    y = pad_height * 0.8
    y_change = 0

    background1_x = 0
    background2_x = background_width

    bat_x = pad_width
    bat_y = random.randrange(0, pad_height)

    fire_x = pad_width
    fire_y = random.randrange(0, pad_height)
    random.shuffle(fires)
    fire = fires[0]

    crashed = False
    while not crashed:
        for event in py.event.get():
            if event.type == py.QUIT:
                crashed = True

            if event.type == py.KEYDOWN:
                if event.key == py.K_UP:
                    y_change = -5

                elif event.key == py.K_DOWN:
                    y_change = 5
                
                elif event.key == py.K_LCTRL:
                    bullet_x = x + aircraft_width
                    bullet_y = y + aircraft_height/2
                    bullet_xy.append([bullet_x, bullet_y])
                    ##py.mixer.Sound.play(shot_sound)

            if event.type == py.KEYUP:
                if event.key == py.K_UP or event.key == py.K_DOWN:
                    y_change = 0

        #Clear gamepad
        gamepad.fill(WHITE)
        
        #Draw Background
        background1_x -= 2
        background2_x -= 2

        if background1_x == -background_width:
            background1_x = background_width

        if background2_x == -background_width:
            background2_x = background_width

        drawObject(background1,background1_x,0)
        drawObject(background2,background2_x,0)

        drawScore(bat_passed, Player_HP)

        #Check the number of BAT passed
        if bat_passed > 5:
            gameComplte()

        #Aircraft Postion
        y += y_change
        if y<0:
            y = 0
        elif y > pad_height - aircraft_height:
            y = pad_height - aircraft_height

        #Bat Pos
        bat_x -= 7
        if bat_x <= 0:
            bat_x = pad_width
            bat_y = random.randrange(0,pad_height)

        #Fireball Pos
        if fire[1] == None:
            fire_x -= 30
        else:
            fire_x -= 15

        if fire_x <= 0:
            fire_x = pad_width
            fire_y = random.randrange(0,pad_height)
            random.shuffle(fires)
            fire = fires[0]

        #Bullet pos
        if len(bullet_xy) != 0:
            for i, bxy in enumerate(bullet_xy):
                bxy[0] += 15
                bullet_xy[i][0] = bxy[0]

                #Check if bullet strike Bat
                if bxy[0] > bat_x:
                    if bxy[1] > bat_y and bxy[1] < bat_y + bat_height:
                        bullet_xy.remove(bxy)
                        bat_passed += 1 
                        isShotBat = True

                if bxy[0] >= pad_width:
                    try:
                        bullet_xy.remove(bxy)
                    except:
                        pass

        #Check aircraft crashed by BAT
        if x + aircraft_width > bat_x:
            if(y > bat_y and y < bat_y + bat_height) or\
            (y+aircraft_height > bat_y and y + aircraft_height < bat_y + bat_height):
                Player_HP += 1
                ##crash()

        #Check aircraft crashed by Fireball
        if fire[1] != None:
            if fire[0] == 0:
                fireball_width = fireball1_width
                fireball_height = fireball1_height
            elif fire[0] == 1:
                fireball_width = fireball2_width
                fireball_height = fireball2_height

            if x+ aircraft_width > fire_x:
                if(y>fire_y and y < fire_y + fireball_height) or\
                (y+ aircraft_height > fire_y and y + aircraft_height < fire_y + fireball_height):
                    crash()
                    

        drawObject(aircraft, x,y)

        if len(bullet_xy) != 0:
            for bx, by in bullet_xy:
                drawObject(bullet, bx, by)

        if not isShotBat:
            drawObject(bat,bat_x,bat_y)
        else:
            drawObject(boom,bat_x,bat_y)
            boom_count +=1
            if boom_count > 5:
                boom_count = 0
                bat_x = pad_width
                bat_y = random.randrange(0, pad_height-bat_height)
                isShotBat = False

        if fire[1] != None:
            drawObject(fire[1], fire_x, fire_y)

        py.display.update()
        clock.tick(60)

    py.quit()
    quit()

def initGame():
    global gamepad, aircraft, clock, background1, background2
    global bat, fires, bullet, boom
    global shot_sound, explosion_sound

    ## 배경음
    ##py.mixer.music.load('주소Game_aFly/Audio/mybgm.wav')
    ##py.mixer.music.play(-1)
    

    fires = []

    py.init()
    gamepad = py.display.set_mode((pad_width, pad_height))
    py.display.set_caption('Sleve_To_Coding')

    aircraft = py.image.load('Game_aFly/Img/plane.png')

    background1 = py.image.load('Game_aFly/Img/background.png')
    background2 = background1.copy()

    bat = py.image.load('Game_aFly/Img/bat.png')

    fires.append((0, py.image.load('Game_aFly/Img/fireball.png')))
    fires.append((1, py.image.load('Game_aFly/Img/fireball2.png')))

    boom = py.image.load('Game_aFly/Img/boom.png')

    for i in range(3):
        fires.append((i+2, None))

    bullet = py.image.load('Game_aFly/Img/bullet.png')

    ##shot_sound = py.mixer.Sound('Game_aFly/Audio/shot.wav')
    ##explosion_sound = py.mixer.Sound('Game_aFly/Audio/explosion.wav')

    clock = py.time.Clock()
    runGame()


if __name__ == '__main__':
    initGame()


## https://m.blog.naver.com/samsjang/220713309790 