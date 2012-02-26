import pygame

import player
import renderer

def user_input(events):
    """Returns dtheta, dphi, dforward"""
    dforward = 0
    for event in events:
        if event.type == pygame.QUIT:
            return
        if event.type == pygame.KEYDOWN:
            if event.key == pygame.K_ESCAPE:
                return
            if event.key == pygame.K_w:
                dforward = 1
            if event.key == pygame.K_s:
                dforward = -1
    # do mouse stuff
    dtheta, dphi = pygame.mouse.get_rel()
    return (dtheta, dphi, dforward)

world = [(x, -2, z) for x in range(-3, 3) for z in range(-6, 6)]
r = renderer.Renderer()
r.init()
p = player.Player()

while True:
    delta = user_input(pygame.event.get())
    if not delta: break
    p.update(delta)
    r.render(p, world)
