from random import randint
import pygame
pygame.init()

import ctypes
user32 = ctypes.windll.user32
screensize = (user32.GetSystemMetrics(1), user32.GetSystemMetrics(0))

BLACK = (0,0,0)
WHITE = (255,255,255)
GREEN = (0,255,0)
BLUE = (0,0,255)
RED = (255,0,0)
COLORS = [BLACK,WHITE,GREEN,BLUE,RED]

x = 0 #for pos index
y = 1

class Main:
    def __init__(self):
        self.SIZE = [800,600] #screen size
        self.screen = pygame.display.set_mode((self.SIZE[0], self.SIZE[1])) #screen
        pygame.display.set_caption('Dot Simulation') #windows name
        self.screenFPS = 1 #RenderedFramePerSecond
        self.screen.fill(WHITE) #screen background
        
        self.addedDotPF = 2 #added dot per frame
        self.deletedDotPF = 1
        self.startingDot = 1
        self.screenBorderLimit = 20 #set the avaliable zone for dot how far from the window border
        
        self.showRange = True  #for debuging purpose
        self.showLines = True

        self.dots = [] #list that store dots
        self.links = []

        for i in range(20):
            self.createDot()


    def run(self): #mainloop
        clock = pygame.time.Clock()
        loop = True
        while loop:
            clock.tick(self.screenFPS)
            for event in pygame.event.get():
                if event.type == pygame.QUIT: #pygame quit windows stuff
                    pygame.quit() 
                    quit()
            #####LOGIC######
            self.linkCreator()
            #self.createDot(50, 2)
            #self.deletedot()
            #####RENDER#####
            self.screen.fill((255,255,255)) #this is important because every frame need fresh background
            self.renderLine()
            self.renderDots()
            self.displayText()
            
            pygame.display.flip()

    def displayText(self):
        font = pygame.font.Font(None, 36)
        text = font.render(str(len(self.dots)), 1, (10, 10, 10))
        textpos = text.get_rect()
        textpos.centerx = self.screen.get_rect().centerx
        self.screen.blit(text, textpos)
    
    def linkCreator(self):
        fakeDots = self.dots.copy()
        dot1 = fakeDots.pop(randint(0, len(fakeDots)-1))
        dot2 = fakeDots.pop(randint(0, len(fakeDots)-1))
        self.createLine(dot1.pos, dot2.pos)

    def createDot(self, minRange = 50, linkLimit = 2):
        pos = randint(self.screenBorderLimit, self.SIZE[x]-self.screenBorderLimit), randint(self.screenBorderLimit, self.SIZE[y]-self.screenBorderLimit)
        tempDot = Dot(pos, minRange, linkLimit, self.showRange)
        if self.canDotable(tempDot.pos, tempDot.minRange):
            self.dots.append(tempDot)
    def createLine(self, pos1, pos2):
        if self.canCreateLine:
            self.links.append(Link(pos1, pos2))
    def deleteDot(self): #can be changed to delete both lines and dots
        if len(self.dots) == 0: #failsafe in case there is not any dot to delete
            return False
        del self.dots[0]

    def renderDots(self):
        for dot in self.dots:
            dot.render(self.screen)          
    def renderLine(self):
        for line in self.links:
            pygame.draw.aaline(self.screen, BLUE, line.pos1, line.pos2)

    def canDotable(self, pos, minRange):
        if len(self.dots) == 0:
            return True
        for dot in self.dots:
            distance = (((pos[x] - dot.pos[x])**2) + ((pos[y] - dot.pos[y])**2)) ** 0.5
            if distance < dot.minRange + minRange:
                return False
        return True    
    def canCreateLine(self, line1, line2):
        D  = line1.A * line2.B - line1.B * line2.A
        #Dx = line1.C * line2.B - line1.B * line2.C for detecting the cord in future
        #Dy = line1.A * line2.C - line1.C * line2.A
        if D != 0:
            #x = Dx / D
            #y = Dy / D
            return True #x,y
        return False


class Dot:
    def __init__(self, pos, minRange, linkLimit, showRange):
        self.pos = pos
        self.minRange = minRange
        self.maxRange = None
        self.linkLimit = linkLimit
        self.linkedDots = []
        self.showRange = True

    def render(self, screen):
        pygame.draw.circle(screen, BLACK, (self.pos[x], self.pos[y]), 2, 1)
        if self.showRange:
            pygame.draw.circle(screen, RED, (self.pos[x], self.pos[y]), self.minRange, 1)

class Link:
    def __init__(self, pos1, pos2):
        self.pos1 = pos1
        self.pos2 = pos2
        self.color = None
        self.distance = None
        self.width = None
        self.A = pos2[y] - pos1[y]
        self.B = pos2[x] - pos1[x]
        #self.C = -((pos1[x] * pos2[y]) - (pos2[x] * pos1[y])) in the future

main = Main()
main.run()

def intersection(line1, line2):
    D  = line1[0] * line2[1] - line1[1] * line2[0]
    Dx = line1[2] * line2[1] - line1[1] * line2[2]
    Dy = line1[0] * line2[2] - line1[2] * line2[0]
    if D != 0:
        x = Dx / D
        y = Dy / D
        return x,y
    else:
        return False

line1 = line([0,4], [2,2])
line2 = line([2,3], [0,4])

