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

    #Renders the Potion on a screen object and also handles animations
    def render(self,screen,offset,enemies):
        self.size = min(1.0,self.size)
        fb = pygame.Surface((100,100),pygame.SRCALPHA)
        fb.blit(pygame.transform.scale_by(self.tiles[115],self.size),(0,0))
        screen.blit(fb,(self.pos[0] + 32 - (32*self.size),self.pos[1]+self.size*64))
        re = pygame.Rect((self.pos[0]+ 32 - (32*self.size),self.pos[1]+self.size*64),(100,64))
        self.hitbox = re
        if self.size <=1.0:
            self.size += 0.050

    def effect(self):
        self.player.hp += 10
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

    #Renders the Sword on a screen object and also handles animations
    def render(self,screen,offset,enemies):
        self.size = min(1.0,self.size)
        fb = pygame.Surface((100,100),pygame.SRCALPHA)
        fb.blit(pygame.transform.scale_by(self.tiles[GOLDSWORD],self.size),(0,0))
        screen.blit(fb,(self.pos[0] + 32 - (32*self.size),self.pos[1]+self.size*64))
        re = pygame.Rect((self.pos[0]+ 32 - (32*self.size),self.pos[1]+self.size*64),(100,64))
        self.hitbox = re
        if self.size <=1.0:
            self.size += 0.050

    def effect(self):
        self.player.weaponid = GOLDSWORD
        self.player.dmg += 2
        self.player.score += Settings.SWORDSCORE