import pygame
import random
import time
from utilityfunctions import *
from Player import Player
from Ghost import Ghost
from EvilWizard import EvilWizard
from Chests import Chest
from mazehandling import generateMaze
from Settings import *

class Game:
    def __init__(self):
        """
        Initializes the Game object with screen
        """
        self.screen = pygame.display.set_mode(SCREENSIZE,pygame.SRCALPHA)
        self.backgroundelements = pygame.Surface(Settings.TOTALMAZESIZE)
        self.foregroundelements = pygame.Surface(Settings.TOTALMAZESIZE,pygame.SRCALPHA)
        self.clock = pygame.time.Clock()
        self.running = True
        self.tiles = loadTileMap('./Assets/kenney_tinyDungeon/Tilemap/tilemap_packed.png')

    def RunGame(self,difficulty):
        """
        selects the Settings for the game and then generates a new maze and starts the game
        """
        pygame.init()
        pygame.font.init()
        random.seed(int(time.time()))
        if difficulty == 0:
            #EASY MODE SETTINGS
            Settings.MAZEDIM = (20,20)
            Settings.TOTALMAZESIZE = (Settings.MAZEDIM[0]*3*64,Settings.MAZEDIM[1]*3*64)
            Settings.GHOSTHP = 1
            Settings.GHOSTDAMAGE = 0.5
            Settings.GRAVESPAWNCHANCE = 1
            Settings.MAXGRAVESPAWNS = 2
            Settings.WIZARDSPAWNCHANCE = 40
            Settings.GRAVESPAWNTIME = 800
            Settings.FIREBALLSPEED = 400
            Settings.SWORDDROPRATE = 10
        elif difficulty == 1:
            #MEDIUM MODE SETTINGS
            Settings.MAZEDIM = (30,30)
            Settings.TOTALMAZESIZE = (Settings.MAZEDIM[0]*3*64,Settings.MAZEDIM[1]*3*64)
            Settings.GHOSTHP = 2
            Settings.GHOSTDAMAGE = 1
            Settings.GRAVESPAWNCHANCE = 2
            Settings.MAXGRAVESPAWNS = 3
            Settings.WIZARDSPAWNCHANCE = 70
            Settings.GRAVESPAWNTIME = 600
            Settings.FIREBALLSPEED = 500
            Settings.SWORDDROPRATE = 20
        elif difficulty == 2:
            #HARD MODE SETTINGS
            Settings.MAZEDIM = (30,30)
            Settings.TOTALMAZESIZE = (Settings.MAZEDIM[0]*3*64,Settings.MAZEDIM[1]*3*64)
            Settings.GHOSTHP = 4
            Settings.GHOSTDAMAGE = 3
        
            Settings.GRAVESPAWNCHANCE = 1
            Settings.WIZARDSPAWNCHANCE = 70
            Settings.MAXGRAVESPAWNS = 5
            Settings.GRAVESPAWNTIME = 600
            Settings.FIREBALLSPEED = 600
            Settings.SWORDDROPRATE = 30
        Settings.SEED = (random.randint(0,1000000))

        self.map = generateMaze(Settings.MAZEDIM[0],Settings.MAZEDIM[1])
        self.map = scalemapup(self.map)
        generatepath(self.map)
        self.running = True


        self.p = Player(self.tiles[96],self.tiles[97],(64,64),self.tiles)
        self.enemies = []
        self.interactables = []
        # self.interactables.append(Chest((128,128),self.tiles,self.p))
        self.enemies = spawngraves(self.map,self.tiles,self.p)
        self.interactables = spawnchests(self.map,self.tiles,self.p,self.enemies)
        self.paused = False
        Smolfont = pygame.font.Font('./Assets/ThaleahFat.ttf',60)
        while self.running:
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    self.running = False
                if event.type == pygame.KEYDOWN:
                    if event.key == pygame.K_SPACE:
                        if(self.p.attack == 0):
                            self.p.attack = 10
                    if event.key == pygame.K_ESCAPE:
                        self.paused = True
            dt = self.clock.tick(60) / 1000

            renderMap(self.map,self.backgroundelements,self.tiles,self.p.offset)
            self.foregroundelements.fill((0,0,0,0))
            
            for i in self.interactables:
                i.render(self.foregroundelements,self.p.offset,self.interactables)
            for en in self.enemies:
                en.render(self.foregroundelements,self.p.offset,self.enemies)
            self.p.render(self.foregroundelements)
            self.screen.blit(self.backgroundelements,-self.p.offset)
            self.screen.blit(self.foregroundelements,-self.p.offset)
            if self.map[int(self.p.pos[1]//64)][int(self.p.pos[0]//64)] == 2:
                self.RunLevelCompleted(1,f"{pygame.time.get_ticks()/1000} seconds",self.p.score)
                return
            self.p.move(dt,self.map)
            for en in self.enemies:
                en.move(dt)

            t = 0
            selected = 0
            while self.paused:
                t+=1
                t%=150
                dt = self.clock.tick(60) / 1000
                for event in pygame.event.get():
                    if event.type == pygame.QUIT:
                        self.running = False
                        self.paused = False
                    if event.type == pygame.KEYDOWN:
                        if event.key == pygame.K_ESCAPE:
                            self.paused = False
                        if event.key in [pygame.K_s, pygame.K_DOWN]:
                            selected+=1
                            selected %= 2
                        if event.key in [pygame.K_w,pygame.K_UP]:
                            selected+=3
                            selected%=2
                        if event.key == pygame.K_RETURN:
                            if selected == 0:
                                self.paused = False 
                            elif selected == 1:
                                self.RunMainMenu()
                                return
                        if event.key == pygame.K_p:
                            pygame.image.save(self.tiles[107],"gold.jpg")
                color = [(255,255,255),(255, 255, 255),(255, 255, 255)]
                if t<75:
                    color[selected] = (255,226,98)

                self.screen.blit(self.backgroundelements,-self.p.offset)
                self.screen.blit(self.foregroundelements,-self.p.offset)

                Resume = Smolfont.render('Resume',False,(54, 65, 83))
                Resumeact = Smolfont.render('Resume',False,color[0])

                QuitGame = Smolfont.render('Main Menu',False,(54, 65, 83))
                QuitGameact = Smolfont.render('Main Menu',False,color[1])

                self.screen.blit(Resume, (SCREENSIZE[0]/2 - (Resume.get_rect().size[0]/2)-4, 300-4))
                self.screen.blit(Resume, (SCREENSIZE[0]/2 - (Resume.get_rect().size[0]/2)-4, 300+4))
                self.screen.blit(Resume, (SCREENSIZE[0]/2 - (Resume.get_rect().size[0]/2)+4, 300-4))
                self.screen.blit(Resume, (SCREENSIZE[0]/2 - (Resume.get_rect().size[0]/2)+4, 300+4))
                self.screen.blit(Resumeact, (SCREENSIZE[0]/2 - (Resumeact.get_rect().size[0]/2), 300))

                self.screen.blit(QuitGame, (SCREENSIZE[0]/2 - (QuitGame.get_rect().size[0]/2)-4, 500-4))
                self.screen.blit(QuitGame, (SCREENSIZE[0]/2 - (QuitGame.get_rect().size[0]/2)-4, 500+4))
                self.screen.blit(QuitGame, (SCREENSIZE[0]/2 - (QuitGame.get_rect().size[0]/2)+4, 500-4))
                self.screen.blit(QuitGame, (SCREENSIZE[0]/2 - (QuitGame.get_rect().size[0]/2)+4, 500+4))
                self.screen.blit(QuitGameact, (SCREENSIZE[0]/2 - (QuitGameact.get_rect().size[0]/2), 500))
                pygame.display.flip()    


            DrawHealthBar(self.screen,self.p.hp/100)
            DisplayScore(self.screen,self.p.score)
            
            
            pygame.display.flip()



            if self.p.attack != 0:
                removeindex = []
                for i in range(len(self.enemies)):
                    en = self.enemies[i]
                    if pygame.Rect.colliderect(self.p.weaponrect,en.hitbox):
                        if en.enemytype == "GRAVE":
                            self.p.score += en.score
                            removeindex.append(i)
                        if en.enemytype == "GHOST":
                            if not en.tinted:
                                en.hp-=self.p.dmg
                                en.tinted = True
                                en.knockback(dt)
                                if en.hp <= 0:
                                    self.p.score += en.score
                                    removeindex.append(i)
                        if en.enemytype == "WIZARD":
                            if not en.tinted:
                                en.hp-=self.p.dmg
                                en.tinted = True
                                en.knockback(dt)
                                if en.hp <= 0:
                                    self.p.score += en.score
                                    removeindex.append(i)
                removeindex.sort(reverse=True)
                for k in removeindex:
                    self.enemies.pop(k)

                removeindex = []
                for i in range(len(self.interactables)):
                    obj = self.interactables[i]
                    if obj.type == "CHEST" and pygame.Rect.colliderect(self.p.weaponrect,obj.hitbox):
                        obj.opened = True
            removeindex = []
            for i in range(len(self.interactables)):
                obj = self.interactables[i]
                if obj.type in ["POTION","SWORD"]  and obj.size>=0.95 and pygame.Rect.colliderect(self.p.hitbox,obj.hitbox):
                    obj.effect()
                    removeindex.append(i)
            removeindex.sort(reverse=True)
            for k in removeindex:
                self.interactables.pop(k)
            
            for i in range(len(self.enemies)):
                en = self.enemies[i]
                if pygame.Rect.colliderect(self.p.hitbox,en.hitbox):
                    if en.enemytype == "GHOST":
                        if not en.tinted:
                            self.p.hp -= Settings.GHOSTDAMAGE
                    if en.enemytype == "FIREBALL":
                        if en.damaged == False:
                            en.damaged = True
                            self.p.hp -= Settings.FIREBALLDAMAGE

            if self.p.hp <= 0:
                self.RunLevelFailed(1)
        pygame.quit()

    def RunMainMenu(self):
        """
        Runs the Main menu GUI
        """
        pygame.init()
        pygame.font.init()
        self.running = True
        selected = 0
        t = 0
        homescr = pygame.image.load('./Assets/homescreen.png')
        while self.running:
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    self.running = False
                if event.type == pygame.KEYDOWN:
                    if event.key in [pygame.K_s, pygame.K_DOWN]:
                        selected+=4
                        selected %= 3
                    if event.key in [pygame.K_w,pygame.K_UP]:
                        selected+=2
                        selected%=3
                    if event.key == pygame.K_RETURN:
                        if selected == 0:
                            self.RunLevelSelect()
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

            
            self.screen.blit(homescr,(0,0))
            Heading = Largefont.render('Main Menu',True, (54, 65, 83))
            Headingact = Largefont.render('Main Menu',True, (255, 255, 255))

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
    
    def RunLevelCompleted(self,levelid,time,score):
        """
        Runs the level completed GUI
        
        Args:
            levelid : takes the difficulty the level was completed at
            time : the time taken to complete the level
            score : the score with which the level was completed
        """
        pygame.init()
        pygame.font.init()
        self.running = True
        selected = 0
        t = 0
        homescr = pygame.image.load('./Assets/homescreen.png')
        name = ""
        Reading = True
        running = True
        while Reading and running:
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    running = False
                    self.running = False
                if event.type == pygame.KEYDOWN:
                    if event.key == pygame.K_RETURN:
                        Reading = False
                    elif event.key == pygame.K_BACKSPACE:
                        if name!="":
                            name = name[:-1]
                    else:
                        name += event.unicode

            self.screen.blit(homescr,(0,0))
            Largefont = pygame.font.Font('./Assets/ThaleahFat.ttf',80)
            Smolfont = pygame.font.Font('./Assets/ThaleahFat.ttf',60)

            Heading = Largefont.render('Enter Your Name',False, (54, 65, 83))
            Headingact = Largefont.render('Enter Your Name',False, (255, 255, 255))

            self.screen.blit(Heading, (SCREENSIZE[0]/2 - (Heading.get_rect().size[0]/2)-4, 100-4))
            self.screen.blit(Heading, (SCREENSIZE[0]/2 - (Heading.get_rect().size[0]/2)-4, 100+4))
            self.screen.blit(Heading, (SCREENSIZE[0]/2 - (Heading.get_rect().size[0]/2)+4, 100-4))
            self.screen.blit(Heading, (SCREENSIZE[0]/2 - (Heading.get_rect().size[0]/2)+4, 100+4))
            self.screen.blit(Headingact, (SCREENSIZE[0]/2 - (Headingact.get_rect().size[0]/2), 100))
            
            InputField = Largefont.render(name,False, (54, 65, 83))
            InputFieldact = Largefont.render(name,False, (255,255,255))
            self.screen.blit(InputField, (SCREENSIZE[0]/2 - (InputField.get_rect().size[0]/2)-4, 300-4))
            self.screen.blit(InputField, (SCREENSIZE[0]/2 - (InputField.get_rect().size[0]/2)-4, 300+4))
            self.screen.blit(InputField, (SCREENSIZE[0]/2 - (InputField.get_rect().size[0]/2)+4, 300-4))
            self.screen.blit(InputField, (SCREENSIZE[0]/2 - (InputField.get_rect().size[0]/2)+4, 300+4))
            self.screen.blit(InputFieldact, (SCREENSIZE[0]/2 - (InputFieldact.get_rect().size[0]/2), 300))

            pygame.display.flip()
        if name!="":
            updateleaderboard(name,score)
        while self.running:
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    self.running = False
                if event.type == pygame.KEYDOWN:
                    if event.key in [pygame.K_s, pygame.K_DOWN]:
                        selected+=3
                        selected %= 2
                    if event.key in [pygame.K_w, pygame.K_UP]:
                        selected+=1
                        selected%=2
                    if event.key == pygame.K_RETURN:
                        if selected == 1:
                            self.RunMainMenu()
                            return 
                        if selected == 0:
                            self.RunLeaderboard()
                            return 
            t+=1
            t%=50
            dt = self.clock.tick(60) / 1000

        
            self.screen.blit(homescr,(0,0))
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

            scoredisp = Smolfont.render(f'Score : {score}',False,(54, 65, 83))
            scoredispact = Smolfont.render(f'Score : {score}',False,(255,255,255))

            Leaderboard = Smolfont.render('Leaderboard',False,(54, 65, 83))
            Leaderboardact = Smolfont.render('Leaderboard',False,color[0])
            MainMenu = Smolfont.render('Main Menu',False,(54, 65, 83))
            MainMenuact = Smolfont.render('Main Menu',False,color[1])

            self.screen.blit(Heading, (SCREENSIZE[0]/2 - (Heading.get_rect().size[0]/2)-4, 50-4))
            self.screen.blit(Heading, (SCREENSIZE[0]/2 - (Heading.get_rect().size[0]/2)-4, 50+4))
            self.screen.blit(Heading, (SCREENSIZE[0]/2 - (Heading.get_rect().size[0]/2)+4, 50-4))
            self.screen.blit(Heading, (SCREENSIZE[0]/2 - (Heading.get_rect().size[0]/2)+4, 50+4))
            self.screen.blit(Headingact, (SCREENSIZE[0]/2 - (Headingact.get_rect().size[0]/2), 50))


            self.screen.blit(timetaken, (SCREENSIZE[0]/2 - (timetaken.get_rect().size[0]/2)-4, 200-4))
            self.screen.blit(timetaken, (SCREENSIZE[0]/2 - (timetaken.get_rect().size[0]/2)-4, 200+4))
            self.screen.blit(timetaken, (SCREENSIZE[0]/2 - (timetaken.get_rect().size[0]/2)+4, 200-4))
            self.screen.blit(timetaken, (SCREENSIZE[0]/2 - (timetaken.get_rect().size[0]/2)+4, 200+4))
            self.screen.blit(timetakenact, (SCREENSIZE[0]/2 - (timetakenact.get_rect().size[0]/2), 200))

            self.screen.blit(scoredisp, (SCREENSIZE[0]/2 - (scoredisp.get_rect().size[0]/2)-4, 300-4))
            self.screen.blit(scoredisp, (SCREENSIZE[0]/2 - (scoredisp.get_rect().size[0]/2)-4, 300+4))
            self.screen.blit(scoredisp, (SCREENSIZE[0]/2 - (scoredisp.get_rect().size[0]/2)+4, 300-4))
            self.screen.blit(scoredisp, (SCREENSIZE[0]/2 - (scoredisp.get_rect().size[0]/2)+4, 300+4))
            self.screen.blit(scoredispact, (SCREENSIZE[0]/2 - (scoredispact.get_rect().size[0]/2), 300))


            self.screen.blit(Leaderboard, (SCREENSIZE[0]/2 - (Leaderboard.get_rect().size[0]/2)-4, 500-4))
            self.screen.blit(Leaderboard, (SCREENSIZE[0]/2 - (Leaderboard.get_rect().size[0]/2)-4, 500+4))
            self.screen.blit(Leaderboard, (SCREENSIZE[0]/2 - (Leaderboard.get_rect().size[0]/2)+4, 500-4))
            self.screen.blit(Leaderboard, (SCREENSIZE[0]/2 - (Leaderboard.get_rect().size[0]/2)+4, 500+4))
            self.screen.blit(Leaderboardact, (SCREENSIZE[0]/2 - (Leaderboardact.get_rect().size[0]/2), 500))


            self.screen.blit(MainMenu, (SCREENSIZE[0]/2 - (MainMenu.get_rect().size[0]/2)-4, 600-4))
            self.screen.blit(MainMenu, (SCREENSIZE[0]/2 - (MainMenu.get_rect().size[0]/2)-4, 600+4))
            self.screen.blit(MainMenu, (SCREENSIZE[0]/2 - (MainMenu.get_rect().size[0]/2)+4, 600-4))
            self.screen.blit(MainMenu, (SCREENSIZE[0]/2 - (MainMenu.get_rect().size[0]/2)+4, 600+4))
            self.screen.blit(MainMenuact, (SCREENSIZE[0]/2 - (MainMenuact.get_rect().size[0]/2), 600))
            pygame.display.flip()
        pygame.quit()

    def RunLevelFailed(self,levelid):
        """
            Runs the level Failed GUI
            Args:
                levelid : takes the difficulty the level was running at
        """
        pygame.init()
        pygame.font.init()
        self.running = True
        selected = 0
        t = 0
        while self.running:
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    self.running = False
                if event.type == pygame.KEYDOWN:
                    if event.key in [pygame.K_s, pygame.K_DOWN]:
                        selected+=3
                        selected %= 1
                    if event.key in [pygame.K_s, pygame.K_UP]:
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
        """
        Runs the leaderboard GUI
        """
        pygame.init()
        pygame.font.init()
        self.running = True
        selected = 0
        t = 0
        leaderboard = getleaderboard()
        leaderboard = [("SCORE","NAME")] +leaderboard
        while self.running:
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    self.running = False
                if event.type == pygame.KEYDOWN:
                    if event.key in [pygame.K_s, pygame.K_DOWN]:
                        selected+=3
                        selected %= 1
                    if event.key in [pygame.K_w, pygame.K_UP]:
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

            homescr = pygame.image.load('./Assets/homescreen.png')
            self.screen.blit(homescr,(0,0))
            Heading = Largefont.render('Leaderboard',False, (54, 65, 83))
            Headingact = Largefont.render('Leaderboard',False, (255, 255, 255))

            
            MainMenu = Smolfont.render('Main Menu',False,(54, 65, 83))
            MainMenuact = Smolfont.render('Main Menu',False,color[0])

            cnt = 0
            for i in leaderboard[:4]:
                ren = Smolfont.render(f"{i[1]}    {i[0]}",False,(54, 65, 83))
                renact = Smolfont.render(f"{i[1]}    {i[0]}",False,(255,255,255))
                self.screen.blit(ren, (SCREENSIZE[0]/2 - (ren.get_rect().size[0]/2)-4, 100+(cnt*80)-4))
                self.screen.blit(ren, (SCREENSIZE[0]/2 - (ren.get_rect().size[0]/2)-4, 100+(cnt*80)+4))
                self.screen.blit(ren, (SCREENSIZE[0]/2 - (ren.get_rect().size[0]/2)+4, 100+(cnt*80)-4))
                self.screen.blit(ren, (SCREENSIZE[0]/2 - (ren.get_rect().size[0]/2)+4, 100+(cnt*80)+4))
                self.screen.blit(renact, (SCREENSIZE[0]/2 - (renact.get_rect().size[0]/2), 100+(cnt*80)))
                cnt+=1

            self.screen.blit(Heading, (SCREENSIZE[0]/2 - (Heading.get_rect().size[0]/2)-4, 30-4))
            self.screen.blit(Heading, (SCREENSIZE[0]/2 - (Heading.get_rect().size[0]/2)-4, 30+4))
            self.screen.blit(Heading, (SCREENSIZE[0]/2 - (Heading.get_rect().size[0]/2)+4, 30-4))
            self.screen.blit(Heading, (SCREENSIZE[0]/2 - (Heading.get_rect().size[0]/2)+4, 30+4))
            self.screen.blit(Headingact, (SCREENSIZE[0]/2 - (Headingact.get_rect().size[0]/2), 30))

            self.screen.blit(MainMenu, (SCREENSIZE[0]/2 - (MainMenu.get_rect().size[0]/2)-4, 600-4))
            self.screen.blit(MainMenu, (SCREENSIZE[0]/2 - (MainMenu.get_rect().size[0]/2)-4, 600+4))
            self.screen.blit(MainMenu, (SCREENSIZE[0]/2 - (MainMenu.get_rect().size[0]/2)+4, 600-4))
            self.screen.blit(MainMenu, (SCREENSIZE[0]/2 - (MainMenu.get_rect().size[0]/2)+4, 600+4))
            self.screen.blit(MainMenuact, (SCREENSIZE[0]/2 - (MainMenuact.get_rect().size[0]/2), 600))
            pygame.display.flip()
        pygame.quit()
    
    def RunLevelSelect(self):
        """
        Runs the Level Select GUI
        """
        pygame.init()
        pygame.font.init()
        self.running = True
        selected = 0
        t = 0
        homescr = pygame.image.load('./Assets/homescreen.png')
        while self.running:
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    self.running = False
                if event.type == pygame.KEYDOWN:
                    if event.key in [pygame.K_s, pygame.K_DOWN]:
                        selected+=4
                        selected %= 3
                    if event.key in [pygame.K_w,pygame.K_UP]:
                        selected+=2
                        selected%=3
                    if event.key == pygame.K_RETURN:
                        self.RunGame(selected)
                        return
            t+=1
            t%=50
            dt = self.clock.tick(60) / 1000
            Largefont = pygame.font.Font('./Assets/ThaleahFat.ttf',80)
            Smolfont = pygame.font.Font('./Assets/ThaleahFat.ttf',60)


            color = [(255,255,255),(255, 255, 255),(255, 255, 255)]
            if t<25:
                color[selected] = (255,226,98)

            
            self.screen.blit(homescr,(0,0))
            Heading = Largefont.render('Select Difficulty',True, (54, 65, 83))
            Headingact = Largefont.render('Select Difficulty',True, (255, 255, 255))

            NewGame = Smolfont.render('Normal',False,(54, 65, 83))
            NewGameact = Smolfont.render('Normal',False,color[0])

            Leaderboard = Smolfont.render('Hard',False,(54, 65, 83))
            Leaderboardact = Smolfont.render('Hard',False,color[1])
            QuitGame = Smolfont.render('Insane',False,(54, 65, 83))
            QuitGameact = Smolfont.render('Insane',False,color[2])

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


g = Game()
g.RunMainMenu()