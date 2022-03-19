from problem import Problem

class EightPuzzle(Problem):
    """ The problem of sliding tiles numbered from 1 to 8 on a 3x3 board,
    where one of the squares is a blank. A state is represented as a tuple of length 9,
    where element at index i represents the tile number  at index i (0 if it's an empty square) """

    def __init__(self, initial, goal=(1, 2, 3, 8, 0, 4, 7, 6, 5)):
        """ Define goal state and initialize a problem """

        self.goal = goal
        Problem.__init__(self, initial, goal)
        self.pattern_dictionary = createPatternDatabase(self)

    def find_blank_square(self, state):
        """Return the index of the blank square in a given statee."""

        return state.index(0)

    def actions(self, state):
        """ Return the actions that can be executed in the given state.
        The result would be a list, since there are only four possible actions
        in any given state of the environment """

        possible_actions = ['UP', 'DOWN', 'LEFT', 'RIGHT']
        index_blank_square = self.find_blank_square(state)

        if index_blank_square % 3 == 0:
            possible_actions.remove('LEFT')
        if index_blank_square < 3:
            possible_actions.remove('UP')
        if index_blank_square % 3 == 2:
            possible_actions.remove('RIGHT')
        if index_blank_square > 5:
            possible_actions.remove('DOWN')

        return possible_actions

    def result(self, state, action):
        """ Given state and action, return a new state that is the result of the action.
        Action is assumed to be a valid action in the state """

        # blank is the index of the blank square
        blank = self.find_blank_square(state)
        new_state = list(state)

        delta = {'UP': -3, 'DOWN': 3, 'LEFT': -1, 'RIGHT': 1}
        neighbor = blank + delta[action]
        new_state[blank], new_state[neighbor] = new_state[neighbor], new_state[blank]

        return tuple(new_state)

    def goal_test(self, state):
        """ Given a state, return True if state is a goal state or False, otherwise """

        return state == self.goal

    def check_solvability(self, state):
        """ Checks if the given state is solvable """

        inversion = 0
        for i in range(len(state)):
            for j in range(i + 1, len(state)):
                if (state[i] > state[j]) and state[i] != 0 and state[j] != 0:
                    inversion += 1

        return inversion % 2 == 0

    def h(self, node):
        """ Return the heuristic value for a given state.
        h2(n) = sum manhattan distances """
        sum_dist = 0
        for i in range(9):
            if node.state[i] == 0:
                continue
            else:
                j = self.goal.index(node.state[i])
                xi = i % 3
                yi = i // 3
                xj = j % 3
                yj = j // 3
                sum_dist += (abs(xi - xj) + abs(yi - yj))
        return sum_dist


def get_key(pd, val):
    key_list = []
    for key, value in pd.items():
        if val == value:
            key_list.append(key)
    return key_list


def createPatternDatabase(e):
    state = list(e.goal)
    pattern_dict = {}
    for k in range(5, 9):
        state[state.index(k)] = '*'  # dont care
    g = 0
    pattern_dict[tuple(state)] = g
    new_pattern_found = True
    while new_pattern_found:
        new_pattern_found = False
        frontier = get_key(pattern_dict, g)
        for state in frontier:
            pa = e.actions(state)
            for a in pa:
                new_state = e.result(state, a)
                if new_state not in pattern_dict:
                    pattern_dict[new_state] = g + 1
                    new_pattern_found = True
        if new_pattern_found:
            g += 1

    return pattern_dict