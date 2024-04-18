import pygame
import random
from utilityfunctions import *
from Player import Player
from mazehandling import generateMaze
from Settings import *



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

map = generateMaze(MAZEDIM[0],MAZEDIM[1])
map = scalemapup(map)

p = Player(tiles[96],tiles[97],(128,128))
while running:
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False

    dt = clock.tick(60) / 1000
    # print(clock.get_fps())
    
    
    renderMap(map,backgroundelements,tiles,p.offset)
    foregroundelements.fill((0,0,0,0))
    p.render(foregroundelements)
    

    screen.blit(backgroundelements,-p.offset)
    screen.blit(foregroundelements,-p.offset)
    p.move(dt,map)
    pygame.display.flip()
        # time.sleep(2)

pygame.quit()