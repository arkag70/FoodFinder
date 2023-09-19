import sys
import pygame
from math import sqrt
from foodfinder import Foodfinder
from food import Food
from obstacle import Obstacle
from utils import *
from time import sleep
from settings import *
from matingpool import MatingPool
from chart import plotChart, viewChart

if __name__ == "__main__":
    # Initialize Pygame
    pygame.init()
    play_music()
    screen, font = display_init()
    generation = 0
    maxBestFitness = 0
    maxAvgFitness = 0
    maxAvgFitnessGen = 0
    bestFitnessGen = 0
    avgFitnessGen = 0
    matingPool = MatingPool()
    bestFitnessList = []
    avgFitnessList = []
    initialDistance = sqrt((WIDTH/2 - FOODX)**2 + (HEIGHT - FOODY)**2)
    
    # Main game loop
    while generation < GENERATION:

        iteration = 0
        foodfinders = Foodfinder.createFoodfinders(matingPool, screen)
        food = Food.createFood(screen)
        obstacle = Obstacle.createObstacle(screen)
        matingPool.reset()

        while iteration < LIFESPAN:
            # Clear the screen with a white background
            screen.fill(BLACK)
            if generation <= 1:
                bestFitnessGen = 0
            display_text(f"Iteration : {iteration}/{LIFESPAN}", 10, 10, WHITE, font, screen)
            display_text(f"Generation: {generation}/{GENERATION}", 10, 30, WHITE, font, screen)
            display_text(f"Higest Fitness : {round(bestFitnessGen * 100,2)} %", 10, 50, WHITE, font, screen)
            display_text(f"Average Fitness : {round(avgFitnessGen*100,2)} %", 10, 70, WHITE, font, screen)
            display_text(f"Best Average Fitness : {round(maxAvgFitness*100,2)} %", 10, 90, WHITE, font, screen)
            display_text(f"Fittest Generation : {maxAvgFitnessGen}", 10, 110, WHITE, font, screen)

            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    running = False

            for i, foodfinder in enumerate(foodfinders):
                # Draw on the canvas (for example, a red rectangle)
                try:
                    foodfinder.draw()
                    food.draw()
                    obstacle.draw()
                except:
                    print(f"Exception foodfinder: {(foodfinder.red, foodfinder.green, foodfinder.blue)}")
                    print(f"Exception food : {(food.color)}")

                if not foodfinder.completed and not foodfinder.crashed:
                    foodfinder.calculateFitness(food)
                    foodfinder.move()
                    foodfinder.checkCollision(obstacle)
            
            refresh()
            iteration+=1
            #end of one generation
        generation +=1
        '''
            for every foodfinder, calculate fitness, which is their distance
            from food at the last iteration, and find the max fitness to normalize it
        '''
        # # find raw fitness as an negative linear relation to distance from food
        # for foodfinder in foodfinders:
        #     foodfinder.calculateFitness(food)

        # find the best fitness of this generation
        bestFitnessGen = max(foodfinders, key=(lambda foodfinder : foodfinder.fitness)).fitness

        # normalize fitness
        for foodfinder in foodfinders:
            foodfinder.fitness = (foodfinder.fitness / maxBestFitness) if maxBestFitness != 0 else (foodfinder.fitness / bestFitnessGen)
            matingPool.addFitness((foodfinder.xvel, foodfinder.yvel), foodfinder.fitness, generation)

        # average fitness of the generation post fitness normalization
        avgFitnessGen = sum(foodfinder.fitness for foodfinder in foodfinders)/len(foodfinders)

        # find the best normalized fitness of this generation
        bestFitnessGen = max(foodfinders, key=(lambda foodfinder : foodfinder.fitness)).fitness
        
        maxBestFitness = max(bestFitnessGen, maxBestFitness)
        if maxAvgFitness < avgFitnessGen:
            maxAvgFitness = avgFitnessGen
            maxAvgFitnessGen = generation

        bestFitnessList.append(bestFitnessGen)
        avgFitnessList.append(avgFitnessGen)
        sleep(PAUSE)
        #end of generation

    plotChart(bestFitnessList, "Generation", "Fitness", "Fitness Chart", "green", "best fitness", (1,1,1))
    plotChart(avgFitnessList, "Generation", "Fitness", "Fitness Chart", "blue", "average fitness", (1,1,1))
    viewChart()

    # Quit Pygame
    pygame.quit()
    sys.exit()
