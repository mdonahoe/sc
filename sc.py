import sys

import pygame

import client
import player
import renderer
import user_input

r = renderer.Renderer()
r.init()
p = player.Player()

if len(sys.argv) > 1:
    client.host = sys.argv[1]

client.connection('username1')

while True:
    user_input.update(pygame.event.get())
    if user_input.escape: break
    p.update(user_input)
    r.render(p, client.world.get_list())
