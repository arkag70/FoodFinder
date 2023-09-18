import numpy as np
# Define the screen dimensions

def getRange(params):
    start, stop, step = params
    return np.arange(start, stop, step, dtype=float)
X_INDEX = 0
Y_INDEX = 1
VELOCITY_VECTOR_SIZE = 6
width = 800
height = 600
length = 20
breadth = 5

accParams = (-0.01, 0.01, 0.0001)
xveclParams = (-1, 1, 0.01)
yveclParams = (-1, 1, 0.01)
xposParams = ((width/2)-1, width/2, 1)
yposParams = (height-1, height, 1)
FREELOADERS = 20
LIFESPAN = 100
GENERATION = 50
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

MUSICFILE = "music/theme.mp3"
VOLUME = 0.05
