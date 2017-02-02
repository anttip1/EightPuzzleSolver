#!usr/bin/env python3

import numpy as np
import distance
from copy import deepcopy
import time
import random



class Board(object):

    def __init__(self, state=None, parent=None, tiles=8):

        self.tiles = tiles
        state_list = [i for i in range(1, self.tiles + 1)]
        for i in range(9 - self.tiles): state_list.append(0)
        self.goal_state = tuple(state_list)

        if state is not None:
            self.state = state
        else:
            self.state = tuple(np.random.permutation(list(self.goal_state)))
            while not self.is_solvable():
                self.state = tuple(np.random.permutation(list(self.goal_state)))

        if parent is not None:
            self.parent = parent
            self.moves = parent.moves + 1
        else:
            self.parent = None
            self.moves = 0

        self.heuristic = self.manhattan_distance_heuristic()
        #self.heuristic = self.hamming_distance_heuristic()

    def __eq__(self, other):
        return self.state == other.state

    def __hash__(self):
        return hash(self.state)

    def hamming_distance_heuristic(self):
        return distance.hamming(self.goal_state, self.state)

    def manhattan_distance_heuristic(self):
        distance = 0
        for index, value in enumerate(self.state):
            if value != 0:
                current_row = int(index / 3)
                current_column = index % 3
                correct_row = int((value - 1) / 3)
                correct_column = (value - 1) % 3
                distance += abs(correct_row - current_row) + abs(correct_column - current_column)
        return distance

    def is_solvable(self):
        # If there are odd number of inversions the state is not solvable (if there are 8 tiles)
        inversions = 0
        state_list = [value for value in list(self.state) if value != 0]

        for index, value in enumerate(state_list):
            for value2 in state_list[index+1:]:
                if value > value2 :
                    inversions += 1
        return False if inversions % 2 != 0 else True

    def get_child_boards(self):

        def add_child_to_list(children_list, index, index_offset):
            # This is a helperfunction to reduce repetition
            temp = self.state[index + index_offset]

            child_state = deepcopy(list(self.state))

            child_state[index + index_offset] = child_state[index]
            child_state[index] = temp

            if self.parent is not None:
                if self.parent.state != tuple(child_state):
                    children_list.append(Board(tuple(child_state), self, self.tiles))
            else:
                children_list.append(Board(tuple(child_state), self, self.tiles))

        children = []  # Let's use list here, because it's faster to iterate than a set.

        if self.tiles == 8:
            index = self.state.index(0)
            row = int(index / 3)
            column = index % 3

            if row > 0:
                add_child_to_list(children, index, -3)
            if row < 2:
                add_child_to_list(children, index, 3)
            if column > 0:
                add_child_to_list(children, index, -1)
            if column < 2:
                add_child_to_list(children, index, 1)
        else:
            state_list = list(self.state)
            for index, element in enumerate(state_list):
                if element != 0:
                    row = int(index / 3)
                    column = index % 3

                    if row > 0:
                        if state_list[index-3] == 0:
                            add_child_to_list(children, index, -3)
                    if row < 2:
                        if state_list[index+3] == 0:
                            add_child_to_list(children, index, 3)
                    if column > 0:
                        if state_list[index - 1] == 0:
                            add_child_to_list(children, index, -1)
                    if column < 2:
                        if state_list[index + 1] == 0:
                            add_child_to_list(children, index, 1)




        return children

    def is_goal_state(self):
        return True if self.state == self.goal_state else False

    def print(self):
        for index, element in enumerate(self.state):
            print(element, end=" ")
            if index % 3 == 2:
                print("\n", end="")


class EightPuzzle(object):
    def __init__(self, max_iterations=5000, starting_state=None, tiles=8, random_select=False, print_trace=False):
        self.unvisited = set()  # It's faster to check if element is in a set than in a list.
        self.visited = set()
        self.max_iterations = max_iterations
        self.starting_state = starting_state
        self.tiles = tiles
        self.random_select = random_select
        self.print_trace = print_trace

    def backtrace(self, current_board):
        backtrace_list = []
        parent = current_board.parent
        while parent is not None:
            backtrace_list.append(current_board)
            current_board = parent
            parent = current_board.parent
        backtrace_list.append(current_board)
        return backtrace_list

    def weighted_a_star(self, weight):
        return self.a_star(weight, False)

    def greedy_best_first(self):
        return self.a_star(1, True)

    def a_star(self, weight=1, greedy=False):
        time_start = time.clock()
        if self.starting_state is not None:
            current_board = Board(self.starting_state, None, self.tiles)
        else:
            current_board = Board(None, None, self.tiles)
        self.unvisited.add(current_board)

        iteration = 0
        #print("********** ------------- ***********")
        #print("Starting the algorithm. Weight = " + str(weight) + ", greedy = " + str(greedy))
        #print("Initial state:")
        #current_board.print()
        while True:

            self.visited.add(current_board)
            self.unvisited.remove(current_board)

            if current_board.is_goal_state():
                time_end = time.clock()
                #print("Reached the solution after: " + str(iteration) + " iterations")
                #current_board.print()
                #print("Total visited states: " + str(len(self.visited)))
                #print("Yet to be explored states: " + str(len(self.unvisited)))
                running_time = time_end - time_start
                #print("Total running time: " + str(time_end - time_start) + "s")
                backtrace = self.backtrace(current_board)
                backtrace.reverse()
                #print("Total steps: " + str(len(backtrace) - 1))
                if self.print_trace:
                    print("The solution trace: ")
                    for state in backtrace:
                        print("\n", end="")
                        state.print()
                    print("*** End of execution ***")
                return True, [iteration, running_time, len(self.visited), len(self.unvisited), len(backtrace)]


            for child in current_board.get_child_boards():
                if child not in self.unvisited or child not in self.visited:
                    self.unvisited.add(child)

            if greedy:
                for index, board in enumerate(self.unvisited):
                    if index == 0:
                        smallest_list = [board]
                    else:
                        if board.heuristic < smallest_list[0].heuristic:
                            smallest_list = [board]
                        elif board.heuristic == smallest_list[0].heuristic:
                            smallest_list.append(board)
            else:
                for index, board in enumerate(self.unvisited):
                    if index == 0:
                        smallest_list = [board]
                    else:
                        if weight * board.heuristic + board.moves < weight * smallest_list[0].heuristic + smallest_list[0].moves:
                            smallest_list = [board]
                        elif weight * board.heuristic + board.moves == weight * smallest_list[0].heuristic + smallest_list[0].moves:
                            smallest_list.append(board)



            iteration += 1


            if iteration >= self.max_iterations:
                #print("Max iterations (" + str(self.max_iterations) + ") reached")
                time_end = time.clock()

                running_time = time_end - time_start
                #print("Total running time: " + str(time_end - time_start) + "s")
                return False, [iteration, running_time]


            if self.random_select:
                current_board = random.choice(smallest_list)
                # If multiple unvisited nodes with same cost, then we can pick the next by random.
                # If you select the next board from the smallest board list by random, then the greedy
                # best first quite often does not converge to the solution within the iteration limit.
            else:
                current_board = smallest_list[0]



        #Let's empty these sets so that we can call this algorithm multiple times for the same instance.
        self.unvisited = set()
        self.visited = set()


def main():


    list_of_puzzles = [EightPuzzle(100000, None, i) for i in range(1, 9)]

    for puzzle in list_of_puzzles:

        for i in range(1, 11):
            print(puzzle.weighted_a_star(i))
        print(puzzle.greedy_best_first())


    #puzzle = EightPuzzle(10000, tuple([5,1,2,4,0,6,3,7,8]), 8 , False)
    #puzzle.a_star()

if __name__ == "__main__":
    main()
