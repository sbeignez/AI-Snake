from snake_game import *
from snake_agent_ai import Agents
# import argparse
import enum




if __name__ == '__main__':

    # Parameters
    params = GameParams()
    params.BOARD_ROWS = 6
    params.BOARD_COLS = 6
    params.SCALE = 40
    params.SPEED = 40
    params.agent = Agents.AGENT_Q_LEARNING
    params.mode = Mode.MODE_TRAIN

    # Parameters Q Learning
    params = GameParams()
    params.BOARD_ROWS = 3
    params.BOARD_COLS = 3
    params.SCALE = 40
    params.SPEED = 8
    params.agent = Agents.AGENT_Q_LEARNING
    params.mode = Mode.MODE_TRAIN

    # Game run!
    Game(params).run()
