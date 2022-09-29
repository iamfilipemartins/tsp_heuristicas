# TSP-heuristics
Implementing heuristics for Travelling Salesman Problem (TSP). Nearest Neighour heuristic (nearestNeighbor.py).

## Description 
	data: this folder has all TSPLIB instances (e.g kroB100.tsp, att48.tsp) 
	utils.py: this python file is used for reading the TSP instances and aux functions.  
	All other python files are implemetation of algorithm

Steps for running algorithms
### Terminal commands
	$ python 'algorithm.py' 'filename'  

* 'algorithm.py': choose the algorithm to run eg. nearestNeighbor.py
* 'filename': choose any file from data folder eg. 'kroB100.tsp' or 'att48.tsp' or 'all' to run all data folder files

### Example runs			
	$ python nearestNeighbor.py kroB100.tsp
	$ python nearestNeighbor.py att48.tsp
