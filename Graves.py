import pygame
from Settings import *
from Ghost import Ghost
import math


#implements the Grave Class
class Grave:

    def __init__(self,pos,tiles,player):
        self.score = Settings.GRAVESCORE
        self.enemytype = "GRAVE"
        self.tiles = tiles
        self.pos = pygame.Vector2(pos[0],pos[1])
        self.player = player
        self.animtime =0 
        self.hitbox = pygame.Rect((-1,-1),(1,1))
        self.spawned = 0

    #Renders the grave on a screen object and also handles animations
    def render(self,screen,offset,enemies):
        if (self.pos[0] >= offset[0] - 50 and self.pos[0]<=offset[0]+SCREENSIZE[0]+50 and self.pos[1] >= offset[1]-128 and self.pos[1] <= offset[1] + SCREENSIZE[1]+128):
            if ((self.animtime == 0 or self.spawned == 0) and self.spawned<Settings.MAXGRAVESPAWNS) and self.pos.x >= offset[0] and self.pos.x<=offset[0]+SCREENSIZE[0] and self.pos.y >= offset[1] and self.pos.y <= offset[1] + SCREENSIZE[1]:
                enemies.append(Ghost(self.tiles[121],(self.pos.x,self.pos.y),self.tiles,self.player))
                self.spawned +=1 
            self.animtime+=1
            self.animtime %= Settings.GRAVESPAWNTIME
            screen.blit(self.tiles[66],(self.pos[0],self.pos[1]))
            screen.blit(self.tiles[65],(self.pos[0],self.pos[1]-64))
            re = pygame.Rect((self.pos[0],self.pos[1]),(64,64))
            self.hitbox = re

    def move(self,dt):
        pass
            
        