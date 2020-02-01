import pygame
import random
import math
from pygame import mixer
pygame.init()
screen = pygame.display.set_mode((800,600))
background = pygame.image.load('background1.jpg')
mixer.music.load('mobamba.mp3')
mixer.music.play(-1)
pygame.display.set_caption("Space Invaders")
icon = pygame.image.load('clownsponge.png')
pygame.display.set_icon(icon)


playerImg = pygame.image.load('hero.png')
playerX = 400
playerY = 550
playerXChange = 0

enemyImg = []
enemyX = []
enemyY = []
enemyXChange = []
enemyYChange = []
num_of_enemies = 6
for i in range(num_of_enemies):
    enemyImg.append(pygame.image.load('enemy.png'))
    enemyX.append(random.randint(0, 735))
    enemyY.append(random.randint(50, 150))
    enemyXChange.append(random.randint(10,30))
    enemyYChange.append(random.randint(10,30))


bulletImg = pygame.image.load('bullet.png')
bulletX = 0
bulletY = 550
bulletXChange = 0
bulletYChange = 25
bulletState = 'ready'

score_value = 0
font = pygame.font.Font('freesansbold.ttf', 32)
textX = 10
textY = 10

death_font = pygame.font.Font('freesansbold.ttf', 64)

def show_score(x,y):
    score = font.render('Score :' +str(score_value), True, (255,255,255))
    screen.blit(score, (x,y))
def game_over():
    over_text = death_font.render('GAME OVER', True, (255,0,0))
    screen.blit(over_text, (300, 250))
    #pygame.mixer.pause()
    #mixer.music.load('theme.mp3')
    #pygame.mixer.unpause()
def enemy(x,y,i):
    screen.blit(enemyImg[i], (x,y))
def player(x,y):
    screen.blit(playerImg, (x, y))
def fireBullet(x,y):
    global bulletState
    bulletState = 'fire'
    screen.blit(bulletImg, (x,y+5))
def isCollision(enemyX,enemyY,bulletX,bulletY):
    distance = math.sqrt(math.pow(enemyX - bulletX,2)+math.pow(enemyY - bulletY,2))
    if distance < 27:
        return True
    else:
        False
running = True

while running:

    screen.fill((0, 0, 0))
    screen.blit(background, (0,0))
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False
        if event.type == pygame.KEYDOWN:
            if event.key == pygame.K_LEFT:
                playerXChange = -10
            if event.key == pygame.K_RIGHT:
                playerXChange = 10
            if event.key == pygame.K_SPACE:
                if bulletState in 'ready':
                    bullet_Sound = mixer.Sound('gunshot.wav')
                    bullet_Sound.play()
                    bulletX = playerX
                    fireBullet(bulletX,bulletY)


    playerX += playerXChange

    if playerX <=0:
        playerX = 0
    elif playerX >=800:
        playerX = 700


    for i in range(num_of_enemies):
        if enemyY[i] > 480:
            for j in range(num_of_enemies):
                enemyY[j] = 2000
            game_over()
            break

        enemyX[i] += enemyXChange[i]
        if enemyX[i] <=0:
            enemyXChange[i] = random.randint(10,30)
            enemyY[i] += enemyYChange[i]
        elif enemyX[i] >= 800:
            enemyXChange[i] = -(random.randint(10,30))
            enemyY[i] += enemyYChange[i]

        collision = isCollision(enemyX[i],enemyY[i], bulletX,bulletY)
        if collision:
            enemy_Sound = mixer.Sound('death.wav')
            enemy_Sound.play()
            bulletY = 550
            bulletState = 'ready'
            score_value += 1
            enemyX[i] = random.randint(0, 735)
            enemyY[i] = random.randint(50, 150)
        enemy(enemyX[i], enemyY[i], i)
    if bulletY <= -10:
        bulletY = 550
        bulletState = 'ready'

    if bulletState in 'fire':
        fireBullet(bulletX,bulletY)
        bulletY -= bulletYChange


    player(playerX, playerY)
    show_score(textX,textY)
    pygame.display.update()
