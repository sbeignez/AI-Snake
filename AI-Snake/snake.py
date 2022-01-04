from snake_game import *
from snake_agent_ai import Agents
# import argparse
import enum




if __name__ == '__main__':

    # Parameters
    params = GameParams()
    params.BOARD_ROWS = 30
    params.BOARD_COLS = 30
    params.SCALE = 80
    params.agent = Agents.AGENT_GREEDY
    params.mode = Mode.MODE_PLAY

    # Game run!
    Game(params).run()