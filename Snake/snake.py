# from snake_agent_human import *
# from snake_agent_ai import *
# from snake_utils import *
from snake_game import *
# from snake_ui import *
# from snake_engine import *

# GAME DEFAULTS
BOARD_ROWS = 10
BOARD_COLS = 10
MODE_AUTO = False



if __name__ == '__main__':

    game = Game(Agents.AGENT_SHORTEST_DISTANCE, BOARD_COLS, BOARD_ROWS)

    game.run()