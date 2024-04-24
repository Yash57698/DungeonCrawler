import pygame
from Settings import *
import math


#implements the Fireball Class
class Fireball:

    def __init__(self,image,pos,tiles,player):
        self.enemytype = "FIREBALL"
        self.tiles = tiles
        self.velocity = Settings.FIREBALLSPEED
        self.pos = pygame.Vector2(pos[0],pos[1])
        self.image = image
        self.player = player
        self.hitbox = pygame.Rect((-1,-1),(1,1))
        self.size = 0.025
        self.damaged = False
        self.dirn = pygame.Vector2(self.player.pos[0]-self.pos[0],self.player.pos[1]-self.pos[1])
        if self.dirn[0] != 0 and self.dirn[1] !=0:
            self.dirn = pygame.Vector2.normalize(self.dirn)

    #Renders the fireball on a screen object and also handles animations
    def render(self,screen,offset,enemies):
        self.size = min(1.0,self.size)
        fb = pygame.Surface((100,100),pygame.SRCALPHA)
        fb.blit(pygame.transform.rotate(pygame.transform.scale_by(self.image,self.size),self.dirn.angle_to((1,0))),(0,0))
        screen.blit(fb,(self.pos[0],self.pos[1]))
        re = pygame.Rect((self.pos[0],self.pos[1]),(100,64))
        self.hitbox = re
        if self.size <=1.0:
            self.size += 0.020


    #moves the fireball towards the player
    def move(self,dt):        
        if(self.size<0.95):
            return
        delta = self.dirn *self.velocity*dt
        self.pos += delta
        self.curvel = delta
