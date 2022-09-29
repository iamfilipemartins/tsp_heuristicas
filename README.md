# TSP-heuristics
Implementing various heuristics for Travelling Salesman Problem (TSP). Nearest Neighour heuristic (nn.py), 2-opt (2-opt.py) genetic algorithm(ga_tsp.py, ga_2-opt_tsp.py), Simulated Annealing (runSA.py, runSA2opt.py)).

## Description 
	data: this folder has all TSPLIB instances (e.g ch130.tsp, a280.tsp) 
	utils.py: this python file is used for reading the TSP instances and aux functions.  
	All other python files are implemetation of algorithm

Steps for running algorithms
### Terminal commands
	$ python 'algorithm.py' 'filename'  

* 'algorithm.py': nearestNeighbor.py
* 'filename' pick any file from data folder eg. kroB100.tsp or att48.tsp

### Example runs			
	$ python nearestNeighbor.py kroB100.tsp
	$ python nearestNeighbor.py att48.tsp
