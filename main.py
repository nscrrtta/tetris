from game import Game
import threading
import pygame
import time


pygame.init()
font = pygame.font.Font(None, 35)
screen = pygame.display.set_mode((510,690))
pygame.display.set_caption('Tetris by Nick Sciarretta')


game = Game()
running = True
flag = 0


def move_down():

    while running: 

        # Hold left shift for speed boost
        keys = pygame.key.get_pressed()
        shift = keys[pygame.K_LSHIFT]

        if shift: time.sleep(0.05)
        else: time.sleep(game.move_speed)

        if game.game_over or game.paused:
            continue

        elif game.tetromino.move_down():
            game.score += shift
            continue
        
        time.sleep(0.2) # Give user time to rotate/move tetromino
        if not game.tetromino.move_down(): game.insert_tetromino()



def move_LR():

    global flag

    while running:

        time.sleep(0.05)
        
        if game.game_over or game.paused:
            continue

        if flag == 0: count = 0
        elif count < 4: count += 1
        elif not game.tetromino.move_LR(flag): flag = 0


threading.Thread(target=move_down).start()
threading.Thread(target=move_LR).start()


while running:

    for event in pygame.event.get():

        if event.type == pygame.QUIT:
            running = False

        elif event.type == pygame.KEYDOWN:

            if event.key == pygame.K_n:
                game.new_game()

            elif game.game_over:pass

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
                if game.tetromino.move_LR(-1): flag = -1

            elif event.key == pygame.K_RIGHT:
                if game.tetromino.move_LR(1): flag = 1
            
        elif event.type == pygame.KEYUP:
            
            keys = pygame.key.get_pressed()

            if    flag == 1 and keys[pygame.K_RIGHT]: pass
            elif  flag ==-1 and keys[pygame.K_LEFT]:  pass
            else: flag = 0

    game.draw(screen, font)
    pygame.display.update()
    

pygame.quit()