import time
execStartTime = time.time() * 1000

import sys
from utils import Utils
import numpy as np
import os

class TwoOpt:
    def __init__(self, file):
        self.file = file
        self.instance = Utils(self.file)
        self.size = self.instance.data['size']
        self.pointsDistances = self.instance.getPointsDistances()
        self.readTime = self.instance.readTime
        self.algorithmTime = 0

    def showExecInfo(self):
        print("\n")
        print("Instance name:", self.instance.name)
        print("Dimension:", self.size)
        print("Distance Type: ", self.instance.data['edgeWeightType'])

    def showExecResults(self, distance, bestTour):
        print("\n")
        print("Tour Distance: ", distance)
        print("Best Tour by 2-opt is: ", bestTour)
        print("\n")
        print("Time to read instance (milisec): ", round(self.readTime))
        print("Time to run instances(milisec): ", round((time.time() * 1000) - execStartTime))
        print("Total Time (milisec): ", round(self.readTime + (time.time() * 1000 - execStartTime)))

    def getInitialRandomTour(self):
        items = np.arange(1,self.size+1)
        np.random.shuffle(items)
        return list(items)

    def swapOnTour(self, tour, x, y):
        newTour = tour[:x] + [*reversed(tour[x:y + 1])] + tour[y + 1:]
        return newTour

    def getDistanceFromTour(self, tour):
        distance = 0
        for index, value in enumerate(tour):
            if index + 1 == len(tour):
                distance += self.pointsDistances[value - 1][tour[0] - 1]
            else:
                distance += self.pointsDistances[value - 1][tour[index + 1] - 1]
        return distance

    def getBestTourResult(self, tours, distancesByTour):
        minDistanceIndex = np.argmin(distancesByTour)
        self.showExecResults(distancesByTour[minDistanceIndex], tours[minDistanceIndex])

    def TwoOptAlgorithm(self, initialTour):
        minimumChange = -1
        tour = initialTour
        while minimumChange < 0:
            minimumChange = 0
            for i in range(self.size - 3):
                for j in range(i + 2, self.size - 1):
                    t1 = tour[i]
                    t2 = tour[i + 1]
                    t3 = tour[j]
                    t4 = tour[j + 1]

                    change = (self.pointsDistances[t1 - 1][t3 - 1] +
                              self.pointsDistances[t2 - 1][t4 - 1] -
                              self.pointsDistances[t1 - 1][t2 - 1] -
                              self.pointsDistances[t3 - 1][t4 - 1])
                    if change < minimumChange:
                        minimumChange = change
                        tour = self.swapOnTour(tour, i + 1, j)
        return tour

    def run(self):
        tours = []
        distancesByTour = []
        self.showExecInfo()
        for _ in range(5):
            initialTour = self.getInitialRandomTour()
            tour = self.TwoOptAlgorithm(initialTour)
            distance = self.getDistanceFromTour(tour)
            tours.append(tour)
            distancesByTour.append(distance)
        self.getBestTourResult(tours, distancesByTour)

if sys.argv[1] == 'all':
  path = "data"
  directoryList = os.listdir(path)
  
  for file in directoryList:
      t = TwoOpt(file)
      t.run()	
else:
  t = TwoOpt(sys.argv[1])
  t.run()	          
