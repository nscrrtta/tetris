from constants import *
import pygame


class Tetromino:

    def __init__(self, index: int, board: list):

        self.index = index
        self.board = board

        self.shape = shapes[index]
        self.colour = colours[index+1]
        self.offset_data = offset_data[index]

        self.row = 0
        self.col = 5-len(self.shape[0])//2

        self.rotation_index = 0

        self.width  = len(self.shape[0])
        self.height = len(self.shape)

        self.calc_ghost_row()


    def calc_ghost_row(self):

        row = self.row
        while not self.invalid_position(row, self.col): row += 1
        self.ghost_row = row-1


    def invalid_position(self, r: int, c: int, shape=None, check_oob=True) -> bool:

        if shape is None: shape = self.shape

        for row in range(len(shape)):
            for col in range(len(shape[0])):

                if shape[row][col] == 0: continue

                # Out of bounds
                if not (0 <= r+row < 20 and 0 <= c+col < 10):
                    if check_oob: return True
                    else: continue

                # Overlap with piece already on board
                if self.board[r+row][c+col] > 0: 
                    return True

        return False


    def move_down(self) -> bool:

        if self.invalid_position(self.row+1, self.col): return False
        self.row += 1
        return True
    

    def drop_down(self) -> int:

        n = self.ghost_row-self.row
        self.row = self.ghost_row
        return 2*n


    def move_LR(self, direction: int) -> bool:

        # 1 = move right, -1 = move left
        if self.invalid_position(self.row, self.col+direction): return False
        
        self.col += direction
        self.calc_ghost_row()
        return True


    def rotate(self, direction: int):

        # 1 = clockwise, -1 = counter-clockwise
        new_rotation_index = (self.rotation_index+direction)%4

        x1, y1 = self.offset_data[self.rotation_index]
        x2, y2 = self.offset_data[new_rotation_index]

        new_shape = list(zip(*self.shape[::-direction]))[::direction]
        new_col = self.col + (x2-x1)
        new_row = self.row + (y2-y1)

        # Check if rotating tetromino will overlap existing pieces
        if self.invalid_position(new_row, new_col, new_shape, check_oob=False): return

        self.rotation_index = new_rotation_index
        self.shape = new_shape
        self.col = new_col
        self.row = new_row

        self.width  = len(self.shape[0])
        self.height = len(self.shape)

        # Check if tetromino rotated out of bounds
        if self.col < 0: self.col = 0
        elif self.col > 10-self.width: self.col = 10-self.width

        if self.row < 0: self.row = 0
        elif self.row > 20-self.height: self.row = 20-self.height

        self.calc_ghost_row()

    
    def draw(self, screen):

        def draw_ghost():

            for row in range(self.height):
                for col in range(self.width):

                    if self.shape[row][col] == 0: continue

                    left = left_edge + sqr_size*(col+self.col)
                    top  = top_edge  + sqr_size*(row+self.ghost_row)

                    rect = pygame.Rect(left, top, sqr_size, sqr_size)
                    pygame.draw.rect(screen, (140,140,140), rect)
                    pygame.draw.rect(screen, (100,100,100), rect, 1)


        def draw_tetromino():

            for row in range(self.height):
                for col in range(self.width):

                    if self.shape[row][col] == 0: continue

                    left = left_edge + sqr_size*(col+self.col)
                    top  = top_edge  + sqr_size*(row+self.row)

                    rect = pygame.Rect(left, top, sqr_size, sqr_size)
                    pygame.draw.rect(screen, self.colour, rect)
                    pygame.draw.rect(screen, (100,100,100), rect, 1)


        if self.ghost_row > self.row: draw_ghost()
        draw_tetromino()
