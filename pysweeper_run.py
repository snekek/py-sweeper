import pygame
from pygame.locals import *

pygame.init()

display_width = 800
display_height = 600

black = (0, 0, 0)
white = (255, 255, 255)
red = (255, 0, 0)

car_width = 73

gameDisplay = pygame.display.set_mode((display_width, display_height))
pygame.display.set_caption('PySweeper')
clock = pygame.time.Clock()

carImg = pygame.image.load('snake.png')


def car(x, y):
    gameDisplay.blit(carImg, (x, y))


def game_loop():
    x = (display_width * 0.45)
    y = (display_height * 0.8)

    x_change = 0
    y_change = 0

    game_exit = False

    while not game_exit:
        for event in pygame.event.get():
            key = pygame.key.get_pressed()
            if event.type == pygame.QUIT:
                game_exit = True
                pygame.quit()
                quit()
            if event.type == pygame.MOUSEBUTTONDOWN:
                '''
                1 - left click
                2 - middle click
                3 - right click
                4 - scroll up
                5 - scroll down
                '''
            gameDisplay.fill(white)
            car(x, y)
            pygame.display.update()
            clock.tick(60)


game_loop()
pygame.quit()
quit()
