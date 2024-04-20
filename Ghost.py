import pygame
from Settings import *
import math


#implements the Ghost Class
class Ghost:

    def __init__(self,image,pos,tiles,player):
        self.score = GHOSTSCORE
        self.enemytype = "GHOST"
        self.hp = GHOSTHP
        self.tiles = tiles
        self.velocity = 100
        self.pos = pygame.Vector2(pos[0],pos[1])
        self.image = image
        self.player = player
        self.animtime =0 
        self.curvel = pygame.Vector2(0,0)
        self.hitbox = 0
        self.disabled = False
        self.tinted = False

    def disable(self):
        self.disabled = True

    #Renders the ghost on a screen object and also handles animations
    def render(self,screen,offset,enemies):
        self.animtime+=1
        self.animtime %= 1000
        if(self.animtime%75 == 0):
            self.tinted = False
        yoff = self.animtime%30
        if(yoff>=15):
            yoff = 30-yoff
        gh = pygame.Surface((64,64),pygame.SRCALPHA)
        gh.blit(self.image,(0,0))
        if self.tinted:
            GB = min(255, max(0, round(255 * (0.8))))
            gh.fill((255, GB, GB), special_flags = pygame.BLEND_MULT)
        screen.blit(gh,(self.pos[0],self.pos[1]+yoff))
        re = pygame.Rect((self.pos[0],self.pos[1]+yoff),(64,64))
        self.hitbox = re


    #moves the Ghost towards the player
    def move(self,dt):
        dirn = pygame.Vector2(self.player.pos[0]-self.pos[0],self.player.pos[1]-self.pos[1])
        
        dist = pygame.Vector2.magnitude(dirn)
        self.velocity = dist
        if self.velocity < 200: self.velocity = 200
        if dirn[0] != 0 and dirn[1] !=0:
            dirn = pygame.Vector2.normalize(dirn)
        dirn = dirn *self.velocity*dt
        self.velocity = 200
        if(self.pos[0] > self.player.pos[0] and self.player.flipped) or (self.pos[0] < self.player.pos[0] and not self.player.flipped):
            dirn = pygame.Vector2.rotate(dirn,90)
        
        if self.tinted:
            # dirn = -pygame.Vector2(self.player.pos[0]-self.pos[0]/abs(self.player.pos[0]-self.pos[0]),0)
            if self.player.pos[0] > self.pos[0]:
                dirn = pygame.Vector2(-1,0)
            else:
                dirn = pygame.Vector2(1,0)
            dirn  = dirn*dt*100
        self.pos += dirn
        self.curvel = dirn

    def knockback(self,dt):
        self.tinted = True
        # dirn = -pygame.Vector2(self.player.pos[0]-self.pos[0]/abs(self.player.pos[0]-self.pos[0]),0)
        if self.player.pos[0] > self.pos[0]:
                dirn = pygame.Vector2(-1,0)
        else:
            dirn = pygame.Vector2(1,0)
        dirn = dirn*dt*100
            
        self.pos += dirn
        self.curvel = dirn
        