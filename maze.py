import pygame
import random

# get maze and cell size
print('enter number of cells each row, col, and cell size, seprate by space')
cell_size = input().split(' ')
num_cells_x, num_cells_y, cell_width = int(
    cell_size[0]), int(cell_size[1]), int(cell_size[2])

# RGB color code
# White(255,255,255)
# Black(0,0,0)
# Green(0,255,0)
# Violet(127,0,255)

# pygame model init
pygame.init()
# window size
window = pygame.display.set_mode((600, 600))
# background color
window.fill((255, 255, 255))
# window title
pygame.display.set_caption('maze')


class cell:
    def __init__(self, x, y, cell_width) -> None:
        self.cell_width = cell_width
        # draw topleft cell
        self.move(x, y, "")

    def move(self, x, y, direction):
        '''break a wall by paint a larger rectangle on top of it'''
        params = [window, (255, 255, 255), (), 0]
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
                # draw a cell at a position
                params[2] = (x + 1, y + 1,
                             self.cell_width-2, self.cell_width-2)
        pygame.draw.rect(*params)
        pygame.display.update()


class maze:
    def __init__(self, cells_col, cells_row, cell_width):
        '''constructor'''
        self.cells_col = cells_col
        self.cells_row = cells_row
        self.cell_width = cell_width
        # a dict(hash table) of all cells created, check if a cell is vaild by check its hash in table
        self.all_cells = {}
        # same, check if a cell is visted by check if its hash in table
        self.visted_cells = {}
        # stack store comming path to move backward when needed
        self.stack = []
        # make the the table of walls
        self.make_table(0, 0)
        # create a cell at top left corner
        self.cell = cell(self.cell_width, self.cell_width, self.cell_width)
        # move the cell around to make maze
        self.make_maze(cell_width, cell_width)

    def make_table(self, x, y):
        '''draw the EXCEL like table'''
        for i in range(1, self.cells_row+1):
            # for each row
            x = self.cell_width
            y += self.cell_width
            for j in range(1, self.cells_col+1):
                # for each position for cells in the row, draw walls
                pygame.draw.line(
                    window, (127, 0, 255), [x, y], [x + self.cell_width, y])
                pygame.draw.line(
                    window, (127, 0, 255), [x + self.cell_width, y], [x + self.cell_width, y + self.cell_width])
                pygame.draw.line(
                    window, (127, 0, 255), [x + self.cell_width, y + self.cell_width], [x, y + self.cell_width])
                pygame.draw.line(window, (127, 0, 255), [
                                 x, y + self.cell_width], [x, y])
                # add cell hash to dict(hash table) keys
                self.all_cells[hash((x, y))] = None
                # next position
                x = x + self.cell_width
        # update screen to display
        pygame.display.update()

    def make_maze(self, x, y):
        # add top left starting cell to stack and visted cells
        self.stack.append((x, y))
        self.visted_cells[hash((x, y))] = None

        # repeat until stack empty
        while len(self.stack):
            # store unvisited near by cells
            near_by_cell = []
            # if the hash key is not in visited cells and in all cells(which indicate it is a valid cell not exceeding boundary)
            near_by_cell.append('u')if (hash((x, y - self.cell_width))
                                        not in self.visted_cells.keys() and hash((x, y - self.cell_width)) in self.all_cells.keys())else None
            near_by_cell.append('d')if (hash((x, y + self.cell_width))
                                        not in self.visted_cells.keys() and hash((x, y + self.cell_width)) in self.all_cells.keys())else None
            near_by_cell.append('l')if (hash((x - self.cell_width, y))
                                        not in self.visted_cells.keys() and hash((x - self.cell_width, y)) in self.all_cells.keys())else None
            near_by_cell.append('r')if (hash((x + self.cell_width, y))
                                        not in self.visted_cells.keys() and hash((x + self.cell_width, y)) in self.all_cells.keys())else None

            # at least one nearby vaild cell
            if len(near_by_cell) > 0:
                # randomly pick one
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

                # make it visted, and add to stack
                self.visted_cells[hash((x, y))] = None
                self.stack.append((x, y))
            else:
                # no nearby cell vaild, move backward try find another path
                x, y = self.stack.pop()


# create a maze
maz = maze(num_cells_x, num_cells_y, cell_width)
# pause to show diagram
input("press any button to continue...")
# quit and clean up
pygame.quit()
