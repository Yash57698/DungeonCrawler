import pygame
import random
from utilityfunctions import *
from Player import Player

SCREENSIZE = (1280,720)
MAZEDIM = (10,10)
TOTALMAZESIZE = (MAZEDIM[0]*3*64,MAZEDIM[1]*3*64)

pygame.init()
screen = pygame.display.set_mode(SCREENSIZE)
backgroundelements = pygame.Surface(TOTALMAZESIZE)
foregroundelements = pygame.Surface(TOTALMAZESIZE,pygame.SRCALPHA)
clock = pygame.time.Clock()
running = True
     

tiles = loadTileMap('./Assets/kenney_tinyDungeon/Tilemap/tilemap_packed.png')
print(tiles[0].get_rect().size)
map = [[0,0,0,0,0,1,0,0,0,0],
       [1,1,1,0,1,1,1,1,0,0],
       [0,0,0,0,1,0,1,0,0,0],
       [0,0,0,0,0,0,0,0,0,0],
       [0,0,0,0,0,1,1,0,0,0],
       [0,0,0,0,0,1,0,0,0,0],
       [0,0,0,0,0,0,0,0,0,0],
       [0,0,0,0,1,1,0,0,0,0],
       [0,0,0,0,1,1,0,0,0,0],
       [0,0,0,0,0,0,0,0,0,0]]
map = scalemapup(map)

p = Player(tiles[96],tiles[97],(300,100))
while running:
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False

    dt = clock.tick(60) / 1000
    
    
    renderMap(map,backgroundelements,tiles)
    foregroundelements.fill((0,0,0,0))
    p.render(foregroundelements)
    

    screen.blit(backgroundelements,-p.offset)
    screen.blit(foregroundelements,-p.offset)
    p.move(dt,map)
    pygame.display.flip()
        # time.sleep(2)

pygame.quit()