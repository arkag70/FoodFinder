import pygame

class Obstacle:

    def __init__(self, x, y, w, h):
        self.xpos = x
        self.ypos = y
        self.width = w
        self.height = h
        self.color = (255, 255, 0)
        self.rect = pygame.Rect(x,y,w,h)

    