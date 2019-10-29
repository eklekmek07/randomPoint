from random import randint
import pygame
pygame.init()

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

        for i in range(self.startingDot):
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
            self.createDot(randint(30,80), 2)
            #self.deleteDot()
            #####RENDER#####
            self.screen.fill((255,255,255)) #this is important because every frame need fresh background
            self.renderLine()
            self.renderDots()
            self.displayText()
            
            pygame.display.flip()

    def displayText(self): #make oop friendly
        font = pygame.font.Font(None, 36)
        text = font.render(str(len(self.dots)), 1, (10, 10, 10))
        textpos = text.get_rect()
        textpos.centerx = self.screen.get_rect().centerx
        self.screen.blit(text, textpos)
    
    def linkCreator(self):
        if len(self.dots) > 1:
            fakeDots = self.dots.copy()
            dot1 = fakeDots.pop(randint(0, len(fakeDots)-1))
            dot2 = fakeDots.pop(randint(0, len(fakeDots)-1))
            self.createLink(dot1, dot2)

    def createDot(self, minRange = 50, linkLimit = 2):
        pos = randint(self.screenBorderLimit, self.SIZE[x]-self.screenBorderLimit), randint(self.screenBorderLimit, self.SIZE[y]-self.screenBorderLimit)
        tempDot = Dot(pos, minRange, linkLimit, self.showRange)
        if self.canDotable(tempDot.pos, tempDot.minRange):
            self.dots.append(tempDot)
    def createLink(self, dot1, dot2):
        mainLink = Link(dot1, dot2)
        for link in self.links:
            if not self.canCreateLink(mainLink, link):
                return False
        tempLink = Link(dot1, dot2)
        dot1.links.append(tempLink)
        self.links.append(tempLink)
    
    def deleteDot(self): #can be changed to delete both lines and dots
        if len(self.dots) == 0: #failsafe in case there is not any dot to delete
            return False 
        self.dots[0].delete()
    def checkLinks(self):
        for link in self.links:
            link.check()

    def renderDots(self):
        for dot in self.dots:
            dot.render(self.screen)          
    def renderLine(self):
        for line in self.links:
            line.render(self.screen)

    def canDotable(self, pos, minRange):
        if len(self.dots) == 0:
            return True
        for dot in self.dots:
            distance = (((pos[x] - dot.pos[x])**2) + ((pos[y] - dot.pos[y])**2)) ** 0.5
            if distance < dot.minRange + minRange:
                return False
        return True    
    def canCreateLink(self, link1, link2):
        D  = link1.A * link2.B - link1.B * link2.A
        if D != 0:
            print("döner")
            return True
        return False


class Dot:
    def __init__(self, pos, minRange, linkLimit, showRange = True):
        self.pos = pos
        self.minRange = minRange
        self.maxRange = None
        self.linkLimit = linkLimit
        self.showRange = showRange
        self.links = []

    def render(self, screen):
        pygame.draw.circle(screen, BLACK, (self.pos[x], self.pos[y]), 2, 1)
        if self.showRange:
            pygame.draw.circle(screen, RED, (self.pos[x], self.pos[y]), self.minRange, 1)

    def delete(self):
        for link in self.links:
            link.live = False

class Link:
    def __init__(self, dot1, dot2, color = BLUE):
        self.live = True #Link do not live if on or two of dots disappear and delete itself
        
        self.pos1 = dot1.pos
        self.pos2 = dot2.pos
        self.connectedDots = []
        self.connectedDots.append(dot1)
        self.connectedDots.append(dot2)
        
        self.color = color
        self.width = None
        
        self.A = self.pos2[y] - self.pos1[y]
        self.B = self.pos2[x] - self.pos1[x]
        #self.C = -((pos1[x] * pos2[y]) - (pos2[x] * pos1[y])) in the future for kesişim..
        self.distance = None

    def check(self): #not useful for now
        self.pos1 = dot1.pos
        self.pos2 = dot2.pos        
        self.distance = None #diy calculate the distance between connected dots
        if self.connectedDots >= 1:
            self.live = False    

    def render(self, screen):
        if self.live:
            pygame.draw.aaline(screen, self.color, self.pos1, self.pos2)

main = Main()
main.run()


