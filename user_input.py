import pygame

escape = False
dtheta = 0
dphi = 0
forward = 0

def update(events):
    global escape, dtheta, dphi, forward
    """Returns dtheta, dphi, dforward"""
    dtheta = 0
    dphi = 0
    for event in events:
        if event.type == pygame.QUIT:
            escape = True
        elif event.type == pygame.KEYDOWN:
            if event.key == pygame.K_ESCAPE:
                escape = True
            elif event.key == pygame.K_w:
                forward = 1
            elif event.key == pygame.K_s:
                forward = -1
        elif event.type == pygame.KEYUP:
            if event.key in (pygame.K_w, pygame.K_s):
                forward = 0
    # do mouse stuff
    dtheta, dphi = pygame.mouse.get_rel()
