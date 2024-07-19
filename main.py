import pygame
import time 
import math 
import random

from pygame import mixer

pygame.init()
screen = pygame.display.set_mode((1200,800))

pygame.display.set_caption("space ")

background = pygame.image.load('background.png')

playerimg = pygame.image.load('spaceship.png')
playerx = 600
playery = 700
playerx_change = 0
def player(x,y):
    screen.blit(playerimg,(x,y))

enemy_num = 7
enemyimg = []
enemyx = []
enemyy = []
enemyx_change = []
enemyy_change = []
for i in range(enemy_num):
    enemyimg.append(pygame.image.load('enemy.png'))
    enemyx.append(random.randint(0,1135))
    enemyy.append(random.randint(0,300))
    enemyx_change.append(0.5)
    enemyy_change.append(0.04)
def enemy(x,y,i):
        screen.blit(enemyimg[i],(x,y))

bullet = pygame.image.load('bullet.png')
bullet_x = 0
bullet_y = 600
bullet_x_change = 0
bullet_y_change = 10
bullet_state = 'ready'
def bullet_fire(x,y):
    global bullet_state
    bullet_state = 'fire'
    screen.blit(bullet,(x,y))

def iscollision(enemyx,enemyy,bullet_x,bullet_y):
    distance = math.sqrt((math.pow(bullet_x-enemyx,2))+(math.pow(bullet_y-enemyy,2)))
    if distance < 28:
        return True
    else:
        return False
score_value = 0

font = pygame.font.Font('freesansbold.ttf',20)
text_x = 10
text_y = 10
def show_score(x,y):
    score = font.render("score : "+ str(score_value),True,(0,225,0))
    screen.blit(score,(x,y))

mixer.music.load('backmus.wav')
mixer.music.play(-1)

game_over = pygame.font.Font('freesansbold.ttf',60)
gtext_x = 200
gtext_y = 400
def game_over_text(x,y):
    over_text = game_over.render(f"GAME OVER !! \n score is {str(score_value)}",True,(225,0,0))
    screen.blit(over_text,(x,y))


running = True
while running:
    screen.fill((225,0,0))
    screen.blit(background,(0,0))
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False
        if event.type == pygame.KEYDOWN:
            if event.key == pygame.K_LEFT:
                playerx_change = -0.7
            if event.key == pygame.K_RIGHT:
                playerx_change = 0.7
            if event.key == pygame.K_SPACE:
                if bullet_state is 'ready':
                    bullet_sound = mixer.Sound('lsound_fire.wav')
                    bullet_sound.play()
                    bullet_x = playerx
                    bullet_fire(bullet_x+18,bullet_y+55)
        if event.type == pygame.KEYUP:
            if event.key == pygame.K_LEFT or event.key == pygame.K_RIGHT:
                playerx_change = 0
        
    if playerx <= 0:
        playerx = 0
    elif playerx >= 1136:
        playerx = 1136

    for i in range(enemy_num):
        if enemyx[i] <= 0:
            enemyx_change[i] = 0.5
        elif enemyx[i] >= 1135:
            enemyx_change[i] = -0.5
        enemyx[i] += enemyx_change[i]
        enemyy[i] += enemyy_change[i]
        enemy(enemyx[i],enemyy[i],i)

        collision = iscollision(enemyx[i],enemyy[i],bullet_x,bullet_y)
        if collision:
            blast = mixer.Sound('blast.wav')
            blast.play()

            bullet_y = 600
            bullet_state = 'ready'
            score_value += 1
            enemyx[i] = random.randint(0,1135)
            enemyy[i] = random.randint(0,300)
        

    if bullet_state is 'fire':
        bullet_fire(bullet_x+18,bullet_y+55)
        bullet_y -= bullet_y_change
    
    if bullet_y <= 0:
        bullet_y = 600
        bullet_state = 'ready'

    if enemyy[i] > 700:
        game_over_text(gtext_x,gtext_y)
        
    

    show_score(text_x,text_y)

    playerx += playerx_change
    player(playerx,playery)
    pygame.display.update()
