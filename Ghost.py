import pygame
from Settings import *
import math


#implements the Ghost Class
class Ghost:

    def __init__(self,image,pos,tiles,player):
        self.tiles = tiles
        self.velocity = 100
        self.pos = pygame.Vector2(pos[0],pos[1])
        self.image = image
        self.player = player
        self.animtime =0 
        self.curvel = pygame.Vector2(0,0)
        self.hitbox = 0
        self.disabled = False

    def disable(self):
        self.disabled = True

    #Renders the ghost on a screen object and also handles animations
    def render(self,screen):
        self.animtime+=1
        self.animtime %= 150
        yoff = self.animtime%30
        # translu =
        if(yoff>=15):
            yoff = 30-yoff
        screen.blit(self.image,(self.pos[0],self.pos[1]+yoff))
        re = pygame.Rect((self.pos[0],self.pos[1]+yoff),(64,64))
        self.hitbox = re


    #moves the Ghost towards the player
    def move(self,dt):
        if(self.pos[0] > self.player.pos[0] and self.player.flipped) or (self.pos[0] < self.player.pos[0] and not self.player.flipped):
            return
        
        dirn = pygame.Vector2(self.player.pos[0]-self.pos[0],self.player.pos[1]-self.pos[1])
        dist = pygame.Vector2.magnitude(dirn)
        self.velocity = dist
        if self.velocity < 200: self.velocity = 200
        if dirn[0] != 0 and dirn[1] !=0:
            dirn = pygame.Vector2.normalize(dirn)
        dirn = dirn *self.velocity*dt
        self.pos += dirn
        self.curvel = dirn

            
        