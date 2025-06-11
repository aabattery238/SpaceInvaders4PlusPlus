import pygame
from pygame import display, image, transform, event, QUIT

# Initialize pygame
pygame.init()

# Set up clock and display
clock = pygame.time.Clock()
mainscreen = display.set_mode((800, 800))
running = True

# Load and prepare image ONCE
pyimage = transform.scale_by(image.load("basicenemysprite1.png"), 8)
pyrect = pyimage.get_rect(center=(400, 550))

# Main loop
while running:
    ticks = clock.tick(5)
    mainscreen.fill((10, 26, 42))

    for e in pygame.event.get():
        if e.type == QUIT:
            running = False

    mainscreen.blit(pyimage, pyrect)
    display.flip()

# Quit pygame
pygame.quit()
