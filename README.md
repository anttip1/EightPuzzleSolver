# EightPuzzleSolver

## Introduction

This is a 8-puzzle solver that utilizes A* algorithm to solve the problem. 
This solver also includes implementations of WA* and Greedy Best First algorithms. 

This code requires the following nonstandard libraries: 

* numpy 
  * pip3 install numpy (If you don’t have it installed)
* distance
  * pip3 install distance (If you don’t have it installed)

The program consists of two files: eightpuzzlesolver.py and eightpuzzlesolver_test.py.
You can run eightpuzzlesolver.py by itself, it’ll print out results in one of the following forms:
  ```python 
  True, [iteration, running_time, len(self.visited), len(self.unvisited), len(backtrace)
  False, [iteration, running_time]
  ```
 
Where True/False denotes whether the run terminated in the given iteration limits. 

You can also uncomment the print statements from the code and get more detailed description.
Additionally, if you give print_trace=True to the EightPuzzleSolver class as a parameter, the solver will print the steps to reach the goal form the initial state. 

eightpuzzlesolver_test.py will generate csv file from the tests that it runs. It’ll run every single algorithm: a*, wa* (weights: 5, 10, 15, 20) and greedy best first with every possible tile amounts. For every tile variation, the tester runs 10 random solvers with the given parameters and calculates their average statistics. 

The tester runs 6 parallel processes to decrease the execution time. 

The code folder also includes an excel file of the tester output for your convenience. 


## Results 

The a_star_stats_excel.xlsx contains the other WA* runs.

WA* with weight = 10 results in the best steps to running time combo. A* is the best considering the shortness of the total steps. Greedy best first on the other hand results in poor performance when the number of tiles is larger, given the scarcity of successful runs, i.e. the runs that terminated in the given iteration limits. 
 
It seems that greedy best first tends to open a lot of nodes, but cannot differentiate between better and worse ones because it does not care about the spent moves. Occasionally it gets lucky and finds the solution quickly. 

