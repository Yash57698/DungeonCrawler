import pygame
from Settings import *
from Ghost import Ghost
import math


#implements the Grave Class
class Grave:

    def __init__(self,pos,tiles,player):
        self.score = GRAVESCORE
        self.enemytype = "GRAVE"
        self.tiles = tiles
        self.pos = pygame.Vector2(pos[0],pos[1])
        self.player = player
        self.animtime =0 
        self.hitbox = 0
        self.spawned = 0

    #Renders the grave on a screen object and also handles animations
    def render(self,screen,offset,enemies):
        if ((self.animtime == 0 or self.spawned == 0) and self.spawned<MAXGRAVESPAWNS) and self.pos.x >= offset[0] and self.pos.x<=offset[0]+SCREENSIZE[0] and self.pos.y >= offset[1] and self.pos.y <= offset[1] + SCREENSIZE[1]:
            enemies.append(Ghost(self.tiles[121],(self.pos.x,self.pos.y),self.tiles,self.player))
            self.spawned +=1 
        self.animtime+=1
        self.animtime %= GRAVESPAWNTIME
        screen.blit(self.tiles[66],(self.pos[0],self.pos[1]))
        screen.blit(self.tiles[65],(self.pos[0],self.pos[1]-64))
        re = pygame.Rect((self.pos[0],self.pos[1]),(64,64))
        self.hitbox = re

    def move(self,dt):
        pass
            
        