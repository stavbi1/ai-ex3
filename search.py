from node import Node
from utils import memoize, PriorityQueue

def best_first_graph_search(problem, f):
    """Search the nodes with the lowest f scores first.
    You specify the function f(node) that you want to minimize; for example,
    if f is a heuristic estimate to the goal, then we have greedy best
    first search; if f is node.depth then we have breadth-first search.
    There is a subtlety: the line "f = memoize(f, 'f')" means that the f
    values will be cached on the nodes as they are computed. So after doing
    a best first search you can examine the f values of the path returned."""
    f = memoize(f, 'f')
    node = Node(problem.initial)
    frontier = PriorityQueue('min', f)
    frontier.append(node)
    explored = set()
    while frontier:
        node = frontier.pop()
        if problem.goal_test(node.state):
            return node
        explored.add(node.state)
        for child in node.expand(problem):
            if child.state not in explored and child not in frontier:
                frontier.append(child)
            elif child in frontier:
                if f(child) < frontier[child]:
                    del frontier[child]
                    frontier.append(child)
    return None

def astar_search(problem, h=None):
    """A* search is best-first graph search with f(n) = g(n)+h(n).
    You need to specify the h function when you call astar_search, or
    else in your Problem subclass."""
    h = memoize(h or problem.h, 'h')
    return best_first_graph_search(problem, lambda n: n.path_cost + h(n))

def depth_first_tree_search(problem):
    """Search the deepest nodes in the search tree first.
        Search through the successors of a problem to find a goal.
        The argument frontier should be an empty queue.
        Repeats infinitely in case of loops. [Figure 3.7]"""

    frontier = [Node(problem.initial)]  # Stack

    while frontier:
        node = frontier.pop()
        if problem.goal_test(node.state):
            return node
        frontier.extend(node.expand(problem))
    return None

def iterative_improvement(problem):
    state = problem.cspInitial
    seen = {state}
    graded_variables = problem.get_conflicted_variables(state)
    conflicted = max(graded_variables, key=lambda x: x.grade)

    while conflicted.grade:
        variable_assignments = problem.assignments_of_variable(state, conflicted.variable, seen)

        while not variable_assignments:
            graded_variables = [var for var in graded_variables if var.variable != conflicted.variable]
            conflicted = max(graded_variables, key=lambda x: x.grade)
            variable_assignments = problem.assignments_of_variable(state, conflicted.variable, seen)

        state = min(variable_assignments, key=lambda x: x.grade).variable
        seen.add(state)
        graded_variables = problem.get_conflicted_variables(state)
        conflicted = max(graded_variables, key=lambda x: x.grade)

    return state












