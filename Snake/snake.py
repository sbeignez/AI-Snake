import pygame
import time
import random
import sys
import enum
from collections import namedtuple

# GAME DEFAULTS
SPEED = 50
BOARD_ROWS = 20
BOARD_COLS = 20
SCALE = 30
# COLORS
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

MODE_AUTO = False

# Direction Enum
class Direction(enum.Enum):
   UP = (0,1)
   DOWN = (0,-1)
   RIGHT = (1,0)
   LEFT = (-1,0)
   STOP = (0,0)



class SnakeGame():
    pass
    # board
    # snake
    #   Block = namedtuple('Block', 'x, y')
    # apple
    # steps, score

    # def nextMove(Direction) -> 
    # retrun: incorrect move, game over, victory

    # def _create_new_apple()
    # def _log games and moves

class AgentHuman():
    pass

class AgentAI():
    pass
    # multiple strategies


def display_board(window, board):

    pygame.display.get_surface().fill(COLOR_BOARD)

    font = pygame.font.SysFont('Courier', int(SCALE / 2), bold=True)
    score = "SCORE: " + ("0000" + str(board["score"]))[-4:] + " - MOVES: " + ("0000000" + str(board["steps"]))[-7:]

    draw_board(window)
    if board["pause"]:
        draw_pause(window)
    draw_moves(window, board["moves"])
    draw_snake(window, board["snake"])
    draw_apple(window, board["apple"][0], board["apple"][1], COLOR_APPLE)
    draw_score(window, font, score)


    pygame.display.update()

def draw_board(window):
    for r in range(BOARD_ROWS):
        for c in range(BOARD_COLS):
            draw_cell(window, r, c, COLOR_CELL_EVEN if ((r + c) % 2) == 0 else COLOR_CELL_ODD)

def draw_cell(window, x, y, color):
    pygame.draw.rect(window, color, pygame.Rect(x * SCALE, y * SCALE, SCALE, SCALE))
    pygame.draw.rect(window, COLOR_CELL, pygame.Rect(x * SCALE, y * SCALE, SCALE, SCALE),1)

def draw_apple(window, x, y, color):
    pygame.draw.circle(window, color, ((x-.5) * SCALE, (BOARD_ROWS - y +.5) * SCALE), (SCALE * .8)/2, 0)

def draw_pause(window):
    pygame.draw.rect(window, COLOR_PAUSE, pygame.Rect(BOARD_COLS * SCALE / 3, BOARD_ROWS * SCALE / 3, BOARD_COLS * SCALE / 9, BOARD_ROWS * SCALE / 3))
    pygame.draw.rect(window, COLOR_PAUSE, pygame.Rect(BOARD_COLS * SCALE * 5 / 9, BOARD_ROWS * SCALE / 3, BOARD_COLS * SCALE / 9, BOARD_ROWS * SCALE / 3))

def draw_snake(window, snake, color = COLOR_SNAKE):
    x_0, y_0 = None, None
    body = snake["body"]
    L = len(body)
    for i, s in enumerate(body):
        x, y = s[0], s[1]
        # pygame.draw.circle(window, color, ((y+.5) * SCALE, (x+.5) * SCALE ), R, 0)
        pygame.draw.rect(window, color if i==L-1 else COLOR_SNAKE_2, pygame.Rect((x-1) * SCALE + 1, (BOARD_ROWS - y) * SCALE + 1, SCALE - 2, SCALE - 2), 0, border_radius= 1)
        if x_0 is not None:
            pygame.draw.line(window, COLOR_SNAKE_SPINE, (((x_0-1)+.5)*SCALE,((BOARD_ROWS-y_0)+.5)*SCALE), (((x-1)+.5)*SCALE, ((BOARD_ROWS-y)+.5)*SCALE,), 4)
        x_0, y_0 = x, y

def draw_moves(window, moves):
    if MODE_AUTO and moves:
        for i, move in enumerate(moves):
            x, y = move[0], move[1]
            pygame.draw.rect(window, COLOR_MOVE_BEST if i==0 else COLOR_MOVES, pygame.Rect((x-1) * SCALE + 1, (BOARD_ROWS - y) * SCALE + 1, SCALE - 2, SCALE - 2), 0, border_radius= 1)

def draw_score(window, font, score):
    window.blit(font.render(score, True, COLOR_SCORE), (0, (SCALE+.5) * BOARD_ROWS))

def is_game_over(board):
    return False


def create_apple(snake):
    if len(snake["body"]) == BOARD_ROWS * BOARD_COLS:
        return None
    cells = { (c+1,r+1) for r in range(BOARD_ROWS) for c in range(BOARD_COLS) } - set(snake["body"]) 
    apple = random.choice(tuple(cells))
    print("APPLE (NEW):", apple)
    return apple

def init_board():
    snake = {
        "body" : [(BOARD_COLS//2,BOARD_ROWS//2)],
        "lenght" : 3,
    }
    apple = create_apple(snake)
    board = {
        "apple" : apple,
        "snake" : snake,
        "pause" : False,
        "score" : 0,
        "steps" : 0,
        "moves" : None,
        "move"  : None,
    }
    return board

def move(board):
    apple = board["apple"]
    moves = []
    body = board["snake"]["body"]
    head = body[-1]
    # DOWN
    if head[1] > 1 and (head[0], head[1]-1) not in body:
        moves.append((head[0], head[1]-1))
    # UP
    if head[1] < BOARD_ROWS and (head[0], head[1]+1) not in body:
        moves.append((head[0], head[1]+1))
    # RIGHT
    if head[0] < BOARD_COLS and (head[0]+1, head[1]) not in body:
        moves.append((head[0]+1, head[1]))
    # LEFT
    if head[0] > 1 and (head[0]-1, head[1]) not in body:
        moves.append((head[0]-1, head[1]))

    print("BODY:", body, "APPLE:", apple)
    moves.sort( key = lambda x : abs(x[0] - apple[0]) + abs(x[1] - apple[1]), reverse = False)
    print("MOVES:", moves)

    # move = min(moves, key = lambda x : abs(x[0] - apple[0]) + abs(x[1] - apple[1]))

    return moves

def start_game():
    window_x_px , window_y_px = BOARD_COLS * SCALE, BOARD_ROWS * SCALE + SCALE

    pygame.init()
    pygame.display.set_caption('Snake A.I. 2022')
    window = pygame.display.set_mode( (window_x_px , window_y_px) )
    
    board = init_board()
    snake = board["snake"]
    direction = Direction.STOP
    global MODE_AUTO

    # waint until user quits
    running, game_over, board["steps"] = True, False, 0
    while running:

        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                running = False
            if event.type == pygame.KEYDOWN:
                # TAB: Restart game
                if event.key == pygame.K_TAB:
                    start_game()
                # SPACE: Pause game
                if event.key == pygame.K_SPACE:
                    board["pause"] = not board["pause"]
                # DELETE: Rewind 1 step
                if event.key == pygame.K_DELETE:
                    pass
                    #rewind()
                # SHIFT: Manual/Auto mode
                if event.key == pygame.K_LSHIFT:
                    MODE_AUTO = not MODE_AUTO

                if event.key == pygame.K_LEFT and direction != Direction.RIGHT:
                    direction = Direction.LEFT
                    board["pause"] = False
                if event.key == pygame.K_RIGHT and direction != Direction.LEFT:
                    direction = Direction.RIGHT
                    board["pause"] = False
                if event.key == pygame.K_UP and direction != Direction.DOWN:
                    direction = Direction.UP
                    board["pause"] = False
                if event.key == pygame.K_DOWN and direction != Direction.UP:
                    direction = Direction.DOWN
                    board["pause"] = False
                print("INPUT KEY: ", event.key, direction)

        # MOVE
        if not board["pause"]:
            
            if MODE_AUTO:
                if board["moves"]:
                    direction = Direction( ( board["moves"][0][0] - snake["body"][-1][0], board["moves"][0][1] - snake["body"][-1][1]))
                    print("DIRECTION (AUTO):", direction)
                else:
                    game_over = True

            new_head = (snake["body"][-1][0] + direction.value[0], snake["body"][-1][1] + direction.value[1])
            
            # COLLISION BOARD BODERS
            if new_head[0] < 1 or new_head[0] > BOARD_COLS or new_head[1] < 1 or new_head[1] > BOARD_ROWS:
                board["pause"] = True
            # COLLISION BODY
            elif new_head in snake["body"]:
                board["pause"] = True
            # OKAY: GROW
            else:
                snake["body"].append(new_head)
                snake["body"] = snake["body"][- snake["lenght"]:]
                board["steps"] += 1


            # EAT APPLE
            if new_head == board["apple"]:
                if len(snake["body"]) == BOARD_ROWS * BOARD_COLS:
                    print("VICTORY")
                board["apple"] = create_apple(snake)
                snake["lenght"] += 1
                board["score"] += 1

            # print(board["snake"], board["apple"]) 

            if MODE_AUTO:
                board["moves"] = move(board)

        display_board(window, board)
        time.sleep( 1/ SPEED )
        



    pygame.quit()



start_game()