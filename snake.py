from snake_game import *
from snake_agent_ai import Agents
# import argparse
import enum



if __name__ == '__main__':

    
    # 1. Parameters for MANUAL
    p00 = GameParams()
    p00.BOARD_ROWS = 8
    p00.BOARD_COLS = 8
    p00.SCALE = 80
    p00.SPEED = 20
    p00.agent = Agents.AGENT_A_STAR
    p00.mode = Game.Mode.MODE_PLAY

    # 1. Parameters for 
    p01 = GameParams()
    p01.BOARD_ROWS = 3
    p01.BOARD_COLS = 2
    p01.SCALE = 40
    p01.SPEED = 40
    p01.agent = Agents.AGENT_A_STAR
    p01.mode = Game.Mode.MODE_PLAY

    # 1. Parameters for MANUAL
    p011 = GameParams()
    p011.BOARD_ROWS = 6
    p011.BOARD_COLS = 6
    p011.SCALE = 100
    p011.SPEED = 20
    p011.agent = Agents.AGENT_SUPER_STAR
    p011.mode = Game.Mode.MODE_PLAY

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
    p03.BOARD_ROWS = 3
    p03.BOARD_COLS = 4
    p03.SCALE = 80
    p03.SPEED = 6
    p03.agent = Agents.AGENT_Q_LEARNING
    p03.mode = Game.Mode.MODE_TRAIN
    p03.log = False

    # 4. Parameters BFS
    p04 = GameParams()
    p04.BOARD_ROWS = 8
    p04.BOARD_COLS = 8
    p04.SCALE = 40
    p04.SPEED = 30
    p04.agent = Agents.AGENT_BFS
    p04.mode = Game.Mode.MODE_PLAY
    p04.log = False


    # Game run!
    Game(p04).run()
