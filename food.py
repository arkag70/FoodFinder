import pygame

class Food:

    def __init__(self, l, b, x, y):
        self.length = l
        self.breadth = b
        self.xpos = x
        self.ypos = y
        self.rect = pygame.Rect(x,y,b,l)
        self.color = (255, 0, 0)

    def draw(self, screen):
        pygame.draw.rect(screen, self.color, self.rect)