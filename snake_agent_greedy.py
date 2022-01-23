from pickletools import int4
from xmlrpc.client import Boolean
from snake_utils import Direction, Agents
from snake_agent_abstract import Agent
import numpy as np



class AgentGreedy(Agent): 

    def __init__ (self, session, agent_type):
        self.session = session
        self.agent_type = agent_type

        self.paths = None

    def next_move(self):
        head = self.session.snake.head()
        moves = []
        # DOWN
        if head[1] > 1 and (head[0], head[1]-1) not in self.session.snake.body:
            moves.append((head[0], head[1]-1))
        # UP
        if head[1] < self.session.board.rows and (head[0], head[1]+1) not in self.session.snake.body:
            moves.append((head[0], head[1]+1))
        # RIGHT
        if head[0] < self.session.board.cols and (head[0]+1, head[1]) not in self.session.snake.body:
            moves.append((head[0]+1, head[1]))
        # LEFT
        if head[0] > 1 and (head[0]-1, head[1]) not in self.session.snake.body:
            moves.append((head[0]-1, head[1]))

        # print("BODY:", self.session.snake.body, self.session.apple)
        moves.sort( key = lambda x : abs(x[0] - self.session.apple.x) + abs(x[1] - self.session.apple.y), reverse = False)
        # print("MOVES:", moves)

        # move = min(moves, key = lambda x : abs(x[0] - apple[0]) + abs(x[1] - apple[1]))

        self.paths = [[move] for move in moves]
        if self.paths:
            direction = Direction( ( self.paths[0][0][0] - self.session.snake.head()[0], self.paths[0][0][1] - self.session.snake.head()[1]))
        else:
            direction = Direction.STOP

        return direction

