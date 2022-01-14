
from snake_agent_factory import *
from snake_utils import *
from collections import deque
import json

class GameSession():

    def __init__(self, game, agent, x, y):

        self.game = game

        self.board = Board(x, y)
        self.agent = AgentFactory(self, agent).get_agent()

        self.snake = Snake()
        self.apple = Apple()

        self.score = 0
        self.steps = 0
        self.steps_since_last = 0

    def create_session(self, agent):
        self.game.engine.init_snake(self)
        self.game.engine.create_apple(self)
        self.agent = AgentFactory(self, agent).get_agent()
        self.score = 0
        self.steps = 0
        self.steps_since_last = 0
        # print("INIT:", self.snake, self.apple)

    def restart_game(self):
        self.game.engine.init_snake(self)
        self.game.engine.create_apple(self)
        self.score = 0
        self.steps = 0
        self.steps_since_last = 0

    def reset(self):
        self.score = 0
        self.steps = 0
        self.steps_since_last = 0

    def toJSON(self):
        return json.dumps([vars(self.board), vars(self.apple)])


class Board():

    def __init__(self, cols, rows) -> None:
        self.cols = cols
        self.rows = rows
        if (self.size) % 2 == 1:
            raise ValueError("Boards' size must be even") 

    @property
    def cols(self):
        return self._cols

    @cols.setter
    def cols(self, cols):
        if cols <2 or cols >100:
            raise ValueError("Boards' number of columns must be between 2 and 100") 
        self._cols = cols

    @property
    def rows(self):
        return self._rows

    @rows.setter
    def rows(self, rows):    
        if rows <2 or rows >100:
            raise ValueError("Boards' number of rows must be between 2 and 100")
        self._rows = rows

    @property
    def size(self):
        return self.cols * self.rows


class Apple():

    def __init__(self, x = None, y = None) -> None:
        self.x = x
        self.y = y

    def cell(self) -> Cell:
        return Cell(self.x, self.y)

    def __str__(self):
        return f"Apple({self.x}, {self.y})"
    __repr__ = __str__



class Snake():

    def __init__(self, snake_body = []):
        self._body = deque(snake_body)
        self._len = len(self.body)

    @property
    def body(self):
        return self._body

    @property
    def len(self) -> int:
        return self._len

    def head(self) -> Cell:
        if not self._body:
            return None
        return self._body[-1]

    def tail(self) -> Cell:
        if not self._body:
            return None
        return self._body[0]

    def append_head(self, cell: Cell):
        self._body.append(cell)
        self._len +=1
    
    def pop_tail(self):
        self._body.popleft()
        self._len -=1

    # def grow(self):
        # snake grows 1 step after eating the apple
        # tail is duplicated
        # self._body.appendleft(self._body[0])

    # def len(self):
    #     return len(self._body)

    def __str__(self):
        return f"Snake({list(self.body)})"
    __repr__ = __str__