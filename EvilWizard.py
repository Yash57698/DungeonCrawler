import pygame
from Settings import *
import math
from fireball import Fireball
import time

#implements the EvilWizard Class
class EvilWizard:

    def __init__(self,image,pos,tiles,player,map):
        self.map = map
        self.score = Settings.WIZARDSCORE
        self.enemytype = "WIZARD"
        self.hp = Settings.WIZARDHP
        self.weaponid = MAGICSTAFF
        self.tiles = tiles
        self.velocity = 200
        self.pos = pygame.Vector2(pos[0],pos[1])
        self.image = image
        self.player = player
        self.animtime =0 
        self.attacktime = 0
        self.attack = 0
        self.curvel = pygame.Vector2(0,0)
        self.hitbox = pygame.Rect((-1,-1),(1,1))
        self.disabled = False
        self.tinted = False
        self.flipped = False
        self.seenplayer = False
        self.target = (-1,-1)
        self.fireballimage = pygame.transform.scale_by(pygame.image.load("./Assets/fire.png"),0.15)

    def disable(self):
        self.disabled = True

    #Renders the Wizard on a screen object and also handles animations
    def render(self,screen,offset,enemies):
            # print(self.pos)
        if (self.pos[0] >= offset[0] - 50 and self.pos[0]<=offset[0]+SCREENSIZE[0]+50 and self.pos[1] >= offset[1]-128 and self.pos[1] <= offset[1] + SCREENSIZE[1]+128):
            self.animtime+=1
            self.animtime %= 1000
            if self.attack != 0:
                self.attacktime +=self.attack
            if self.attacktime <= 0:
                self.animtime = 0
                self.attack = 0
            if self.attack>0 and self.attacktime > 80:
                self.attack = 5
            elif self.attack>0 and self.attacktime > 40:
                self.attack = 3
            if(self.animtime%30 == 0):
                self.tinted = False
            yoff = (self.animtime%88)//11
            if(yoff>=4):
                yoff = 7-yoff

            wiz = pygame.Surface((64,64),pygame.SRCALPHA)
            wiz.blit(self.image,(0,0))
            if self.tinted:
                GB = min(255, max(0, round(255 * (0.8))))
                wiz.fill((255, GB, GB), special_flags = pygame.BLEND_MULT)
            screen.blit(wiz,(self.pos[0],self.pos[1]+yoff))
            re = pygame.Rect((self.pos[0],self.pos[1]+yoff),(64,64))
            self.hitbox = re

            if self.curvel[0] <0 :
                self.flipped = False
            if self.curvel[0] > 0:
                self.flipped = True
            weapon = pygame.Surface((120,100),pygame.SRCALPHA)
            ywepoff =0 
            angle = 0
            if self.attacktime !=0:
                if self.attacktime<=80 and self.attack<0:
                    self.attacktime = 0
                if(self.attacktime<=40):
                    ywepoff = self.attacktime/2
                elif(self.attacktime<=80):
                    ywepoff = (80-self.attacktime)/2
                else:
                    angle = -(self.attacktime-80)
                    if(self.attacktime>150):
                        self.attack = -1
            if(self.attack>0 and self.attacktime == 5):
                enemies.append(Fireball(self.fireballimage,(self.pos[0]+16,self.pos[1]+16),self.tiles,self.player))
            weapon.blit(pygame.transform.rotate(self.tiles[self.weaponid],angle),(30,-(math.cos((angle*math.pi)/180)*10) +10 ))
            screen.blit(wiz if self.flipped else pygame.transform.flip(wiz,True,False),(self.pos[0],self.pos[1]+yoff))
            screen.blit(weapon if self.flipped else pygame.transform.flip(weapon,True,False),(self.pos[0],self.pos[1]+yoff-ywepoff) if self.flipped else (self.pos[0]-60,self.pos[1]+yoff-ywepoff))

            weaponpos = pygame.Vector2((self.pos[0],self.pos[1]+yoff) if self.flipped else (self.pos[0]-70,self.pos[1]+yoff))
            weaponpos += pygame.Vector2((30,-(math.cos((angle*math.pi)/180)*10) +10 ))
            re = pygame.Rect((weaponpos[0],weaponpos[1]),(math.sin((-angle*math.pi)/180)*60+30,math.cos((-angle*math.pi)/180)*60))
            self.weaponrect = re
            self.hitbox = pygame.Rect((self.pos[0],self.pos[1]+yoff),(64,64))


    def pathfind(self):
        offset = self.player.offset
        stk = []
        t = time.time()
        # print(self.map[int((self.pos[1]+32)//64)][int((self.pos[0]+32)//64)] , self.map[int((self.player.pos[1]+32)//64)][int((self.player.pos[0]+32)//64)])
        if (self.pos[0] >= offset[0] - 50 and self.pos[0]<=offset[0]+SCREENSIZE[0]+50 and self.pos[1] >= offset[1]-128 and self.pos[1] <= offset[1] + SCREENSIZE[1]+128):
            if(self.map[int((self.pos[1]+32)//64)][int((self.pos[0]+32)//64)] != 0 or self.map[int((self.player.pos[1]+32)//64)][int((self.player.pos[0]+32)//64)] != 0):
                return
            stk.append((int((self.pos[1]+32)//64),int((self.pos[0]+32)//64)))
            maze = []
            for i in range(len(self.map)):
                row = []
                for j in range(len(self.map[0])):
                    row.append((400,(-1,-1)))
                maze.append(row)
            maze[int((self.pos[1]+32)//64)][int((self.pos[0]+32)//64)] = (0,(-1,-1))
            while len(stk) >0:
                y,x = stk.pop(0)
                if y == int((self.player.pos[1]+32)//64) and x == int((self.player.pos[0]+32)//64):
                    break
                if y!=0 and self.map[y-1][x] == 0 and maze[y-1][x][0] == 400:
                    maze[y-1][x] = (maze[y][x][0] +1,(y,x))
                    stk.append((y-1,x))
                if x!=0 and self.map[y][x-1] == 0 and maze[y][x-1][0] == 400:
                    maze[y][x-1] = (maze[y][x][0] +1,(y,x))
                    stk.append((y,x-1))
                if y!=len(self.map)-1 and self.map[y+1][x] == 0 and maze[y+1][x][0] == 400:
                    maze[y+1][x] = (maze[y][x][0] +1,(y,x))
                    stk.append((y+1,x))
                if x!=len(self.map[0])-1 and self.map[y][x+1] == 0 and maze[y][x+1][0] == 400:
                    maze[y][x+1] = (maze[y][x][0] +1,(y,x))
                    stk.append((y,x+1))
            cur = (int((self.player.pos[1]+32)//64),int((self.player.pos[0]+32)//64))
            path =[]
            prev = cur
            while(maze[cur[0]][cur[1]][1][0] != -1 ):
                if(time.time() - t >0.01):
                    break
                path.append(cur)
                prev = cur
                cur = maze[cur[0]][cur[1]][1]

            if not self.seenplayer and len(path)<=10:
                self.seenplayer = True
            elif self.seenplayer and len(path) >5:
                self.target = (prev[1]*64,prev[0]*64)
            elif self.seenplayer and self.attack == 0:
                self.attack = 1


    #moves the Wizard towards the player
    def move(self,dt):
        if (self.map[int((self.pos[1]+32)//64)][int((self.pos[0]+32)//64)] == 0 or self.map[int((self.player.pos[1]+32)//64)][int((self.player.pos[0]+32)//64)]== 0) :
            self.pathfind()
            
            if (self.attack!=0) or int((self.pos[1]+32)//64) == int(self.target[1]//64) and int((self.pos[0]+32)//64) == int(self.target[0]//64):
                dirn = pygame.Vector2(0,0)
            else:
                dirn = pygame.Vector2(self.target[0]-self.pos[0],self.target[1]-self.pos[1])
                if dirn[0] != 0 and dirn[1] !=0:
                    dirn = pygame.Vector2.normalize(dirn)
                dirn = dirn *self.velocity*dt
            if self.tinted:
                # dirn = -pygame.Vector2(self.player.pos[0]-self.pos[0]/abs(self.player.pos[0]-self.pos[0]),0)
                if self.player.pos[0] > self.pos[0]:
                    dirn = pygame.Vector2(-1,0)
                else:
                    dirn = pygame.Vector2(1,0)
                dirn  = dirn*dt*100
            self.pos += dirn
            self.curvel = dirn
            if self.map[int((self.pos[1]+32)//64)][int((self.pos[0]+32)//64)] == 1:
                self.pos -=dirn
                self.curvel = pygame.Vector2(0,0)
        

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
        