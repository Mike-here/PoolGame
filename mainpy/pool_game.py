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

diameter = 36

# Colours.
background_color = (100, 100, 150)

# Load images
cue_image = pygame.image.load(os.path.join("assets/cue.png")).convert_alpha()
pool_board = pygame.image.load(os.path.join("assets/table.png")).convert_alpha()
ball_images =  []
for i in range(1, 17):
    ball_img = pygame.image.load(os.path.join(f"assets/ball_{i}.png")).convert_alpha()
    ball_images.append(ball_img)

# Create a ball.
def create_ball(radius, pos):
    body = pymunk.Body()
    body.position = pos
    shape = pymunk.Circle(body, radius)
    shape.mass = 20
    shape.elasticity = 0.9
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
        pos = (200 + (col * ((diameter - 3))), 220 + (row * ((diameter - 3)) + (col * diameter / 2)))
        new_ball = create_ball(diameter / 2, pos)
        balls.append(new_ball)
    rows -= 1   

cue_ball = create_ball(diameter / 2, (800, screen_height / 2))
balls.append(cue_ball)
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

class Cue():
    def __init__(self, pos):
        self.original_image = cue_image
        self.angle = 0
        self.image = pygame.transform.rotate(self.original_image, self.angle)
        self.rect = self.image.get_rect()
        self.rect.center = pos

    def draw(self, surface):
        self.image = pygame.transform.rotate(self.original_image, self.angle)
        surface.blit(self.image, self.rect)

cue = Cue(balls[-1].body.position)            #instance for the cue and passed the position which is at the of the list "balls"

# Game loop.
run = True
while run:

    clock.tick(fps)
    space.step(1 / fps)             #inverse

    # Fill the background.
    screen.fill(background_color)

    # Draw the pool board.
    screen.blit(pool_board, (0, 0))

    # Draw ball images
    for i, ball in enumerate(balls):
        screen.blit(ball_images[i], (ball.body.position[0] - ball.radius, ball.body.position[1] - ball.radius))

    # Draw the cue
    cue.draw(screen)    

    # Event handler.
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            run = False
        if event.type == pygame.MOUSEBUTTONDOWN:
            cue_ball.body.apply_impulse_at_local_point((-3000, 0), (0, 0))   

    space.debug_draw(draw_options)
    pygame.display.update()        
            
pygame.quit()
sys.exit()