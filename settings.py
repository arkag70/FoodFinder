import numpy as np
# Define the screen dimensions

def getRange(params):
    start, stop, step = params
    return np.arange(start, stop, step, dtype=float)

width = 800
height = 600
length = 20
breadth = 5

accParams = (-0.01, 0.01, 0.0001)
veclParams = (-0.02, 1, 0.01)
xposParams = (width/3, 2*width/3, 10)
yposParams = (3*height/4, height, 10)
FREELOADERS = 20
LIFESPAN = 100
GENERATION = 10
MIN_POPULATION_SIZE = 0.05 * FREELOADERS
damp = 0.8
freeloaders = []
objects = []
iteration = 0
delay = 30
averageAgeList = []
populationSizeList = []

# Define colors
white = (255, 255, 255)
black = (0, 0, 0)

FOODX = width/2
FOODY = height/10
FOODLEN = 20
FOODWID = 20
