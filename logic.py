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
        #screenStuff
        self.SIZE = [800,600] #screen size
        self.screen = pygame.display.set_mode((self.SIZE[0], self.SIZE[1])) #screen
        pygame.display.set_caption('Dot Simulation') #windows name 
        self.screen.fill(WHITE) #screen background
        self.screenFPS = 60 #RenderedFramePerSecond       
        self.fpsCount = 0
        #dotCreation
        self.addedDotPF = 0 #added dot per frame
        self.deletedDotPF = 0
        self.startingDot = 3
        self.screenBorderLimit = 20 #set the avaliable zone for dot how far from the window border
        self.cratedLinePF = 0
        #dotSetings
        self.showRange = True  #for debuging purpose
        self.showLines = True
        #memory
        self.dots = [] #list that store dots
        self.links = []
        #mouseStuff
        self.selectedDots = []
        for i in range(self.startingDot):
            self.createDot(randint(30,80), 2)

    def run(self): #mainloop
        clock = pygame.time.Clock()
        loop = True
        while loop:
            self.fpsCount += 1
            if self.fpsCount > self.screenFPS:
                self.fpsCount = 0
            clock.tick(self.screenFPS)
            #print(clock.tick(self.screenFPS)) #testing can the system keep up
            for event in pygame.event.get():
                if event.type == pygame.QUIT: #pygame quit windows stuff
                    pygame.quit() 
                    quit()
                if event.type == pygame.MOUSEBUTTONUP:
                    self.mousePos = pygame.mouse.get_pos()
                    self.mouseSelection()
                if event.type == pygame.KEYDOWN:
                    if event.key ==pygame.K_p: #Make Line by Hand
                        self.createLinkByChoosen()
                    if event.key == pygame.K_LEFT:
                        for dot in self.selectedDots:
                            dot.pos[x] -= 10
                    if event.key == pygame.K_RIGHT:
                        for dot in self.selectedDots:
                            dot.pos[x] += 10
                    if event.key == pygame.K_UP:
                        for dot in self.selectedDots:
                            dot.pos[y] -= 10
                    if event.key == pygame.K_DOWN:
                        for dot in self.selectedDots:
                            dot.pos[y] += 10                    
            ######DOT_CREATION######
            if self.fpsCount == 0:
                for i in range(self.deletedDotPF):
                    self.deleteDot()
                for i in range(self.addedDotPF):
                    self.createDot(randint(30,80), 2)
                for i in range(self.cratedLinePF):
                    self.linkCreate()

            #########RENDER#########
            self.screen.fill((WHITE)) #this is important because every frame need fresh background
            self.renderLine()
            self.renderDots()
            self.displayText()
                                
            pygame.display.flip()

    def mouseSelection(self):
        for dot in self.dots:
            if dot.posInRange(self.mousePos):
                if dot.selected:
                    dot.rangeColor = RED
                    dot.selected = False
                    self.selectedDots.remove(dot)
                else:
                    dot.rangeColor = GREEN
                    dot.selected = True
                    self.selectedDots.append(dot)

    def displayText(self): #make oop friendly
        font = pygame.font.Font(None, 36)
        text = font.render(str(len(self.dots)), 1, (10, 11, 10))
        textpos = text.get_rect()
        textpos.centerx = self.screen.get_rect().centerx
        self.screen.blit(text, textpos)
    
    def displayPos(self, pos):
        font = pygame.font.Font(None, 36)
        text = font.render(str(round(pos[0],round(pos[1]))), 1, (10, 10, 10))
        self.screen.blit(text, pos)

    def createLinkByChoosen(self):
        if len(self.selectedDots) < 1:
            return False
        tempList = self.selectedDots.copy()
        for dot1 in tempList:
            tempList.remove(dot1)   
            for dot2 in tempList:
                tempLink = Link(dot1, dot2)
                dot1.links.append(tempLink)
                dot2.links.append(tempLink)
                self.links.append(tempLink)
        return True

    def createDot(self, minRange = 50, linkLimit = 2):
        pos = randint(self.screenBorderLimit, self.SIZE[x]-self.screenBorderLimit), randint(self.screenBorderLimit, self.SIZE[y]-self.screenBorderLimit)
        tempDot = Dot(pos, minRange, linkLimit, self.showRange)
        if tempDot.canForm(self.dots):
            self.dots.append(tempDot)
    
    def createLinkByAI(self, dot1, dot2):
        tempLink = Link(dot1, dot2)
        for link in self.links:
            if not self.linkIntersection(tempLink, link):
                return False
        dot1.links.append(tempLink)
        dot2.links.append(tempLink)
        self.links.append(tempLink)

    def deleteDot(self): #can be changed to delete both lines and dots
        if len(self.dots) == 0: #failsafe in case there is not any dot to delete
            return False 
        self.dots[0].delete()
        del self.dots[0]

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

    def linkIntersection(self, link1, link2):
        D  = link1.A * link2.B - link1.B * link2.A
        Dx = link1.C * link2.B - link1.B * link2.C
        Dy = link1.A * link2.C - link1.C * link2.A
        if D != 0:
            x = Dx / D
            y = Dy / D
            return True
        else:
            return False

class Dot:
    def __init__(self, pos, minRange, linkLimit, showRange = True):
        self.pos = list(pos)
        self.minRange = minRange
        self.linkLimit = linkLimit
        self.showRange = showRange
        self.links = []
        self.rangeColor = RED
        self.oldPos = self.pos
        self.selected = False

    def render(self, screen):
        pygame.draw.circle(screen, BLACK, (self.pos[x], self.pos[y]), 2, 1)
        if self.showRange:
            pygame.draw.circle(screen, self.rangeColor, (self.pos[x], self.pos[y]), self.minRange, 1)

    def delete(self):
        for link in self.links:
            link.live = False
    
    def posInRange(self, pos):
        distanceToPos = (((self.pos[x] - pos[x])**2) + ((self.pos[y] - pos[y])**2))**0.5
        if distanceToPos < self.minRange:
            return True
        return False

    def canForm(self, otherDots):
        if len(otherDots) == 0:
            return True
        for dot in otherDots:
            distance = (((self.pos[x] - dot.pos[x])**2) + ((self.pos[y] - dot.pos[y])**2)) ** 0.5
            if distance < dot.minRange + self.minRange:
                return False
        return True

    def canMove(self):
        pass

class Link:
    def __init__(self, dot1, dot2, color = BLUE):
        self.live = True #Link do not live if on or two of dots disappear and delete itself
        self.dot1 = dot1
        self.dot2 = dot2
        self.connectedDots = []
        self.connectedDots.append(dot1)
        self.connectedDots.append(dot2)
        self.A = self.dot1.pos[y] - self.dot2.pos[y]
        self.B = self.dot2.pos[x] - self.dot1.pos[x]
        self.C = -((self.dot1.pos[x] * self.dot2.pos[y]) - (self.dot2.pos[x] * self.dot1.pos[y]))
        self.color = color
        self.width = None
        self.check()

    def check(self): #not useful for now      
        self.distance = (((self.dot1.pos[x] - self.dot2.pos[x])**2) + ((self.dot1.pos[y] - self.dot2.pos[y])**2))**0.5
        if self.distance > 943:
            self.color = RED
        else:
            self.color = (self.distance / 3.7, 255 - self.distance/3.7 , 0)       
        if len(self.connectedDots) <= 1: #if line has no connected dots line die
            self.live = False    
    
    def render(self, screen):
        self.check()
        if self.live:
            pygame.draw.aaline(screen, self.color, self.dot1.pos, self.dot2.pos)

main = Main()
main.run()


def ccw(A,B,C):
	return (C.pos[y]-A.pos[y])*(B.pos[x]-A.pos[x]) > (B.pos[y]-A.pos[y])*(C.pos[x]-A.pos[x])

def intersect(A,B,C,D):
	return ccw(A,C,D) != ccw(B,C,D) and ccw(A,B,C) != ccw(A,B,D)
