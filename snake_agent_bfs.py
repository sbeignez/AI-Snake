from pickletools import int4
from platform import node
from xmlrpc.client import Boolean
from snake_utils import Direction, Agents
from snake_agent_abstract import Agent
import numpy as np

from collections import deque

class Node():
    def __init__(self, state, parent = None, action = None, path_cost = 1):
        self.state = state #snake: list of possition
        self.parent = parent
        self.action = action
        self.path_cost = path_cost

    def __repr__(self):
        return f"(N:{self.state})"

class AgentBFS(Agent): 

    def __init__ (self, session, agent_type):
        self.session = session
        self.agent_type = agent_type
        self.paths = []
        self.path = deque()

    def next_move(self):

        if len(self.path) > 0 :
            next_step = self.path.popleft()
            action = Direction.dir(self.session.snake.head(), next_step)
            print("next (mem):", next_step)
            return action

        
        path = AgentBFS.search((self.session.board.cols, self.session.board.rows),
                list(self.session.snake.body), self.session.apple.node())

        if path:
            self.path = deque(path)
            current_step = self.path.popleft()
            next_step = self.path.popleft()
            print("next:", next_step)
            action = Direction.dir(self.session.snake.head(), next_step)
            return action
        else:
            return Direction.STOP


    def search(grid, snake, apple) -> Node:

        def expand(grid, node) -> list('Node'):
            nodes = []
            snake = node.state
            for action in valid_actions(grid, snake):
                next_snake = move(snake, action)
                nodes.append(Node(next_snake, node, action, 1))
            return nodes

        def valid_actions(grid, snake):
            actions = []
            x_head, y_head = snake[-1]
            cols, rows = grid
            if x_head > 1 and (x_head - 1, y_head) not in snake:
                actions.append(Direction.LEFT)
            if x_head < cols and (x_head + 1, y_head) not in snake:
                actions.append(Direction.RIGHT)
            if y_head < rows and (x_head, y_head + 1) not in snake:
                actions.append(Direction.UP)
            if y_head > 1 and (x_head, y_head - 1) not in snake:
                actions.append(Direction.DOWN)
            return actions

        def move(snake, action):
            new_snake = snake.copy()
            new_snake.append(Direction.add(snake[-1], action))
            new_snake = new_snake[1:]
            return new_snake

        def bfs(grid, snake, apple):
            node = Node(snake, None, )
            if snake[-1] == apple:
                return node

            frontier = deque([node]) # of nodes
            reached = { tuple(snake) } # of states

            while frontier:
                node = frontier.popleft()
                for child in expand(grid, node):
                    
                    state = child.state
                    if state[-1] == apple:
                        return child
                    if tuple(state) not in reached:
                        reached.add(tuple(state))
                        frontier.append(child)

            print(">>", reached, frontier)
            return None

        def path(node):
            if not node:
                return []
            path = [node.state[-1]]
            while node.parent:
                node = node.parent
                path = [node.state[-1]] + path
            # print("path:", path)
            return path    


        node = bfs(grid, snake, apple)
        path = path(node)
        # print("bfs", "s", snake, "a", apple, node, "p", path)
        return path





