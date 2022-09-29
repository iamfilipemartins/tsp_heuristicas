

import time
start_time = time.time() * 1000

import sys
import numpy as np
from math import sqrt

class Utils():
    def __init__(self, filename):
        self.name = filename[:-4]
        self.size = self.getSize()
        self.edgeWeightType = self.getEdgeWeightType()
        self.readTime = 0

    def getEdgeWeightType(self):
        try:
            EdgeType = "None"
            with open(f'data/{self.name}.tsp') as data:
              for line in data.readlines():
                  elements = line.split(' ')
                  if elements[0] == "EDGE_WEIGHT_TYPE:":
                      EdgeType = elements[1].strip()
                      break
                  elif elements[0] == "EDGE_WEIGHT_TYPE":
                      EdgeType = elements[2].strip()
                      break
            return EdgeType
        except IOError:
            print("Input file not found")
            sys.exit(1)

    def getSize(self):
        try:
            size = 0
            with open(f'data/{self.name}.tsp') as data:
                for line in data.readlines():
                    elements = line.split(' ')
                    if elements[0] == "DIMENSION:":
                        size = elements[1]
                        break
                    elif elements[0] == "DIMENSION":
                        size = elements[2]
                        break
            return int(size)
        except IOError:
            print("Input file not found")
            sys.exit(1)

    def readDataFromTspFile(self):
        try:
          cities = []
          with open(f'data/{self.name}.tsp') as data:
            for line in data.readlines():
                try:
                    elements = line.split(' ')
                    cities.append([float(elements[0]), float(elements[1]), float(elements[2])])
                except ValueError:
                    continue
          return np.array(cities)
        except IOError:
            print("Input file not found")
            sys.exit(1)

    def getPointsDistances(self):
        DistanceMat = None
        if self.edgeWeightType == "ATT":
            DistanceMat = self.getPseudoEuclidianDistances()
        elif self.edgeWeightType == "EUC_2D":
            DistanceMat = self.getEuclidianDistances()
        self.readTime = time.time() * 1000 - start_time
        return DistanceMat

    def getEuclidianDistances(self):
        cities = self.readDataFromTspFile()
        cost_matrix = []
        for i in range(self.size):
            row = []
            for j in range(self.size):
                row.append(np.round(sqrt((cities[i][1] - cities[j][1]) ** 2 + (cities[i][2] - cities[j][2]) ** 2)))
            cost_matrix.append(row)
        return np.asarray(cost_matrix, dtype=np.float32)
     
    def getPseudoEuclidianDistances(self):
        cities = self.readDataFromTspFile()
        cost_matrix = []
        for i in range(self.size):
            row = []
            for j in range(self.size):
                row.append(np.round(sqrt(((cities[i][1] - cities[j][1]) ** 2 + (cities[i][2] - cities[j][2]) ** 2) / 10)))
            cost_matrix.append(row)
        return np.asarray(cost_matrix, dtype=np.float32)