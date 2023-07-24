from tetromino import Tetromino
from random import randint
from constants import *
import pygame


class Game:

    def __init__(self):

        self.new_game()
    

    def new_game(self):

        self.game_over = self.paused = False
        self.move_speed = 0.65
        self.score = -4

        self.board = [[0 for _ in range(10)] for _ in range(20)]
        self.queue = [randint(0,6) for _ in range(5)]
        self.new_tetromino()

    
    def new_tetromino(self):

        self.score += 4
        self.queue.append(randint(0,6))
        self.tetromino = Tetromino(self.queue.pop(0), self.board)


    def insert_tetromino(self):

        for row in range(self.tetromino.height):
            for col in range(self.tetromino.width):

                if self.tetromino.shape[row][col] == 0: continue

                r, c = row+self.tetromino.row, col+self.tetromino.col
                self.board[r][c] = self.tetromino.index+1

        # Game over if top row (row 0) contains part of a tetromino
        # but the row is not full
        if 0 < self.board[0].count(0) < 10:
            self.game_over = True
            return

        self.clear_rows()
        self.new_tetromino()
        if self.move_speed > 0.1: self.move_speed -= 0.001


    def clear_rows(self):

        n = 0 # Number of full rows
        row = 19 # Start at bottom row

        while row > 0:

            if self.board[row].count(0) > 0:
                row -= 1 # Move one row up
                continue

            n += 1

            # Move every row above <row> down one
            for i in range(row, 0, -1):
                self.board[i] = self.board[i-1][:]

            self.board[0] = [0 for _ in range(10)]

        self.score += 5*n*(n+1)

    
    def draw(self, screen, font):

        screen.fill((100,100,100))


        def draw_board():

            for row in range(20):
                for col in range(10):

                    left = left_edge+col*sqr_size
                    top  = top_edge +row*sqr_size
                    colour = colours[self.board[row][col]]

                    rect = pygame.Rect(left, top, sqr_size, sqr_size)
                    pygame.draw.rect(screen, colour, rect, 0)
                    pygame.draw.rect(screen, (100,100,100), rect, 1)

        
        def draw_text():

            screen.blit(
                font.render(f'Score: {self.score}', True, (255,255,255)),
                (left_edge, 20)
            )

            if self.paused: screen.blit(
                font.render('Paused', True, (255,255,255)),
                (245, 20)
            )

            screen.blit(
                font.render('Next', True, (255,255,255)),
                (393, 20)
            )
        

        def draw_queue():

            t = 0 # Vertical spacing of pieces
            for i in self.queue:

                shape = shapes[i]

                for row in range(len(shape)):
                    for col in range(len(shape[0])):

                        if shape[row][col] == 0: continue

                        left = left_edge + sqr_size*(13+col-len(shape[0])/2)
                        top  = top_edge  + sqr_size*(t+row)
                        colour = colours[i+1]

                        rect = pygame.Rect(left, top, sqr_size, sqr_size)
                        pygame.draw.rect(screen, colour, rect, 0)
                        pygame.draw.rect(screen, (100,100,100), rect, 1)

                t += len(shape)+1


        draw_board()
        draw_queue()
        draw_text()
        self.tetromino.draw(screen)
