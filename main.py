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

# initiate pygame
pygame.init()

# define colors

black = (0,0,0)
white = (255,255,255)
red = (255,0,0)
block_color = (53,115,255)

car_width = 57
car_height = 115


## game options ## 

# game resolution
display_width = 800
display_height = 600

# set size of game display
gameDisplay = pygame.display.set_mode((display_width, display_height))

# title of game window
pygame.display.set_caption('Super Car Cat')

# define game clock
clock = pygame.time.Clock()


### GAME ###

## CAR ##
carImg = pygame.image.load('car_small.png')

## functions ##


def things_dodged(count):
    font = pygame.font.SysFont(None, 25)
    text = font.render("Score: " + str(count), True, black)
    gameDisplay.blit(text, (0,0))

def time_passed(count):
    font = pygame.font.SysFont(None, 25)
    text = font.render("Time passed: " + str(count), True, black)
    gameDisplay.blit(text, (0,25))

# =============================================================================
# def xspeed(count):
#     font = pygame.font.SysFont(None, 25)
#     text = font.render("X-speed: " + str(count), True, black)
#     gameDisplay.blit(text, (0,50))
#     
# def yspeed(count):
#     font = pygame.font.SysFont(None, 25)
#     text = font.render("Y-speed: " + str(count), True, black)
#     gameDisplay.blit(text, (0,75))
# =============================================================================

# things to avoid in the game
def things(thingx, thingy, thingw, thingh, color):
    pygame.draw.rect(gameDisplay, color, [thingx, thingy, thingw, thingh])
    

# display car in game
def car(x,y):
    # refence to display
    gameDisplay.blit(carImg, (x,y))

def text_objects(text, font):
    textSurface = font.render(text, True, black)
    return textSurface, textSurface.get_rect()

def message_display(text):
    largeText = pygame.font.Font('freesansbold.ttf', 115)
    TextSurf, TextRect = text_objects(text, largeText)
    TextRect.center = ((display_width/2),(display_height/2))
    gameDisplay.blit(TextSurf, TextRect)
    
    pygame.display.update()
    
    time.sleep(2)
    
    game_loop()
    
def crash():
    message_display('GAME OVER!')

#


# main game loop
def game_loop():
    
    # starting position
    x = (display_width * 0.45)
    y = (display_height * 0.8)
    
    # change in position
    x_change = 0
    y_change = 0
    
    
    # object start positoins
    thing_startx = random.randrange(0, display_width)
    thing_starty = -600
    # speed
    thing_speed = 7
    # size of object
    thing_width = 100
    thing_height = 100
    # above are parameters used in things function
    
    
    dodged = 0
    
    startTime = time.time()
    
    timePassed = 0

    
    ## game stop parameter
    gameExit = False
    
    # game will run so long as crashed is equal to false
    while not gameExit: 
        
        # gets all events happening in the game cursor movements, key clicks etc. 
        for event in pygame.event.get():
            # if user clicks on 'x' in top right corner, set 'crashed' to True, thereby ending game
            if event.type == pygame.QUIT:
                pygame.quit()
                quit()
            
            
            # car controls
            if event.type == pygame.KEYDOWN:
                keys = pygame.key.get_pressed()
                
                if keys[pygame.K_LEFT]:
                    x_change = - 5
            
                if keys[pygame.K_RIGHT]:
                    x_change = 5
                
                if keys[pygame.K_UP]:
                    y_change = -5
            
                if keys[pygame.K_DOWN]:
                    y_change = 5
                
            
            
            """key=pygame.key.get_pressed()  #checking pressed keys
            if key[pygame.K_a]:x_change = -5
            if key[pygame.K_d]:x_change = 5
            if key[pygame.K_w]:y_change = -5
            if key[pygame.K_s]:y_change = 5"""
            
            
            # stop moving when keys are no longer pressed (needs more work)
            if event.type == pygame.KEYUP:
                if event.key == pygame.K_LEFT or event.key == pygame.K_RIGHT:
                    x_change = 0
                    
            if event.type == pygame.KEYUP:
                if event.key == pygame.K_UP or event.key == pygame.K_DOWN:
                    y_change = 0
            
                    
    
        # update car position         
        x += x_change
        y += y_change
                
        # background color of game
        gameDisplay.fill(white)
        
        
        # display things
        things(thing_startx, thing_starty, thing_width, thing_height, block_color)
        # update position of things/object
        thing_starty += thing_speed
        
        #display car
        car(x,y)
        
        # score
        things_dodged(dodged)
        
        # time passed
        time_passed(timePassed)
        
        
        # game boundary
        if x > display_width - car_width or x < 0:
            crash()
        
        # when object exits screen, a new one spawns
        if thing_starty > display_height:
            # start at top of screen
            thing_starty = 0 - thing_height
            # starts at random x-coordinate
            thing_startx = random.randrange(0, display_width)
            dodged += 1
            
            
            
        # collision detection
        if x < thing_startx + thing_width and\
        x + car_width > thing_startx and\
        y < thing_starty + thing_height and\
        y + car_height > thing_starty:
            crash()
        
        
        
        # draw lines from car to objects
        # vertical distance lines
        pygame.draw.line(gameDisplay, black, (x,y), (x, thing_starty+thing_height),1)
        pygame.draw.line(gameDisplay, black, (x+car_width,y), (x+car_width, thing_starty+thing_height),1)
        # horizontal distance lines
        if x > thing_startx+thing_width:
            pygame.draw.line(gameDisplay, black, (x,y),(thing_startx+thing_width,y),1,)
        
        if x + car_width < thing_startx:
            pygame.draw.line(gameDisplay, black, (x+car_width,y),(thing_startx,y),1,)

        
        
        
        timePassed = round((time.time() - startTime), 4)

        # update display after events  
        pygame.display.update()
        
        # define clock / frames per second
        clock.tick(60)

# run game loop
game_loop()
    
# stop pygame
pygame.quit()

# stop .py program
quit()




