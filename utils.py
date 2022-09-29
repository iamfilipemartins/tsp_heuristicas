

import time
execStartTime = time.time() * 1000

import sys
import numpy as np
from math import sqrt

class Utils():
    def __init__(self, filename):
        self.name = filename[:-4]
        self.readTime = 0
        self.data = self.readDataFromTspFile()

    def readDataFromTspFile(self):
        try:
          cities = []
          edgeWeightType = "None"
          size = 0
          with open(f'data/{self.name}.tsp') as data:
            for line in data.readlines():
                elements = line.split(' ')
                try:
                    cities.append([float(elements[0]), float(elements[1]), float(elements[2])])
                except ValueError:
                    if elements[0] == "DIMENSION:":
                        size = int(elements[1])
                    elif elements[0] == "DIMENSION":
                        size = int(elements[2])
                    elif elements[0] == "EDGE_WEIGHT_TYPE:":
                        edgeWeightType = elements[1].strip()
                    elif elements[0] == "EDGE_WEIGHT_TYPE":
                        edgeWeightType = elements[2].strip()
          return dict(cities=np.array(cities), edgeWeightType=edgeWeightType, size=size)
        except IOError:
            print("Input file not found")
            sys.exit(1)

    def getPointsDistances(self):
        pointsDistances = None
        if self.data['edgeWeightType'] == "ATT":
            pointsDistances = self.getPseudoEuclidianDistances()
        elif self.data['edgeWeightType'] == "EUC_2D":
            pointsDistances = self.getEuclidianDistances()
        self.readTime = time.time() * 1000 - execStartTime
        return pointsDistances

    def getEuclidianDistances(self):
        cost_matrix = []
        for i in range(self.data['size']):
            row = []
            for j in range(self.data['size']):
                row.append(np.round(sqrt((self.data['cities'][i][1] - self.data['cities'][j][1]) ** 2 + (self.data['cities'][i][2] - self.data['cities'][j][2]) ** 2)))
            cost_matrix.append(row)
        return np.asarray(cost_matrix, dtype=np.float32)
     
    def getPseudoEuclidianDistances(self):
        cost_matrix = []
        for i in range(self.data['size']):
            row = []
            for j in range(self.data['size']):
                row.append(np.round(sqrt(((self.data['cities'][i][1] - self.data['cities'][j][1]) ** 2 + (self.data['cities'][i][2] - self.data['cities'][j][2]) ** 2) / 10)))
            cost_matrix.append(row)
        return np.asarray(cost_matrix, dtype=np.float32)