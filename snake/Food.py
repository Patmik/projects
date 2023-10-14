import pygame
from pygame.locals import *
import random


class Food():
    def __init__(self,window, windowWidth, windowHeight):
        self.window = window
        self.windowWidth = windowWidth
        self.windowHeight = windowHeight
        self.color = (0, 255, 0) 

        self.position = (0,0)
        self.randomize_position()


        

    def randomize_position(self):
        self.position = (random.randrange(1, (self.windowWidth//10)) * 10, random.randrange(1, (self.windowHeight//10)) * 10)

    def draw(self):
        pygame.draw.rect(self.window, self.color, (self.position[0], self.position[1], 10, 10), 0)
    