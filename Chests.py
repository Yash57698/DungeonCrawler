import pygame
from Settings import *
from Collectables import *


#implements the Chest Class
class Chest:

    def __init__(self,pos,tiles,player):
        self.tiles = tiles
        self.type = "CHEST"
        self.pos = pygame.Vector2(pos[0],pos[1])
        self.player = player
        self.animtime =0 
        self.hitbox = pygame.Rect((-1,-1),(1,1))
        self.opened = False

    def render(self,screen,offset,interactables):
        """
        Renders the Chest on a screen object and also handles animations
        Args:
            screen: the pygame screen object to render the object to.
            offset: the offset to check whether to render the object
            interactables: the list of interactable items in the game
        """
        if (self.pos[0] >= offset[0] - 50 and self.pos[0]<=offset[0]+SCREENSIZE[0]+50 and self.pos[1] >= offset[1]-128 and self.pos[1] <= offset[1] + SCREENSIZE[1]+128):
            if self.animtime <20 and self.opened:
                self.animtime += 1
            tile = 89
            if self.opened:
                if self.animtime <=5:
                    tile = 89
                elif self.animtime <=10:
                    tile = 90
                else:
                    tile = 91
            if self.opened and self.animtime == 19:
                random.seed(((40))*self.pos[0]+self.pos[1]+Settings.SEED)
                ty = random.randint(1,100)
                if ty>=(100-Settings.SWORDDROPRATE):
                    interactables.append(Sword((self.pos[0],self.pos[1]),self.tiles,self.player))
                else:
                    interactables.append(Potion((self.pos[0],self.pos[1]),self.tiles,self.player))
            screen.blit(self.tiles[tile],(self.pos[0],self.pos[1]))
            re = pygame.Rect((self.pos[0],self.pos[1]),(64,64))
            self.hitbox = re

    def move(self,dt):
        pass
            
        