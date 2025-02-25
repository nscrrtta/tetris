from game import Game
import threading
import pygame
import time


pygame.init()
screen = pygame.display.set_mode((510,690))
pygame.display.set_caption('Tetris by Nick Sciarretta')

game = Game()
direction = 0
running = True


def move_down():
    while running: 
        time.sleep(0.05)
        if game.game_over or game.paused: continue

        keys = pygame.key.get_pressed()
        shift_held = keys[pygame.K_LSHIFT] or keys[pygame.K_RSHIFT]
        if shift_held is False: time.sleep(game.move_speed)

        if game.tetromino.move_down():
            if shift_held: game.score += 1
        else: game.insert_tetromino()


def move_lateral():
    global direction
    while running:
        time.sleep(0.05)
        if game.game_over or game.paused: continue

        if direction == 0: count = 0
        elif count < 5: count += 1
        elif game.tetromino.move_lateral(direction) is False: direction = 0


threading.Thread(target=move_down).start()
threading.Thread(target=move_lateral).start()


while running:

    for event in pygame.event.get():

        if event.type == pygame.QUIT:
            running = False

        elif event.type == pygame.KEYDOWN:

            if event.key == pygame.K_n:
                game.new_game()

            elif game.game_over: pass

            elif event.key == pygame.K_ESCAPE:
                game.paused = not game.paused

            elif game.paused: pass

            elif event.key == pygame.K_SPACE:
                game.score += game.tetromino.drop_down()
                game.insert_tetromino()

            elif event.key == pygame.K_UP:
                game.tetromino.rotate(1)
                
            elif event.key == pygame.K_DOWN:
                game.tetromino.rotate(-1)

            elif event.key == pygame.K_LEFT:
                if game.tetromino.move_lateral(-1): direction = -1

            elif event.key == pygame.K_RIGHT:
                if game.tetromino.move_lateral(1): direction = 1
            
        elif event.type == pygame.KEYUP:

            keys = pygame.key.get_pressed()

            if    direction > 0 and keys[pygame.K_RIGHT]: pass
            elif  direction < 0 and keys[pygame.K_LEFT]:  pass
            else: direction = 0

    game.draw(screen)
    pygame.display.update()
    

pygame.quit()