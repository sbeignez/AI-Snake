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
        GAME_OVER: - np.inf,
    }

    def __init__ (self, session, agent_type):
        self.session = session
        self.agent_type = agent_type
        self.paths = []

        
        
        self.learning_rate = 0.8 # alpha
        self.discount_factor = 0.8 # gamma
        self.epsilon = 0.2 # epsilon greedy?

        self.ACTIONS = Direction.all_dirs() # N S E W 
        # print("Action:",self.ACTIONS)

        self.NUM_ACTION = len(self.ACTIONS)

        self.STATES = [
            ( xh, yh, xt, yt, xa, ya )
            for xh in range(1, self.session.board.cols+1)
            for yh in range(1, self.session.board.rows+1)
            for xt in range(1, self.session.board.cols+1)
            for yt in range(1, self.session.board.rows+1)
            for xa in range(1, self.session.board.cols+1)
            for ya in range(1, self.session.board.rows+1)            
            ]

        self.NUM_STATES= len(self.STATES)

        
        self.Qvalues = { (state, action) : 0 for state in self.STATES for action in self.ACTIONS } # np.zeros([len(self.STATES), len(self.ACTIONS)])
        print("QValues", self.print_Q())


    def next_move(self, training=True) -> Direction:
        """ Return action
        Exploration policy: Epsilon-Greedy 
        """
        
        coin = np.random.random_sample()
        # epsilon_t = self.epsilon ** steps

        # print(coin, self.epsilon, coin < self.epsilon, training, )

        if coin < self.epsilon and training:
            # Explore action space
            action = self.sample_actions() 
            infos = {"Policy action": "Explore"}
        else:
            # Exploit learned values
            # action = np.argmax(self.Qvalues[self.session_to_state()]
            q_values = { key : value for key, value in self.Qvalues.items() if key[0] == self.session_to_state()}

            state, action = max(q_values, key = q_values.get)
            infos = {"Policy action": "Exploit"}

        return action, infos

    def update_q_value(self, old_state, new_state, status, action):

        reward = self.reward[status]
        if self.session.game.params.log: print(old_state, action, ">", new_state, "Reward", reward, "Status", status, self.Qvalues[(old_state, action)])
        if self.session.game.params.log: print( [ values for key, values in self.Qvalues.items() if key[0] == new_state])

        terminal = status in [2,3,4]

        if terminal:
            maxQ = 0
        else:
            # maxQ = np.max(q_func[next_state_1, next_state_2, :, :])
            maxQ = max([ values for key, values in self.Qvalues.items() if key[0] == new_state])
        
        self.Qvalues[(old_state, action)] = (
                (1 - self.learning_rate) * self.Qvalues[(old_state, action)] 
                + self.learning_rate * (reward + self.discount_factor * maxQ)
            )

    def session_to_state(self):
        # observation
        return (
            self.session.snake.head()[0], self.session.snake.head()[1],
            self.session.snake.tail()[0], self.session.snake.tail()[1],
            self.session.apple.x, self.session.apple.y,
        )

    def sample_states(self):
        return random.choice(self.STATES)

    def sample_actions(self):
        actions = [ action for (state, action), value in self.Qvalues.items() if state == self.session_to_state() and not value == -np.inf]
        # print("Possible actions", len(actions), actions)
        action = random.choice(actions) if actions else random.choice(self.ACTIONS)
        # random.choice(self.ACTIONS)
        return action


    def render_text(self):
        xh, yh, xt, yt, xa, ya = self.session_to_state()
        rows, cols = self.session.board.rows, self.session.board.cols

        # print(self.session.snake, self.session_to_state())
        print("+---"*cols+"+")
        for r in range(rows, 0, -1):
            line = "| "
            for c in range(1, cols+1):
                if (c,r) == (xh, yh):
                    line += "O"
                elif (c,r) == (xt, yt):
                    line += "o"
                elif (c,r) == (xa, ya):
                    line += "A"
                else:
                    line += "."
                line += " | "
            print(line)
            print("+---"*cols+"+")

    def print_Q(self, state = None):
        for key, value in self.Qvalues.items():
            if state:
                if key[0] == state :
                    print(key, value)
            else:
                if not value == 0 :
                    print(key, value)