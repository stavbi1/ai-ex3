import matplotlib.pyplot as plt
from nqueen import NQueensProblem
from search import depth_first_tree_search, iterative_improvement, astar_search
from time import time
from eightPuzzle import EightPuzzle


def measure_queens_search(max_queens, search):
    times = []
    queens_to_check = range(4, max_queens, 2)

    for i in queens_to_check:
        start = time()
        result = search(NQueensProblem(i))
        end = time()
        times.append(end - start)
        print("{} queens done".format(i))

    fig, ax = plt.subplots()
    ax.plot(queens_to_check, times)

    plt.xlabel("Queens")
    plt.ylabel("Time (s)")
    plt.show()


def nqueens_backtracking():
    measure_queens_search(26, depth_first_tree_search)


def nqueens_iterative_improvement():
    measure_queens_search(100, iterative_improvement)


def solve_eight_puzzle():
    result = astar_search(EightPuzzle(initial=(4, 7, 8, 6, 3, 2, 0, 5, 1)))
    print(result.solution())


if __name__ == '__main__':
    solve_eight_puzzle()
