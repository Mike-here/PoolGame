import pygame
import sys
import pymunk
import pymunk.pygame_util

pygame.init()

# Screen sizes.
screen_width = 1200
screen_height = 678

# Game window
screen = pygame.display.set_mode((screen_width, screen_height))
pygame.display.set_caption("The Real Pool Game")

# Pymunk space.
space = pymunk.Space()
static_body = space.static_body
draw_options  = pymunk.pygame_util.DrawOptions(screen)

# Clock.
clock = pygame.time.Clock()
fps = 120

# Colours.
background_color = (100, 100, 150)

# Load images
pool_board = pygame.image.load("assets/table.png")

# Create a ball.
def create_ball(radius, pos):
    body = pymunk.Body()
    body.position = pos
    shape = pymunk.Circle(body, radius)
    shape.mass = 3
    # use a pivot joint to add friction.
    pivot = pymunk.PivotJoint(static_body, body, (0, 0), (0, 0))
    pivot.max_bias = 0 
    pivot.max_force = 100    # Emulate linear friction

    space.add(body, shape, pivot)
    return shape


first_ball = create_ball(25, (300, 200))
cue_ball = create_ball(25, (800, 230))


# Game loop.
run = True
while run:

    clock.tick(fps)
    space.step(1 / fps)             #inverse

    # Fill the background.
    screen.fill(background_color)

    # Event handler.
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            run = False
        if event.type == pygame.MOUSEBUTTONDOWN:
            cue_ball.body.apply_impulse_at_local_point((-1000, 0), (0, 0))   

    space.debug_draw(draw_options)
    pygame.display.update()        
            
pygame.quit()
sys.exit()