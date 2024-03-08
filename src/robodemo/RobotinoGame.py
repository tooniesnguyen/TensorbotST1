import pygame
import RobotController
import pid
import numpy as np
import time
import math
# from pygame.sprite import _Group
import Button
# import pyttsx3

pygame.init()
clock = pygame.time.Clock()
FPS = 60

SCREEN_WIDTH = 600
SCREEN_HEIGHT = int(SCREEN_WIDTH * 0.8)

screen = pygame.display.set_mode((SCREEN_WIDTH,SCREEN_HEIGHT))
pygame.display.set_caption("Introduction of Mechatronic")

x = 200
y = 200
scale = 3
start_img = pygame.image.load('img/start_btn.png').convert_alpha()
exit_img = pygame.image.load('img/exit_btn.png').convert_alpha()

Room1_button = Button.Button(100,100,start_img,0.5)
Room2_button = Button.Button(SCREEN_WIDTH // 2 - 55,100,start_img,0.5)
Room3_button = Button.Button(400,100,start_img,0.5)

Room4_button = Button.Button(100,300,start_img,0.5)
Room5_button = Button.Button(SCREEN_WIDTH // 2 - 55,300,start_img,0.5)
Room6_button = Button.Button(400,300,start_img,0.5)

exitRoom_button = Button.Button(SCREEN_WIDTH // 2 - 55,200,exit_img,0.5)

start_button = Button.Button(SCREEN_WIDTH // 2 -130,SCREEN_HEIGHT //2 -150,start_img,1)
exit_button = Button.Button(SCREEN_WIDTH // 2 -110,SCREEN_HEIGHT //2 + 50,exit_img,1)

text_font = pygame.font.SysFont("turok.ttf",30,bold = True ,italic=True)
font2 = pygame.font.SysFont("turok.ttf",50,bold = True ,italic=True)

FollowGiaoVien = pygame.mixer.Sound('sound/GiaoVienFollow.wav')
FollowE1303 = pygame.mixer.Sound('sound/E1303Follow.wav')
FollowE1304 = pygame.mixer.Sound('sound/E1308Follow.wav')
FollowE1308 = pygame.mixer.Sound('sound/E1308Follow.wav')

IntroGiaoVien = pygame.mixer.Sound('sound/GiaoVienIntro.wav')
IntroE1303 = pygame.mixer.Sound('sound/E1303intro.wav')
IntroE1304 = pygame.mixer.Sound('sound/e1304intro.wav')
IntroE1308 = pygame.mixer.Sound('sound/e1308intro.wav')

DoneWarning = pygame.mixer.Sound('sound/DoneWarning.wav')
def playSound(sound):
    sound.play()

    # Chờ cho đến khi tệp wav được phát xong
    while pygame.mixer.get_busy():
        pygame.time.wait(100)

def draw_text (text, font ,text_col, x, y):
    img = font.render(text, True,text_col)
    screen.blit(img,(x,y))

class ScreenFade():
    def __init__(self,direction,colour,speed):
        self.direction = direction
        self.colour = colour
        self.speed = speed
        self.fade_counter = 0
    def fade(self):
        fade_complete = False
        self.fade_counter += self.speed
        if self.direction == 1 :
            pygame.draw.rect(screen, self.colour,(0 ,0,SCREEN_WIDTH//2,0))
            
        if self.direction == 2 :
            pygame.draw.rect(screen,self.colour,(0,0,SCREEN_WIDTH,0+self.fade_counter))
        # print(self.fade_counter)
        if self.fade_counter >= SCREEN_WIDTH:
            fade_complete = True
        return fade_complete
#Sound Define 


#define colours
BG = (144,201,120)
BG2 = (255,69,0)
RED = (255,0,0)
WHITE = (255,255,255)
GREEN = (0,255,0)
BLACK = (0,0,0)
PINK = (235,65,54)

def draw_bg(color):
    screen.fill(color)


#Robot Define and Funtion :
ROBOTINOIP = "192.168.0.101"
PARAMS = {'sid':'example_circle'}
lookAheadDis = 0.15
RoomPrevious = 1
RoomNow = 0
RoomDesired = 1

HomeWaiting = 0
def pathReverse(chuoi):
  return list(reversed(chuoi))
pathBack = [[0,0],[0.5,0],[0.5,0.5]]
Room1ToRoom2 = [[0,0],[0.5,0],[0.5,0.5]] 
Room2ToRoom1 = pathReverse(Room1ToRoom2)

Room1ToRoom4 = [[0,0],[0.5,0],[0.5,-0.5]] 
Room4ToRoom1 = pathReverse(Room1ToRoom4)

Room1ToRoom5 = [[0,0],[0.5,0],[1.0,0]] 
Room5ToRoom1 = pathReverse(Room1ToRoom5)


# Room1ToRoom3 = 

Robotino = RobotController.robot(ROBOTINOIP,PARAMS,lookAheadDis)
pidX = pid.PID(0.8,0.6,-0.6)
pidY = pid.PID(0.8,0.6,-0.6)
pidTheta = pid.PID(0.03,0.3,-0.3)

#Page Define :

def Running_screen():   
    global run
    clock.tick(120)
    screen.fill((202,228,241))
    draw_text("Follow me !!!",font2,BLACK,300,200)
    Robot1.draw()
    Robot1.update_animation()
    if exit_button.draw(screen) : 
        Robotino.run = False
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            run = False
        pygame.display.update()

def Starting_Screen():
    global start_game
    global run
    draw_bg(BG)
    if start_button.draw(screen) :
        start_game = 2
    if exit_button.draw(screen) :
        run = False

def Fading_Screen():
    global start_game
    if Gamefade.fade() == True:
        start_game = 3
        Gamefade.fade_counter = 0
 
path = [[]]
def Waiting_Screen():
    global RoomNow,RoomPrevious,RoomDesired
    global start_game
    global RobotRun
    global HomeWaiting
    global path
    draw_bg(BG) 

    draw_text("E1-307",text_font,WHITE,100,80)
    if Room1_button.draw(screen) :
        playSound(IntroGiaoVien)
        HomeWaiting = 0
        if RoomPrevious == 2:
            path = Room2ToRoom1
            RoomDesired = 1
            RobotRun = True
        if RoomPrevious == 4:
            path = Room4ToRoom1
            RoomDesired = 1
            RobotRun = True
        if RoomPrevious == 5:
            path = Room5ToRoom1
            RoomDesired = 1
            RobotRun = True

    draw_text("E1-308",text_font,WHITE,SCREEN_WIDTH // 2 - 55,80)
    if Room2_button.draw(screen) :
        playSound(IntroE1308)
        HomeWaiting = 0
        if RoomPrevious == 1:
            RoomDesired = 2
            path = Room1ToRoom2
            RobotRun = True
    draw_text("E1-304",text_font,WHITE,400,80)
    if Room3_button.draw(screen) :
        HomeWaiting = 0
        pass
        # path = pathBack
        # RobotRun = True
    draw_text("E1-303",text_font,WHITE,100,280)
    if Room4_button.draw(screen) :

        HomeWaiting = 0
        if RoomPrevious == 1:
            RoomDesired = 4
            path = Room1ToRoom4
            RobotRun = True
    draw_text("E1-302",text_font,WHITE,SCREEN_WIDTH // 2 - 55,280)
    if Room5_button.draw(screen) :
        HomeWaiting = 0
        if RoomPrevious == 1:
            RoomDesired = 5
            path = Room1ToRoom5
            RobotRun = True
    draw_text("E1-301",text_font,WHITE,400,280)
    if Room6_button.draw(screen) :
        HomeWaiting = 0
        pass
        # path = pathBack
        # RobotRun = True
    
    if exitRoom_button.draw(screen) :
        HomeWaiting = 0
        start_game = 1
    if (RoomDesired != 1):
        
        RoomPreviousPath = pathReverse(path)
        print(RoomPreviousPath)
        HomeWaiting += 1  
        if HomeWaiting > 1000 :
            path = RoomPreviousPath
            RobotRun = True
            RoomDesired = 1
    if(RobotRun == True):
        if RoomDesired == 1:
            playSound(FollowGiaoVien)
        if RoomDesired == 2:
            playSound(FollowE1308)
        pathFollow(path)
        if RoomDesired != 1:
            playSound(DoneWarning)
        RoomPrevious = RoomDesired
        HomeWaiting = 0
        RobotRun = False



def pathFollow(path):
    Robotino.run = True
    vec = [0,0,0]
    goalPt = [0,0]
    SteadyCheck = 0
    lastFoundIndex = 0
    MoveFlag = 0
    while Robotino.run == True :
        Running_screen()

        OdoX = Robotino.OdometryRead()[0] 
        OdoY = Robotino.OdometryRead()[1] 
        OdoR = Robotino.OdometryRead()[2]
        currentPos = [OdoX,OdoY]
        goalPt,lastFoundIndex = Robotino.pure_pursuit_step(path, currentPos, lastFoundIndex)
        if lastFoundIndex == len(path)-1:
            goalPt = [path[lastFoundIndex][0], path[lastFoundIndex][1]]

        Angle = OdoR*180/(np.pi)

        u = pidX.PidCal(goalPt[0],OdoX)
        v = pidY.PidCal(goalPt[1],OdoY)
        r = pidTheta.PidCal(0,Angle)

        uControl = (math.cos(-OdoR)*u - math.sin(-OdoR)*v)
        vControl = (math.sin(-OdoR)*u + math.cos(-OdoR)*v)
        MoveFlag = Robotino.osticaleAvoid2(vControl,uControl)
        MoveFlag2 = Robotino.bumper()

        if (MoveFlag == 0 and MoveFlag2 == 0):              
            vec[0] = uControl
            vec[1] = vControl
            vec[2] = r
        else :
            vec[0] = 0
            vec[1] = 0
            vec[2] = 0

        if (abs(goalPt[0] - OdoX)<0.05 and abs(goalPt[1] - OdoY)<0.05):
            SteadyCheck += 1
        else :
            SteadyCheck = 0
        
        Robotino.set_vel(vec)

        if (lastFoundIndex == len(path)-1):
            if SteadyCheck > 10:
                print('Done')
                Robotino.run = False
                break


class Robot(pygame.sprite.Sprite):
    def __init__(self,char_type,x,y,scale,speed):
        pygame.sprite.Sprite.__init__(self)
        self.char_type = char_type
        self.speed = speed
        self.direction = 1
        self.flip = False
        self.animation_list = []
        self.frame_index = 0
        self.update_time = pygame.time.get_ticks()
        for i in range(6):
            img = pygame.image.load(f'img/{self.char_type}/Run/{i}.png')
            img = pygame.transform.scale(img,(int(img.get_width()*scale),(int(img.get_height()*scale))))
            self.animation_list.append(img)
        # self.image = pygame.transform.scale(img,(int(img.get_width()*scale),(int(img.get_height()*scale))))
        self.image = self.animation_list[self.frame_index]
        self.rect = self.image.get_rect()
        self.rect.center = (x,y)

    def move(self, moving_Left,moving_right):
        dx = 0
        dy = 0

        if moving_Left:
            dx = -self.speed
            self.flip = True
            self.direction = -1
        if moving_right:
            dx = self.speed
            self.flip = False
            self.direction = 1
        self.rect.x += dx
        self.rect.y += dy

    def update_animation(self):
        ANIMATION_COOLDOWN = 100

        self.image = self.animation_list[self.frame_index]
        if pygame.time.get_ticks() - self.update_time >  ANIMATION_COOLDOWN:
            self.update_time = pygame.time.get_ticks()
            self.frame_index += 1
        if self.frame_index >= len(self.animation_list):
            self.frame_index = 0

    def draw(self):
        screen.blit(pygame.transform.flip(self.image,self.flip,False),self.rect)

Robot1 = Robot('player',200,200,3,5)  
        
#Flag Define
RobotRun = False
run = True
start_game = 1
Gamefade = ScreenFade(2,BLACK,4)

while run :
    # print (dao_nguoc_chuoi(Room1ToRoom2))
    clock.tick(FPS)
    if start_game == 1 :
        Starting_Screen()
    elif start_game == 2 :
        Fading_Screen()
    elif start_game == 3 :  
        Waiting_Screen()
        

    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            run = False
    
    pygame.display.update()