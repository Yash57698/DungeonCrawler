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

    def render(self,screen,offset,enemies):
        """
        Renders the Fireball on a screen object and also handles animations
        Args:
            screen: the pygame screen object to render the object to.
            offset: the offset to check whether to render the object
            enemies: the list of enemies in the game
        """
        self.size = min(1.0,self.size)
        fb = pygame.Surface((100,100),pygame.SRCALPHA)
        fb.blit(pygame.transform.rotate(pygame.transform.scale_by(self.image,self.size),self.dirn.angle_to((1,0))),(0,0))
        screen.blit(fb,(self.pos[0],self.pos[1]))
        re = pygame.Rect((self.pos[0],self.pos[1]),(100,64))
        self.hitbox = re
        

    def move(self,dt):     
        """
        handles the movement of the ghost enemy
        moves the Ghost towards the player
        Args:
            dt: the time passed between this frame and the last
        """   
        self.size = min(1.0,self.size)
        if self.size <=1.0:
            self.size += 0.020
        if(self.size<0.95):
            return
        delta = self.dirn *self.velocity*dt
        self.pos += delta
        self.curvel = delta
