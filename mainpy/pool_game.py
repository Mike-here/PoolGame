import pygame
import sys
import pymunk
import pymunk.pygame_util

pygame.init()

# Screen sizes.
screen_width = 1200
screen_height = 630

# Game window
screen = pygame.display.set_mode((screen_width, screen_height))
pygame.display.set_caption("The Real Pool Game")

# Pymunk space.
space = pymunk.Space()
draw_options  = pymunk.pygame_util.DrawOptions(screen)

# Create a ball.
def create_ball(radius, pos):
    body = pymunk.Body()
    body.position = pos
    shape = pymunk.Circle(body, radius)
    shape.mass = 3

    space.add(body, shape)
    return shape


created_ball = create_ball(25, (800, 400))


# Game loop.
run = True
while run:

    # Event handler.
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            run = False

    space.debug_draw(draw_options)
    pygame.display.update()        
            
pygame.quit()