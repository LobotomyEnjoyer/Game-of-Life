import pygame as pg
import sys
import time

# TODO:
# . Реализовать правила для клеток
# . Реализовать игровое поле и его обновление
# . Реализовать размещение клеток курсором (перед симуляцией поле пустое!)
# . Реализовать паузу

#====НАЧАЛЬНЫЕ ПАРАМЕТРЫ====

SQUARE_SIDE = 30

W = 1024
H = 1024

GREY = (32, 32, 32)
ORANGE = (255, 150, 0)
BLUE = (0, 150, 255)
BLACK = (0,0,0)

def update_field(f1: list, f2: list):
    """Updates cells on the field."""

pg.init()
screen = pg.display.set_mode((W, H))

r = pg.Rect(0, 0, SQUARE_SIDE, SQUARE_SIDE)

ROWS = H//SQUARE_SIDE
COLS = W//SQUARE_SIDE

field_before = [[0 for _ in range(ROWS+1)] for _ in range(COLS+1)]
field_after = [[0 for _ in range(ROWS+1)] for _ in range(COLS+1)]

def draw_grid():
    for i in range(0, H//SQUARE_SIDE+1):
        pg.draw.line(screen, GREY, (0, i*SQUARE_SIDE), (W, i*SQUARE_SIDE))
        pg.draw.line(screen, GREY, (i*SQUARE_SIDE, 0), (i*SQUARE_SIDE, W))

while True:
    for event in pg.event.get():
        if event.type == pg.QUIT:
            pg.quit()
            sys.exit()
    
    screen.fill(BLACK)
    draw_grid()

    pg.draw.rect(screen, ORANGE, r)
    pg.display.flip()
    
    time.sleep(0.5)