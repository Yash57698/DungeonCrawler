import pygame
from Settings import *
import math


#implements the Ghost Class
class Ghost:

    def __init__(self,image,pos,tiles,player):
        """
            initilizes the ghost object
        """
        self.score = Settings.GHOSTSCORE
        self.enemytype = "GHOST"
        self.hp = Settings.GHOSTHP
        self.tiles = tiles
        self.velocity = 100
        self.pos = pygame.Vector2(pos[0],pos[1])
        self.image = image
        self.player = player
        self.animtime =0 
        self.curvel = pygame.Vector2(0,0)
        self.hitbox = pygame.Rect((-1,-1),(1,1))
        self.disabled = False
        self.tinted = False

    def render(self,screen,offset,enemies):
        """
        Renders the ghost on a screen object and also handles animations
        Args:
            screen: the pygame screen object to render the object to.
            offset: the offset to check whether to render the object
            enemies: the list of enemies in the game
        """
        if (self.pos[0] >= offset[0] - 50 and self.pos[0]<=offset[0]+SCREENSIZE[0]+50 and self.pos[1] >= offset[1]-128 and self.pos[1] <= offset[1] + SCREENSIZE[1]+128):
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

    def move(self,dt):
        """
        handles the movement of the ghost enemy
        moves the Ghost towards the player
        Args:
            dt: the time passed between this frame and the last
        """
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
        """
        Handles the knockback after getting hit by the player
        Args:
            dt:the time passed between this frame and the last
        """
        self.tinted = True
        # dirn = -pygame.Vector2(self.player.pos[0]-self.pos[0]/abs(self.player.pos[0]-self.pos[0]),0)
        if self.player.pos[0] > self.pos[0]:
                dirn = pygame.Vector2(-1,0)
        else:
            dirn = pygame.Vector2(1,0)
        dirn = dirn*dt*100
            
        self.pos += dirn
        self.curvel = dirn
        