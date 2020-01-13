import pygame as pg
import random, time, os
# colors  ---------------------------------------------- #
black = (0,0,0)
white = (255,255,255)
blue = (0,0,255)
green = (0,255,0)
red = (255,0,0)
grey = (127,127,127)
grey1 = (192,192,192)
# window ----------------------------------------------- #
W_WIDTH, W_HEIGTH = 400,900
win = pg.display.set_mode((W_WIDTH,W_HEIGTH))
pg.display.set_caption("Piano Tiles!")
# font ------------------------------------------------- #
pg.font.init()
FONT = pg.font.SysFont("comicsans",60)
FONT_S = pg.font.SysFont("comicsans",20)

screen = 0 # variable that tells in which screen player is #

def clr(win,color=white): # clears the screen #
    win.fill(color)

directory = os.getcwd()
directory += "\\level_lib" # directory of levels #
try:
    level_names = [name.replace(".txt","") for name in os.listdir(directory)]
except:
    level_names = [""]
# format the level names #
if not level_names:
    level_names.append("random")
for i,name in enumerate(level_names):
    if not name:
        level_names[i] = "random"
def random_level(n: int = 100): # return list containing n rows, each with random tiles #
    level = []
    for i in range(n):
        av = [(0,0),(0,1),(1,0)]
        a = random.choice(av)
        if a == (0,0): # prevent from situation, where there's no tile in a row #
            av.pop(av.index(a))
        b = random.choice(av)
        level.append([*a,*b])
    return level

def open_levels(name): # open a level file to read it #
    if name and not "random" in name.lower() and name.lower() != "random": # if hame is diferent from "" and "random" #
        with open(os.path.join(directory,name+".txt"),"r") as f: # read its properties !to do! #
            level = f.read()
            if level:
                level = eval(level)
                return level
            else:
                return random_level(n=100)
    else: # if there's no name or there is 'random' in it, return the random level #
        if name:
            try: # if file of that name exists, try extracting a 
                with open(os.path.join(directory,name+".txt"),"r") as f:
                    rang = f.read()
                    try:
                        rang = int(rang)
                        if isinstance(rang,int):
                            if not 500 >= rang >= 10:
                                rang = 100
                                raise ValueError(f"Invalid number {rang}")
                    except:
                        rang = 100
            except FileNotFoundError:
                rang = 100
        return random_level(n=rang)

levels = [(name,open_levels(name)) for name in level_names] # list of all levels available #


class Menu:
    def __init__(self): # screens -> 0 - mainMenu, 0.5 - settings, 0.75 - gameMenu, 1 - game, 1.25 - pause menu #
        self.coords = [(100,int(100*(2.5*i+1.4))) for i in range(3)]
        self.sett = self.restore()
        self.settText = [(25,i*50+50) for i in range(len(self.sett)+1)] # names of the settings #
        self.settBB = [(x-10,y+15) for x,y in self.settText] # coords for buttons to configure settings #
        self.settId = [name for name in self.sett.keys()] # lists that binds keys from self.sett into integers #
        self.settSelected = None # variable that tells which setting is selected #

    def restore(self): # restores default values of settings #
        return {"speed":5.,"gainSpeed":2.5,"volume":5}

    def display(self,win): # displays the mainScreen with buttons for (play or sett or exit) #
        clr(win,color=blue)
        names = ("Play","Settings","Exit")
        for i,string in enumerate(names):
            x,y = self.coords[i]
            pg.draw.rect(win,green,(x,y,200,80)) # draw buttons #
            s = FONT.render(string,1,black)
            x1 = 10+x+s.get_width()//2 if i != 1 else 110
            win.blit(s,(x1,y+20))

    def check(self,x,y,s): # checks if user clicked any button # 
        if s == 0 or s == 1.25: # mainMenu #
            for i,(x1,y1) in enumerate(self.coords):
                if x1+200 >= x >= x1 and y1+80 >= y >= y1:
                    return i
        elif s == 0.5: # mainMenu -> settings #
            for i, (x1,y1) in enumerate(self.settBB):
                d = ((x-x1)**2 + (y-y1)**2)**0.5
                if d <= 7: # check whether a player clicked any circle #
                    if i <= len(self.sett)-1:
                        self.settSelected = i
                        return True
                    else:
                        self.sett = self.restore()
        elif s == 0.75: # gameMenu # 
            x1 = 10
            for i, _ in enumerate(level_names):    
                y1 = i*50+20
                d = ((x-x1)**2+(y-y1)**2)**0.5 # check whether a player clicked any circle #
                if d <= 7:
                    return i
        return None

    def display_settigs(self,win): # displays the settings (see ^ self.restore()) #
        clr(win,color=blue)
        for i,(sett,value) in enumerate(self.sett.items()): # render settings, with its value and buttons #
            color = red
            color1 = black
            if self.settSelected != None and self.settSelected == i:
                color = blue
                color1 = red # setting, that player is overriding is on red color #
            win.blit(FONT.render(f"{value} = {sett}",1,color1),self.settText[i])
            pg.draw.circle(win,color,self.settBB[i],7)
            if i >= len(self.sett)-1: # at the end draw a restore defaults button #
                pg.draw.circle(win,green,self.settBB[i+1],7)  
        win.blit(FONT.render("Restore defaults?",1,black),(25,len(self.sett)*50+50))
    
    def display_gameMenu(self,win):
        clr(win)
        for i,name in enumerate(level_names): # display the names and buttons of available levels #
            pg.draw.circle(win,grey,(10,i*50+20),7)
            win.blit(FONT.render(name,1,black),(20,i*50))

    def display_pause(self,win): # !dont clear the screen! #
        #pg.draw.rect(win,blue,(25,50,350,800))
        pauseSurface = pg.Surface((350,800), pg.SRCALPHA)
        pauseSurface.fill((153,255,51,1))
        names = ["Resume","Menu","Exit"]
        for i,name in enumerate(names):
            x,y = self.coords[i]
            pg.draw.rect(win,blue,(x,y,200,80))
            color = red if i == 2 else black
            s = FONT.render(name,1,color)
            win.blit(s,(115,y))
        win.blit(pauseSurface,(25,50))

class Grid:
    def __init__(self,vel,gainVel): 
        self.next = True
        self.sett_update(vel,gainVel)
        self.reset_board() # each cube is 100 width and 150 height #                                        

    def draw(self,win):
        clr(win)
        # draw lines V #
        for i in range(len(self.board)): # loop thru all rows #
            for j in range(len(self.board[i])): # loop thru all cube in row #
                color = None
                if self.board[i][j] == 1: # if cube is a piano tile, draw a black rectangle #
                    color = black
                elif self.board[i][j] == 0.5: # if cube is a clicked piano tile, draw a grey rectangle #
                    color = grey
                if color:
                    pg.draw.rect(win,color,(j*100,i*150+self.offset-150,100,150))
                if i == len(self.board)-1:
                    pg.draw.line(win, grey1, (j*100,0),(j*100,W_HEIGTH),1) # draw 4 horizontal lines #
                    #pg.draw.circle(win,black,(j*100,0),10)
                pg.draw.line(win, grey1, (0,i*150+self.offset-150),(W_WIDTH,i*150+self.offset-150),1) # draw 6 vertival lines #
        scoreS = FONT.render(f"{self.score}",1,blue)
        win.blit(scoreS,(W_WIDTH//2-scoreS.get_width()//2,25))
    
    def move(self):
        self.offset += self.vel # move all the cubes and vertical lines of value of the vel #
        if self.offset >= 150:
            self.next = True
            self.offset -= 150  # if offset is grater that 150 (some lines are outside the screen), #
                                # so it looks like its moving endlessly #
    
    def check(self,x,y): # check if the player clicked any tile, and if so set its color to grey and increase the value of score #
        for i, row in enumerate(self.board):
            for j, cube in enumerate(row):
                if cube == 1 and i == (y-self.offset+150)//150 and j == x //100:
                    self.board[i][j] = 0.5
                    self.score += 1
                    return True
        return False
        
    def sett_update(self,vel,gainVel): # update the settings #
        self.vel = vel
        self.gainVel = gainVel
        fill = ""
        if vel <= 0:
            fill = "speed"
            f1 = ""
        elif gainVel < 0:
            fill = "gainSpeed"
            f1 = "="
        if fill: # if values are not valid, raise an error #
            raise ValueError(f"Value of '{fill}' too small (it has to be >{f1} 0)")

    def countdown(self,win,secs: int,visible = True): # countdown to resume the game #
        s = secs
        for _ in range(secs):
            if visible:
                self.draw(win)
                win.blit(FONT.render(str(s),1,red),(180,0))
                pg.display.flip()
            s -= 1
            for _ in range(100):
                time.sleep(0.01)
                for _ in pg.event.get(): # loop thru all events so, program doesnt freeze #
                    pass
    def reset_board(self):
        self.i = 0
        self.score = 0
        self.offset = 0
        self.board = [ 
            [0 for _ in range(4)] for _ in range(7) # 6 + 1 extra rows, each contains 4 cubes #
        ]

            
def _any(alist):
    for v in alist:
        if v == 1:
            return True
    return False

def reset_game(MenuObj,GridObj): # reset the level, speed etc #
    GridObj.reset_board()
    GridObj.sett_update(*[v for i,v in enumerate(MenuObj.sett.values()) if i < len(MenuObj.sett)-1 ])

# main code ---------------------------------- #
def run():
    screen = 0 # variable that tells in which screen player is #   
    menu = Menu()
    grid = Grid(*[v for i,v in enumerate(menu.sett.values()) if i < len(menu.sett)-1 ])
    string = '' # string to change the setting
    clock = pg.time.Clock()
    tick = 0
    level = None
    lost = False
    won = False
    
    while True:
        if won or lost:
            if won:
                win.blit(FONT.render("You did it!",1,blue),(135,800))
                won = False
            elif lost:
                win.blit(FONT.render("You lost.",1,blue),(140,800))
                lost = False
            pg.display.flip()
            grid.countdown(win,3,visible=False)
            reset_game(menu,grid)
            level = None
            screen = 0  
        clock.tick(60)
        # displays mainMenu---------------------#
        # screens -> 0 - mainMenu, 0.5 - settings, 0.75 - gameMenu, 1 - game, 1.25 - pause menu #
        if screen == 0: # display mainMenu #
            menu.display(win)
        elif screen == 0.5: # display mainMenu -> settings #
            menu.display_settigs(win)
        elif screen == 0.75:
            menu.display_gameMenu(win)
        elif screen == 1: 
            grid.move()
            tick += 1
            if tick >= 60:
                grid.vel *= 1+grid.gainVel/100
                tick = 0
            if grid.next:
                deleted = grid.board.pop() # delete the last row, which is outside the screen #
                if _any(deleted): # if in deleted row was any unclicked tile, stop the game # 
                    lost = True
                try:
                    grid.board.insert(0,level[grid.i]) # add a new row to the beggining #
                except:
                    won = True
                grid.i += 1
                grid.next = False
                
            grid.draw(win)
        elif screen == 1.25:
            menu.display_pause(win)
        #checks events ----------------------------#
        for event in pg.event.get():
            if event.type == pg.QUIT:
                pg.quit()
                break
            # mouse -------------------------------------------------------#
            if event.type == pg.MOUSEBUTTONDOWN: # if player clicked a left button of mouse, check if he clicked any button V #
                if event.button == 1:
                    pos = event.pos
                    if screen == 0: # if player is in mainMenu #
                        clicked = menu.check(*pos,screen)   # * #
                        if clicked != None:
                            if clicked == 0: # go to -> gameMenu #
                                screen = 0.75
                            elif clicked == 1: # go to -> settings #
                                screen = 0.5
                            elif clicked == 2: # quit the program #
                                pg.quit()
                                break
                    elif screen == 0.5:
                        clicked = menu.check(*pos,screen)
                    elif screen == 0.75:
                        clicked = menu.check(*pos,screen)   # * #
                        if clicked != None:
                            level = open_levels(level_names[clicked])
                            SC = 0
                            for row in level: # calculate the number of the titles in the level #
                                for v in row:
                                    if v:
                                        SC += 1
                            level = [*level[:],*[[0,0,0,0] for i in range(14)]] # add a few empty rows to the level so it doest crash duo to IndexError #
                            screen = 1
                    elif screen == 1: # gameMenu #
                        clicked = grid.check(*pos)
                        if clicked:
                            grid.draw(win)
                        if grid.score >= SC:
                            won = True   
                    elif screen == 1.25: # pauseMenu #
                        clicked = menu.check(*pos,screen)
                        if clicked == 0:
                            screen = 1
                            grid.countdown(win,5) # execute the countdown #
                            pg.event.clear() # clear the events in queue, so player cant click tiles while being in pause menu #
                            break
                        elif clicked == 1: # go to the mainMenu #
                            reset_game(menu,grid)
                            screen = 0
                        elif clicked == 2: # exit the program #
                            pg.quit()
                            break
            # keyboard ---------------------------------------------- #
            if event.type == pg.KEYDOWN:
                # screens -> 0 - mainMenu, 0.5 - settings, 0.75 - gameMenu, 1 - game, 1.25 - pause menu #
                if event.key == pg.K_ESCAPE:
                    if screen == 0.5: # if screen is settings go to -> mainMenu #
                        screen = 0
                    elif screen == 1: # if screen is game go to -> pause menu #
                        screen = 1.25
                    elif screen == 1.25: # execute the countdown #
                        grid.countdown(win,5)
                        screen = 1
                        pg.event.clear() # clear the events in queue, so player cant click tiles while being in pause menu #
                        break
                    elif screen == 0.75: # if screen is gameMenu go to -> mainMenu #
                        screen = 0
                    else:
                        screen -= 0.25 # go to prevorious screen #
                # numbers in mainMenu -> settings #
                if screen == 0.5 and menu.settSelected != None:
                    # get the user input V #
                    if event.key == pg.K_PERIOD or event.key == pg.K_KP_PERIOD:
                        string += "."
                    elif event.key == pg.K_BACKSPACE:
                        try:
                            string = string[:-1]
                        except:
                            pass
                    if event.key == pg.K_0 or event.key == pg.K_KP0:
                        string += "0"
                    elif event.key == pg.K_1 or event.key == pg.K_KP1:
                        string += "1"
                    elif event.key == pg.K_2 or event.key == pg.K_KP2:
                        string += "2"
                    elif event.key == pg.K_3 or event.key == pg.K_KP3:
                        string += '3'
                    elif event.key == pg.K_4 or event.key == pg.K_KP4:
                        string += "4"
                    elif event.key == pg.K_5 or event.key == pg.K_KP5:
                        string += "5"
                    elif event.key == pg.K_6 or event.key == pg.K_KP6:
                        string += "6"
                    elif event.key == pg.K_7 or event.key == pg.K_KP7:
                        string += "7"
                    elif event.key == pg.K_8 or event.key == pg.K_KP8:
                        string += "8"
                    elif event.key == pg.K_9 or event.key == pg.K_KP9:
                        string += "9"
                    elif event.key == pg.K_ESCAPE:
                        menu.settSelected = None
                        string = ""
                    # change the value of selected sett and reset input and selected setting #
                    elif event.key == pg.K_RETURN or event.key == pg.K_KP_ENTER:
                        if string:
                            try:
                                menu.sett[menu.settId[menu.settSelected]] = float(string)
                                grid.sett_update(*[v for i,v in enumerate(menu.sett.values()) if i < len(menu.sett)-1 ])
                            except:
                                pass
                            menu.settSelected = None
                            string = ""    

        if screen < 0:
            pg.quit()
            break
        try:        
            pg.display.flip()
        except:
            break 

if __name__ == "__main__":
    run()
