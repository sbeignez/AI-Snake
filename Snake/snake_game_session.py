
from snake_agent_ai import *
from snake_utils import *

class GameSession():

    def __init__(self, game, agent, x, y):

        self.game = game

        self.agent = AgentAI(self, agent)

        self.board = Board(x, y)
        self.snake = Snake()
        self.apple = Apple()

        self.score = 0
        self.steps = 0

        # self.board = {
        #     "apple" : None,
        #     "snake" : [],
        #     # "pause" : False,
        #     # "score" : 0,
        #     # "steps" : 0,
        #     "paths" : None,
        #     "move"  : None,
        #     "board" : self.board_,
        #     "mode"  : "",
        #     # "game-over": False,
        # }

    def create_session(self, agent):
        self.game.engine.init_snake(self)
        self.game.engine.create_apple(self)
        self.agent = AgentAI(self, agent)


class Board():

    def __init__(self, cols, rows) -> None:

        if cols <3 or cols >100:
            raise ValueError("Boards' number of columns must be between 3 and 100") 
        if rows <3 or rows >100:
            raise ValueError("Boards' number of rows must be between 3 and 100")

        self.cols = cols
        self.rows = rows

    def size(self):
        return self.cols * self.rows


class Apple():

    def __init__(self, x = None, y = None) -> None:
        self.x = x
        self.y = y

    def cell(self):
        return (self.x, self.y)


class Snake():

    def __init__(self, snake_body = []):
        # TODO change to deque
        self.body = snake_body

    def body(self):
        return self.body

    def head(self):
        return self.body[-1]

    def move_to(self, cell: Cell):
        self.body.append(cell)
        self.body.pop(0)
    
    def grow(self):
        self.body.insert(0, self.body[0])



