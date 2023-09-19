from random import choice, random
from numpy import concatenate
from settings import FITNESSBONUS

class MatingPool:

    def __init__(self):
        self.dnaPool = list(tuple())

    def addFitness(self, dna, fitness):
        ''' 
            0 < fitness < 1,
            mutiply by 100 and round off,
            append dna to the dnaPool
            the number of times defined by their 
            fitness so that they've high 
            probalibity of getting picked
        '''
        fitness = fitness * FITNESSBONUS if fitness == 1 else fitness
        N = int(fitness * 100)
        for _ in range(N):
            self.dnaPool.append(dna)
    
    def selection(self):
        return choice(self.dnaPool)
    
    @staticmethod
    def crossover(dnaA, dnaB, crossoverRate):
        xParamsA, yParamsA = dnaA
        xParamsB, yParamsB = dnaB

        if random() < crossoverRate:
            childXDna = concatenate((xParamsA[:int(len(xParamsA)/2)], xParamsB[int(len(xParamsB)/2): len(xParamsB)]))
            childYDna = concatenate((yParamsA[:int(len(yParamsA)/2)], yParamsB[int(len(yParamsB)/2): len(yParamsB)]))
            return (childXDna, childYDna)
        
        return (xParamsA, yParamsA)
    
    @staticmethod
    def mutation(dna, mutationRate):

        xParams, yParams = dna
        if random() < mutationRate:
            xParams = [(val+ 2*random() - 1) for val in xParams]
            yParams = [(val+ 2*random() - 1) for val in yParams]
        return (xParams, yParams)
    
    def reset(self):
        self.dnaPool = list(tuple())