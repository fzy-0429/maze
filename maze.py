# Fangzhou Ye
# fxy210002
# CS 3345.0U1

# if you want to run it you need to install python and pygame model

# for UI
import pygame
# for random direction choosing
import random
# for key interuption
import keyboard

# get maze and cell size
print('enter number of cells each row, col, and cell size(in pixels), seprate by space')
cell_size = input().split(' ')
columns, rows, cell_width = int(
    cell_size[0]), int(cell_size[1]), int(cell_size[2])

# RGB color code
# White(255,255,255)
# Red(255,0,0)
# Green(0,255,0)
# Violet(127,0,255)

# pygame model init
pygame.init()
# window size
window = pygame.display.set_mode((800, 800))
# background color
window.fill((255, 255, 255))
# window title
pygame.display.set_caption('maze')


class cell:
    def __init__(self, x, y, cell_width):
        '''constructor'''

        self.cell_width = cell_width
        # use position of a cell as a key to track positon of its parent cell
        self.backtrace = {}
        # print top-left cell to start
        self.move(x, y, "")

    def move(self, x, y, direction, color=(255, 255, 255)):
        '''break a wall by print a larger rectangle on top of it'''

        # changing printing param to print rectangles to remove wall in different direction
        params = [window, color, (), 0]
        match(direction):
            case 'u':
                params[2] = (x + 1, y - self.cell_width +
                             1, self.cell_width-1, 2*self.cell_width-1)
                self.backtrace[(x + 1, y - self.cell_width +
                               1)] = (x, y)
            case 'd':
                params[2] = (x + 1, y + 1,
                             self.cell_width-1, 2*self.cell_width-1)
                self.backtrace[(x + 1, y + 1,
                                self.cell_width-1)] = (x, y)
            case 'l':
                params[2] = (x - self.cell_width + 1, y +
                             1, 2*self.cell_width-1, self.cell_width-1)
                self.backtrace[(x - self.cell_width + 1, y +
                                1)] = (x, y)
            case 'r':
                params[2] = (x + 1, y + 1,
                             2*self.cell_width-1, self.cell_width-1)
                self.backtrace[(x + 1, y + 1)] = (x, y)
            case 'c':
                # print circle
                pygame.draw.circle(window, color,
                                   (0.5*self.cell_width+x + 1, 0.5*self.cell_width+y + 1), self.cell_width/4)
                pygame.display.update()
                return
            case _:
                # print a square
                params[2] = (x + 1, y + 1,
                             self.cell_width-2, self.cell_width-2)

        # actual printing and update
        pygame.draw.rect(*params)
        pygame.display.update()

    def solve_maze(self, x, y):
        # order of how to move from end to start
        path = ''
        # print a red circle at the end cell
        self.move(x, y, 'c', (255, 0, 0))
        # tracking backward from end to start cell
        while (x, y) != (self.cell_width, self.cell_width):
            # only one direction moving each time, so either vertical or horizontal
            if (self.backtrace[(x, y)][0] != x):
                # horizontal
                if self.backtrace[(x, y)][0] > x:
                    # which direction by checking x
                    path += ' W'
                else:
                    path += ' E'
            else:
                # vertical
                if self.backtrace[(x, y)][1] > y:
                    # which direction by checking y
                    path += ' N'
                else:
                    path += ' S'
            # update to continue tracking backward
            x, y = self.backtrace[(x, y)]
            # print a green circle at the next position
            self.move(x, y, 'c', (0, 255, 0))

        # print starting point to red
        self.move(x, y, 'c', (255, 0, 0))
        # inverse path(cause it is from end to start, we want start to end)
        path = path[::-1]
        print(path)


class maze:
    def __init__(self, cells_col, cells_row, cell_width):
        '''constructor'''

        self.cells_col = cells_col
        self.cells_row = cells_row
        self.cell_width = cell_width

        # use dict to speed up as checking if a key exist in a dict is O(1) in python, and I don't really need the value
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
        '''print the EXCEL-like table'''

        # for each row
        for i in range(1, self.cells_row+1):
            x = self.cell_width
            y += self.cell_width

            # for each position for cells in the row, draw walls
            for j in range(1, self.cells_col+1):
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
        '''make the maze by moving the cell around and take down walls'''

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
                # randomly pick one, remove wall, add backtrace record
                match(random.choice(near_by_cell)):
                    case('u'):
                        # remove the top wall by moving up
                        self.cell.move(x, y, 'u')
                        # save to back tracking stack
                        self.cell.backtrace[(x, y-self.cell_width)] = (x, y)
                        # change value, y reduce a cell width to move up
                        y -= self.cell_width
                    case('d'):
                        self.cell.move(x, y, 'd')
                        self.cell.backtrace[(x, y+self.cell_width)] = (x, y)
                        y += self.cell_width
                    case('r'):
                        self.cell.move(x, y, 'r')
                        self.cell.backtrace[(x+self.cell_width, y)] = (x, y)
                        x += self.cell_width
                    case('l'):
                        self.cell.move(x, y, 'l')
                        self.cell.backtrace[(x-self.cell_width, y)] = (x, y)
                        x -= self.cell_width
                # make it visted, and add to stack
                self.visted_cells[hash((x, y))] = None
                self.stack.append((x, y))
            else:
                # no nearby cell vaild, move backward try find another path
                x, y = self.stack.pop()


# create a maze
maz = maze(columns, rows, cell_width)
# end cell position (x*width,y*width)
maz.cell.solve_maze(columns*cell_width, rows*cell_width)

# pause to show diagram
print("press any button to continue...")
while (True):
    # keyboard interuption
    if keyboard.read_key():
        # quit and clean up
        pygame.quit()
        exit()
