import pygame as pg
import sys
import time

# TODO:
# . Реализовать правила для клеток
# . Реализовать игровое поле и его обновление
# . Реализовать размещение клеток курсором (перед симуляцией поле пустое!)
# . Реализовать паузу
# . Реализовать скорость симуляции

# ==== ПРАВИЛА ====
# клетка "смотрит" на 8 соседей рядом с собой
# 1) у живой меньше 2 живых соседей - смерть
# 2) у живой 2-3 живых соседа - ничего
# 3) у живой больше 3 живых соседей - смерть
# 4) у мертвой ровно 3 живых соседа - жизнь


# ==== НАЧАЛЬНЫЕ ПАРАМЕТРЫ ====
SQUARE_SIDE = 30
W = 20*SQUARE_SIDE + 2*SQUARE_SIDE # [W]idth or [H]eight = (amount of cells inside of red area in [W]idth/[H]eight) * SQUARE_SIDE + (magic value) 
H = 20*SQUARE_SIDE + 2*SQUARE_SIDE

ROWS = H//SQUARE_SIDE
COLS = W//SQUARE_SIDE

GREY = (32, 32, 32)
ORANGE = (255, 150, 0)
BLUE = (0, 150, 255)
RED = (255, 0, 0)
BLACK = (0,0,0)
WHITE = (255,255,255)

# ==== ФУНКЦИИ ====

def update_field(field_before: list, field_after: list):
    """Updates cells on the field."""
    counter = 0
    for row in range(1, ROWS):
        for col in range(1, COLS):
            if field_before[row-1][col]: counter += 1
            if field_before[row+1][col]: counter += 1
            if field_before[row][col-1]: counter += 1
            if field_before[row][col+1]: counter += 1
            if field_before[row-1][col-1]: counter += 1
            if field_before[row-1][col+1]: counter += 1
            if field_before[row+1][col-1]: counter += 1
            if field_before[row+1][col+1]: counter += 1

            if field_before[row][col]:
                if counter < 2: field_after[row][col] = 0
                elif counter > 3: field_after[row][col] = 0
            else:
                if counter == 3: field_after[row][col] = 1
            

def draw_grid():
    """Draws a grid and a boundary over field."""
    # Draws horizontal lines
    for i in range(2, H//SQUARE_SIDE - 1):
        pg.draw.line(screen, GREY, (SQUARE_SIDE, i*SQUARE_SIDE), (W-SQUARE_SIDE, i*SQUARE_SIDE))
    # Draws vertical lines
    for i in range(2, W//SQUARE_SIDE - 1):
        pg.draw.line(screen, GREY, (i*SQUARE_SIDE, SQUARE_SIDE), (i*SQUARE_SIDE, H-SQUARE_SIDE))
    
    # red lines
    pg.draw.line(screen, RED, (SQUARE_SIDE, SQUARE_SIDE), (W - SQUARE_SIDE, SQUARE_SIDE))
    pg.draw.line(screen, RED, (SQUARE_SIDE, SQUARE_SIDE), (SQUARE_SIDE, H - SQUARE_SIDE))
    pg.draw.line(screen, RED, (SQUARE_SIDE, H - SQUARE_SIDE), (W - SQUARE_SIDE, H - SQUARE_SIDE))
    pg.draw.line(screen, RED, (W - SQUARE_SIDE, SQUARE_SIDE), (W - SQUARE_SIDE, H - SQUARE_SIDE))

def matrix_visualizer(matrix: list):
    """Converts 1's in a matrix into colored squares"""
    for row in range(1, ROWS):
        for col in range(1, COLS):
            if matrix[row][col]:
                r = pg.Rect(col*SQUARE_SIDE, row*SQUARE_SIDE, SQUARE_SIDE, SQUARE_SIDE)
                pg.draw.rect(screen, BLUE, r)

def put_cell(pos: tuple, matrix: list):
    """Puts a cell on the screen upon mouse click."""
    if matrix[pos[1]//SQUARE_SIDE][pos[0]//SQUARE_SIDE] == 0: matrix[pos[1]//SQUARE_SIDE][pos[0]//SQUARE_SIDE] = 1
    else: matrix[pos[1]//SQUARE_SIDE][pos[0]//SQUARE_SIDE] = 0


pg.init()
screen = pg.display.set_mode((W, H))
# r = pg.Rect(SQUARE_SIDE, SQUARE_SIDE, SQUARE_SIDE, SQUARE_SIDE)
#               ^                ^
#              x-pos            y-pos

field_before = [[0 for _ in range(ROWS+1)] for _ in range(COLS+1)]
field_after = [[0 for _ in range(ROWS+1)] for _ in range(COLS+1)]

pause = True

while True:
    for event in pg.event.get():
        if event.type == pg.QUIT:
            pg.quit()
            sys.exit()
        elif event.type == pg.MOUSEBUTTONDOWN:
            # (x,y) = (col, row)
            put_cell(event.pos, field_before)
            matrix_visualizer(field_before)
        elif event.type == pg.K_SPACE:
            pause = False if pause else True

    if pause:
        screen.fill(BLACK)
        matrix_visualizer(field_before)
        draw_grid()
        pg.display.flip()
    else:
        update_field(field_before, field_after)
        screen.fill(BLACK)
        matrix_visualizer(field_after)
        draw_grid()
        pg.display.flip()

    time.sleep(0.2)