import pygame
from settings import OBS_X, OBS_Y, OBS_W, OBS_H

class Obstacle:

    def __init__(self, x, y, w, h, screen):
        self.xpos = x
        self.ypos = y
        self.width = w
        self.height = h
        self.screen = screen
        self.color = (255, 255, 0)
        self.rect = pygame.Rect(x,y,w,h)
    
    def draw(self):
        pygame.draw.rect(self.screen, self.color, self.rect)

    @staticmethod
    def createObstacle(screen):
        return Obstacle(OBS_X, OBS_Y, OBS_W, OBS_H, screen)