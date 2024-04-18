import pygame

SCREENSIZE = (1280,720)
MAZEDIM = (10,10)
TOTALMAZESIZE = (MAZEDIM[0]*3*64,MAZEDIM[1]*3*64)

class Player:
    bounds = (200,100)
    pos = pygame.Vector2(0,0)
    offset= pygame.Vector2(0,0)
    minoffset = pygame.Vector2(0,0)
    maxoffset = pygame.Vector2(TOTALMAZESIZE[0]-SCREENSIZE[0],TOTALMAZESIZE[1]-SCREENSIZE[1])
    vel = 300
    curvel = pygame.Vector2(0,0)
    flipped = False
    idletime = 0 
    def __init__(self,image,image2,pos):
        self.pos = pos
        self.image = image
        self.image2 = image2

    def render(self,screen):
        #TO-DO : Idle animation + hopanimation
        if self.curvel.x != 0 or self.curvel.y != 0:
            self.idletime =0
        else:
            self.idletime += 1

        yoff =0
        if self.idletime > 20:
            yoff = (self.idletime%88)//11
        if yoff >=4:
            yoff = 7-yoff

        im = self.image
        if self.idletime > 100:
            im = self.image2
        
        screen.blit(im if self.flipped else pygame.transform.flip(im,True,False),(self.pos[0],self.pos[1]+yoff))

    def move(self,dt,map):
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