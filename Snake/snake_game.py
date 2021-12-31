import time
import pygame
from snake_game_session import *
from snake_engine import *
from snake_ui import *
# from snake_agent_ai import *
# from snake_agent_ai import AgentAI


class Game():

    GAME_RUN = 2
    GAME_PAUSED = 1
    GAME_WON = 3
    GAME_OVER = 4

    SPEED = 20
    MODE_AUTO = "Auto"

    def __init__(self, agent, x, y):

        self.engine = GameEngine(self)
        self.session = GameSession(self, agent, x, y)
        self.ui = UI(self, x, y)
        


    best_score = 0
    game_played = 0

    agent_default = Agents.AGENT_A_STAR

    status = GAME_RUN

    def is_auto(self):
        return self.MODE_AUTO == "Auto"

    def rotate_mode(self):
        if self.is_auto():
            self.MODE_AUTO = "Manual"
        else:
            self.MODE_AUTO = "Auto"

    run = "pause" # or "run"

    def is_game_over(self):
        return self.status == self.GAME_OVER

    def pause(self):
        self.run = "pause"

    def unpause(self):
        self.run = "run"

    def rotate_pause(self):
        if self.is_paused():
            self.unpause()
        else:
            self.pause()

    def is_paused(self):
        return self.run == "pause"

    def restart(self):
        # self.session = GameSession(self, None, self.session.board.cols, self.session.board.rows)
        self.session.create_session(self.agent_default)
    
    def end(self):
        pygame.quit()


    def run(self):

        self.session.create_session(Agents.AGENT_A_STAR)

        board = self.session.board

        # board["snake"] = engine.init_snake(board)
        # board["apple"] = engine.create_apple(board)

        # init game session
        direction = Direction.STOP

        # wait until user quits

        while not self.run == "quit":

            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    self.run = "quit"
                if event.type == pygame.KEYDOWN:
                    # TAB: Restart game
                    if event.key == pygame.K_TAB:
                        print("Restart()")
                        self.restart()
                    # SPACE: Pause game
                    if event.key == pygame.K_SPACE:
                        print("Rotate_pause()")
                        self.rotate_pause()
                    # DELETE: Rewind 1 step
                    if event.key == pygame.K_DELETE:
                        pass
                        #rewind()
                    # SHIFT: Manual/Auto mode
                    if event.key == pygame.K_LSHIFT:
                        self.rotate_mode()

                    if event.key == pygame.K_LEFT and direction != Direction.RIGHT:
                        direction = Direction.LEFT
                        self.unpause()
                    if event.key == pygame.K_RIGHT and direction != Direction.LEFT:
                        direction = Direction.RIGHT
                        self.unpause()
                    if event.key == pygame.K_UP and direction != Direction.DOWN:
                        direction = Direction.UP
                        self.unpause()
                    if event.key == pygame.K_DOWN and direction != Direction.UP:
                        direction = Direction.DOWN
                        self.unpause()
                    print("INPUT KEY: ", direction)


            if not self.is_game_over():

                # MOVE
                if not self.is_paused() and not self.is_game_over():

                    # Agent turn
                    if self.is_auto():
                        action = self.session.agent.next_move()
                        
                        if action == Direction.STOP:
                            if self.engine.is_game_over(self.session):
                                self.status = self.GAME_OVER
                            else:
                                self.rotate_mode()
                                self.pause()
                    else:
                        action = direction
                        if self.engine.is_valid_action(self.session, action):
                            print("Manual action:", action)
                        else:
                            action = Direction.STOP
                            self.pause()




                    # Game Engine turn: Update Model
                    if not action == Direction.STOP:
                        status = self.engine.next_state(self.session, action)
                        print("snake_game.run :status", status)
                
                elif not self.is_game_over():
                    if self.engine.is_game_over(self.session):
                        self.status = self.GAME_OVER
                        print("GAME OVER")

                # DISPLAY
                self.ui.draw_ui()
                time.sleep( 1/ self.SPEED )


        self.end()
