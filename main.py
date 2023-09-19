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
    matingPool = MatingPool()
    bestFitnessList = []
    avgFitnessList = []
    initialDistance = sqrt((WIDTH/2 - FOODX)**2 + (HEIGHT - FOODY)**2)
    minimumDistance = 1000
    
    # Main game loop
    while generation < GENERATION:

        iteration = 0
        generation +=1
        bestFitness = 0
        avgFitness = 0
        foodfinders = Foodfinder.createFoodfinders(matingPool, screen)
        food = Food.createFood(screen)
        obstacle = Obstacle.createObstacle(screen)
        matingPool.reset()

        while iteration < LIFESPAN:
            iteration+=1
            # Clear the screen with a white background
            screen.fill(BLACK)

            display_text(f"Iteration : {iteration}/{LIFESPAN}", 10, 10, WHITE, font, screen)
            display_text(f"Generation: {generation}/{GENERATION}", 10, 30, WHITE, font, screen)
            display_text(f"Higest Fitness : {round(bestFitness*100,2)} %", 10, 50, WHITE, font, screen)
            display_text(f"Average Fitness : {round(avgFitness*100,2)} %", 10, 70, WHITE, font, screen)
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
                    foodfinder.checkCollision(obstacle)
                except:
                    print(f"Exception foodfinder: {(foodfinder.red, foodfinder.green, foodfinder.blue)}")
                    print(f"Exception food : {(food.color)}")

                if not foodfinder.completed and not foodfinder.crashed:
                    foodfinder.move()
            '''
                for every foodfinder, calculate fitness, which is their distance
                from food at the last iteration, and find the max fitness to normalize it
            '''
            # find raw fitness as an inverse relation to distance from food
            for foodfinder in foodfinders:
                minimumDistance = min(foodfinder.calculateFitness(food, initialDistance), minimumDistance)

            # find max fitness for this generation and compare with the all time bestFitness
            maxFitnessFoodfinder = max(foodfinders, key=(lambda foodfinder : foodfinder.fitness))
            bestFitness = max(maxFitnessFoodfinder.fitness, bestFitness)

            avgFitness = sum(foodfinder.fitness for foodfinder in foodfinders)/len(foodfinders)

            # normalize fitness
            for foodfinder in foodfinders:
                foodfinder.fitness = (foodfinder.fitness / maxBestFitness) if maxBestFitness != 0 else (foodfinder.fitness / bestFitness)
                matingPool.addFitness((foodfinder.xvel, foodfinder.yvel), foodfinder.fitness)

            refresh()
            #end of iteration

        maxBestFitness = max(maxBestFitness, bestFitness)
        if maxAvgFitness < avgFitness:
            maxAvgFitness = avgFitness
            maxAvgFitnessGen = generation

        bestFitnessList.append(bestFitness)
        avgFitnessList.append(avgFitness)
        sleep(PAUSE)
        #end of generation

    plotChart(bestFitnessList, "Generation", "Fitness", "Fitness Chart", "green", "best fitness", (1,1,1))
    plotChart(avgFitnessList, "Generation", "Fitness", "Fitness Chart", "blue", "average fitness", (1,1,1))
    viewChart()

    # Quit Pygame
    pygame.quit()
    sys.exit()
