import pygame
from settings import FOODLEN, FOODWID, FOODX, FOODY, ALPHA

class Food:

    def __init__(self, l, b, x, y, screen):
        self.height = l
        self.width = b
        self.xpos = x
        self.ypos = y
        self.rect = pygame.Rect(x,y,b,l)
        self.color = (255, 0, 0, ALPHA)
        self.screen = screen

    def draw(self):
        pygame.draw.rect(self.screen, self.color, self.rect)

    @staticmethod
    def createFood(screen):
        return Food(FOODLEN, FOODWID, FOODX, FOODY, screen)