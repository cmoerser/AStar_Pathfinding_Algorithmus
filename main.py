import pygame
import time
import threading
import math

pygame.init()


WIDTH, HEIGHT = 600, 300

BLACK = (0,0,0)
GREEN = (0, 50, 0)
GRAY = (100, 100, 100)
WHITE = (255, 255, 255)
RED = (255,0,0)
YELLOW = (255,255,0)
BLUE = (0,0,100)
LIGHTBLUE = (100,150,255)


allNodes = []
endList = []

unknownList = []
openList = []
closedList = []

startNode = None
endNode = None
finish = False


class Node:
    def __init__(self,pos,id):
        self.id = id

        self.pos = pos
        self.size = (10,10)
        self.rect = pygame.Rect(pos,self.size)
        
        self.isWall = False

        self.neighbors = []
        self.preNode = None
        self.distanceToGoal = -1
        self.f = -1
       

def prepareAllNodes():
    id = 0
    for w in range(0,600,10):
        for h in range(0,300,10):
            n = Node((w,h),id)
            allNodes.append(n)
            id +=1 
    
def initializeNodes():    
    global startNode
    global endNode
    #startNode = allNodes[0]
    #endNode = allNodes[1799] 
    
    for n in allNodes:
        n.distanceToGoal = math.sqrt(math.pow(n.pos[0]-endNode.pos[0],2)+math.pow(n.pos[1]-endNode.pos[1],2)) 
        
        nNW = (n.pos[0]-10,n.pos[1]-10)
        nSO = (n.pos[0]+10,n.pos[1]+10)
        nSW = (n.pos[0]-10,n.pos[1]+10)
        nNO = (n.pos[0]+10,n.pos[1]-10)
        
        
        nN = (n.pos[0],n.pos[1]-10)
        nS = (n.pos[0],n.pos[1]+10)
        nW = (n.pos[0]-10,n.pos[1])
        nO = (n.pos[0]+10,n.pos[1])
        tmpN = [x for x in allNodes if not x.isWall and ((nN == x.pos) or (nS == x.pos) or (nW == x.pos) or (nO == x.pos) or (nNW == x.pos) or (nNO == x.pos) or (nSW == x.pos) or (nSO == x.pos))] 
        
        for nE in tmpN:
            n.neighbors.append([nE,10])

        if not n.isWall and n != startNode: unknownList.append(n)
    
    startNode.f = startNode.distanceToGoal
    openList.append(startNode)

      
def aStar(WIN):
    global finish
    while len(openList) > 0:
        lowF = openList[0]
        for n in openList:      # Suche Node mit niedrigstem f
            if n.f < lowF.f:
                lowF = n
        
        if lowF == endNode: 
            #pygame.draw.rect(WIN,RED,lowF.rect,0)
            break
        
        for nE in lowF.neighbors:       # Gehe alle Nachbarn durch, berechne f und füge openList hinzu
            if nE[0] in closedList: continue

            if nE[0] not in openList:
                openList.append(nE[0])
                unknownList.remove(nE[0])
                #pygame.draw.rect(WIN,YELLOW,nE[0].rect,0)
                
    
            newF = (lowF.f - lowF.distanceToGoal) + nE[1] + nE[0].distanceToGoal
            if nE[0].f == -1 or newF < nE[0].f:
                nE[0].f = newF
                nE[0].preNode = lowF

        openList.remove(lowF)
        closedList.append(lowF)   
        #pygame.draw.rect(WIN,RED,lowF.rect,0)
        time.sleep(0.05)

    
    tmpNode = endNode
    while tmpNode != None:
        endList.append(tmpNode)
        tmpNode = tmpNode.preNode
    finish = True
    

def selectNode(pos):
    #ret = [x for x in allNodes if x.pos == pos]
    for n in allNodes:
        if n.pos[0] <= pos[0] and pos[0] < n.pos[0]+n.size[0]:
            if n.pos[1] <= pos[1] and pos[1] < n.pos[1]+n.size[1]:
                return n       
    return None


def drawAll(WIN):
    while True:
        pass


def main():
    global startNode
    global endNode
    global wallList
    global finish
    
    WIN = pygame.display.set_mode((WIDTH, HEIGHT))
    pygame.display.set_caption("Pathfinder")
    WIN.fill(WHITE)
    
    prepareAllNodes()
    

    for n in allNodes:
        pygame.draw.rect(WIN,BLACK,n.rect,1)
    pygame.display.flip()

    #pygame.draw.rect(WIN,LIGHTBLUE,startNode.rect,0)
    #pygame.draw.rect(WIN,BLUE,endNode.rect,0)
    

    run = True
    draw = False
    erase = False

    isSolving = False

    clock = pygame.time.Clock()

    while run:
        clock.tick(60)
        
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                run = False

            if event.type == pygame.MOUSEBUTTONDOWN and not isSolving:
                if startNode == None: 
                    selectedNode = selectNode(event.pos)
                    if selectedNode != None: 
                        startNode = selectedNode
                elif endNode == None:
                    selectedNode = selectNode(event.pos)
                    if selectedNode != None: 
                        endNode = selectedNode 
                else:
                    if event.button == 1 and not erase:
                        draw = True 
                    elif event.button == 3 and not draw:
                        erase = True
                    
            if event.type == pygame.MOUSEBUTTONUP and not isSolving:
                if event.button == 1:
                    draw = False 
                elif event.button == 3:
                    erase = False

            if event.type == pygame.KEYDOWN and not isSolving:
                if event.key == pygame.K_SPACE:
                    if startNode != None and endNode != None:
                        isSolving = True                
                        initializeNodes()
                        threading._start_new_thread(aStar,(WIN,))
        

        if draw:
            selectedNode = selectNode(pygame.mouse.get_pos())
            if selectedNode != None: 
                if selectedNode!=startNode and selectedNode!=endNode: 
                    selectedNode.isWall = True                 
        elif erase:
            selectedNode = selectNode(pygame.mouse.get_pos())
            if selectedNode != None: 
                if selectedNode!=startNode and selectedNode!=endNode: 
                    selectedNode.isWall = False           

        # PAINTING

        WIN.fill(WHITE)

        for o in openList:
            pygame.draw.rect(WIN,YELLOW,o.rect,0)

        for c in closedList:
            pygame.draw.rect(WIN,RED,c.rect,0)

        for e in endList:
            pygame.draw.rect(WIN,GREEN,e.rect,0)
              

        if startNode != None: pygame.draw.rect(WIN,LIGHTBLUE,startNode.rect,0)        
        if endNode != None: pygame.draw.rect(WIN,BLUE,endNode.rect,0)

        for n in allNodes:
            if n.isWall:
                pygame.draw.rect(WIN,BLACK,n.rect,0)
            else:
                pygame.draw.rect(WIN,GRAY,n.rect,1)


        pygame.display.flip()

    
    pygame.quit()



if __name__ == "__main__":
    main()
