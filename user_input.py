import pygame

escape = False
dtheta = 0
dphi = 0
forward = 0
sideways = 0

def update(events):
    global escape, dtheta, dphi, forward, sideways
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
            elif event.key == pygame.K_a:
                sideways = -1
            elif event.key == pygame.K_d:
                sideways = 1
        elif event.type == pygame.KEYUP:
            if event.key == pygame.K_w and forward == 1:
                forward = 0
            if event.key == pygame.K_s and forward == -1:
                forward = 0
            if event.key == pygame.K_d and sideways == 1:
                sideways = 0
            if event.key == pygame.K_a and sideways == -1:
                sideways = 0
    # do mouse stuff
    dtheta, dphi = pygame.mouse.get_rel()
