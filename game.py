from tetromino import Tetromino
from constants import *
import random
import pygame


class Game:

    def __init__(self):
        self.font = pygame.font.Font(None, 35)
        self.new_game()
    

    def new_game(self):
        self.game_over = self.paused = False
        self.move_speed = 0.65
        self.score = 0

        self.board = [[0 for _ in range(10)] for _ in range(20)]
        self.queue = [Tetromino() for _ in range(6)]

        self.tetromino = self.queue.pop(0)
        self.tetromino.board = self.board
        self.tetromino.calc_lowest_row()

    
    def new_tetromino(self):
        self.tetromino = self.queue.pop(0)
        self.tetromino.board = self.board
        self.tetromino.calc_lowest_row()

        self.queue.append(Tetromino())
        self.score += 4
    

    def insert_tetromino(self):
        for row, col in self.tetromino.squares:
            r = row + self.tetromino.row
            c = col + self.tetromino.col
            self.board[r][c] = self.tetromino.index + 1

        # Game over if top row (row 0) contains part of a tetromino
        if self.board[0].count(0) < 10:
            self.game_over = True
            return

        self.clear_rows()
        self.new_tetromino()
        self.move_speed = max(0.1, self.move_speed - 0.001)


    def clear_rows(self):
        full_rows = 0

        row = 19
        while row > 0:
            if self.board[row].count(0) > 0:
                row -= 1 # Move one row up
                continue

            # Move every row above this row down one
            for i in range(row, 0, -1):
                self.board[i] = self.board[i-1][:]

            self.board[0] = [0 for _ in range(10)]
            full_rows += 1

        self.score += 5 * full_rows * (full_rows + 1)

    
    def draw(self, screen: pygame.Surface):
        screen.fill((100, 100, 100))
        self.draw_board(screen)
        self.draw_queue(screen)
        self.draw_text(screen)
        self.tetromino.draw(screen)


    def draw_board(self, screen: pygame.Surface):
        for row in range(20):
            for col in range(10):
                left = LEFT_EDGE + col * SQUARE_SIZE
                top = TOP_EDGE + row * SQUARE_SIZE
                color = COLORS[self.board[row][col]]

                rect = pygame.Rect(left, top, SQUARE_SIZE, SQUARE_SIZE)
                pygame.draw.rect(screen, color, rect, 0)
                pygame.draw.rect(screen, (100, 100, 100), rect, 1)

        
    def draw_text(self, screen: pygame.Surface):
        screen.blit(
            self.font.render(f'Score: {self.score}', True, (255, 255, 255)),
            (LEFT_EDGE, 20))

        screen.blit(
            self.font.render('Next', True, (255, 255, 255)),
            (375, 20))
        
        if self.paused: screen.blit(
            self.font.render('Paused', True, (255, 255, 255)),
            (210, 20))

        if self.game_over: screen.blit(
            self.font.render('Game Over!', True, (255, 255, 255)),
            (210, 20))
        

    def draw_queue(self, screen: pygame.Surface):
        spacing = 0

        for tetromino in self.queue:
            for row, col in tetromino.squares:

                left = LEFT_EDGE + SQUARE_SIZE * (13 + col - tetromino.width / 2)
                top = TOP_EDGE + SQUARE_SIZE * (spacing + row)
                color = tetromino.color

                rect = pygame.Rect(left, top, SQUARE_SIZE, SQUARE_SIZE)
                pygame.draw.rect(screen, color, rect, 0)
                pygame.draw.rect(screen, (100, 100, 100), rect, 1)

            spacing += tetromino.height + 1
