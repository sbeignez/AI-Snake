import time
import pygame
from snake_game_session import *
from snake_engine import *
from snake_ui import *
# from snake import *
# from snake_agent_ai import AgentAI
import timeit


class Mode(enum.Enum):
    MODE_PLAY = "Mode: Visual sim"
    MODE_BENCHMARK = "Mode: Benchmark"
    MODE_TRAIN = "Trainning"



class GameParams():

    def __init__(self):

        self.BOARD_ROWS = 3
        self.BOARD_COLS = 3
        self.SCALE = 40

        self.SPEED = 30

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
        print("run:", self.params.mode)

        if self.params.mode == Mode.MODE_PLAY:
            self._run_play()
        elif self.params.mode == Mode.MODE_BENCHMARK:
            self._run_benchmark()
        elif self.params.mode == Mode.MODE_TRAIN:
            self._run_train()
        else:
            raise ValueError(f"Game.run(): Unvalid Mode '{self.params.mode}'")

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

                    if new_status in [self.GAME_OVER, self.GAME_WIN, self.GAME_PAUSED,]:
                        print(self.status)
                    if self.status in [self.GAME_PAUSED, self.GAME_OVER, self.GAME_WIN,]:
                        self.pause()

            # DISPLAY
            self.ui.draw_ui()
            self.clock.tick(self.params.SPEED)
            # time.sleep( 1/ self.params.SPEED )


        self.end()


    def _run_benchmark(self):
        print("_run_benchmark")

        n_epoch = 1000
        epochs = []
        start_time = timeit.default_timer()

        for e in range(n_epoch):
            if e % 10 == 0: print(f"Epic #{e}")
            self.session.create_session(self.params.agent)
            self.ui.get_keyboard_events()

            while True:
                action = self.session.agent.next_move()
                if action == Direction.STOP:
                    break
                new_status = self.engine.next_state(self.session, action)
                self.set_status(new_status)
                # self.ui.draw_ui()

            epochs.append({"n" : e, "length" : self.session.snake.len, "steps" : self.session.steps})
            
        stop_time = timeit.default_timer()
        execution_time = round(stop_time - start_time, 3) 

        
        avg_len = sum([ e["length"] for e in epochs ]) / n_epoch
        avg_steps = sum([ e["steps"] for e in epochs ]) / n_epoch
        print("=====================================")
        print(f"BENCHMARK: {self.session.agent.agent_type}")
        print(f"{n_epoch} epics in {execution_time}s")
        print(f"Avg Apples: {avg_len}")
        print(f"Avg Steps: {avg_steps}")
        print(f"Avg Steps/Apple: {avg_steps/avg_len}")

        # for e in epochs:
        #     print(f"{e['n']}, {e['length']}, {e['steps']}")

    def _run_train(self):
        print("_run_train: start")

        # Episode vs epoch vs batch ?
        n_episodes = 100_000
        win = 0
        apples = 0

        for e in range(n_episodes):

            if e % 100 == 0:
                print(f"Episode #{e}")

            epochs = 0
            
            self.status = self.GAME_RUN

            self.session.restart_game()
            # print(self.session.snake, self.session.apple)

            while self.status in [ self.GAME_RUN, self.GAME_RUN_EAT ]:

                # 1. AGENT PLAY
                old_state = self.session.agent.session_to_state()
                # print("Old State:", old_state)

                action = self.session.agent.next_move()
                # print("Action:", action)
                if action == Direction.STOP:
                    break

                # 2. ENGINE PLAY
                self.status = self.engine.next_state(self.session, action)
                # print(self.status, self.session.snake, self.session.apple)

                new_state = self.session.agent.session_to_state()
                # print("New State:", new_state)

                # 2.2 Agent update 
                self.session.agent.update_q_value(old_state, new_state, self.status, action)

                epochs += 1

            if e % 1000 == 0:
                self.ui.draw_ui()
                # time.sleep( 1/ self.params.SPEED )
            
            if self.status == self.GAME_WIN:
                win += 1

            if e % 10000 == 0:
                print(e, epochs, apples, "Win rate:", win/(e+1))

        print("_run_train: end")

        for key, value in self.session.agent.Qvalues.items():
            if not value == 0 :
                print(key, value)


