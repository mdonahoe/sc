import pygame

import user_input
import player
import renderer

world = [(x, -2, z) for x in range(-3, 3) for z in range(-6, 6)]
r = renderer.Renderer()
r.init()
p = player.Player()

while True:
    user_input.update(pygame.event.get())
    if user_input.escape: break
    p.update(user_input)
    r.render(p, world)
