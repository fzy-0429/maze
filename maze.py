import pygame
import random

WINDOW_SIZE = (800, 800)
print('enter the number of colmns and rows, seprate by space')
COLS_AND_ROWS = input().split(" ")
COLS = int(COLS_AND_ROWS[0])
ROWS = int(COLS_AND_ROWS[1])
WALL_THICKNESS = int(200/max(COLS, ROWS))
CELLS_EXIST = 0
TOP_LEFT = (0, 0)


class cell:
    def __init__(self, row, col, index) -> None:
        self.row = row
        self.col = col
        self.id = hash(row*31+col*31 ^ 2)
        self.visted = False
        self.walls = {'UP': False, 'DOWN': False,
                      'LEFT': False, 'RIGHT': False}


class maze:
    def __init__(self, row, col) -> None:
        self.row = row
        self.col = col
        self.maze = [[cell(r, c) for c in range(col)] for r in range(row)]
        self.maze_init()

    def maze_init():
        pass


pygame.init()
windows = pygame.display.set_mode(WINDOW_SIZE)

while (1):
    windows.fill((255, 255, 255))
    pygame.display.update()
