import pygame
import random

print('enter number of all_cells each row, col, and cell size, seprate by space')
cell_size = input().split(' ')
num_cells_x, num_cells_y, cell_width = int(
    cell_size[0]), int(cell_size[1]), int(cell_size[2])

pygame.init()
screen = pygame.display.set_mode((800, 800), pygame.RESIZABLE)
screen.fill((255, 255, 255))
pygame.display.set_caption('maze')

all_cells = []


class cell:
    def __init__(self, x, y, cell_width) -> None:
        self.cell_width = cell_width
        self.move(x, y, "")

    def move(self, x, y, direction):
        params = [screen, (255, 255, 255), (), 0]
        match(direction):
            case 'u':
                params[2] = (x + 1, y - self.cell_width +
                             1, self.cell_width-1, 2*self.cell_width-1)
            case 'd':
                params[2] = (x + 1, y + 1,
                             self.cell_width-1, 2*self.cell_width-1)
            case 'l':
                params[2] = (x - self.cell_width + 1, y +
                             1, 2*self.cell_width-1, self.cell_width-1)
            case 'r':
                params[2] = (x + 1, y + 1,
                             2*self.cell_width-1, self.cell_width-1)
            case _:
                params[2] = (x + 1, y + 1,
                             self.cell_width-2, self.cell_width-2)
        pygame.draw.rect(*params)
        pygame.display.update()


class maze:
    def __init__(self, cells_col, cells_row, cell_width) -> None:
        self.cells_col = cells_col
        self.cells_row = cells_row
        self.cell_width = cell_width
        self.visted_cells = {}
        self.move_stack = []
        self.make_table(0, 0)
        self.cell = cell(self.cell_width, self.cell_width, self.cell_width)
        self.make_maze(cell_width, cell_width)

    def make_table(self, x, y):
        '''draw the EXCEL like table'''
        for i in range(1, self.cells_row+1):
            x = self.cell_width
            y += self.cell_width
            for j in range(1, self.cells_col+1):
                pygame.draw.line(
                    screen, (127, 0, 255), [x, y], [x + self.cell_width, y])
                pygame.draw.line(
                    screen, (127, 0, 255), [x + self.cell_width, y], [x + self.cell_width, y + self.cell_width])
                pygame.draw.line(
                    screen, (127, 0, 255), [x + self.cell_width, y + self.cell_width], [x, y + self.cell_width])
                pygame.draw.line(screen, (127, 0, 255), [
                                 x, y + self.cell_width], [x, y])
                all_cells.append((x, y))
                x = x + self.cell_width
        pygame.display.update()

    def make_maze(self, x, y):
        self.move_stack.append((x, y))
        self.visted_cells[hash((x, y))] = None
        while len(self.move_stack):
            near_by_cell = []
            near_by_cell.append('r')if (hash((x + self.cell_width, y))
                                        not in self.visted_cells.keys() and (x + self.cell_width, y) in all_cells)else None
            near_by_cell.append('l')if (hash((x - self.cell_width, y))
                                        not in self.visted_cells.keys() and (x - self.cell_width, y) in all_cells)else None
            near_by_cell.append('u')if (hash((x, y - self.cell_width))
                                        not in self.visted_cells.keys() and (x, y - self.cell_width) in all_cells)else None
            near_by_cell.append('d')if (hash((x, y + self.cell_width))
                                        not in self.visted_cells.keys() and (x, y + self.cell_width) in all_cells)else None
            if len(near_by_cell) > 0:
                match(random.choice(near_by_cell)):
                    case('u'):
                        self.cell.move(x, y, 'u')
                        y -= self.cell_width
                    case('d'):
                        self.cell.move(x, y, 'd')
                        y += self.cell_width
                    case('r'):
                        self.cell.move(x, y, 'r')
                        x += self.cell_width
                    case('l'):
                        self.cell.move(x, y, 'l')
                        x -= self.cell_width

                self.visted_cells[hash((x, y))] = None
                self.move_stack.append((x, y))
            else:
                x, y = self.move_stack.pop()
                self.cell.move(x, y, '')


maz = maze(num_cells_x, num_cells_y, cell_width)
input("press any button to continue")
pygame.quit()
