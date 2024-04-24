import pygame
import random
from Settings import *
from EvilWizard import EvilWizard
from Chests import Chest
from Graves import Grave
import csv


def DrawHealthBar(screen,health):
    heartimg = pygame.transform.scale_by(pygame.image.load("./Assets/heartim.png"),0.045)
    heart = pygame.Surface((50,50),pygame.SRCALPHA)
    heart.blit(heartimg,(0,0))
    pygame.draw.rect(screen,(0,0,0),pygame.Rect((815,40),(400,30)))
    pygame.draw.rect(screen,(48, 39, 38),pygame.Rect((818,43),(394,24)))
    pygame.draw.rect(screen,(204, 36, 36),pygame.Rect((818,43),(health*394,24)))
    screen.blit(heart,(800,30))

def DisplayScore(screen,score):
    Smolfont = pygame.font.Font('./Assets/ThaleahFat.ttf',60)
    Score = Smolfont.render(f'Score: {score}',False,(54, 65, 83))
    Scoreact = Smolfont.render(f'Score: {score}',False,(255, 255, 255))
    screen.blit(Score,(1215 - Score.get_rect().width-4,80-4))
    screen.blit(Score,(1215 - Score.get_rect().width-4,80+4))
    screen.blit(Score,(1215 - Score.get_rect().width+4,80-4))
    screen.blit(Score,(1215 - Score.get_rect().width+4,80+4))
    screen.blit(Scoreact,(1215 - Score.get_rect().width,80))

def updateleaderboard(newname = "",newscore = -1):
    leaderboard = []
    with open(LEADERBOARDFILE) as csv_file:
        csv_reader = csv.reader(csv_file, delimiter=',')
        line_count = 0
        for row in csv_reader:
            if line_count == 0:
                line_count+=1
                pass
            else:
                if len(row)!=0:
                    leaderboard.append((int(row[1]),row[0]))
        if newscore !=-1:
            leaderboard.append((newscore,newname))
        print(leaderboard)
        leaderboard.sort(reverse=True)

        leaderboard = leaderboard[:-1]
    
    with open(LEADERBOARDFILE, mode='w') as file:
        writer = csv.writer(file, delimiter=',')

        writer.writerow(['Name', 'Score'])
        for row in leaderboard:
            writer.writerow([row[1], row[0]])

def getleaderboard():
    leaderboard = []
    with open(LEADERBOARDFILE) as csv_file:
        csv_reader = csv.reader(csv_file, delimiter=',')
        line_count = 0
        for row in csv_reader:
            if line_count == 0:
                line_count+=1
                pass
            else:
                if len(row)!=0:
                    leaderboard.append((row[1],row[0]))
    return leaderboard
    
        


# Loads the TileMap from location given to it
def loadTileMap(file):
    size = (64,64)
    margin = 0
    spacing = 0
    x0 = margin
    y0 = margin
    dx = size[0] + spacing
    dy = size[1] + spacing

    tiles = []
    image = pygame.transform.scale_by(pygame.image.load(file),4.0)
    rect = image.get_rect()
    print(rect.size)
    for y in range(y0,rect.height,dy):
        for x in range(x0,rect.width,dx):
            tile = pygame.Surface(size,pygame.SRCALPHA)
            tile.blit((image),(0,0),(x,y,*(size)))
            tiles.append(tile)
    print(f"loaded tileset with {len(tiles)} tiles from file : {file}")
    return tiles

#scales the maze map generated to make the paths 3 wide
def scalemapup(map):
    newmap = []
    for i in range(len(map)*3):
        row = []
        for j in range(len(map[0])*3):
            row.append(0)
        newmap.append(row)

    for y in range(len(map)):
        for x in range(len(map[0])):
            center = (1+(3*y),1+(3*x))
            if(map[y][x] == 1):
                for p in range(-1,2):
                    for q in range(-1,2):
                        newmap[center[0]+p][center[1]+q] = 1
            
    newmap[len(newmap)-7][len(newmap[0])-1] = 2
    return newmap

#renders the map onto a specified screen
#Only renders those tiles which can be seen on the screen
def renderMap(map,screen,tiles,offset):
    for y in range(len(map)):
        for x in range(len(map[0])):
            if(64*x >= offset[0] - 50 and 64*x<=offset[0]+SCREENSIZE[0]+50 and 64*y >= offset[1]-128 and 64*y <= offset[1] + SCREENSIZE[1]+128):
                if map[y][x] == 0:
                    if y!=0 and map[y-1][x] == 1 and x!=0 and map[y][x-1] == 1:
                        screen.blit(pygame.transform.flip(tiles[52],True,False),(64*x,64*y))#rounded shadow
                    elif x!=0 and map[y][x-1] == 1 and y!=0 and map[y-1][x-1] == 0 and map[y-1][x] == 0:
                        screen.blit(pygame.transform.flip(pygame.transform.flip(tiles[53],True,True),True,False),(64*x,64*y))#smol round
                    elif y!=0 and map[y-1][x] == 0 and x!=0 and map[y][x-1] == 0 and map[y-1][x-1] == 1:
                        screen.blit(tiles[53],(64*x,64*y))
                    elif x!=0 and map[y][x-1] == 1:
                        random.seed(((len(map))*y)+x+Settings.SEED)
                        ty = random.randint(0,9)
                        tile = 50
                        if ty<2:
                            tile = 51
                        screen.blit(pygame.transform.rotate(tiles[tile],90),(64*x,64*y))
                    elif y!=0 and map[y-1][x] == 1:
                        random.seed(((len(map))*y)+x+Settings.SEED)
                        ty = random.randint(0,9)
                        tile = 50
                        if ty<2:
                            tile = 51
                        screen.blit(pygame.transform.rotate(tiles[tile],0),(64*x,64*y))
                        if ty == 9:

                            screen.blit(pygame.transform.rotate(tiles[30],0),(64*x,64*y))
                            screen.blit(pygame.transform.rotate(tiles[18],0),(64*x,64*(y-1)))
                            screen.blit(pygame.transform.rotate(tiles[6],0),(64*x,64*(y-2)))
                    else:
                        random.seed(((len(map))*y)+x+Settings.SEED)
                        ty = random.randint(0,99)
                        if ty>89:
                            screen.blit(tiles[49],(64*x,64*y))
                        elif ty<2:
                            screen.blit(tiles[42],(64*x,64*y))
                        else:
                            screen.blit(tiles[48],(64*x,64*y))    

                elif map[y][x] == 1 or map[y][x] == 2:
                    if y!=0 and x!=0 and map[y-1][x] == 0 and map[y][x-1] ==0:
                        screen.blit(tiles[4],(64*x,64*y)) #top left roof
                    elif y!=0 and x!=(len(map[0])-1) and map[y-1][x] == 0 and map[y][x+1] ==0:
                        screen.blit(tiles[5],(64*x,64*y))#top right roof
                    elif y!=0 and map[y-1][x] == 0:
                        screen.blit(tiles[26],(64*x,64*y))#top roof
                    elif y< (len(map)-2) and map[y+1][x] == 1 and map[y+2][x] == 0 and x!=0 and map[y][x-1] == 0:
                        screen.blit(tiles[16],(64*x,64*y))#bottom left roof
                    elif y< (len(map)-2) and map[y+1][x] == 1 and map[y+2][x] == 0 and x!=(len(map[0])-1) and map[y][x+1] == 0:
                        screen.blit(tiles[17],(64*x,64*y))#bottom right roof
                    elif y!=(len(map)-1) and map[y+1][x] == 0 and x!=0 and map[y][x-1] == 0:
                        screen.blit(tiles[57],(64*x,64*y))#bottom left wall
                    elif y!=(len(map)-1) and map[y+1][x] == 0 and x!=(len(map[0])-1) and map[y][x+1] == 0:
                        screen.blit(tiles[59],(64*x,64*y))#bottom right wall
                    elif y!=(len(map)-1) and map[y+1][x] == 0:
                        random.seed(((len(map))*y)+x+Settings.SEED)
                        ty = random.randint(0,100)
                        if ty<4:
                            screen.blit(tiles[29],(64*x,64*y))#flag wall
                        else:
                            screen.blit(tiles[40],(64*x,64*y))#bottom wall
                    elif y< (len(map)-2) and map[y+1][x] == 1 and map[y+2][x] == 0:
                        screen.blit(tiles[2],(64*x,64*y))#bottom roof
                    elif x!=0 and (map[y][x-1] == 0 or (map[y][x-1] == 1 and y!=(len(map)-1) and map[y+1][x-1] == 0)):
                        screen.blit(tiles[15],(64*x,64*y))#left roof
                    elif x!=(len(map[0])-1) and (map[y][x+1] == 0 or (map[y][x+1] == 1 and y!=(len(map)-1) and map[y+1][x+1] == 0)):
                        screen.blit(tiles[13],(64*x,64*y))#right roof
                    elif y< (len(map)-2) and x!=(len(map[0])-1) and map[y+1][x] == 1 and map[y+2][x] == 1 and map[y+2][x+1] == 0:
                        screen.blit(tiles[1],(64*x,64*y))#left turn
                    elif x!=0 and y!=0 and map[y-1][x-1] == 0:
                        screen.blit(tiles[27],(64*x,64*y))# turn
                    elif x!=(len(map[0])-1) and y!=0 and map[y-1][x+1] == 0:
                        screen.blit(tiles[25],(64*x,64*y))# turn
                    elif x!=0 and y<(len(map)-2) and map[y][x-1] == 1 and map[y+1][x-1] == 1 and map[y+2][x-1] == 0:
                        screen.blit(tiles[3],(64*x,64*y))# turn
                    else :
                        random.seed(((len(map))*y)+x+Settings.SEED)
                        ty = random.randint(0,100)
                        if ty<5:
                            screen.blit(tiles[12],(64*x,64*y))
                        elif ty<10:
                            screen.blit(tiles[24],(64*x,64*y))
                        else:
                            screen.blit(tiles[0],(64*x,64*y))
                if y == len(map)-7 and x == len(map[0])-1:
                    screen.blit(tiles[45],(64*x,64*y)) 

def spawngraves(map,tiles,player):
    enemies = []
    offset = (0,0)
    for y in range(len(map)):
        for x in range(len(map[0])):
            if not (64*x >= offset[0] - 50 and 64*x<=offset[0]+SCREENSIZE[0]+50 and 64*y >= offset[1]-50 and 64*y <= offset[1] + SCREENSIZE[1]+50):
                if map[y][x] == 0 and y>=2 and map[y-1][x] == 0 and map[y-2][x] == 0:
                    random.seed(((len(map))*y)+x+Settings.SEED)  
                    ty = random.randint(1,100)
                    if ty <= Settings.GRAVESPAWNCHANCE:
                        enemies.append(Grave((64*x,64*y),tiles,player))
    return enemies

def spawnchests(map,tiles,player,enemies):
    interactables = []
    offset = (0,0)
    for y in range(len(map)):
        for x in range(len(map[0])):
            if not (64*x >= offset[0] - 50 and 64*x<=offset[0]+SCREENSIZE[0]+50 and 64*y >= offset[1]-50 and 64*y <= offset[1] + SCREENSIZE[1]+50):
                if map[y][x] == 0 and y>=2 and map[y-1][x] == 1 and x!=0 and map[y-1][x-1] == 1 and x!=(len(map[0])-1) and map[y-1][x+1] == 1:
                    random.seed(((len(map))*y)+x+Settings.SEED)  
                    ty = random.randint(1,100)
                    if ty <= Settings.CHESTSPAWNCHANCE:
                        interactables.append(Chest((64*x,64*y),tiles,player))
                        k = random.randint(1,100)
                        if k<= Settings.WIZARDSPAWNCHANCE:
                            enemies.append(EvilWizard(tiles[111],(64*x,64*y),tiles,player,map))
    return interactables