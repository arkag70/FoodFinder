import pygame
from settings import *
from matingpool import MatingPool
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
        self.completed = False
        self.crashed = False

    def draw(self):
        pygame.draw.rect(self.screen, self.color, self.rect)

    def move(self):

        self.rect.x += choice(self.xvel)
        self.rect.y += choice(self.yvel)

        self.xvel += self.xacc
        self.yvel += self.yacc

    def calculateFitness(self, target, initialDistance):

        targetx, targety, targetLen = target.xpos, target.ypos, target.length
        distance = sqrt((targetx - self.rect.x)**2 + (targety - self.rect.y)**2)
        self.fitness = 1 if (distance < targetLen) else (1/distance)
        
        if self.fitness == 1:
            self.completed = True
            self.color = target.color
        
        return distance
    
    def checkCollision(self, obstacle):
        
        if (self.rect.x  >= obstacle.xpos and self.rect.x <= obstacle.xpos + obstacle.width) and (self.rect.y  >= obstacle.ypos and self.rect.y <= obstacle.ypos + obstacle.height):
            self.crashed = True

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