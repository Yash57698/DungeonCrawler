import pygame
from Settings import *
import math

#implements the Potion Class
class Potion:

    def __init__(self,pos,tiles,player):
        self.type = "POTION"
        self.tiles = tiles
        self.pos = pygame.Vector2(pos[0],pos[1])
        self.player = player
        self.hitbox = pygame.Rect((-1,-1),(1,1))
        self.size = 0.025

    def render(self,screen,offset,enemies):
        """
        Renders the Potion on a screen object and also handles animations
        Args:
            screen: the pygame screen object to render the object to.
            offset: the offset to check whether to render the object
            enemies: the list of enemies in the game
        """
        self.size = min(1.0,self.size)
        fb = pygame.Surface((100,100),pygame.SRCALPHA)
        fb.blit(pygame.transform.scale_by(self.tiles[115],self.size),(0,0))
        screen.blit(fb,(self.pos[0] + 32 - (32*self.size),self.pos[1]+self.size*64))
        re = pygame.Rect((self.pos[0]+ 32 - (32*self.size),self.pos[1]+self.size*64),(100,64))
        self.hitbox = re
        if self.size <=1.0:
            self.size += 0.050

    def effect(self):
        """
        handles the effect given to the player on consuming the Potion
        """
        self.player.hp += 30
        self.player.hp = min(self.player.hp,100)
        self.player.score += Settings.POTIONSCORE

#implements the Sword Class
class Sword:

    def __init__(self,pos,tiles,player):
        self.type = "SWORD"
        self.tiles = tiles
        self.pos = pygame.Vector2(pos[0],pos[1])
        self.player = player
        self.hitbox = 0
        self.size = 0.025

    def render(self,screen,offset,enemies):
        """
        Renders the Sword on a screen object and also handles animations
        Args:
            screen: the pygame screen object to render the object to.
            offset: the offset to check whether to render the object
            enemies: the list of enemies in the game
        """
        self.size = min(1.0,self.size)
        fb = pygame.Surface((100,100),pygame.SRCALPHA)
        fb.blit(pygame.transform.scale_by(self.tiles[GOLDSWORD],self.size),(0,0))
        screen.blit(fb,(self.pos[0] + 32 - (32*self.size),self.pos[1]+self.size*64))
        re = pygame.Rect((self.pos[0]+ 32 - (32*self.size),self.pos[1]+self.size*64),(100,64))
        self.hitbox = re
        if self.size <=1.0:
            self.size += 0.050

    def effect(self):
        """
        handles the effect given to the player on getting the sword
        """
        self.player.weaponid = GOLDSWORD
        self.player.dmg += 2
        self.player.score += Settings.SWORDSCORE