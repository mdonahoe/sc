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
if len(sys.argv) > 2:
    username = sys.argv[2]
else:
    username = 'anon'


client.connection(username)
send_interval = 0
while True:
    user_input.update(pygame.event.get())
    if user_input.escape: break
    p.update(user_input)
    send_interval += 1
    if send_interval > 30:
        send_interval = 0
        client.blockupdate(username, p.pos)
    r.render(p, client.world.get_list())
