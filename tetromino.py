from constants import *
import random
import pygame


class Tetromino:

    def __init__(self):
        self.index = random.randint(0, 6)

        self.shape = SHAPES[self.index]
        self.color = COLORS[self.index+1]
        self.offsets = OFFSETS[self.index]

        self.rotation_index = 0

        self.width = len(self.shape[0])
        self.height = len(self.shape)

        self.row = 0
        self.col = 5 - self.width // 2

        self.board: list[list[int]] = []
        self.set_squares()

    
    def set_squares(self):
        self.squares = []

        for row in range(self.height):
            for col in range(self.width):
                if self.shape[row][col] == 0: pass
                else: self.squares.append((row, col))


    def calc_lowest_row(self):
        for row in range(self.row, 20):
            if self.invalid_position(row + 1, self.col): break
        self.lowest_row = row


    def invalid_position(self, row: int, col: int, **kwargs) -> bool:
        shape = kwargs.get('shape', self.shape)
        
        for shape_row in range(len(shape)):
            for shape_col in range(len(shape[0])):
                if shape[shape_row][shape_col] == 0: continue

                if row + shape_row not in range(20) \
                or col + shape_col not in range(10):
                    return True
                
                if self.board[row + shape_row][col + shape_col]:
                    return True

        return False


    def move_down(self) -> bool:
        if self.invalid_position(self.row + 1, self.col): return False
        self.row += 1
        return True
    

    def drop_down(self) -> int:
        n = self.lowest_row - self.row
        self.row = self.lowest_row
        return 2 * n


    def move_lateral(self, direction: int) -> bool:
        """
        direction: 1 = right, -1 = left
        """
        if self.invalid_position(self.row, self.col + direction): return False
        self.col += direction
        self.calc_lowest_row()
        return True


    def rotate(self, direction: int):
        """
        direction: 1 = clockwise, -1 = counter-clockwise
        """
        rotation_index = (self.rotation_index + direction) % 4

        x1, y1 = self.offsets[self.rotation_index]
        x2, y2 = self.offsets[rotation_index]

        col = self.col + x2 - x1
        row = self.row + y2 - y1

        shape = list(zip(*self.shape[::-direction]))[::direction]

        if self.invalid_position(row, col, shape=shape): return

        self.rotation_index = rotation_index
        self.shape = shape

        self.width = len(self.shape[0])
        self.height = len(self.shape)

        # Keep tetromino inbounds
        self.col = min(10 - self.width, max(0, col))
        self.row = min(20 - self.height, max(0, row))

        self.calc_lowest_row()
        self.set_squares()

    
    def draw(self, screen: pygame.Surface):
        for row, col in self.squares:
            left = LEFT_EDGE + SQUARE_SIZE * (col + self.col)

            top = TOP_EDGE + SQUARE_SIZE * (row + self.lowest_row)
            rect = pygame.Rect(left, top, SQUARE_SIZE, SQUARE_SIZE)

            pygame.draw.rect(screen, (140, 140, 140), rect)
            pygame.draw.rect(screen, (100, 100, 100), rect, 1)

            top = TOP_EDGE + SQUARE_SIZE * (row + self.row)
            rect = pygame.Rect(left, top, SQUARE_SIZE, SQUARE_SIZE)

            pygame.draw.rect(screen, self.color, rect)
            pygame.draw.rect(screen, (100, 100, 100), rect, 1)
