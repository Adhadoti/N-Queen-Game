import pygame
from pygame.locals import *
from sys import exit
# Define some colors
BLACK = (0, 0, 0)
WHITE = (255, 255, 255)
GREEN = (0, 255, 0)
RED = (255, 0, 0)
# Set the width and height of each cell
WIDTH = 40
HEIGHT = 40
# Grid constants
ROWS = 3
COLUMNS = 8
# GAP between each cell
GAP = 5

pygame.init()
# Set the width and height of the screen [width, height]
SCREEN_SIZE = (365, 140)
screen = pygame.display.set_mode(SCREEN_SIZE)
# Set the title of the screen
pygame.display.set_caption("Turtle Game")
# Used to manage how fast the screen updates (fps)
clock = pygame.time.Clock()

while True:
    for event in pygame.event.get():
        if event.type == QUIT:
            exit()
    # Set the screen background
    screen.fill(BLACK)
    for row in range(ROWS):
        for column in range(COLUMNS):
            color = WHITE
            pygame.draw.rect(screen, color, [(GAP + WIDTH) * column +GAP, (GAP + HEIGHT) * row + GAP, WIDTH, HEIGHT])
    # Limit to 60 frames per second
    clock.tick(60)
    pygame.display.flip()
pygame.quit()