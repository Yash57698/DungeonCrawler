import pygame
from Settings import *
import math


#implements the player Class
class Player:
    
    def __init__(self,image,image2,pos,tiles):
        self.score = 0
        self.hp = 100
        self.pos = pos
        self.tiles = tiles
        self.weaponid = SWORD
        self.image = image
        self.image2 = image2
        self.bounds = (200,100)
        self.pos = pygame.Vector2(0,0)
        self.offset= pygame.Vector2(0,0)
        self.minoffset = pygame.Vector2(0,0)
        self.maxoffset = pygame.Vector2(TOTALMAZESIZE[0]-SCREENSIZE[0],TOTALMAZESIZE[1]-SCREENSIZE[1])
        self.vel = 300
        self.curvel = pygame.Vector2(0,0)
        self.flipped = False
        self.idletime = 0 
        self.walktime = 0
        self.attack = 0
        self.attacktime = 0
        self.weaponrect = 0
        self.hitbox =0
        
    #Renders the player on a screen object and also handles animations
    def render(self,screen):

        if self.attack != 0:
            self.attacktime +=self.attack
        if self.attacktime == 0:
            self.attack = 0
        if self.curvel.x != 0 or self.curvel.y != 0:
            self.idletime =0
            self.walktime +=1
        else:
            self.idletime += 1
            self.walktime = 0
        yoff =0
        if self.idletime > 20:
            yoff = (self.idletime%88)//11
            if yoff >=4:
                yoff = 7-yoff

        if self.curvel.x != 0 or self.curvel.y != 0:
            yoff = (self.walktime%15)//1
            if yoff >=7:
                yoff = 14-yoff

        im = self.image
        if self.idletime > 100:
            im = self.image2

        player = pygame.Surface((64,80),pygame.SRCALPHA)
        player.blit(im,(0,0))
        weapon = pygame.Surface((120,100),pygame.SRCALPHA)
        angle = -(self.attacktime)
        if(self.attacktime>70):
            self.attack = -5
        weapon.blit(pygame.transform.rotate(self.tiles[self.weaponid],angle),(30,-(math.cos((angle*math.pi)/180)*10) +10 ))
        screen.blit(player if self.flipped else pygame.transform.flip(player,True,False),(self.pos[0],self.pos[1]+yoff))
        screen.blit(weapon if self.flipped else pygame.transform.flip(weapon,True,False),(self.pos[0],self.pos[1]+yoff) if self.flipped else (self.pos[0]-60,self.pos[1]+yoff))

        weaponpos = pygame.Vector2((self.pos[0],self.pos[1]+yoff) if self.flipped else (self.pos[0]-70,self.pos[1]+yoff))
        weaponpos += pygame.Vector2((30,-(math.cos((angle*math.pi)/180)*10) +10 ))
        re = pygame.Rect((weaponpos[0],weaponpos[1]),(math.sin((-angle*math.pi)/180)*60+30,math.cos((-angle*math.pi)/180)*60))
        self.weaponrect = re
        self.hitbox = pygame.Rect((self.pos[0],self.pos[1]+yoff),(64,64))
        
    #moves the player according to WASD control and handles the screenscroll effect
    def move(self,dt,map):
        keys = pygame.key.get_pressed()
        
        if self.attack !=0:
            return

        dx,dy = 0,0
        if keys[pygame.K_w] or keys[pygame.K_UP]:
            dy = - self.vel* dt
        if keys[pygame.K_s] or keys[pygame.K_DOWN]:
            dy = self.vel * dt
        if keys[pygame.K_a] or keys[pygame.K_LEFT]:
            dx = -self.vel * dt
        if keys[pygame.K_d] or keys[pygame.K_RIGHT]:
            dx = self.vel * dt


        if dx <0 :
            self.flipped = False
        if dx > 0:
            self.flipped = True

        self.pos += pygame.Vector2(dx,dy)
        if(self.pos.x < 0 or self.pos.y < 0 or self.pos.x+53 > TOTALMAZESIZE[0] or self.pos.y+53 > TOTALMAZESIZE[1] or map[int(self.pos.y//64)][int(self.pos.x//64)] == 1 or map[int((self.pos.y+53)//64)][int((self.pos.x+53)//64)] == 1 or map[int((self.pos.y+53)//64)][int((self.pos.x)//64)] == 1 or map[int((self.pos.y)//64)][int((self.pos.x+53)//64)] == 1):
            self.pos -= pygame.Vector2(dx,dy)
            dx = 0
            dy = 0


        if self.pos[0] -((SCREENSIZE[0]/2) + self.offset.x) > self.bounds[0] and dx >0:
            self.offset.x +=  dx
        if self.pos[0] -((SCREENSIZE[0]/2) + self.offset.x) < -self.bounds[0] and dx <0:
            self.offset.x +=  dx

        if self.pos[1] -((SCREENSIZE[1]/2) + self.offset.y) > self.bounds[1] and dy > 0:
            self.offset.y += dy
        if self.pos[1] -((SCREENSIZE[1]/2) + self.offset.y) < -self.bounds[1] and dy < 0:
            self.offset.y += dy

        if self.offset.x < self.minoffset.x : self.offset.x = self.minoffset.x
        if self.offset.y < self.minoffset.y : self.offset.y = self.minoffset.y

        if self.offset.x >self.maxoffset.x : self.offset.x = self.maxoffset.x
        if self.offset.y >self.maxoffset.y : self.offset.y = self.maxoffset.y
        
        self.curvel = pygame.Vector2(dx,dy)