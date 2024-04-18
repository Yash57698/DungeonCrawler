import pygame
import random
from Settings import *

# Loads the TileMap from location given to it
def loadTileMap(file):
    size = (64,64)
    margin = 0
    spacing = 0
    x0 = margin
    y0 = margin
    dx = size[0] + spacing
    dy = size[1] + spacing

    tiles = []
    image = pygame.transform.scale_by(pygame.image.load(file),4.0)
    rect = image.get_rect()
    print(rect.size)
    for y in range(y0,rect.height,dy):
        for x in range(x0,rect.width,dx):
            tile = pygame.Surface(size,pygame.SRCALPHA)
            tile.blit((image),(0,0),(x,y,*(size)))
            tiles.append(tile)
    print(f"loaded tileset with {len(tiles)} tiles from file : {file}")
    return tiles

#scales the maze map generated to make the paths 3 wide
def scalemapup(map):
    newmap = []
    for i in range(len(map)*3):
        row = []
        for j in range(len(map[0])*3):
            row.append(0)
        newmap.append(row)

    for y in range(len(map)):
        for x in range(len(map[0])):
            center = (1+(3*y),1+(3*x))
            if(map[y][x] == 1):
                for p in range(-1,2):
                    for q in range(-1,2):
                        newmap[center[0]+p][center[1]+q] = 1
    return newmap

#renders the map onto a specified screen
#Only renders those tiles which can be seen on the screen
def renderMap(map,screen,tiles,offset):
    for y in range(len(map)):
        for x in range(len(map[0])):
            if(64*x >= offset[0] - 50 and 64*x<=offset[0]+SCREENSIZE[0]+50 and 64*y >= offset[1]-50 and 64*y <= offset[1] + SCREENSIZE[1]+50):
                if map[y][x] == 0:
                    if y!=0 and map[y-1][x] == 1 and x!=0 and map[y][x-1] == 1:
                        screen.blit(pygame.transform.flip(tiles[52],True,False),(64*x,64*y))#rounded shadow
                    elif x!=0 and map[y][x-1] == 1 and y!=0 and map[y-1][x-1] == 0 and map[y-1][x] == 0:
                        screen.blit(pygame.transform.flip(pygame.transform.flip(tiles[53],True,True),True,False),(64*x,64*y))#smol round
                    elif y!=0 and map[y-1][x] == 0 and x!=0 and map[y][x-1] == 0 and map[y-1][x-1] == 1:
                        screen.blit(tiles[53],(64*x,64*y))
                    elif x!=0 and map[y][x-1] == 1:
                        random.seed(((len(map))*y)+x)
                        ty = random.randint(0,9)
                        tile = 50
                        if ty<2:
                            tile = 51
                        screen.blit(pygame.transform.rotate(tiles[tile],90),(64*x,64*y))
                    elif y!=0 and map[y-1][x] == 1:
                        random.seed(((len(map))*y)+x)
                        ty = random.randint(0,9)
                        tile = 50
                        if ty<2:
                            tile = 51
                        screen.blit(pygame.transform.rotate(tiles[tile],0),(64*x,64*y))
                    else:
                        random.seed(((len(map))*y)+x)
                        ty = random.randint(0,99)
                        if ty>89:
                            screen.blit(tiles[49],(64*x,64*y))
                        elif ty<2:
                            screen.blit(tiles[42],(64*x,64*y))
                        else:
                            screen.blit(tiles[48],(64*x,64*y))
                if map[y][x] == 1:
                    if y!=0 and x!=0 and map[y-1][x] == 0 and map[y][x-1] ==0:
                        screen.blit(tiles[4],(64*x,64*y)) #top left roof
                    elif y!=0 and x!=(len(map[0])-1) and map[y-1][x] == 0 and map[y][x+1] ==0:
                        screen.blit(tiles[5],(64*x,64*y))#top right roof
                    elif y!=0 and map[y-1][x] == 0:
                        screen.blit(tiles[26],(64*x,64*y))#top roof
                    elif y< (len(map)-2) and map[y+1][x] == 1 and map[y+2][x] == 0 and x!=0 and map[y][x-1] == 0:
                        screen.blit(tiles[16],(64*x,64*y))#bottom left roof
                    elif y< (len(map)-2) and map[y+1][x] == 1 and map[y+2][x] == 0 and x!=(len(map[0])-1) and map[y][x+1] == 0:
                        screen.blit(tiles[17],(64*x,64*y))#bottom right roof
                    elif y!=(len(map)-1) and map[y+1][x] == 0 and x!=0 and map[y][x-1] == 0:
                        screen.blit(tiles[57],(64*x,64*y))#bottom left wall
                    elif y!=(len(map)-1) and map[y+1][x] == 0 and x!=(len(map[0])-1) and map[y][x+1] == 0:
                        screen.blit(tiles[59],(64*x,64*y))#bottom right wall
                    elif y!=(len(map)-1) and map[y+1][x] == 0:
                        screen.blit(tiles[40],(64*x,64*y))#bottom wall
                    elif y< (len(map)-2) and map[y+1][x] == 1 and map[y+2][x] == 0:
                        screen.blit(tiles[2],(64*x,64*y))#bottom roof
                    elif x!=0 and (map[y][x-1] == 0 or (map[y][x-1] == 1 and y!=(len(map)-1) and map[y+1][x-1] == 0)):
                        screen.blit(tiles[15],(64*x,64*y))#left roof
                    elif x!=(len(map[0])-1) and (map[y][x+1] == 0 or (map[y][x+1] == 1 and y!=(len(map)-1) and map[y+1][x+1] == 0)):
                        screen.blit(tiles[13],(64*x,64*y))#right roof
                    elif y< (len(map)-2) and x!=(len(map[0])-1) and map[y+1][x] == 1 and map[y+2][x] == 1 and map[y+2][x+1] == 0:
                        screen.blit(tiles[1],(64*x,64*y))#left turn
                    elif x!=0 and y!=0 and map[y-1][x-1] == 0:
                        screen.blit(tiles[27],(64*x,64*y))# turn
                    elif x!=(len(map[0])-1) and y!=0 and map[y-1][x+1] == 0:
                        screen.blit(tiles[25],(64*x,64*y))# turn
                    elif x!=0 and y<(len(map)-2) and map[y][x-1] == 1 and map[y+1][x-1] == 1 and map[y+2][x-1] == 0:
                        screen.blit(tiles[3],(64*x,64*y))# turn
                    else :
                        random.seed(((len(map))*y)+x)
                        ty = random.randint(0,100)
                        if ty<5:
                            screen.blit(tiles[12],(64*x,64*y))
                        elif ty<10:
                            screen.blit(tiles[24],(64*x,64*y))
                        else:
                            screen.blit(tiles[0],(64*x,64*y))