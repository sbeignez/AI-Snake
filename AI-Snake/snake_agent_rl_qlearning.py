from snake_utils import Direction, Agents
from snake_agent_abstract import Agent

import random
import enum

import numpy as np



class AgentQLearning(Agent): 

    GAME_RUN = 0
    GAME_RUN_EAT = 1
    GAME_PAUSED = 2
    GAME_WIN = 3
    GAME_OVER = 4

    reward = {
        GAME_RUN: -.01,
        GAME_RUN_EAT: 10,
        GAME_WIN: 100,
        GAME_PAUSED: -10,
        GAME_OVER: -10
    }

    def __init__ (self, session, agent_type):
        self.session = session
        self.agent_type = agent_type
        self.paths = []

        
        
        self.learning_rate = 0.5 # alpha
        self.discount_factor = 0.8 # gamma
        self.epsilon = 0.2 # epsilon greedy?

        self.ACTIONS = Direction.all_dirs() # N S E W 

        self.STATES = [
            ( xh, yh, xt, yt, xa, ya )
            for xh in range(1, self.session.board.cols+1)
            for yh in range(1, self.session.board.rows+1)
            for xt in range(1, self.session.board.cols+1)
            for yt in range(1, self.session.board.rows+1)
            for xa in range(1, self.session.board.cols+1)
            for ya in range(1, self.session.board.rows+1)            
            ]
        # print("States:",self.STATES[0:3])
        
        self.Qvalues = { (state, action) : 0 for state in self.STATES for action in self.ACTIONS } # np.zeros([len(self.STATES), len(self.ACTIONS)])
        # print("QValues", self.Qvalues)


    def next_move(self) -> Direction:
        if random.uniform(0, 1) < self.epsilon:
            # Explore action space
            action = self.sample_actions() 
            # print("Explore", action)
        else:
            # Exploit learned values
            # action = np.argmax(self.Qvalues[self.session_to_state()]
            state, action = max(self.Qvalues, key = self.Qvalues.get)
            # print("Exploit", action)
        return action

    def update_q_value(self, old_state, new_state, status, action):

        reward = self.reward[status]
        # print(reward)
        
        self.Qvalues[(old_state, action)] = (
                (1 - self.learning_rate) * self.Qvalues[(old_state, action)] 
                + self.learning_rate * ( reward + self.discount_factor * np.max(self.Qvalues[(new_state,action)]) )
            )

    def session_to_state(self):
        return (
            self.session.snake.head()[0], self.session.snake.head()[1],
            self.session.snake.tail()[0], self.session.snake.tail()[1],
            self.session.apple.x, self.session.apple.y,
        )

    def sample_states(self):
        return random.choice(self.STATES)

    def sample_actions(self):
        return random.choice(self.ACTIONS)
