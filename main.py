import pygame
from utilityfunctions import *

SCREENSIZE = (1280,720)

pygame.init()
screen = pygame.display.set_mode(SCREENSIZE)
clock = pygame.time.Clock()
running = True
     

tiles = loadTileMap('./Assets/kenney_tinyDungeon/Tilemap/tilemap_packed.png')
while running:
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False

    dt = clock.tick(60) / 1000

    # player postion update
    for y in range(11):
        for x in range(12):
            screen.blit(tiles[y*12 + x],(64*x , 64*y))
    # for i in range(132):
    #     screen.blit(tiles[i],(0,0))
    pygame.display.flip()
        # time.sleep(2)

pygame.quit()