import pygame
import sys
import pymunk
import pymunk.pygame_util
import os

pygame.init()

# Screen sizes.
screen_width = 1076
screen_height = 608

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

diameter = 48

# Colours.
background_color = (100, 100, 150)

# Load images
pool_board = pygame.image.load(os.path.join("assets/table.png"))

# Create a ball.
def create_ball(radius, pos):
    body = pymunk.Body()
    body.position = pos
    shape = pymunk.Circle(body, radius)
    shape.mass = 3
    shape.elasticity = 0.75
    # use a pivot joint to add friction.
    pivot = pymunk.PivotJoint(static_body, body, (0, 0), (0, 0))
    pivot.max_bias = 0 
    pivot.max_force = 900    # Emulate linear friction

    space.add(body, shape, pivot)
    return shape

# Game's setup
balls = []
rows = 5
# Potting balls
for col in range(5):
    for row in range(rows):
        pos = (200 + (col * diameter), 200 + (row * diameter) + (col * diameter / 2))
        new_ball = create_ball(diameter / 2, pos)
        balls.append(new_ball)
    rows -= 1    
cue_ball = create_ball(25, (800, screen_height / 2))

# Create pool board cushions.
cushions = [
    [(80, 50), (98, 68), (500, 68), (507.2, 50)],
    [(555, 50), (565.2, 68), (976, 68), (990, 50)],
    [(80, 558), (98, 540), (500, 540), (507.2, 558)],
    [(555, 558), (565.2, 540), (976, 540), (990, 558)],
    [(50.3, 86), (68, 106.3), (68, 500), (50.3, 521)],
    [(1025.7, 86), (1008, 106.3), (1008, 500), (1025.7, 521)]
]

# Functions for creating cushions
def create_cushion(poly_dims):
    body = pymunk.Body(body_type = pymunk.Body.STATIC)
    body.position = ((0, 0))
    shape = pymunk.Poly(body, poly_dims)
    shape.elasticity = 0.75
    space.add(body, shape)

for c in cushions:
    create_cushion(c)

# Game loop.
run = True
while run:

    clock.tick(fps)
    space.step(1 / fps)             #inverse

    # Fill the background.
    screen.fill(background_color)

    # Draw the pool board.
    screen.blit(pool_board, (0, 0))

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