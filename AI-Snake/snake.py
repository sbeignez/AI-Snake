from snake_game import *
from snake_agent_ai import Agents
# import argparse
import enum




if __name__ == '__main__':

    # Parameters
    params = GameParams()
    params.BOARD_ROWS = 3
    params.BOARD_COLS = 3
    params.SCALE = 50
    params.agent = Agents.AGENT_SHORTEST_DISTANCE
    params.mode = Mode.MODE_PLAY

    # Game run!
    Game(params).run()