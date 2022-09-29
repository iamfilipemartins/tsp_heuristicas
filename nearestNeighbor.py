
import time
start_time = time.time() * 1000

import sys
from utils import Utils
import numpy as np
import os

class NearestNeighbor():
    def __init__(self, file):
        self.file = file
        self.instance = Utils(self.file)
        self.size = self.instance.size
        self.pointsDistances = self.instance.getPointsDistances()
        self.readTime = self.instance.readTime

    def getDistances(self):
        distances = self.pointsDistances.copy()
        for i in range(self.size):
            distances[i][i] = np.inf
        return distances

    def nearestNeighborAlgorithm(self, startPoint):
        distances = self.getDistances()
        tour = [startPoint]
        for _ in range(self.size-1):
            minDistanceIndex = np.argmin(distances[tour[-1]])
            for t in tour:
                distances[minDistanceIndex][t] = np.inf
                distances[t][minDistanceIndex] = np.inf
            tour.append(minDistanceIndex)
        return np.array(tour)
    
    def run(self):
        distancesByTour = []
        tours = []
        self.showExecInfo()
        startPoints = self.getStartPoints()
        for point in startPoints:
            tour = self.nearestNeighborAlgorithm(point)
            dist = self.getDistanceFromTour(tour)
            tours.append(tour)
            distancesByTour.append(dist)
        self.getBestTourResult(tours, distancesByTour) 

    def getBestTourResult(self, tours, distancesByTour):
        minDistanceIndex = np.argmin(distancesByTour)
        self.showExecResults(distancesByTour[minDistanceIndex], tours[minDistanceIndex])

    def getDistanceFromTour(self, tour):
        dist = 0
        for i,t in enumerate(tour):
            try:
                dist+=self.pointsDistances[t][tour[i+1]]
            except IndexError:
                dist+=self.pointsDistances[t][tour[0]]
        return dist

    def showExecInfo(self):
        print("\n \nInstance name: ", self.instance.name)
        print("Dimension: ", self.size)
        print("Distance Type: ", self.instance.edgeWeightType)
        print("\nRunning nn over 10 random tour")

    def showExecResults(self,distance, bestTour):
        print("\nTour Distance: ", distance)
        print("Points in Tour: ", len(bestTour))
        print("Best Tour by nn is: \n", bestTour)
        print("\nTime to read instance (milisec): ", round(self.readTime))
        print("Time to run instances(milisec): ", round((time.time() * 1000) - start_time))
        print("Total Time (milisec): ", round(self.readTime + (time.time() * 1000 - start_time)))
   
    def getStartPoints(self):
        #np.random.seed(1)
        a = round(self.size*0.1)
        min = 10
        max = 1000
        if a > max:
            list = np.random.choice(self.size, max, replace=False)
        elif a <= min:
            list = np.random.choice(self.size, min, replace=False)
        else:
            list = np.random.choice(self.size, a, replace=False)
        return list


if len(sys.argv)<2:
    print("need input file")
    sys.exit(1)


if sys.argv[1] == 'all':
  # Get the list of all files and directories
  path = "data"
  dir_list = os.listdir(path)
  
  for file in dir_list:
      if ".tsp" in file:
        t = NearestNeighbor(file)
        t.run()	
else:
  t = NearestNeighbor(sys.argv[1])
  t.run()	          
