###################################
# Python maze generator program
# using PyGame for animation
# Davis MT
# Python 3.4
# 10.02.2018
###################################

import pygame
import time
import random

# set up pygame window
WIDTH = 500
HEIGHT = 600
FPS = 30

# Define colours
WHITE = (255, 255, 255)
GREEN = (0, 255, 0,)
BLUE = (0, 0, 255)
YELLOW = (255, 255, 0)

# initalise Pygame
pygame.init()
pygame.mixer.init()
screen = pygame.display.set_mode((WIDTH, HEIGHT))
pygame.display.set_caption("Python Maze Generator")
clock = pygame.time.Clock()

# setup maze variables
# x = 0                    # x axis
# y = 0                    # y axis
w = 20                   # width of cell
grid = []
visited = []
stack = []
solution = {}


# build the grid
def build_grid(x, y, w):
    for i in range(1, 21):
        # set x coordinate to start position
        x = 20
        # start a new row
        y = y + 20
        for j in range(1, 21):
            pygame.draw.line(screen, WHITE, [x, y], [
                             x + w, y])           # top of cell
            # right of cell
            pygame.draw.line(screen, WHITE, [x + w, y], [x + w, y + w])
            # bottom of cell
            pygame.draw.line(screen, WHITE, [x + w, y + w], [x, y + w])
            # left of cell
            pygame.draw.line(screen, WHITE, [x, y + w], [x, y])
            # add cell to grid list
            grid.append((x, y))
            # move cell to new position
            x = x + 20


def push_up(x, y):
    # draw a rectangle twice the width of the cell
    pygame.draw.rect(screen, BLUE, (x + 1, y - w + 1, 19, 39), 0)
    # to animate the wall being removed
    pygame.display.update()


def push_down(x, y):
    pygame.draw.rect(screen, BLUE, (x + 1, y + 1, 19, 39), 0)
    pygame.display.update()


def push_left(x, y):
    pygame.draw.rect(screen, BLUE, (x - w + 1, y + 1, 39, 19), 0)
    pygame.display.update()


def push_right(x, y):
    pygame.draw.rect(screen, BLUE, (x + 1, y + 1, 39, 19), 0)
    pygame.display.update()


def single_cell(x, y):
    pygame.draw.rect(screen, GREEN, (x + 1, y + 1, 18, 18),
                     0)          # draw a single width cell
    pygame.display.update()


def backtracking_cell(x, y):
    # used to re-colour the path after single_cell
    pygame.draw.rect(screen, BLUE, (x + 1, y + 1, 18, 18), 0)
    # has visited cell
    pygame.display.update()


def solution_cell(x, y):
    # used to show the solution
    pygame.draw.rect(screen, YELLOW, (x+8, y+8, 5, 5), 0)
    # has visited cell
    pygame.display.update()


def carve_out_maze(x, y):
    # starting positing of maze
    single_cell(x, y)
    # place starting cell into stack
    stack.append((x, y))
    # add starting cell to visited list
    visited.append((x, y))
    while len(stack) > 0:                                          # loop until stack is empty
        # slow program now a bit
        time.sleep(.07)
        cell = []                                                  # define cell list
        if (x + w, y) not in visited and (x + w, y) in grid:       # right cell available?
            # if yes add to cell list
            cell.append("right")

        if (x - w, y) not in visited and (x - w, y) in grid:       # left cell available?
            cell.append("left")

        if (x, y + w) not in visited and (x, y + w) in grid:     # down cell available?
            cell.append("down")

        if (x, y - w) not in visited and (x, y - w) in grid:      # up cell available?
            cell.append("up")

        # check to see if cell list is empty
        if len(cell) > 0:
            # select one of the cell randomly
            cell_chosen = (random.choice(cell))

            if cell_chosen == "right":                             # if this cell has been chosen
                # call push_right function
                push_right(x, y)
                # solution = dictionary key = new cell, other = current cell
                solution[(x + w, y)] = x, y
                x = x + w                                          # make this cell the current cell
                # add to visited list
                visited.append((x, y))
                # place current cell on to stack
                stack.append((x, y))

            elif cell_chosen == "left":
                push_left(x, y)
                solution[(x - w, y)] = x, y
                x = x - w
                visited.append((x, y))
                stack.append((x, y))

            elif cell_chosen == "down":
                push_down(x, y)
                solution[(x, y + w)] = x, y
                y = y + w
                visited.append((x, y))
                stack.append((x, y))

            elif cell_chosen == "up":
                push_up(x, y)
                solution[(x, y - w)] = x, y
                y = y - w
                visited.append((x, y))
                stack.append((x, y))
        else:
            # if no cells are available pop one from the stack
            x, y = stack.pop()
            # use single_cell function to show backtracking image
            single_cell(x, y)
            # slow program down a bit
            time.sleep(.05)
            # change colour to green to identify backtracking path
            backtracking_cell(x, y)


def plot_route_back(x, y):
    # solution list contains all the coordinates to route back to start
    solution_cell(x, y)
    # loop until cell position == start position
    while (x, y) != (20, 20):
        # "key value" now becomes the new key
        x, y = solution[x, y]
        # animate route back
        solution_cell(x, y)
        time.sleep(.1)


x, y = 20, 20                     # starting position of grid
# 1st argument = x value, 2nd argument = y value, 3rd argument = width of cell
build_grid(40, 0, 20)
carve_out_maze(x, y)               # call build the maze  function
# plot_route_back(400, 400)         # call the plot solution function


# ##### pygame loop #######
running = True
while running:
    # keep running at the at the right speed
    clock.tick(FPS)
    # process input (events)
    for event in pygame.event.get():
        # check for closing the window
        if event.type == pygame.QUIT:
            running = False
