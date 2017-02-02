#!usr/bin/env python3

import eightpuzzlesolver as ep
from multiprocessing import Pool
import csv

def main():

    execution_runs = 10
    p = Pool(6)
    statistics = p.starmap(a_star_process, [(1, execution_runs, False), (5, execution_runs, False), (10, execution_runs, False), (15, execution_runs, False), (20, execution_runs, False), (1, execution_runs, True)])

    with open("a_star_stats.csv", "w") as csvfile:
        statwriter = csv.writer(csvfile)
        statwriter.writerow(["All averages are calculated from 10 runs"])
        statwriter.writerow([""])
        for line in statistics:
            test_name = line[0]
            test_data = line[1]
            statwriter.writerow([test_name])
            statwriter.writerow(["", "", "avg(iterations)", "avg(running time)", "avg(visited nodes)", "avg(unexplored nodes)", "avg(steps to solution)", "successful runs"])
            for index, set_line in enumerate(test_data):
                statwriter.writerow(["", str(index+1) + " tile(s)"] + set_line)

def a_star_process(weight, executions, greedy):
    statistics = []
    for tiles in range(1, 9):
        data = []
        for i in range(executions):
            puzzle = ep.EightPuzzle(5000, None, tiles)
            success, stats = puzzle.a_star(weight, greedy)
            if success:
                data.append(stats)
        sums = [0 for i in range(len(data[0]))]
        for column_index in range(5):
            for row in data:
                sums[column_index] += row[column_index]
        for index, column in enumerate(sums):
            sums[index] = column / len(data)
        sums.append(len(data))
        statistics.append(sums)
    if greedy:
        return "Greedy best first", statistics
    else:
        return "Weighed a star with weight = " + str(weight), statistics



if __name__ == "__main__":
    main()
