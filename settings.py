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
XPOSPARAMS = WIDTH/2
YPOSPARAMS = HEIGHT
FOODFINDERS = 100
LIFESPAN = 75
GENERATION = 30
CROSSOVERRATE = 0.01
MUTATIONRATE = 0.005
FITNESSBONUS = 10
DELAY = 30
FOODLEN = 20
FOODWID = 20
FOODX = randint(FOODLEN, WIDTH - FOODLEN)
FOODY = randint(FOODLEN, HEIGHT/2 - FOODLEN)
ALPHA = 11
OBS_X = 100
OBS_Y = 400
OBS_W = 600
OBS_H = 20
MUSICFILE = "music/theme.mp3"
VOLUME = 0.05
# Define colors
WHITE = (255, 255, 255)
BLACK = (0, 0, 0)
PAUSE = 0.3

foodfinders = []
objects = []
iteration = 0
averageAgeList = []
populationSizeList = []

def getRange(params):
    start, stop, step = params
    return np.arange(start, stop, step, dtype=float)