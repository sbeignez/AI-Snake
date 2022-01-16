from pickletools import int4
from xmlrpc.client import Boolean
from snake_utils import Direction, Agents
from snake_agent_abstract import Agent
import numpy as np
import enum

import networkx as nx
from itertools import islice
from matplotlib import pyplot as plt


# class AgentAI(Agent):

#     def __init__ (self, session, agent_type : Agents):
#         self.session = session
#         self.agent_type = agent_type

#         self.paths = None

#     def next_move(self):
#         return self._get_next_move()


#     def _get_next_move(self):
#         if self.agent_type == Agents.AGENT_SHORTEST_DISTANCE:
#             return self.next_move_greedy()
#         if self.agent_type == Agents.AGENT_A_STAR:
#             return self.next_move_a_star()

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


class AgentSuperStar(Agent):

    def __init__ (self, session, agent_type):
        self.session = session
        self.agent_type = agent_type
        self.path = []
        self.paths = None

    def next_move(self):

        if len(self.path) > 1 :
            action = Direction.dir(self.path[0],self.path[1])
            self.path = self.path[1:]
            return action

        grid = nx.grid_graph(dim=(range(1, self.session.board.cols+1), range(1, self.session.board.rows+1)))
        grid.remove_nodes_from(list(self.session.snake.body)[0:-1])

        source = self.session.snake.head()
        target = self.session.apple.node()

        k = 150
        print(source, target)

        for path in self.k_shortest_paths(grid, source, target, k):
            print(path)
            if self.valid_path(list(self.session.snake.body), path, self.session.snake.len): # valid
                print(path, "is valid")
                action = Direction.dir(path[0],path[1])
                self.path = path[1:]
                # self.draw(grid)
                return action
                
        self.draw(grid) 
        return Direction.STOP


    def k_shortest_paths(self, G, source, target, k, weight=None):
        try:
            return list(islice(nx.shortest_simple_paths(G, source, target, weight=weight), k))
        except:
            return []

    def valid_path(self, snake, path, length) -> Boolean:

        future_snake = (snake + path[1:])[-(length+1): -1]  # without head
        future_head = path[-1]
        # print(f"P:{snake}+{path} L:{length} FS:{future_snake} FH:{future_head}")
        grid = nx.grid_graph(dim=(range(1, self.session.board.cols+1), range(1, self.session.board.rows+1)))
        grid.remove_nodes_from(future_snake)

        for node in grid.nodes():
            if not nx.has_path(grid, future_head, node):
                return False
        return True


    def draw(self, G):
        pos = {(x,y):(x,y) for x,y in G.nodes()}
        nx.draw(G, pos=pos, 
            node_color='lightblue', 
            with_labels=True,
            node_size=600)
        plt.show()




if __name__ == '__main__':
    
    G=nx.Graph()
    G.add_edge(1,2)
    G.add_edge(2,3)

    print(G)
    print(nx.dijkstra_path(G,1,3))
    print(nx.is_connected(G))

    G2 = nx.grid_2d_graph(2,3)
    print(G2)


    G = nx.grid_graph(dim=(range(1, 11), range(1, 11)))
    G.remove_node((5,5))
    G.remove_nodes_from([(6,6), (6,7)])

    # plt.figure(figsize=(6,6))
    pos = {(x,y):(x,y) for x,y in G.nodes()}
    nx.draw(G, pos=pos, 
        node_color='lightblue', 
        with_labels=True,
        node_size=600)

    from itertools import islice
    def k_shortest_paths(G, source, target, k, weight=None):
        return list(
            islice(nx.shortest_simple_paths(G, source, target, weight=weight), k)
        )
    for path in k_shortest_paths(G, (4,4), (7,8), 3):
        print(path)

    plt.show()



