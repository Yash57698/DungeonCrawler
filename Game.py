import pygame
import random
from utilityfunctions import *
from Player import Player
from Ghost import Ghost
from mazehandling import generateMaze
from Settings import *

class Game:
    def __init__(self):
        self.screen = pygame.display.set_mode(SCREENSIZE,pygame.SRCALPHA)
        self.backgroundelements = pygame.Surface(TOTALMAZESIZE)
        self.foregroundelements = pygame.Surface(TOTALMAZESIZE,pygame.SRCALPHA)
        self.clock = pygame.time.Clock()
        self.running = True
        self.tiles = loadTileMap('./Assets/kenney_tinyDungeon/Tilemap/tilemap_packed.png')

    def RunGame(self):
        pygame.init()
        self.map = generateMaze(MAZEDIM[0],MAZEDIM[1])
        self.map = scalemapup(self.map)
        self.running = True
        self.p = Player(self.tiles[96],self.tiles[97],(128,128),self.tiles)
        self.enemies = [ Ghost(self.tiles[121],(256,256),self.tiles,self.p)]
        while self.running:
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    self.running = False
                if event.type == pygame.KEYDOWN:
                    if event.key == pygame.K_SPACE:
                        if(self.p.attack == 0):
                            self.p.attack = 10

            dt = self.clock.tick(60) / 1000
            renderMap(self.map,self.backgroundelements,self.tiles,self.p.offset)
            self.foregroundelements.fill((0,0,0,0))
            self.p.render(self.foregroundelements)
            for en in self.enemies:
                en.render(self.foregroundelements)
            self.screen.blit(self.backgroundelements,-self.p.offset)
            self.screen.blit(self.foregroundelements,-self.p.offset)
            if self.map[int(self.p.pos[1]//64)][int(self.p.pos[0]//64)] == 2:
                self.RunLevelCompleted(1,f"{pygame.time.get_ticks()/1000} seconds")
                return
            self.p.move(dt,self.map)
            for en in self.enemies:
                en.move(dt)

            DrawHealthBar(self.screen,self.p.hp/100)

            
            pygame.display.flip()

            if self.p.attack != 0:
                removeindex = []
                for i in range(len(self.enemies)):
                    en = self.enemies[i]
                    if pygame.Rect.colliderect(self.p.weaponrect,en.hitbox):
                        removeindex.append(i)
                removeindex.sort(reverse=True)
                for k in removeindex:
                    self.enemies.pop(k)
            
            for i in range(len(self.enemies)):
                en = self.enemies[i]
                if pygame.Rect.colliderect(self.p.hitbox,en.hitbox):
                        self.p.hp -= 1

            if self.p.hp <= 0:
                self.RunLevelFailed(1)
        pygame.quit()

    def RunMainMenu(self):
        pygame.init()
        self.running = True
        selected = 0
        t = 0
        while self.running:
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    self.running = False
                if event.type == pygame.KEYDOWN:
                    if event.key == pygame.K_s:
                        selected+=4
                        selected %= 3
                    if event.key == pygame.K_w:
                        selected+=2
                        selected%=3
                    if event.key == pygame.K_RETURN:
                        if selected == 0:
                            self.RunGame()
                            return  
                        elif selected == 1:
                            self.RunLeaderboard()
                            self.running = False
                        elif selected == 2:
                            self.running = False
            t+=1
            t%=50
            dt = self.clock.tick(60) / 1000
            Largefont = pygame.font.Font('./Assets/ThaleahFat.ttf',80)
            Smolfont = pygame.font.Font('./Assets/ThaleahFat.ttf',60)


            color = [(255,255,255),(255, 255, 255),(255, 255, 255)]
            if t<25:
                color[selected] = (255,226,98)

            homescr = pygame.image.load('./Assets/homescreen.png')
            self.screen.blit(homescr,(0,0))
            Heading = Largefont.render('Main Menu',False, (54, 65, 83))
            Headingact = Largefont.render('Main Menu',False, (255, 255, 255))

            NewGame = Smolfont.render('New Game',False,(54, 65, 83))
            NewGameact = Smolfont.render('New Game',False,color[0])

            Leaderboard = Smolfont.render('Leaderboard',False,(54, 65, 83))
            Leaderboardact = Smolfont.render('Leaderboard',False,color[1])
            QuitGame = Smolfont.render('Quit Game',False,(54, 65, 83))
            QuitGameact = Smolfont.render('Quit Game',False,color[2])

            self.screen.blit(Heading, (SCREENSIZE[0]/2 - (Heading.get_rect().size[0]/2)-4, 100-4))
            self.screen.blit(Heading, (SCREENSIZE[0]/2 - (Heading.get_rect().size[0]/2)-4, 100+4))
            self.screen.blit(Heading, (SCREENSIZE[0]/2 - (Heading.get_rect().size[0]/2)+4, 100-4))
            self.screen.blit(Heading, (SCREENSIZE[0]/2 - (Heading.get_rect().size[0]/2)+4, 100+4))
            self.screen.blit(Headingact, (SCREENSIZE[0]/2 - (Headingact.get_rect().size[0]/2), 100))


            self.screen.blit(NewGame, (SCREENSIZE[0]/2 - (NewGame.get_rect().size[0]/2)-4, 300-4))
            self.screen.blit(NewGame, (SCREENSIZE[0]/2 - (NewGame.get_rect().size[0]/2)-4, 300+4))
            self.screen.blit(NewGame, (SCREENSIZE[0]/2 - (NewGame.get_rect().size[0]/2)+4, 300-4))
            self.screen.blit(NewGame, (SCREENSIZE[0]/2 - (NewGame.get_rect().size[0]/2)+4, 300+4))
            self.screen.blit(NewGameact, (SCREENSIZE[0]/2 - (NewGameact.get_rect().size[0]/2), 300))


            self.screen.blit(Leaderboard, (SCREENSIZE[0]/2 - (Leaderboard.get_rect().size[0]/2)-4, 400-4))
            self.screen.blit(Leaderboard, (SCREENSIZE[0]/2 - (Leaderboard.get_rect().size[0]/2)-4, 400+4))
            self.screen.blit(Leaderboard, (SCREENSIZE[0]/2 - (Leaderboard.get_rect().size[0]/2)+4, 400-4))
            self.screen.blit(Leaderboard, (SCREENSIZE[0]/2 - (Leaderboard.get_rect().size[0]/2)+4, 400+4))
            self.screen.blit(Leaderboardact, (SCREENSIZE[0]/2 - (Leaderboardact.get_rect().size[0]/2), 400))


            self.screen.blit(QuitGame, (SCREENSIZE[0]/2 - (QuitGame.get_rect().size[0]/2)-4, 500-4))
            self.screen.blit(QuitGame, (SCREENSIZE[0]/2 - (QuitGame.get_rect().size[0]/2)-4, 500+4))
            self.screen.blit(QuitGame, (SCREENSIZE[0]/2 - (QuitGame.get_rect().size[0]/2)+4, 500-4))
            self.screen.blit(QuitGame, (SCREENSIZE[0]/2 - (QuitGame.get_rect().size[0]/2)+4, 500+4))
            self.screen.blit(QuitGameact, (SCREENSIZE[0]/2 - (QuitGameact.get_rect().size[0]/2), 500))
            pygame.display.flip()
        pygame.quit()
        exit()
    
    def RunLevelCompleted(self,levelid,time):
        pygame.init()
        self.running = True
        selected = 0
        t = 0
        while self.running:
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    self.running = False
                if event.type == pygame.KEYDOWN:
                    if event.key == pygame.K_s:
                        selected+=3
                        selected %= 2
                    if event.key == pygame.K_w:
                        selected+=1
                        selected%=2
                    if event.key == pygame.K_RETURN:
                        if selected == 1:
                            self.RunMainMenu()
                            return  
            t+=1
            t%=50
            dt = self.clock.tick(60) / 1000

            Largefont = pygame.font.Font('./Assets/ThaleahFat.ttf',80)
            Smolfont = pygame.font.Font('./Assets/ThaleahFat.ttf',60)


            color = [(255,255,255),(255, 255, 255),(255, 255, 255)]
            if t<25:
                color[selected] = (255,226,98)

            # homescr = pygame.image.load('./Assets/homescreen.png')
            # self.screen.blit(homescr,(0,0))
            Heading = Largefont.render('Level Completed',False, (54, 65, 83))
            Headingact = Largefont.render('Level Completed',False, (255, 255, 255))

            timetaken = Smolfont.render(f'Time Taken : {time}',False,(54, 65, 83))
            timetakenact = Smolfont.render(f'Time Taken : {time}',False,(255,255,255))

            Leaderboard = Smolfont.render('Leaderboard',False,(54, 65, 83))
            Leaderboardact = Smolfont.render('Leaderboard',False,color[0])
            MainMenu = Smolfont.render('Main Menu',False,(54, 65, 83))
            MainMenuact = Smolfont.render('Main Menu',False,color[1])

            self.screen.blit(Heading, (SCREENSIZE[0]/2 - (Heading.get_rect().size[0]/2)-4, 100-4))
            self.screen.blit(Heading, (SCREENSIZE[0]/2 - (Heading.get_rect().size[0]/2)-4, 100+4))
            self.screen.blit(Heading, (SCREENSIZE[0]/2 - (Heading.get_rect().size[0]/2)+4, 100-4))
            self.screen.blit(Heading, (SCREENSIZE[0]/2 - (Heading.get_rect().size[0]/2)+4, 100+4))
            self.screen.blit(Headingact, (SCREENSIZE[0]/2 - (Headingact.get_rect().size[0]/2), 100))


            self.screen.blit(timetaken, (SCREENSIZE[0]/2 - (timetaken.get_rect().size[0]/2)-4, 300-4))
            self.screen.blit(timetaken, (SCREENSIZE[0]/2 - (timetaken.get_rect().size[0]/2)-4, 300+4))
            self.screen.blit(timetaken, (SCREENSIZE[0]/2 - (timetaken.get_rect().size[0]/2)+4, 300-4))
            self.screen.blit(timetaken, (SCREENSIZE[0]/2 - (timetaken.get_rect().size[0]/2)+4, 300+4))
            self.screen.blit(timetakenact, (SCREENSIZE[0]/2 - (timetakenact.get_rect().size[0]/2), 300))


            self.screen.blit(Leaderboard, (SCREENSIZE[0]/2 - (Leaderboard.get_rect().size[0]/2)-4, 400-4))
            self.screen.blit(Leaderboard, (SCREENSIZE[0]/2 - (Leaderboard.get_rect().size[0]/2)-4, 400+4))
            self.screen.blit(Leaderboard, (SCREENSIZE[0]/2 - (Leaderboard.get_rect().size[0]/2)+4, 400-4))
            self.screen.blit(Leaderboard, (SCREENSIZE[0]/2 - (Leaderboard.get_rect().size[0]/2)+4, 400+4))
            self.screen.blit(Leaderboardact, (SCREENSIZE[0]/2 - (Leaderboardact.get_rect().size[0]/2), 400))


            self.screen.blit(MainMenu, (SCREENSIZE[0]/2 - (MainMenu.get_rect().size[0]/2)-4, 500-4))
            self.screen.blit(MainMenu, (SCREENSIZE[0]/2 - (MainMenu.get_rect().size[0]/2)-4, 500+4))
            self.screen.blit(MainMenu, (SCREENSIZE[0]/2 - (MainMenu.get_rect().size[0]/2)+4, 500-4))
            self.screen.blit(MainMenu, (SCREENSIZE[0]/2 - (MainMenu.get_rect().size[0]/2)+4, 500+4))
            self.screen.blit(MainMenuact, (SCREENSIZE[0]/2 - (MainMenuact.get_rect().size[0]/2), 500))
            pygame.display.flip()
        pygame.quit()

    def RunLevelFailed(self,levelid):
        pygame.init()
        self.running = True
        selected = 0
        t = 0
        while self.running:
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    self.running = False
                if event.type == pygame.KEYDOWN:
                    if event.key == pygame.K_s:
                        selected+=3
                        selected %= 1
                    if event.key == pygame.K_w:
                        selected+=1
                        selected%=1
                    if event.key == pygame.K_RETURN:
                        if selected == 0:
                            self.RunMainMenu()
                            return  
            t+=1
            t%=50
            dt = self.clock.tick(60) / 1000

            Largefont = pygame.font.Font('./Assets/ThaleahFat.ttf',80)
            Smolfont = pygame.font.Font('./Assets/ThaleahFat.ttf',60)


            color = [(255,255,255),(255, 255, 255),(255, 255, 255)]
            if t<25:
                color[selected] = (255,226,98)

            Heading = Largefont.render('You Died!',False, (54, 65, 83))
            Headingact = Largefont.render('You Died',False, (255, 255, 255))

            MainMenu = Smolfont.render('Main Menu',False,(54, 65, 83))
            MainMenuact = Smolfont.render('Main Menu',False,color[0])

            self.screen.fill((0,0,0,100))
            self.screen.blit(Heading, (SCREENSIZE[0]/2 - (Heading.get_rect().size[0]/2)-4, 100-4))
            self.screen.blit(Heading, (SCREENSIZE[0]/2 - (Heading.get_rect().size[0]/2)-4, 100+4))
            self.screen.blit(Heading, (SCREENSIZE[0]/2 - (Heading.get_rect().size[0]/2)+4, 100-4))
            self.screen.blit(Heading, (SCREENSIZE[0]/2 - (Heading.get_rect().size[0]/2)+4, 100+4))
            self.screen.blit(Headingact, (SCREENSIZE[0]/2 - (Headingact.get_rect().size[0]/2), 100))

            self.screen.blit(MainMenu, (SCREENSIZE[0]/2 - (MainMenu.get_rect().size[0]/2)-4, 500-4))
            self.screen.blit(MainMenu, (SCREENSIZE[0]/2 - (MainMenu.get_rect().size[0]/2)-4, 500+4))
            self.screen.blit(MainMenu, (SCREENSIZE[0]/2 - (MainMenu.get_rect().size[0]/2)+4, 500-4))
            self.screen.blit(MainMenu, (SCREENSIZE[0]/2 - (MainMenu.get_rect().size[0]/2)+4, 500+4))
            self.screen.blit(MainMenuact, (SCREENSIZE[0]/2 - (MainMenuact.get_rect().size[0]/2), 500))
            pygame.display.flip()
        pygame.quit()

    def RunLeaderboard(self):
        pygame.init()
        self.running = True
        selected = 0
        t = 0
        while self.running:
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    self.running = False
                if event.type == pygame.KEYDOWN:
                    if event.key == pygame.K_s:
                        selected+=3
                        selected %= 1
                    if event.key == pygame.K_w:
                        selected+=1
                        selected%=1
                    if event.key == pygame.K_RETURN:
                        if selected == 0:
                            self.RunMainMenu()
                            return  
            t+=1
            t%=50
            dt = self.clock.tick(60) / 1000

            Largefont = pygame.font.Font('./Assets/ThaleahFat.ttf',80)
            Smolfont = pygame.font.Font('./Assets/ThaleahFat.ttf',60)


            color = [(255,255,255),(255, 255, 255),(255, 255, 255)]
            if t<25:
                color[selected] = (255,226,98)

            # homescr = pygame.image.load('./Assets/homescreen.png')
            # self.screen.blit(homescr,(0,0))
            Heading = Largefont.render('Leaderboard',False, (54, 65, 83))
            Headingact = Largefont.render('Leaderboard',False, (255, 255, 255))

            
            MainMenu = Smolfont.render('Main Menu',False,(54, 65, 83))
            MainMenuact = Smolfont.render('Main Menu',False,color[0])

            self.screen.blit(Heading, (SCREENSIZE[0]/2 - (Heading.get_rect().size[0]/2)-4, 50-4))
            self.screen.blit(Heading, (SCREENSIZE[0]/2 - (Heading.get_rect().size[0]/2)-4, 50+4))
            self.screen.blit(Heading, (SCREENSIZE[0]/2 - (Heading.get_rect().size[0]/2)+4, 50-4))
            self.screen.blit(Heading, (SCREENSIZE[0]/2 - (Heading.get_rect().size[0]/2)+4, 50+4))
            self.screen.blit(Headingact, (SCREENSIZE[0]/2 - (Headingact.get_rect().size[0]/2), 50))

            self.screen.blit(MainMenu, (SCREENSIZE[0]/2 - (MainMenu.get_rect().size[0]/2)-4, 600-4))
            self.screen.blit(MainMenu, (SCREENSIZE[0]/2 - (MainMenu.get_rect().size[0]/2)-4, 600+4))
            self.screen.blit(MainMenu, (SCREENSIZE[0]/2 - (MainMenu.get_rect().size[0]/2)+4, 600-4))
            self.screen.blit(MainMenu, (SCREENSIZE[0]/2 - (MainMenu.get_rect().size[0]/2)+4, 600+4))
            self.screen.blit(MainMenuact, (SCREENSIZE[0]/2 - (MainMenuact.get_rect().size[0]/2), 600))
            pygame.display.flip()
        pygame.quit()
g = Game()
g.RunMainMenu()