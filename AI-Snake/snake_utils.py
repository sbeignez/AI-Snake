import enum
from collections import namedtuple

# Agents Enum
class Agents(enum.Enum):
    AGENT_GREEDY = "Shortest Distance"
    AGENT_A_STAR = "A*"
    AGENT_Q_LEARNING = "Q Learning"

# Cell
Cell = namedtuple('Cell', 'x, y')

# Direction Enum
class Direction(enum.Enum):
    UP = (0,1)
    DOWN = (0,-1)
    RIGHT = (1,0)
    LEFT = (-1,0)
    STOP = (0,0)

    def add(block: Cell, dir):
        if dir:
            return (block[0] + dir.value[0], block[1] + dir.value[1])
        else:
            return block

    def dir(start, end):
        if end and start:
            return Direction( ( end[0] - start[0], end[1] - start[1]))
        else:
            return Direction.STOP

    def all_dirs():
        return [Direction.UP, Direction.RIGHT, Direction.DOWN, Direction.LEFT]




# import matplotlib.pyplot as plt
# plt.