from pickletools import int4
from xmlrpc.client import Boolean
from snake_utils import Direction, Agents
from snake_agent_abstract import Agent
import numpy as np
import enum

import networkx as nx
from itertools import islice
from matplotlib import pyplot as plt


class AgentAStar(Agent):

    def __init__ (self, session, agent_type):
        self.session = session
        self.agent_type = agent_type

        self.paths = None

    def next_move(self):

        def reconstruct_path(came_from, current):
            path = []
            while current in came_from:
                current = came_from[current]
                path.insert(0, current)
            return path

        block_start = self.session.snake.head()
        block_end = self.session.apple.cell()
        blocks_open = ( { (x,y) for x in range(1, self.session.board.cols +1) for y in range(1, self.session.board.rows+1) } - set(self.session.snake.body) ) | { block_start } # | union

        # print("A* ===============")
        # print("BLOCKS", blocks_open, len(blocks_open))
        # print("START", block_start, "END", block_end, "SNAKE", set(board["snake"]["body"]))

        openSet = {block_start}
        cameFrom = {}

        def distance_L1(block_start, block_end):
            return abs(block_start[0] - block_end[0]) + abs(block_start[0] - block_end[0])


        gScore = { (block[0],block[1]) : None for block in blocks_open }
        gScore[block_start] = 0

        fScore = { (block[0],block[1]) : None for block in blocks_open }
        fScore[block_start] = distance_L1(block_start, block_end)

        while openSet:

            if openSet:
                current = min(openSet, key = lambda x : fScore[x] ) # openSet.get

            if current == block_end:
                path = reconstruct_path(cameFrom, current) + [block_end]
                # print("A* PATH:", path)
                direction = Direction.STOP
                if len(path) >= 2:
                    direction = Direction.dir(path[0], path[1])

                # print("AGENT (AI) action:", direction)
                self.paths = [path]
                return direction

            openSet.remove(current)

            neighbors = { (current[0] + direction.value[0], current[1] + direction.value[1]) for direction in Direction.all_dirs() } & blocks_open # &: intersection

            for neighbor in neighbors:
                tentative_gScore = gScore[current] + 1 # d(current, neighbor)
                if gScore[neighbor] == None or tentative_gScore < gScore[neighbor]:
                    cameFrom[neighbor] = current
                    gScore[neighbor] = tentative_gScore
                    fScore[neighbor] = tentative_gScore + distance_L1(neighbor, block_end)
                    if neighbor not in openSet:
                        openSet.add(neighbor)
        
        return Direction.STOP

