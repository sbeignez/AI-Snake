from pickletools import int4
from xmlrpc.client import Boolean
from snake_utils import Direction, Agents
from snake_agent_abstract import Agent
import numpy as np
import enum

import networkx as nx
from itertools import islice
from matplotlib import pyplot as plt


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



