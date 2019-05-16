# -*- coding: utf-8 -*-
"""
Created on Tue May 14 11:03:30 2019

My first attempt at a game in python
This is a racing game.
Game will stop if car crashes

@author: Steven
"""
## preample ##

# import library
import pygame
import time
import random
from os import path

img_dir = path.join(path.dirname(__file__), 'img')

# initiate pygame
pygame.init()

# pygame module for loading and playing sounds
pygame.mixer.init()

# define colors
black = (0, 0, 0)
white = (255, 255, 255)
red = (255, 0, 0)
block_color = (53, 115, 255)

car_width = 100
car_height = 100
carSpeed = 5

## GAME OPTIONS ##

# game resolution
display_width = 800
display_height = 600
# set size of game display
gameDisplay = pygame.display.set_mode((display_width, display_height))
# title of game window
pygame.display.set_caption('Super Car Cat')
# define game clock
clock = pygame.time.Clock()

# ASSETS

# Load graphics
playerImg = pygame.image.load(path.join(img_dir, 'car.png')).convert_alpha()

# Sprites
class Player(pygame.sprite.Sprite):
    def __init__(self):
        pygame.sprite.Sprite.__init__(self)
        self.image = pygame.transform.scale(playerImg, (car_width, car_height))
        self.rect = self.image.get_rect()
        self.rect.centerx = display_width / 2
        self.rect.bottom = display_height * 0.8
        self.speedx = 0
        self.speedy = 0

    def update(self):

        # stops movement when no keys are pressed
        self.speedx = 0
        self.speedy = 0

        # player movement
        keystate = pygame.key.get_pressed()
        if keystate[pygame.K_LEFT]:
            self.speedx = -carSpeed
        if keystate[pygame.K_RIGHT]:
            self.speedx = carSpeed
        self.rect.x += self.speedx

        if keystate[pygame.K_UP]:
            self.speedy = -carSpeed
        if keystate[pygame.K_DOWN]:
            self.speedy = carSpeed
        self.rect.y += self.speedy

class Object(pygame.sprite.Sprite):
    def __init__(self, nr):
        pygame.sprite.Sprite.__init__(self)
        self.image = pygame.image.load(path.join(img_dir, 'Car_{0}.png'.format(nr))).convert_alpha()
        self.image = pygame.transform.flip(self.image, False, True)
        self.image = pygame.transform.scale(self.image, (car_width, car_height))
        self.rect = self.image.get_rect()
        self.rect.x = random.randrange(0, display_width-self.rect.width)
        self.rect.y = random.randrange(-1200, -100)
        self.speedy = 6

    def update(self):
        self.rect.y += self.speedy
        if self.rect.top > display_height + 45:
            self.rect.x = random.randrange(0, display_width - self.rect.width)
            self.rect.y = random.randrange(-1200, -100)
            self.speedy = 6

# Definitions
def time_passed(count):
    font = pygame.font.SysFont(None, 25)
    text = font.render("Time passed: " + str(count), True, black)
    gameDisplay.blit(text, (0, 25))

def text_objects(text, font):
    textSurface = font.render(text, True, black)
    return textSurface, textSurface.get_rect()

font_name = pygame.font.match_font('arial')
def draw_text(surf, text, size, x, y):
    font = pygame.font.Font(font_name, size)
    text_surface = font.render(text, True, black)
    text_rect = text_surface.get_rect()
    text_rect.midtop = (x, y)
    surf.blit(text_surface, text_rect)

def message_display(text):
    largeText = pygame.font.Font('freesansbold.ttf', 115)
    TextSurf, TextRect = text_objects(text, largeText)
    TextRect.center = ((display_width / 2), (display_height / 2))
    gameDisplay.blit(TextSurf, TextRect)
    pygame.display.update()

def crash():
    message_display('GAME OVER!')
    #time.sleep(2)
    gameExit = True
    game_loop()

def show_go_screen():
    gameDisplay.fill(white)
    draw_text(gameDisplay, 'Super Car Cat', 64, display_width/2, display_height/4)
    draw_text(gameDisplay, 'Arrow keys to move', 32, display_width/2, display_height/2)
    draw_text(gameDisplay, 'Press any key to start', 24, display_width/2, display_height*3/4)
    pygame.display.flip()
    waiting = True
    while waiting:
        clock.tick(60)
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
            if event.type == pygame.KEYUP:
                waiting = False

def game_loop():


    # game stop parameter
    gameExit = False
    gameOver = True

    # game will run so long as crashed is equal to false
    while not gameExit:
        # define clock / frames per second
        clock.tick(60)
        if gameOver:
            show_go_screen()
            gameOver = False
            startTime = time.time()
            all_sprites = pygame.sprite.Group()
            blocks = pygame.sprite.LayeredUpdates()
            player = Player()
            #object = Object()
            all_sprites.add(player)
            for i in range(1, 6):
                m = Object(nr=random.randrange(1, 5))
                all_sprites.add(m)
                blocks.add(m)

        # pygame.sprite.collide_mask

        ## EVENTS ##
        # gets all events happening in the game cursor movements, key clicks etc. 
        for event in pygame.event.get():
            # if user clicks on 'x' in top right corner, set 'crashed' to True, thereby ending game
            if event.type == pygame.QUIT:
                pygame.quit()
                quit()


        ## UPDATE GAME STATE ##

        # update all_sprites group
        all_sprites.update()

        # collision detection
        hits = pygame.sprite.spritecollide(player, blocks, False, pygame.sprite.collide_mask)

        #hits = pygame.sprite.collide_mask(player, object)
        if hits:
            gameOver = True

        timePassed = round((time.time() - startTime), 4)


        ## RENDER ###
        # background color of game
        gameDisplay.fill(white)
        # score
        time_passed(timePassed)
        # all sprites
        all_sprites.draw(gameDisplay)
        # update display after events  
        pygame.display.flip()


# run game loop
game_loop()

# stop pygame
pygame.quit()

# stop .py program
quit()
