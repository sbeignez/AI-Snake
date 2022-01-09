import time
import pygame
from snake_game_session import *
from snake_engine import *
from snake_ui import *
# from snake import *
# from snake_agent_ai import AgentAI
import timeit




class GameParams():

    def __init__(self):

        self.BOARD_ROWS = 3
        self.BOARD_COLS = 3
        self.SCALE = 40

        self.SPEED = 30

        self.agent = Agents.AGENT_A_STAR
        self.mode = Game.Mode.MODE_PLAY

        self.log = False



class Game():

    class Mode(enum.Enum):
        MODE_PLAY = "Mode: Visual sim"
        MODE_BENCHMARK = "Mode: Benchmark"
        MODE_TRAIN = "Trainning"

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

        if self.params.mode == Game.Mode.MODE_PLAY:
            self._run_play()
        elif self.params.mode == Game.Mode.MODE_BENCHMARK:
            self._run_benchmark()
        elif self.params.mode == Game.Mode.MODE_TRAIN:
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
                    new_status, _, _, _ = self.engine.step(self.session, action)
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


    def _run_benchmark(self, n_episodes = 100):
        print("="*40)
        print("_run_benchmark")

        history = []
        n_episodes_split = n_episodes // 10

        self.session.create_session(self.params.agent)
        self.ui.get_keyboard_events()

        start_time = timeit.default_timer()

        for i_episode in range(n_episodes):
            if i_episode % n_episodes_split == 0:
                print(f"Episode #{i_episode}")
                self.ui.draw_ui()

            self.engine.reset()

            while True:
                action = self.session.agent.next_move()
                new_status, reward, done, info = self.engine.step(self.session, action)
                self.set_status(new_status)
                if done:
                    break
            

            history.append({"n" : i_episode, "length" : self.session.snake.len, "steps" : self.session.steps})
            
        stop_time = timeit.default_timer()
        execution_time = round(stop_time - start_time, 3) 

        
        avg_len = sum([ e["length"] for e in history ]) / n_episodes
        avg_steps = sum([ e["steps"] for e in history ]) / n_episodes
        print("="*40)
        print(f"BENCHMARK: {self.session.agent.agent_type}")
        print(f"{n_episodes} episodes in {execution_time}s")
        print(f"Avg Apples: {avg_len}")
        print(f"Avg Steps: {avg_steps}")
        print(f"Avg Steps/Apple: {avg_steps/avg_len}")

        # for e in history:
        #     print(f"{e['n']}, {e['length']}, {e['steps']}")

    def _run_train(self):
        print("_run_train: start")

        # Episode vs epoch vs batch ?
        n_episodes = 3_000
        n_episodes_split = n_episodes // 10 + 1
        win = 0
        apples = 0

        for e in range(n_episodes):

            if self.params.log: print("="*40)

            if e % n_episodes_split == 0:
                print(f"Episode #{e}")

            timesteps = 0
            history = []
            
            self.status = self.GAME_RUN
            self.session.restart_game()
            

            while self.status in [ self.GAME_PAUSED, self.GAME_RUN, self.GAME_RUN_EAT ]:

                # print(self.session.snake, self.session.apple)
                if self.params.log: print(self.session.agent.render_text())

                # 1. AGENT PLAY
                old_state = self.session.agent.session_to_state()
                # print("Old State:", old_state, self.session.snake, self.session.apple)

                action = self.session.agent.next_move()
                # if self.log: print("Action:", action)
                # if action == Direction.STOP:
                #     break
                history.append(action)

                # 2. ENGINE PLAY
                self.status, _, done, _ = self.engine.step(self.session, action)
                if self.params.log: print("STATUS", self.status, self.session.snake, self.session.apple)

                new_state = self.session.agent.session_to_state()
                # print("New State:", new_state)

                # 2.2 Agent update 
                self.session.agent.update_q_value(old_state, new_state, self.status, action)
                
                if self.params.log: self.session.agent.print_Q(state = old_state)

                timesteps += 1

                if self.params.log: print("-"*40)

            if e % n_episodes_split == 0:
                print(history)
                # print(self.session.agent.render_text())
                # self.ui.draw_ui()
                # time.sleep( 1/ self.params.SPEED )
            
            if self.status == self.GAME_WIN:
                win += 1

            if e % n_episodes_split == 0:
                print("#:", e, timesteps, "Apples:", apples, "Win rate:", win/(e+1))

        print("_run_train: end")
        self.session.agent.print_Q()

        self._run_train_play()


    def _run_train_play(self):

        self.session.agent.epsilon = 0

        n_episodes = 4
        n_episodes_split = n_episodes // 10

        self.ui.get_keyboard_events()

        for i_episode in range(n_episodes):

            self.engine.reset()

            while True:
                self.ui.draw_ui()
                self.clock.tick(self.params.SPEED)

                action = self.session.agent.next_move()
                new_status, reward, done, info = self.engine.step(self.session, action)
                self.set_status(new_status)
                if done:
                    break        


