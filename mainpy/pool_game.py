import pygame
import sys

pygame.init()

screen_width = 1200
screen_height = 630

screen = pygame.display.set_mode((screen_width, screen_height))
pygame.display.set_caption("The Real Pool Game")


# Game loop.
run = True
while run:

    # Event handler.
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            run = False
            
pygame.quit()