import pygame
from settings import *
from matingpool import MatingPool
from math import sqrt
from random import choice
CRASHWEIGHT = 5

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
        self.fitness = 1
        self.screen = screen
        self.completed = False
        self.crashed = False

    def draw(self):
        pygame.draw.rect(self.screen, self.color, self.rect)

    def move(self):

        self.rect.x += choice(self.xvel)
        self.rect.y += choice(self.yvel)

        self.xvel += self.xacc
        self.yvel += self.yacc

    def calculateFitness(self, target):

        targetx, targety = target.xpos, target.ypos
        distance = sqrt((targetx - self.rect.x)**2 + (targety - self.rect.y)**2)
        initialDistance = sqrt((targetx - XPOSPARAMS)**2 + (targety - YPOSPARAMS)**2)
        relative = initialDistance - distance
        self.fitness = relative/initialDistance if relative >= 0 else 0

        if distance < target.width:
            self.completed = True
            self.color = target.color

        if self.crashed == True:
            self.fitness /= CRASHWEIGHT
    
    def checkCollision(self, obstacle):
        # with obstacle
        if (self.rect.x  >= obstacle.xpos and self.rect.x <= obstacle.xpos + obstacle.width) and (self.rect.y  >= obstacle.ypos - self.length and self.rect.y <= obstacle.ypos + obstacle.height):
            self.crashed = True
        # with left right walls
        if (self.rect.x  <= 0 or self.rect.x >= self.screen.get_width()-self.breadth ):
            self.xrev(DAMP)
        # top bottom walls
        if (self.rect.y <= 0 or self.rect.y >= self.screen.get_height() - self.length):
            self.yrev(DAMP)

    def xrev(self, damp):
        self.xvel = [-1 * xvel for xvel in self.xvel]
        self.xacc *= damp
    
    def yrev(self, damp):
        self.yvel = [-1 * yvel for yvel in self.yvel]
        self.yacc *= damp

    @staticmethod
    def createFoodfinders(matingPool, screen):

        foodfinders = []
        for _ in range(FOODFINDERS):
            xvelarr = []
            yvelarr = []
            
            if(len(matingPool.dnaPool) == 0):
                # generate random dna (velocity)
                for _ in range(VELOCITY_VECTOR_SIZE):
                    xvelarr.append(choice(getRange(XVECLPARAMS)))
                    yvelarr.append(choice(getRange(YVECLPARAMS)))
            else:
                # select dna from matingPool
                parentA = matingPool.selection()
                parentB = matingPool.selection()

                #crossover between two parents
                selectedDNA = MatingPool.crossover(parentA, parentB, CROSSOVERRATE)
                #mutation on the selected DNA
                selectedDNA = MatingPool.mutation(selectedDNA, MUTATIONRATE)
                for _ in range(VELOCITY_VECTOR_SIZE):
                    xvelarr.append(choice(selectedDNA[X_INDEX]))
                    yvelarr.append(choice(selectedDNA[Y_INDEX]))

            foodfinders.append(Foodfinder(LENGTH, BREADTH, 
                XPOSPARAMS ,YPOSPARAMS, 
                xvelarr, yvelarr, 
                choice(getRange(ACCPARAMS)), choice(getRange(ACCPARAMS)), screen))
        return foodfinders