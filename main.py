import sys
from random import choice
from freeloader import Freeloader, pygame
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

def createFreeloaders(matingPool, screen):

    freeloaders = []
    for _ in range(FREELOADERS):
        xvelarr = []
        yvelarr = []
        
        if(len(matingPool.dnaPool) == 0):
            for _ in range(VELOCITY_VECTOR_SIZE):
                xvelarr.append(choice(getRange(xveclParams)))
                yvelarr.append(choice(getRange(yveclParams)))
        else:
            selectedDNA = matingPool.selection()
            for _ in range(VELOCITY_VECTOR_SIZE):
                xvelarr.append(choice(selectedDNA[X_INDEX]))
                yvelarr.append(choice(selectedDNA[Y_INDEX]))

        freeloaders.append(Freeloader(length, breadth, 
            choice(getRange(xposParams)) ,choice(getRange(yposParams)), 
            xvelarr, yvelarr, 
            choice(getRange(accParams)), choice(getRange(accParams)), screen))
    return freeloaders

def createFood(screen):
    return Food(FOODLEN, FOODWID, FOODX, FOODY, screen)

if __name__ == "__main__":
    # Initialize Pygame
    pygame.init()

    music_thread = threading.Thread(target=play_music)
    music_thread.daemon = True  # This will allow the program to exit even if the thread is running
    music_thread.start()

    # Create a Pygame window
    screen = pygame.display.set_mode((width, height))
    font = pygame.font.Font(None, 24)
    # Set the window title
    pygame.display.set_caption("Pygame Canvas")

    generation = 0
    maxFitness = 0
    avgFitness = 0
    matingPool = MatingPool()
    bestFitnessList = []
    avgFitnessList = []
    # Main game loop
    while generation < GENERATION:

        iteration = 0
        generation +=1
        freeloaders = createFreeloaders(matingPool, screen)
        food = createFood(screen)
        matingPool.reset()

        while iteration < LIFESPAN:
            iteration+=1
            # Clear the screen with a white background
            screen.fill(black)

            display_text(f"Iteration : {iteration}/{LIFESPAN}", 10, 10, white, font, screen)
            display_text(f"Generation: {generation}/{GENERATION}", 10, 30, white, font, screen)
            display_text(f"Higest Fitness : {round(maxFitness*100,2)} %", 10, 50, white, font, screen)
            display_text(f"Average Fitness : {round(avgFitness*100,2)} %", 10, 70, white, font, screen)
            
            bestFitnessList.append(maxFitness)
            avgFitnessList.append(avgFitness)

            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    running = False

            for i, freeloader in enumerate(freeloaders):
                # Draw on the canvas (for example, a red rectangle)
                try:
                    freeloader.draw()
                    food.draw()
                except:
                    print(f"Exception freeloader: {(freeloader.red, freeloader.green, freeloader.blue)}")
                    print(f"Exception food : {(food.color)}")

                freeloader.move()
          
            pygame.time.delay(delay)
            # Update the display
            pygame.display.update()
        '''
            for every freeloader, calculate fitness, which is their distance
            from food at the last iteration, and find the max fitness to normalize it
        '''
        # find raw fitness as an inverse relation to distance from food
        for freeloader in freeloaders:
            freeloader.calculateFitness((FOODX, FOODY))
            # print(f"Fitness : {freeloader.fitness}")

        # find max fitness for this generation and compare with the all time maxFitness
        maxFitnessFreeloader = max(freeloaders, key=(lambda freeloader : freeloader.fitness))
        maxFitness = max(maxFitnessFreeloader.fitness, maxFitness)

        avgFitness = sum(freeloader.fitness for freeloader in freeloaders)/len(freeloaders)

        # normalize fitness
        for freeloader in freeloaders:
            freeloader.fitness = freeloader.fitness / maxFitness
            matingPool.addFitness((freeloader.xvel, freeloader.yvel), freeloader.fitness)

        print(f'''Generation: {generation}/{GENERATION}\tIteration : {iteration}/{LIFESPAN}\tBest Fitness : {maxFitness}\tAverage Fitness : {avgFitness}''')

    plotChart(bestFitnessList, "Generation", "Fitness", "Fitness Chart", "green", (1,1,1))
    plotChart(avgFitnessList, "Generation", "Fitness", "Fitness Chart", "blue", (1,1,1))
    viewChart()

    # Quit Pygame
    pygame.quit()
    sys.exit()
