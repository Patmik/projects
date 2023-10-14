import pygame
from pygame.locals import *
import random

class Sanke():
    
    def __init__(self, window, windowWidth, windowHeight):
        self.window = window
        self.windowWidth = windowWidth
        self.windowHeight = windowHeight
        self.color = (255, 0, 0)
        self.score = 0
        self.length = 1
        self.direction = (0,-10)
        self.positions = [(320, 220)]
        self.flag = True
        

    def change_direction(self,direction):
        if direction == 'UP':
            self.direction = (0,-10)
        elif direction == 'DOWN':
            self.direction = (0,10)
        elif direction == 'LEFT':
            self.direction = (-10,0)
        elif direction == 'RIGHT':
            self.direction = (10,0)

    
    def move(self):
        head = (self.positions[0][0],self.positions[0][1])
        new_head = (head[0] + self.direction[0],head[1] + self.direction[1])
        self.positions.insert(0,new_head)
        if self.length < len(self.positions):
            self.positions.pop()
        if new_head[0] < 0 or new_head[0] > self.windowWidth:
            self.game_over()
        if new_head[1] <0 or new_head[1] > self.windowHeight:
            self.game_over()
        if new_head in self.positions[1::]:
            self.game_over()
            
            

    def eat(self,food,flag):
        if flag == True:
            if self.positions[0][0] == food[0] and self.positions[0][1] == food[1]:
                self.positions.append((food[0],food[1]))
                self.length += 1
                self.flag = False
                self.score += 1
            else:
                self.flag = True
        return self.flag
    

    def game_over(self):
        self.length = 1
        self.direction = (0,-10)
        self.positions = [(320, 220)]
        self.flag = True
        self.score = 0
        
    
    def score(self):
        return self.score
    
    def draw(self):
        for position in self.positions:
            pygame.draw.rect(self.window, self.color, (position[0], position[1], 10, 10), 0)
            