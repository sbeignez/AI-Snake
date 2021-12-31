# from _typeshed import Self
import pygame
import pygame.gfxdraw
# from snake import *

class UI():

    # UI DEFAULTS
    SCALE = 40
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

    def __init__(self, game, cols, rows):

        self.game = game
        self.rows = rows
        self.cols = cols

        self.window_x_px = cols * self.SCALE + self.WINDOW_SCORE
        self.window_y_px = rows * self.SCALE

        pygame.init()
        pygame.display.set_caption('Snake Challenge 2022')
        self.window = pygame.display.set_mode( (self.window_x_px , self.window_y_px) )


    def draw_ui(self):

        # Erase
        self.erase_ui()

        # Draw UI elements
        self.draw_board()
        if self.game.is_auto():
            self.draw_paths(self.game.session.agent.paths)
        self.draw_snake(self.game.session.snake)
        self.draw_apple(self.game.session.apple)
        self.draw_score()
        if self.game.is_paused():
            self.draw_pause()

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
        pygame.draw.rect(self.window, color, pygame.Rect(x * self.SCALE, y * self.SCALE, self.SCALE, self.SCALE))
        pygame.draw.rect(self.window, self.COLOR_CELL, pygame.Rect(x * self.SCALE, y * self.SCALE, self.SCALE, self.SCALE),1)

    def draw_apple(self, apple):
        x, y = apple.x, apple.y
        pygame.draw.circle(self.window, self.COLOR_APPLE, ((x-.5) * self.SCALE, (self.rows - y +.5) * self.SCALE), (self.SCALE * .8)/2, 0)

    def draw_pause(self):
        rect1 = pygame.Rect(self.cols * self.SCALE / 3, self.rows * self.SCALE / 3, self.cols * self.SCALE / 9, self.rows * self.SCALE / 3)
        rect2 = pygame.Rect(self.cols * self.SCALE * 5 / 9, self.rows * self.SCALE / 3, self.cols * self.SCALE / 9, self.rows * self.SCALE / 3)
        
        pygame.gfxdraw.box(self.window, rect1, (*self.COLOR_PAUSE, 150))
        pygame.gfxdraw.box(self.window, rect2, (*self.COLOR_PAUSE, 150))
        pygame.draw.rect(self.window, self.COLOR_PAUSE, rect1, 1)
        pygame.draw.rect(self.window, self.COLOR_PAUSE, rect2, 1)

    def draw_game_over(self):
        rect1 = pygame.Rect(self.cols * self.SCALE / 3, self.rows * self.SCALE / 3, self.cols * self.SCALE / 3, self.rows * self.SCALE / 3)
        pygame.gfxdraw.box(self.window, rect1, (*self.COLOR_PAUSE, 150))
        pygame.draw.rect(self.window, self.COLOR_PAUSE, rect1, 1)

    def draw_snake(self, snake):
        x_0, y_0 = None, None
        L = len(snake.body)
        for i, s in enumerate(snake.body):
            x, y = s[0], s[1]
            # pygame.draw.circle(window, color, ((y+.5) * SCALE, (x+.5) * SCALE ), R, 0)
            pygame.draw.rect(self.window, self.COLOR_SNAKE if i==L-1 else self.COLOR_SNAKE_2, pygame.Rect((x-1) * self.SCALE + 1, (self.rows - y) * self.SCALE + 1, self.SCALE - 2, self.SCALE - 2), 0, border_radius= 1)
            if x_0 is not None:
                pygame.draw.line(self.window, self.COLOR_SNAKE_SPINE, (((x_0-1)+.5)*self.SCALE,((self.rows-y_0)+.5)*self.SCALE), (((x-1)+.5)*self.SCALE, ((self.rows-y)+.5)*self.SCALE,), 4)
            x_0, y_0 = x, y

    def draw_paths(self, paths):
        if paths:
            for path in paths:
                for i, move in enumerate(path):
                    x, y = move[0], move[1]
                    pygame.draw.rect(self.window, self.COLOR_MOVE_BEST if i==0 else self.COLOR_MOVES, pygame.Rect((x-1) * self.SCALE + 1, (self.rows - y) * self.SCALE + 1, self.SCALE - 2, self.SCALE - 2), 0, border_radius= 1)

    def draw_score(self):
        font = pygame.font.SysFont('Courier', self.FONT_SIZE, bold=True)

        texts = [
            "SNAKE CHALLENGE",
            "MOVES: " + ("        " + str(self.game.session.steps))[-8:],
            "SCORE: " + ("        " + str(self.game.session.score))[-8:],
            "",
            "MODE: " + self.game.MODE_AUTO,
            "PAUSED" if self.game.is_paused() else "",
            "GAME-OVER" if self.game.is_game_over() else "",
        ]

        for line_number, text in enumerate(texts):
            self.window.blit(font.render(text, True, self.COLOR_SCORE), (self.cols * self.SCALE + self.PADDING, self.PADDING + 25 * line_number))



if __name__ == '__main__':
    pass