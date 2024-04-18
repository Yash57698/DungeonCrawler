import pygame
import random
from utilityfunctions import *

SCREENSIZE = (1280,720)
TOTALMAZESIZE = (1920,1920)
pygame.init()
screen = pygame.display.set_mode(SCREENSIZE)
backgroundelements = pygame.Surface(TOTALMAZESIZE)
foregroundelements = pygame.Surface(TOTALMAZESIZE,pygame.SRCALPHA)
clock = pygame.time.Clock()
running = True
     

tiles = loadTileMap('./Assets/kenney_tinyDungeon/Tilemap/tilemap_packed.png')
print(tiles[0].get_rect().size)
map = [[0,0,0,0,0,1,0,0,0],
       [1,1,1,0,1,1,1,1,0],
       [0,0,0,0,1,0,1,0,0],
       [0,0,0,0,0,0,0,0,0],
       [0,0,0,0,0,1,1,0,0],
       [0,0,0,0,0,1,0,0,0],
       [0,0,0,0,0,0,0,0,0]]

map = scalemapup(map)

class Player:
    bounds = (200,100)
    pos = pygame.Vector2(0,0)
    offset= pygame.Vector2(0,0)
    minoffset = pygame.Vector2(0,0)
    vel = 300
    curvel = pygame.Vector2(0,0)
    flipped = False

    def __init__(self,image,pos):
        self.pos = pos
        self.image = image

    def render(self,screen):
        #TO-DO : Idle animation + hopanimation

        screen.blit(self.image if self.flipped else pygame.transform.flip(self.image,True,False),(self.pos[0],self.pos[1]))

    def move(self,dt):
        keys = pygame.key.get_pressed()
        
        dx,dy = 0,0
        if keys[pygame.K_w]:
            dy = - self.vel* dt
        if keys[pygame.K_s]:
            dy = self.vel * dt
        if keys[pygame.K_a]:
            dx = -self.vel * dt
        if keys[pygame.K_d]:
            dx = self.vel * dt


        if dx <0 :
            self.flipped = False
        if dx > 0:
            self.flipped = True

        self.pos += pygame.Vector2(dx,dy)
        if self.pos[0] -((SCREENSIZE[0]/2) + p.offset.x) > self.bounds[0] and dx >0:
            self.offset.x +=  dx
        if self.pos[0] -((SCREENSIZE[0]/2) + p.offset.x) < -self.bounds[0] and dx <0:
            self.offset.x +=  dx

        if self.pos[1] -((SCREENSIZE[1]/2) + p.offset.y) > self.bounds[1] and dy > 0:
            self.offset.y += dy
        if self.pos[1] -((SCREENSIZE[1]/2) + p.offset.y) < -self.bounds[1] and dy < 0:
            self.offset.y += dy

        if self.offset.x < self.minoffset.x : self.offset.x = self.minoffset.x
        if self.offset.y < self.minoffset.y : self.offset.y = self.minoffset.y
        
        self.curvel = (dx,dy)

p = Player(tiles[96],(300,300))
while running:
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False

    dt = clock.tick(60) / 1000
    
    
    renderMap(map,backgroundelements,tiles)
    foregroundelements.fill((0,0,0,0))
    p.render(foregroundelements)
    

    screen.blit(backgroundelements,-p.offset)
    screen.blit(foregroundelements,-p.offset)
    p.move(dt)
    pygame.display.flip()
        # time.sleep(2)

pygame.quit()