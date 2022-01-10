from snake_game import *
from snake_agent_ai import Agents
# import argparse
import enum



if __name__ == '__main__':

    
    # 1. Parameters for MANUAL
    p00 = GameParams()
    p00.BOARD_ROWS = 2
    p00.BOARD_COLS = 2
    p00.SCALE = 80
    p00.SPEED = 20
    p00.agent = Agents.AGENT_GREEDY
    p00.mode = Game.Mode.MODE_PLAY

    # 1. Parameters for 
    p01 = GameParams()
    p01.BOARD_ROWS = 6
    p01.BOARD_COLS = 6
    p01.SCALE = 40
    p01.SPEED = 40
    p01.agent = Agents.AGENT_A_STAR
    p01.mode = Game.Mode.MODE_PLAY

    # 2. Parameters Becnhmark
    p02 = GameParams()
    p02.BOARD_ROWS = 10
    p02.BOARD_COLS = 10
    p02.SCALE = 40
    p02.SPEED = 8
    p02.agent = Agents.AGENT_A_STAR
    p02.mode = Game.Mode.MODE_BENCHMARK

    # 3. Parameters Q Learning
    p03 = GameParams()
    p03.BOARD_ROWS = 4
    p03.BOARD_COLS = 2
    p03.SCALE = 40
    p03.SPEED = 4
    p03.agent = Agents.AGENT_Q_LEARNING
    p03.mode = Game.Mode.MODE_TRAIN
    p03.log = False

    # Game run!
    Game(p03).run()
