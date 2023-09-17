
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
        N = int(fitness*100)
        for _ in range(N):
            self.dnaPool.append(dna)

    def reset(self):
        self.dnaPool = list(tuple())