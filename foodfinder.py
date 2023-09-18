import pygame
from math import sqrt
from random import choice
class Foodfinder:

    def __init__(self, l, b, x, y, vxarr, vyarr, ax, ay, screen) -> None:
        
        self.length = l
        self.breadth = b
        self.xvel = vxarr
        self.yvel = vyarr
        self.xacc = ax
        self.yacc = ay
        self.red = 255
        self.green = 255
        self.blue = 255
        self.color = (self.red, self.green, self.blue)
        self.rect = pygame.Rect(x, y, b, l)
        self.fitness = 0
        self.screen = screen

    def draw(self):
        pygame.draw.rect(self.screen, self.color, self.rect)

    def move(self):

        self.rect.x += choice(self.xvel)
        self.rect.y += choice(self.yvel)

        self.xvel += self.xacc
        self.yvel += self.yacc

    def calculateFitness(self, target):
        targetx, targety = target
        distance = sqrt((targetx - self.rect.x)**2 + (targety - self.rect.y)**2)
        self.fitness = 1 if distance==0 else 1/(distance)
        return distance