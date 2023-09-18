import pygame
from math import sqrt
from random import choice
class Freeloader:

    def __init__(self, l, b, x, y, vxarr, vyarr, ax, ay) -> None:
        
        self.length = l
        self.breadth = b
        self.xpos = x
        self.ypos = y
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

    def draw(self, screen):
        pygame.draw.rect(screen, self.color, self.rect)

    def move(self):

        self.rect.x += choice(self.xvel)
        self.rect.y += choice(self.yvel)

        self.xvel += self.xacc
        self.yvel += self.yacc

    def calculateFitness(self, target):
        targetx, targety = target
        distance = sqrt((targetx - self.xpos)**2 + (targety - self.ypos)**2)
        self.fitness = 1/(1+distance) # in case distance is 0

    # def boundaryCheck(self, canvaswidth, canvasheight, damp):
    #     if(self.rect.x < 0 or self.rect.x > (canvaswidth - self.breadth)):
    #         self.xrev(damp)
    #     if(self.rect.y < 0 or self.rect.y > (canvasheight - self.length)):
    #         self.yrev(damp)

    # def onCollision(self):
    #     self.age+=1

    #     if self.blue > 0:
    #         self.blue = (self.blue - DROP) if (self.blue - DROP) > 0 else 0
    #         if self.green < 255:
    #             self.green = (self.green + DROP) if (self.green + DROP) < 255 else 255
    #     else:
    #         if self.green > 0:
    #             self.green = (self.green - DROP) if (self.green - DROP) > 0 else 0
    #             if self.red < 255:
    #                 self.red = (self.red + DROP) if (self.red + DROP) < 255 else 255

    # def xrev(self, damp):
    #     self.xvel *= -1
    #     self.xacc *= damp
    #     self.onCollision()
    
    # def yrev(self, damp):
    #     self.yvel *= -1
    #     self.yacc *= damp
    #     self.onCollision()