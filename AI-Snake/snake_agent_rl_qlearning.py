from snake_utils import Direction, Agents
from snake_agent_abstract import Agent
import enum

import numpy as np



class AgentQLearning(Agent): 

    def __init__ (self, session, agent_type):
        self.session = session
        self.agent_type = agent_type

        self.Qvalues = np.zeros()
        
        self.learning_rate = 0.5 # alpha
        self.discount_factor = 0.9 # gamma

    def next_move(self) -> Direction:


        direction = Direction.STOP

        return direction

