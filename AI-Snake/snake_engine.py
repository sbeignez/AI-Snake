import random
from snake_utils import *
from snake_game_session import Snake, Apple, GameSession


class GameEngine():

    GAME_RUN = 0
    GAME_RUN_EAT = 1
    GAME_PAUSED = 2
    GAME_WIN = 3
    GAME_OVER = 4

    def __init__(self, game):
        self.game = game

    def is_game_over(self, session):
        if self.is_game_win(session):
            return False
        moves_possible = [ Direction.add(session.snake.head(), d) for d in Direction.all_dirs()]
        game_over = not any([ self.is_valid_move(session, move) for move in moves_possible])
        return game_over

    def is_game_win(self, session: GameSession):
        return session.snake.len == session.board.size

    def is_valid_action(self, session, action):
        return self.is_valid_move(session, Direction.add(session.snake.head(), action))

    def is_valid_move(self, session, block):
        return self.is_valid_move_board(session, block) and self.is_valid_move_snake(session, block)

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
        


    def next_state(self, session: GameSession, action: Direction):

        new_head = Direction.add(session.snake.head(), action)
        
        # VALID MOVE - No COLLISION BOARD BODERS and BODY
        if self.is_valid_move(session, new_head):

            session.steps += 1

            # MOVE
            session.snake.append_head(new_head)
            
            if self.is_game_win(session):
                return self.GAME_WIN
            if self.is_game_over(session):
                return self.GAME_OVER

            is_apple: bool = ( new_head == session.apple.cell() )
            if is_apple:
                # eat apple
                self.game.engine.create_apple(session)
                session.score += 1
                return self.GAME_RUN_EAT 
            else:
                session.snake.pop_tail()
                return self.GAME_RUN

        # INVALID MOVE - Pause game, Chance to retry for Human agent
        else:
            #if self.game.mode == Game.Mode.MODE_PLAY:
            #     return self.GAME_PAUSED
            return self.GAME_OVER

