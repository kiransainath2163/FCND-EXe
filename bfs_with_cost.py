import numpy as np
from enum import Enum


# Define your action set using Enum()
class Action(Enum):
    """
        An action is represented by a 3 element tuple.

        The first 2 values are the delta of the action relative
        to the current grid position. The third and final value
        is the cost of performing the action.
    """
    LEFT = (0, -1, 1)
    RIGHT = (0, 1, 1)
    UP = (-1, 0, 1)
    DOWN = (1, 0, 1)

    def __str__(self):
        if self == self.LEFT:
            return '<'
        elif self == self.RIGHT:
            return '>'
        elif self == self.UP:
            return '^'
        elif self == self.DOWN:
            return 'v'

    @property
    def cost(self):
        return self.value[2]

    @property
    def delta(self):
        return (self.value[0], self.value[1])


# Define a function that returns a list of valid actions from the current node
def valid_actions(grid, current_node):
    """
    Returns a list of valid actions given a grid and current node.
    """
    valid = [Action.UP, Action.LEFT, Action.RIGHT, Action.DOWN]
    n, m = grid.shape[0] - 1, grid.shape[1] - 1
    x, y = current_node

    # check if the node is off the grid or
    # it's an obstacle

    if x - 1 < 0 or grid[x - 1, y] == 1:
        valid.remove(Action.UP)
    if x + 1 > n or grid[x + 1, y] == 1:
        valid.remove(Action.DOWN)
    if y - 1 < 0 or grid[x, y - 1] == 1:
        valid.remove(Action.LEFT)
    if y + 1 > m or grid[x, y + 1] == 1:
        valid.remove(Action.RIGHT)

    return valid


def visualize_path(grid, path, start):
    sgrid = np.zeros(np.shape(grid), dtype=np.str)
    sgrid[:] = ' '
    sgrid[grid[:] == 1] = 'O'

    pos = start

    for a in path:
        da = a.value
        sgrid[pos[0], pos[1]] = str(a)
        pos = (pos[0] + da[0], pos[1] + da[1])
    sgrid[pos[0], pos[1]] = 'G'
    sgrid[start[0], start[1]] = 'S'
    print(sgrid)
    return sgrid


def uniform_cost(grid, start, goal):
    # Below:
    # "queue" is meant to contain your partial paths
    # "visited" is meant to contain your visited cells
    # TODO: Replace the None values for "queue" and "visited" with data structure types

    queue =[(start,0)]  # TODO: Choose a data structure type for your partial paths
    visited = list()  # TODO: Choose a data structure type for your visited list

    branch = {}
    found = False

    # Run loop while queue is not empty
    while not found:  # e.g, replace True with queue.empty() if using a Queue:
        # TODO: Replace "None" to remove the first element from the queue
        current_node, current_cost = queue.pop(0)
        if current_node not in visited:
            visited.append(current_node)
        # TODO: Replace "False" to check if the current vertex corresponds to the goal state
        if current_node == goal:
            print('Found a path.')
            found = True
            break
        else:
            # Get the new vertexes connected to the current vertex
            for action in valid_actions(grid, current_node):
                # delta of performing the action
                da = action.delta
                # TODO: compute the new cost
                next_node = (current_node[0] + da[0], current_node[1] + da[1])

                # TODO: Check if the new vertex has not been visited before.
                if next_node not in visited:
                    visited.append(next_node)
                    new_cost = current_cost + action.cost
                    queue.append((next_node,new_cost ))
                # If the node has not been visited you will need to
                # 1. Mark it as visited
                # 2. Add it to the queue
                    branch[next_node] = (current_node, action, new_cost)

    path = []
    path_cost = 0
    if found:
        # retrace steps
        path = []
        n = goal
        path_cost = branch[n][2]
        while branch[n][0] != start:
            path.append(branch[n][1])
            n = branch[n][0]
        path.append(branch[n][1])

    return path[::-1], path_cost


if __name__ == "__main__":
    # Define a start and goal location
    start = (0, 0)
    goal = (4, 4)
    # Define your grid-based state space of obstacles and free space
    grid = np.array([
        [0, 1, 0, 0, 0, 0],
        [0, 1, 0, 1, 0, 0],
        [0, 1, 0, 0, 0, 0],
        [0, 1, 0, 0, 1, 0],
        [0, 0, 0, 1, 0, 0],
    ])

    path, path_cost = uniform_cost(grid, start, goal)
    print(path_cost, path)


    # S -> start, G -> goal, O -> obstacle
    visualize_path(grid, path, start)