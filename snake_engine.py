from typing import Optional

import gym
from gym import spaces, logger

import random
from snake_utils import *
from snake_game_session import Snake, Apple, GameSession
from snake_core import Env


class GameEngine(Env):
    """
        Description:
            Snake...
        Source:
            ...
        Observation:
            Type: Box(4)
            Num     Observation               Min                     Max
            0       Cart Position             -2.4                    2.4
            1       Cart Velocity             -Inf                    Inf
            2       Pole Angle                -0.209 rad (-12 deg)    0.209 rad (12 deg)
            3       Pole Angular Velocity     -Inf                    Inf
        Actions:
            Type: Discrete(5)
            Num   Action
            0     PAUSE
            1     UP
            2     ..
            3     ..
            4     ..
            Note: ..
        Reward:
            Reward is ...
        Starting State:
            ..
        Episode Termination:
            GAME OVER
                Snake hit wall.
                Snake hit its own body.
                Snake is in a loop: Episode lenght is greater than .. TODO
            GAME WIN:
            When snake len = board size
        """
    GAME_RUN = 0
    GAME_RUN_EAT = 1
    GAME_PAUSED = 2
    GAME_WIN = 3
    GAME_OVER = 4

    def __init__(self, game):
        self.game = game

        self.action_space = spaces.Discrete(5)
        # self.observation_space = spaces.Box(-high, high, dtype=np.float32)
        
    def reset(self, seed: Optional[int] = None):
        # super().reset(seed=seed)

        self.init_snake(self.game.session)
        self.create_apple(self.game.session)
        self.game.session.reset()

    def step(self, session: GameSession, action: Direction):

        err_msg = f"{action!r} ({type(action)}) invalid"
        # assert self.action_space.contains(action), err_msg

        obs, reward, done, info = None, 0, False, {}

        new_head = Direction.add(session.snake.head(), action)
        
        # VALID MOVE - No COLLISION BOARD BODERS and BODY
        if self.is_valid_move(session, new_head):

            

            # MOVE
            session.snake.append_head(new_head)
            session.steps += 1
            session.steps_since_last += 1
            
            if self.is_game_win(session):
                obs = self.GAME_WIN
                done = True
                reward = 10
            elif self.is_game_over(session):
                obs = self.GAME_OVER
                done = True
            else:
                is_apple: bool = ( new_head == session.apple.cell() )
                if is_apple:
                    # eat apple
                    self.game.engine.create_apple(session)
                    session.score += 1
                    session.steps_since_last = 0
                    obs = self.GAME_RUN_EAT
                    reward = 1
                else:
                    session.snake.pop_tail()
                    obs = self.GAME_RUN

        # INVALID MOVE - Pause game, Chance to retry for Human agent
        else:
            #if self.game.mode == Game.Mode.MODE_PLAY:
            #     return self.GAME_PAUSED
            obs = self.GAME_OVER
            done = True

        return obs, reward, done, info

    def is_game_over(self, session):
        if self.is_game_win(session):
            return False
        if self.game.session.steps_since_last > 2 * self.game.session.board.size:
            return True
        moves_possible = [ Direction.add(session.snake.head(), d) for d in Direction.all_dirs()]
        game_over = not any([ self.is_valid_move(session, move) for move in moves_possible])
        return game_over

    def is_game_win(self, session: GameSession):
        return session.snake.len == session.board.size

    def is_valid_action(self, session, action):
        return self.is_valid_move(session, Direction.add(session.snake.head(), action))

    def is_valid_move(self, session, block):
        return self.is_valid_move_snake(session, block) and self.is_valid_move_board(session, block)

    def is_valid_move_board(self, session, block):
        return block[0] >= 1 and block[0] <= session.board.cols and block[1] >= 1 and block[1] <= session.board.rows

    def is_valid_move_snake(self, session, block):
        return block not in session.snake.body



    def init_snake(self, session):
        """ Rules to initialize the snake. Options:
        # 1. Random
        # 2. Head in center, Tail upward
        """
        # 1.
        session.snake = Snake([(random.randint(1, self.game.session.board.cols), random.randint(1, self.game.session.board.rows),)])
        # 2.
        n = 2
        snake_body = [ ((session.board.cols+1)//2, (session.board.rows+1)//2 + (n-1) - i) for i in range(n) ]
        # print("Engine.init_snake()", snake_body)
        session.snake = Snake(snake_body)



    def create_apple(self, session):
        """ Create new apple randomly
        Exclude cells with snake body
        """

        if session.snake.len == session.board.size:
            return None
        cells = { (c,r) for r in range(1, session.board.rows+1) for c in range(1, session.board.cols + 1) } - set(session.snake.body) 
        
        if len(cells) != 0:
            apple = Apple(* random.choice(tuple(cells)))
            session.apple = apple
        else:
            print("Engine.create_apple(): error")
            print("cells", cells, session.snake.len(), session.board.size, session.snake, session.apple)

        # print("Engine.create_apple()", apple)

    def close(self):
        pass

    def seed(self, seed=None):
        pass

    def render(self, mode='human', close=False):
        pass

    def configure(self, *args, **kwargs):
        pass

def demo_game_engine(env, seed=None, render=False):
    print("TODO")
    pass



if __name__ == "__main__":
    demo_game_engine(GameEngine(), render=True)