import numpy as np
from random import randint
# Define the screen dimensions

X_INDEX = 0
Y_INDEX = 1
VELOCITY_VECTOR_SIZE = 6
WIDTH = 800
HEIGHT = 600
LENGTH = 20
BREADTH = 5
ACCPARAMS = (-0.01, 0.01, 0.0001)
XVECLPARAMS = (-5, 5, 0.01)
YVECLPARAMS = (-5, 5, 0.01)
XPOSPARAMS = ((WIDTH/2)-1, WIDTH/2, 1)
YPOSPARAMS = (HEIGHT-1, HEIGHT, 1)
FOODFINDERS = 20
LIFESPAN = 150
GENERATION = 20
CROSSOVERRATE = 0.05
MUTATIONRATE = 0.01
FITNESSBONUS = 10
DELAY = 30
FOODLEN = 20
FOODWID = 20
FOODX = randint(FOODLEN, WIDTH - FOODLEN)
FOODY = randint(FOODLEN, HEIGHT/2 - FOODLEN)
MUSICFILE = "music/theme.mp3"
VOLUME = 0.05
# Define colors
WHITE = (255, 255, 255)
BLACK = (0, 0, 0)

foodfinders = []
objects = []
iteration = 0
averageAgeList = []
populationSizeList = []

def getRange(params):
    start, stop, step = params
    return np.arange(start, stop, step, dtype=float)