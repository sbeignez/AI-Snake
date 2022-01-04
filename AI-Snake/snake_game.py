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

        self.SPEED = 20

        self.agent = Agents.AGENT_A_STAR
        self.mode = Mode.MODE_PLAY



class Game():

    GAME_RUN = 0
    GAME_RUN_EAT = 1
    GAME_PAUSED = 2
    GAME_WIN = 3
    GAME_OVER = 4

    MODE_AUTO = "Auto"

    clock = pygame.time.Clock()
    

    def __init__(self, params):

        self.params = params
        self.engine = GameEngine(self)
        self.session = GameSession(self, params.agent, params.BOARD_COLS, params.BOARD_ROWS)
        self.ui = UI(self)

        self.status = self.GAME_RUN
        self.running = "pause"
        self.quit = False
        
    best_score = 0
    game_played = 0

    def restart(self):
        self.session = GameSession(self, self.params.agent, self.session.board.cols, self.session.board.rows)
        self.session.create_session(self.params.agent)
        self.status = self.GAME_RUN

    

    def is_auto(self):
        return self.MODE_AUTO == "Auto"

    def rotate_mode(self):
        if self.is_auto():
            self.MODE_AUTO = "Manual"
        else:
            self.MODE_AUTO = "Auto"





    def set_status(self, status):
        self.status = status

    def is_game_over(self):
        return self.status == self.GAME_OVER

    def is_game_end(self):
        return self.is_game_over() or self.status == self.GAME_WIN


    def pause(self):
        self.running = "pause"

    def unpause(self):
        self.running = "run"

    def rotate_pause(self):
        if self.is_paused():
            self.unpause()
        else:
            self.pause()

    def is_paused(self):
        return self.run == "pause"
    
    def end(self):
        pygame.quit()


    def run(self):
        print(self.params.mode)

        if self.params.mode == Mode.MODE_PLAY:
            self._run_play()
        elif self.params.mode == Mode.MODE_BENCHMARK:
            self._run_benchmark()
        elif self.params.mode == Mode.TRAIN:
            self._run_train()
        else:
            print("run: unvalid mode")

    def _run_play(self):

        self.session.create_session(self.params.agent)

        # init game session
        direction = Direction.STOP

        # Run loop until user quits
        while not self.quit:

            self.ui.get_keyboard_events()

            if not self.is_game_end():

                # MOVE
                if not self.is_paused():

                    # 1. AGENT TURN
                    # 1.a AI Agent
                    if self.is_auto(): 
                        action = self.session.agent.next_move()
                        
                        
                    # 1.b Human Agent
                    else: 
                        action = self.ui.action_key

                        if not action or not self.engine.is_valid_action(self.session, action):
                            action = Direction.STOP
                        else:
                            print("Manual action:", action)


                    # 2. ENGINE turn: Update Model
                    # if action != Direction.STOP:
                    new_status = self.engine.next_state(self.session, action)
                    self.set_status(new_status)

                    if self.status in [self.GAME_PAUSED, self.GAME_OVER, self.GAME_WIN]:
                        self.pause()

            # DISPLAY
            self.ui.draw_ui()
            self.clock.tick(self.params.SPEED)
            # time.sleep( 1/ self.params.SPEED )


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

    def _run_train(self):
        print("_run_train")

        n_epics = 100
        epics = []
            # snake_length
            # steps
            # 

        for e in range(n_epics):
            if e % 100 == 0: print(f"Epic #{e}")

            self.session.create_session(self.params.agent)

            while True:
                action = self.session.agent.next_move()
                if action == Direction.STOP:
                    break
                status = self.engine.next_state(self.session, action)
                self.ui.draw_ui()

            epics.append({"length" : self.session.snake.len(), "steps" : self.session.steps})

