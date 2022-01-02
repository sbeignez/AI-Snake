import time
import pygame
from snake_game_session import *
from snake_engine import *
from snake_ui import *
# from snake import *
# from snake_agent_ai import AgentAI


class Mode(enum.Enum):
    MODE_PLAY = "Mode: Visual sim"
    MODE_BENCHMARK = "Mode: Benchmark"



class GameParams():

    def __init__(self):

        self.BOARD_ROWS = 3
        self.BOARD_COLS = 3
        self.SCALE = 40

        self.SPEED = 30

        self.agent = Agents.AGENT_A_STAR
        self.mode = Mode.MODE_PLAY



class Game():

    GAME_RUN = 2
    GAME_PAUSED = 1
    GAME_WON = 3
    GAME_OVER = 4

    MODE_AUTO = "Auto"

    def __init__(self, params):

        self.params = params
        self.engine = GameEngine(self)
        self.session = GameSession(self, params.agent, params.BOARD_COLS, params.BOARD_ROWS)
        self.ui = UI(self)
        
    best_score = 0
    game_played = 0

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
        self.session.create_session(self.params.agent)
    
    def end(self):
        pygame.quit()


    def run(self):
        print(self.params.mode)

        if self.params.mode == Mode.MODE_PLAY:
            self._run_play()
        elif self.params.mode == Mode.MODE_BENCHMARK:
            self._run_benchmark()
        else:
            print("run: unvalid mode")

    def _run_play(self):

        self.session.create_session(self.params.agent)

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

                    if event.key == pygame.K_LEFT:
                        direction = Direction.LEFT
                        self.unpause()
                    if event.key == pygame.K_RIGHT:
                        direction = Direction.RIGHT
                        self.unpause()
                    if event.key == pygame.K_UP:
                        direction = Direction.UP
                        self.unpause()
                    if event.key == pygame.K_DOWN:
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
                        if self.engine.is_valid_action(self.session, direction):
                            action = direction
                            print("Manual action:", action)
                        else:
                            action = Direction.STOP
                            self.pause()


                    # Game Engine turn: Update Model
                    if not action == Direction.STOP:
                        status = self.engine.next_state(self.session, action)
                        # print("snake_game.run :status", status)
                
                elif not self.is_game_over():
                    if self.engine.is_game_over(self.session):
                        self.status = self.GAME_OVER
                        print("GAME OVER")

                # DISPLAY
                self.ui.draw_ui()
                time.sleep( 1/ self.params.SPEED )


        self.end()


    def _run_benchmark(self):
        print("_run_benchmark")

        n_epics = 100
        epics = []
            # snake_length
            # steps
            # 

        for e in range(n_epics):
            if e % 100 == 0: print(f"Epic #{e}")

            self.session.create_session(self.params.agent)
            self.ui.draw_ui()

            while True:
                action = self.session.agent.next_move()
                if action == Direction.STOP:
                    break
                status = self.engine.next_state(self.session, action)
                self.ui.draw_ui()

            epics.append({"length" : self.session.snake.len(), "steps" : self.session.steps})
            
        print("=====================================")
        print(f"BENCHMARK: {self.session.agent.agent_type}")
        print(f"Epics: {n_epics}")
        print("Avg Lenght:", sum([ e["length"] for e in epics ]) / n_epics )
        print("Avg Steps:", sum([ e["steps"] for e in epics ]) / n_epics)


