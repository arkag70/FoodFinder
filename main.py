import sys
from random import choice
from foodfinder import Foodfinder, pygame, sqrt
import threading
from settings import *
from food import Food
from matingpool import MatingPool
from chart import plotChart, viewChart

# Function to display text on the screen
def display_text(text, x, y, color, font, screen):
    text_surface = font.render(text, True, color)
    screen.blit(text_surface, (x, y))

def play_music():
    pygame.mixer.init()
    pygame.mixer.music.load(MUSICFILE)  # Replace with your music file
    pygame.mixer.music.set_volume(VOLUME)  # Adjust the volume as needed
    pygame.mixer.music.play(-1)  # -1 indicates infinite loop

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
            choice(getRange(XPOSPARAMS)) ,choice(getRange(YPOSPARAMS)), 
            xvelarr, yvelarr, 
            choice(getRange(ACCPARAMS)), choice(getRange(ACCPARAMS)), screen))
    return foodfinders

def createFood(screen):
    return Food(FOODLEN, FOODWID, FOODX, FOODY, screen)

if __name__ == "__main__":
    # Initialize Pygame
    pygame.init()

    music_thread = threading.Thread(target=play_music)
    music_thread.daemon = True  # This will allow the program to exit even if the thread is running
    music_thread.start()

    # Create a Pygame window
    screen = pygame.display.set_mode((WIDTH, HEIGHT))
    font = pygame.font.Font(None, 24)
    # Set the window title
    pygame.display.set_caption("Pygame Canvas")

    generation = 0
    maxFitness = 0
    avgFitness = 0
    matingPool = MatingPool()
    bestFitnessList = []
    avgFitnessList = []
    initialDistance = sqrt((WIDTH/2 - FOODX)**2 + (HEIGHT - FOODY)**2)
    # Main game loop
    minimumDistance = 2*HEIGHT + 2*WIDTH
    while generation < GENERATION:

        iteration = 0
        generation +=1
        foodfinders = createFoodfinders(matingPool, screen)
        food = createFood(screen)
        matingPool.reset()
        bestFitnessList.append(maxFitness)
        avgFitnessList.append(avgFitness)

        while iteration < LIFESPAN:
            iteration+=1
            # Clear the screen with a white background
            screen.fill(BLACK)

            display_text(f"Iteration : {iteration}/{LIFESPAN}", 10, 10, WHITE, font, screen)
            display_text(f"Generation: {generation}/{GENERATION}", 10, 30, WHITE, font, screen)
            display_text(f"Higest Fitness : {round(maxFitness*100,2)} %", 10, 50, WHITE, font, screen)
            display_text(f"Average Fitness : {round(avgFitness*100,2)} %", 10, 70, WHITE, font, screen)
            if iteration > 1:
                display_text(f"Closest foodfinder: {int(minimumDistance)} px", 10, 90, WHITE, font, screen)

            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    running = False

            for i, foodfinder in enumerate(foodfinders):
                # Draw on the canvas (for example, a red rectangle)
                try:
                    foodfinder.draw()
                    food.draw()
                except:
                    print(f"Exception foodfinder: {(foodfinder.red, foodfinder.green, foodfinder.blue)}")
                    print(f"Exception food : {(food.color)}")

                if not foodfinder.completed:
                    foodfinder.move()
            
            # find raw fitness as an inverse relation to distance from food
            for foodfinder in foodfinders:
                minimumDistance = min(foodfinder.calculateFitness(food, initialDistance), minimumDistance)
                
                # print(f"Fitness : {foodfinder.fitness}")

            # find max fitness for this generation and compare with the all time maxFitness
            maxFitnessFoodfinder = max(foodfinders, key=(lambda foodfinder : foodfinder.fitness))
            maxFitness = max(maxFitnessFoodfinder.fitness, maxFitness)

            avgFitness = sum(foodfinder.fitness for foodfinder in foodfinders)/len(foodfinders)

            # normalize fitness
            for foodfinder in foodfinders:
                foodfinder.fitness = foodfinder.fitness / maxFitness
                matingPool.addFitness((foodfinder.xvel, foodfinder.yvel), foodfinder.fitness)
          
            pygame.time.delay(DELAY)
            # Update the display
            pygame.display.update()
        '''
            for every foodfinder, calculate fitness, which is their distance
            from food at the last iteration, and find the max fitness to normalize it
        '''

    plotChart(bestFitnessList, "Generation", "Fitness", "Fitness Chart", "green", "best fitness", (1,1,1))
    plotChart(avgFitnessList, "Generation", "Fitness", "Fitness Chart", "blue", "average fitness", (1,1,1))
    viewChart()

    # Quit Pygame
    pygame.quit()
    sys.exit()
