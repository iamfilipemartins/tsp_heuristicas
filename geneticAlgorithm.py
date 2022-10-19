
import time
execStartTime = time.time() * 1000

import random, operator, pandas as pd
import sys
from utils import Utils
import numpy as np
import os

from utils import Utils

class City:
    def __init__(self, label, distances):
        self.label = label
        self.distances = distances
    
    def distance(self, city):
        distance = self.distances[(city.label)-1]
        return distance
    
    def __repr__(self):
        return "[" +str(self.label) + "]"

class Fitness:
    def __init__(self, route):
        self.route = route
        self.distance = 0
        self.fitness= 0.0
    
    def routeDistance(self):
        if self.distance ==0:
            pathDistance = 0
            for i in range(0, len(self.route)):
                fromCity = self.route[i]
                toCity = None
                if i + 1 < len(self.route):
                    toCity = self.route[i + 1]
                else:
                    toCity = self.route[0]
                pathDistance += fromCity.distance(toCity)
            self.distance = pathDistance
        return self.distance
    
    def routeFitness(self):
        if self.fitness == 0:
            self.fitness = 1 / float(self.routeDistance())
        return self.fitness

class GeneticAlgorithm():
    def __init__(self, file):
        self.file = file
        self.instance = Utils(self.file)
        self.size = self.instance.data['size']
        self.pointsDistances = self.instance.getPointsDistances()
        self.readTime = self.instance.readTime

    def createRoute(self, cityList):
        route = random.sample(cityList, len(cityList))
        return route

    def initialPopulation(self, popSize, cityList):
        population = []

        for _ in range(0, popSize):
            population.append(self.createRoute(cityList))
        return population

    def rankRoutes(self, population):
        fitnessResults = {}
        for i in range(0,len(population)):
            fitnessResults[i] = Fitness(population[i]).routeFitness()
        return sorted(fitnessResults.items(), key = operator.itemgetter(1), reverse = True)

    def selection(self, popRanked, eliteSize):
        selectionResults = []
        df = pd.DataFrame(np.array(popRanked), columns=["Index","Fitness"])
        df['cumSum'] = df.Fitness.cumsum()
        df['percentage'] = 100 * df.cumSum / df.Fitness.sum()
        
        for i in range(0, eliteSize):
            selectionResults.append(popRanked[i][0])
        for i in range(0, len(popRanked) - eliteSize):
            pick = 100*random.random()
            for i in range(0, len(popRanked)):
                if pick <= df.iat[i,3]:
                    selectionResults.append(popRanked[i][0])
                    break
        return selectionResults

    def matchingPool(self, population, selectionResults):
        matching = []
        for i in range(0, len(selectionResults)):
            index = selectionResults[i]
            matching.append(population[index])
        return matching

    def breed(self, parent1, parent2):
        child = []
        childP1 = []
        childP2 = []
        
        geneA = int(random.random() * len(parent1))
        geneB = int(random.random() * len(parent1))
        
        startGene = min(geneA, geneB)
        endGene = max(geneA, geneB)

        for i in range(startGene, endGene):
            childP1.append(parent1[i])
            
        childP2 = [item for item in parent2 if item not in childP1]

        j=0

        for i in range(0, len(parent1)):
            if (i < startGene):
                child.append(childP2[i])
                j = j + 1
            elif (i < endGene):
                child.append(childP1[i-startGene])
            else:
                child.append(childP2[j])
                j = j + 1
        return child

    def breedPopulation(self, matching, eliteSize):
        children = []
        length = len(matching) - eliteSize
        pool = random.sample(matching, len(matching))

        for i in range(0,eliteSize):
            children.append(matching[i])
        
        for i in range(0, length):
            child = self.breed(pool[i], pool[len(matching)-i-1])
            children.append(child)
        return children

    def mutate(self, individual, mutationRate):
        for swapped in range(len(individual)):
            if(random.random() < mutationRate):
                swapWith = int(random.random() * len(individual))
                
                city1 = individual[swapped]
                city2 = individual[swapWith]
                
                individual[swapped] = city2
                individual[swapWith] = city1
        return individual

    def mutatePopulation(self, population, mutationRate):
        mutatedPop = []
        
        for ind in range(0, len(population)):
            mutatedInd = self.mutate(population[ind], mutationRate)
            mutatedPop.append(mutatedInd)
        return mutatedPop

    def nextGeneration(self, currentGen, eliteSize, mutationRate):
        popRanked = self.rankRoutes(currentGen)
        selectionResults = self.selection(popRanked, eliteSize)
        matching = self.matchingPool(currentGen, selectionResults)
        children = self.breedPopulation(matching, eliteSize)
        nextGeneration = self.mutatePopulation(children, mutationRate)
        return nextGeneration

    def geneticAlgorithmPlot(self, population, popSize, eliteSize, mutationRate, generations):
        pop = self.initialPopulation(popSize, population)
        progress = []
        progressDistance = []
        progress.append(1 / self.rankRoutes(pop)[0][1])
        minDistance = 0
        bestTour = []
        c = 0
        for i in range(0, generations):
            pop = self.nextGeneration(pop, eliteSize, mutationRate)
            dist = 1 / self.rankRoutes(pop)[0][1]
            if(i == 0):
                minDistance = 1 / self.rankRoutes(pop)[0][1]
                bestTourIndex = self.rankRoutes(pop)[0][0]
                bestTour = pop[bestTourIndex]
            else:
                if(minDistance > dist):
                    minDistance = 1 / self.rankRoutes(pop)[0][1]
                    bestTourIndex = self.rankRoutes(pop)[0][0]
                    bestTour = pop[bestTourIndex]
                    c = 0
            c = c+1
            progress.append(dist)
            progressDistance.append(minDistance)
            if (c > generations):
                break

        self.showExecResults(minDistance, bestTour)

    def showExecResults(self, distance, bestTour):
        print("\n")
        print("Tour Distance: ", distance)
        print("Points in Tour: ", len(bestTour))
        print("Best Tour by ga is: ", bestTour)
        print("\n")
        print("Time to read instance (milisec): ", round(self.readTime))
        print("Time to run instances (milisec): ", round((time.time() * 1000) - execStartTime))
        print("Total Time (milisec): ", round(self.readTime + (time.time() * 1000 - execStartTime)))

    def run(self):
        size = self.size
        distances = self.pointsDistances
        cities = []

        for _ in range(15):
          for i in range(size):
              cities.append(City(label = i+1, distances = distances[i]))

          self.geneticAlgorithmPlot(population=cities, popSize=500, eliteSize=100, mutationRate=0.01, generations=20)

if len(sys.argv) < 2:
  print("need input file")
  sys.exit(1)

if sys.argv[1] == 'all':
  path = "data"
  directoryList = os.listdir(path)
  
  for file in directoryList:
    t = GeneticAlgorithm(file)
    t.run()	
else:
  t = GeneticAlgorithm(sys.argv[1])
  t.run()	          