import time
execStartTime = time.time() * 1000

import sys
from utils import Utils
import numpy as np
import os
import csv

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

        with open('results/nearestNeighbor_' + self.instance.name + '.csv', 'a', encoding='UTF8', newline='') as f:
          writer = csv.writer(f)
          writer.writerow([distance, round(self.readTime), round((time.time() * 1000) - execStartTime), round(self.readTime + (time.time() * 1000 - execStartTime))]) 

    def getStartPoints(self):
        a = round(self.size*0.1)
        min = 10
        max = 1000
        if a > max:
            return np.random.choice(self.size, max, replace=False)
        elif a < min:
            return np.random.choice(self.size, min, replace=False)
        else:
            return np.random.choice(self.size, a, replace=False)

    def getDistances(self):
        distances = self.pointsDistances.copy()
        for i in range(self.size):
            distances[i][i] = np.inf
        return distances

    def getBestTourResult(self, tours, distancesByTour):
        minDistanceIndex = np.argmin(distancesByTour)
        self.showExecResults(distancesByTour[minDistanceIndex], tours[minDistanceIndex])

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
        startPoints = self.getStartPoints()
        for point in startPoints:
            tour = self.nearestNeighborAlgorithm(point)
            distance = self.getDistanceFromTour(tour)
            tours.append(tour)
            distancesByTour.append(distance)
        self.getBestTourResult(tours, distancesByTour) 

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
