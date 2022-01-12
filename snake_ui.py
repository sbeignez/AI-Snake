# from _typeshed import Self
import pygame
import pygame.gfxdraw
from snake_utils import Direction

class UI():

    # UI DEFAULTS
    WINDOW_SCORE = 300

    FONT_SIZE = 20
    PADDING = 5

    # UI COLORS
    COLOR_BOARD = (20, 20, 20)
    COLOR_APPLE = (200, 0, 0)
    COLOR_CELL = (40, 40, 44)
    COLOR_CELL_EVEN = (30, 30, 34)
    COLOR_CELL_ODD = (36, 36, 40)
    COLOR_SNAKE = (200, 200, 0)
    COLOR_SNAKE_2 = (150, 150, 0)
    COLOR_SNAKE_SPINE = (40, 40, 0)
    COLOR_PAUSE = (200, 200, 200)
    COLOR_SCORE = (200, 200, 200)
    COLOR_MOVE_BEST = (30, 30, 200)
    COLOR_MOVES = (30, 30, 100)

    def __init__(self, game):

        self.game = game

        self.rows = game.session.board.rows
        self.cols = game.session.board.cols
        self.scale = game.params.SCALE

        self.window_x_px = self.cols * self.scale + self.WINDOW_SCORE
        self.window_y_px = self.rows * self.scale

        pygame.init()
        pygame.display.set_caption('Snake Challenge 2022')
        self.window = pygame.display.set_mode( (self.window_x_px , self.window_y_px) )
        
        self.erase_ui()
        pygame.display.update()
        
        keys = [pygame.KEYDOWN, pygame.QUIT]
        pygame.event.set_blocked(None)
        pygame.event.set_allowed(keys)
        pygame.event.get()
        self.action_key = None


    def draw_ui(self):

        # Erase
        self.erase_ui()

        # Draw UI elements
        self.draw_board()
        if self.game.is_auto():
            self.draw_paths(self.game.session.agent.paths)
        self.draw_snake(self.game.session.snake)
        self.draw_apple(self.game.session.apple)

        if self.game.is_game_over():
            self.draw_game_over()
        elif self.game.is_paused():
            self.draw_pause()

        self.draw_score()

        # Update Diplay
        pygame.display.update()


    def erase_ui(self):
        pygame.display.get_surface().fill(self.COLOR_BOARD)


    def draw_board(self):
        for r in range(self.rows):
            for c in range(self.cols):
                color = self.COLOR_CELL_EVEN if ((r + c) % 2) == 0 else self.COLOR_CELL_ODD
                self.draw_cell(c, r, color)

    def draw_cell(self, x, y, color):
        pygame.draw.rect(self.window, color, pygame.Rect(x * self.scale, y * self.scale, self.scale, self.scale))
        pygame.draw.rect(self.window, self.COLOR_CELL, pygame.Rect(x * self.scale, y * self.scale, self.scale, self.scale),1)

    def draw_apple(self, apple):
        x, y = apple.x, apple.y
        if x and y:
            pygame.draw.circle(self.window, self.COLOR_APPLE, ((x-.5) * self.scale, (self.rows - y +.5) * self.scale), (self.scale * .8)/2, 0)

    def draw_pause(self):
        rect1 = pygame.Rect(self.cols * self.scale / 3, self.rows * self.scale / 3, self.cols * self.scale / 9, self.rows * self.scale / 3)
        rect2 = pygame.Rect(self.cols * self.scale * 5 / 9, self.rows * self.scale / 3, self.cols * self.scale / 9, self.rows * self.scale / 3)
        
        pygame.gfxdraw.box(self.window, rect1, (*self.COLOR_PAUSE, 150))
        pygame.gfxdraw.box(self.window, rect2, (*self.COLOR_PAUSE, 150))
        pygame.draw.rect(self.window, self.COLOR_PAUSE, rect1, 1)
        pygame.draw.rect(self.window, self.COLOR_PAUSE, rect2, 1)

    def draw_game_over(self):
        rect1 = pygame.Rect(self.cols * self.scale / 3, self.rows * self.scale / 3, self.cols * self.scale / 3, self.rows * self.scale / 3)
        pygame.gfxdraw.box(self.window, rect1, (*self.COLOR_PAUSE, 150))
        pygame.draw.rect(self.window, self.COLOR_PAUSE, rect1, 1)

    def draw_snake(self, snake):
        x_0, y_0 = None, None
        L = len(snake.body)
        for i, s in enumerate(snake.body):
            x, y = s[0], s[1]
            # pygame.draw.circle(window, color, ((y+.5) * scale, (x+.5) * scale ), R, 0)
            pygame.draw.rect(self.window, self.COLOR_SNAKE if i==L-1 else self.COLOR_SNAKE_2, pygame.Rect((x-1) * self.scale + 1, (self.rows - y) * self.scale + 1, self.scale - 2, self.scale - 2), 0, border_radius= 1)
            if x_0 is not None:
                pygame.draw.line(self.window, self.COLOR_SNAKE_SPINE, (((x_0-1)+.5)*self.scale,((self.rows-y_0)+.5)*self.scale), (((x-1)+.5)*self.scale, ((self.rows-y)+.5)*self.scale,), 4)
            x_0, y_0 = x, y

    def draw_paths(self, paths):
        if paths:
            for path in paths:
                for i, move in enumerate(path):
                    x, y = move[0], move[1]
                    pygame.draw.rect(self.window, self.COLOR_MOVE_BEST if i==0 else self.COLOR_MOVES, pygame.Rect((x-1) * self.scale + 1, (self.rows - y) * self.scale + 1, self.scale - 2, self.scale - 2), 0, border_radius= 1)

    def draw_score(self):
        font = pygame.font.SysFont('Courier', self.FONT_SIZE, bold=True)

        texts = [
            "SNAKE CHALLENGE",
            "MOVES: " + ("(" + str(self.game.session.steps_since_last) + ") "+ str(self.game.session.steps)).rjust(8),
            "SCORE: " + ("        " + str(self.game.session.score))[-8:],
            "MODE: " + self.game.MODE_AUTO,
            "AGENT: " + self.game.session.agent.agent_type.value,
            "PAUSED" if self.game.is_paused() else "",
            "GAME-OVER" if self.game.is_game_over() else "",
        ]

        for line_number, text in enumerate(texts):
            self.window.blit(font.render(text, True, self.COLOR_SCORE), (self.cols * self.scale + self.PADDING, self.PADDING + 25 * line_number))



    def get_keyboard_events(self):

            for event in pygame.event.get():

                if event.type == pygame.QUIT:
                    self.game.quit = True
                if event.type == pygame.KEYDOWN:
                    # TAB: Restart game
                    if event.key == pygame.K_TAB:
                        print("Restart()")
                        self.game.restart()
                    # SPACE: Pause game
                    if event.key == pygame.K_SPACE:
                        print("Rotate_pause()")
                        self.game.rotate_pause()
                    # DELETE: Rewind 1 step
                    if event.key == pygame.K_DELETE:
                        pass
                        #rewind()
                    # /?: INFO
                    if event.key == pygame.K_SLASH:
                        print(self.game.session.snake)
                        print(self.game.session.apple)
                        print("status", self.game.status)
                        print("running", self.game.running)
                    # SHIFT: Manual/Auto mode
                    if event.key == pygame.K_LSHIFT:
                        self.game.rotate_mode()

                    # USER ACTION
                    if self.game.MODE_AUTO == "Manual" and not self.game.is_game_over():
                        self.action_key = None

                        if event.key == pygame.K_LEFT:
                            self.action_key = Direction.LEFT
                        elif event.key == pygame.K_RIGHT:
                            self.action_key = Direction.RIGHT
                        elif event.key == pygame.K_UP:
                            self.action_key = Direction.UP
                        elif event.key == pygame.K_DOWN:
                            self.action_key = Direction.DOWN

                        print("INPUT KEY: ", self.action_key)



if __name__ == '__main__':
    pass