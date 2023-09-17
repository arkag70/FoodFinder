import sys
from random import choice
from freeloader import Freeloader, pygame
import threading
from settings import *
from food import Food
from matingpool import MatingPool

def play_music():
    pygame.mixer.init()
    pygame.mixer.music.load("music/theme.mp3")  # Replace with your music file
    pygame.mixer.music.set_volume(0.05)  # Adjust the volume as needed
    pygame.mixer.music.play(-1)  # -1 indicates infinite loop

def createFreeloaders():
    freeloaders = []
    for _ in range(FREELOADERS):
        xvelarr = []
        yvelarr = []
        for _ in range(6):
            xvelarr.append(choice(getRange(veclParams)))
            yvelarr.append(choice(getRange(veclParams)))

        freeloaders.append(Freeloader(length, breadth, 
            choice(getRange(xposParams)) ,choice(getRange(yposParams)), 
            xvelarr, yvelarr, 
            choice(getRange(accParams)), choice(getRange(accParams))))
    return freeloaders

def createFood():
    return Food(FOODLEN, FOODWID, FOODX, FOODY)

if __name__ == "__main__":
    # Initialize Pygame
    pygame.init()

    music_thread = threading.Thread(target=play_music)
    music_thread.daemon = True  # This will allow the program to exit even if the thread is running
    music_thread.start()

    # Create a Pygame window
    screen = pygame.display.set_mode((width, height))

    # Set the window title
    pygame.display.set_caption("Pygame Canvas")

    generation = 0
    matingPool = MatingPool()
    # Main game loop
    while generation < GENERATION:

        iteration = 0
        generation +=1
        freeloaders = createFreeloaders()
        food = createFood()
        matingPool.reset()

        while iteration < LIFESPAN:
            iteration+=1
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    running = False

            # Clear the screen with a white background
            screen.fill(black)

            print(f'''Generation: {generation}/{GENERATION}\tIteration : {iteration}/{LIFESPAN}''')

            for i, freeloader in enumerate(freeloaders):
                # Draw on the canvas (for example, a red rectangle)
                try:
                    freeloader.draw(screen)
                    food.draw(screen)
                except:
                    print(f"Exception freeloader: {(freeloader.red, freeloader.green, freeloader.blue)}")
                    print(f"Exception food : {(food.color)}")

                freeloader.move()
          
            pygame.time.delay(delay)
            # Update the display
            pygame.display.flip()
        '''
            for every freeloader, calculate fitness, which is their distance
            from food at the last iteration, and find the max fitness to normalize it
        '''
        # find raw fitness as an inverse relation to distance from food
        for freeloader in freeloaders:
            freeloader.calculateFitness((FOODX, FOODY))

        # find max fitness
        maxFitnessFreeloader = max(freeloaders, key=(lambda freeloader : freeloader.fitness))
        maxFitness = maxFitnessFreeloader.fitness

        # normalize fitness
        for freeloader in freeloaders:
            freeloader.fitness = freeloader.fitness / maxFitness
            matingPool.addFitness((freeloader.xvel, freeloader.yvel), freeloader.fitness)
        break

    # Quit Pygame
    pygame.quit()
    sys.exit()
