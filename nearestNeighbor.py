import time
execStartTime = time.time() * 1000

import sys
from utils import Utils
import numpy as np
import os

class NearestNeighbor():
    def __init__(self, file):
        self.file = file
        self.instance = Utils(self.file)
        self.size = self.instance.data['size']
        self.pointsDistances = self.instance.getPointsDistances()
        self.readTime = self.instance.readTime
  
    def showExecResults(self, distance, bestTour):
        print("\n")
        print("Tour Distance: ", distance)
        print("Points in Tour: ", len(bestTour))
        print("Best Tour by nn is: ", bestTour)
        print("\n")
        print("Time to read instance (milisec): ", round(self.readTime))
        print("Time to run instances (milisec): ", round((time.time() * 1000) - execStartTime))
        print("Total Time (milisec): ", round(self.readTime + (time.time() * 1000 - execStartTime)))

    def getStartPoints(self):
        return np.random.choice(self.size, 15, replace=False)

    def getDistances(self):
        distances = self.pointsDistances.copy()
        for i in range(self.size):
            distances[i][i] = np.inf
        return distances

    def getBestTourResult(self, tours, distancesByTour):
        minDistanceIndex = np.argmin(distancesByTour)
        self.showExecResults(distancesByTour[minDistanceIndex], tours[minDistanceIndex])

    def showToursData(self, executionTimeByTour, distancesByTour):
        print("\n")
        print('Algorithm: Nearest Neighbor')
        print('File name: ', self.file)
        print("Mean distances from tours: ", sum(distancesByTour) / len(distancesByTour))
        print("Mean Time (milisec): ", sum(executionTimeByTour) / len(executionTimeByTour))

    def getDistanceFromTour(self, tour):
        distance = 0
        for i, t in enumerate(tour):
            try:
                distance+=self.pointsDistances[t][tour[i+1]]
            except IndexError:
                distance+=self.pointsDistances[t][tour[0]]
        return distance

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
        executionTimeByTour = []
        startPoints = self.getStartPoints()
        for point in startPoints:
            execStartTourTime = time.time() * 1000
            tour = self.nearestNeighborAlgorithm(point)
            distance = self.getDistanceFromTour(tour)
            tours.append(tour)
            distancesByTour.append(distance)
            executionTimeByTour.append(time.time() * 1000 - execStartTourTime)
        self.getBestTourResult(tours, distancesByTour) 
        self.showToursData(executionTimeByTour, distancesByTour) 

if len(sys.argv)<2:
    print("need input file")
    sys.exit(1)

if sys.argv[1] == 'all':
  path = "data"
  directoryList = os.listdir(path)
  
  for file in directoryList:
      t = NearestNeighbor(file)
      t.run()	
else:
  t = NearestNeighbor(sys.argv[1])
  t.run()	          
