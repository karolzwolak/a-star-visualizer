import pygame as pg
import time
W_WIDTH, W_HEIGHT = 1200,900

win = pg.display.set_mode((W_WIDTH,W_HEIGHT))

pg.display.set_caption("pathfinding visualization")

black = (0,0,0)
white = (255,255,255)
green = (0,255,0)
pathC =  (255,255,0)
cl = (0,255,255)
op = (30,144,255)
red = (255,0,0)

class Node:
    def __init__(self,pos=None,parentNode=None,startPos=None,targetPos=None):
        if startPos != None and targetPos != None:
            self.pos = startPos
            self.g_cost = 0
            self.h_cost = 0
            self.cost = 0
        elif pos != None and parentNode != None:
            self.parent = parentNode
            self.pos = pos
            self.g_cost = parentNode.g_cost + self.distance(self.parent.pos)
            self.h_cost = self.get_h_val()
            self.cost = self.g_cost+self.h_cost

    def get_h_val(self):
        a = abs(self.pos[0] - targetNode[0])
        b = abs(self.pos[1] - targetNode[1])
        return a+b

    def distance(self,fromPos):
        dis = ((self.pos[0]-fromPos[0])**2+(self.pos[1]-fromPos[1])**2)**0.5
        return dis

    def getNeighbors(self,board):
        n = (0,1,2,3,4,5)
        y,x = self.pos
        down = False
        up = False
        left_up = False
        left_down = False
        right_up = False
        right_down = False
        h_len = len(board[0]) # x, pos[1] #
        v_len = len(board) # y, pos[0] #
        neighbors = []
        if y < v_len-1:
            y1 = y+1
            x1 = x
            down = True
            if board[y1][x1] in n:
                neighbors.append(Node(pos=(y1,x1),parentNode=self))
                left_down = True
                right_down = True
                
        if y > 0:
            y1 = y-1
            x1 = x
            up = True
            if board[y1][x1] in n:
                neighbors.append(Node(pos=(y1,x1),parentNode=self))
                left_up = True
                right_up = True

        if x < h_len-1:
            y1 = y
            x1 = x+1
            if board[y1][x1] in n:
                neighbors.append(Node(pos=(y1,x1),parentNode=self))
                right_up = True
                right_down = True
            '''
            else:
                right_up = False
                right_down = False'''
            if right_up and up:
                y1 = y-1
                if board[y1][x1] in n:
                    neighbors.append(Node(pos=(y1,x1),parentNode=self))
            if right_down and down:
                y1 = y+1
                if board[y1][x1] in n:
                    neighbors.append(Node(pos=(y1,x1),parentNode=self))
        if x > 0:
            y1 = y
            x1 = x-1
            if board[y1][x1] in n:
                neighbors.append(Node(pos=(y1,x1),parentNode=self))
                left_up = True
                left_down = True
                
            if left_up and up:
                y1 = y-1
                if board[y1][x1] in n:
                    neighbors.append(Node(pos=(y1,x1),parentNode=self))
            if left_down and down:
                y1 = y+1
                if board[y1][x1] in n:
                    neighbors.append(Node(pos=(y1,x1),parentNode=self))
        return neighbors

class NodeList:
    def __init__(self):
        self.items = []
    
    def contains(self,obj):
        if len(self.items) > 0 :
            for i,node in enumerate(self.items):
                if obj.pos == node.pos:
                    return i
        return -1
    
    def getMin(self):
        if len(self.items) > 0:
            curr = 0
            for i in range(len(self.items)):
                node = self.items[i]
                if node.cost < self.items[curr].cost:
                    curr = i
            return curr
        return -1
    
    def _print(self):
        for node in self.items:
            print(node.pos,end=",")
        print()

class Grid:

    def __init__(self,length):
        self.length = length
        self.board = [ [ 0 for _ in range(W_WIDTH//length) ] for _ in range(W_HEIGHT//length) ]
        self.board[0][0] = 1
        self.board[-1][-1] = 2
        self.startNode = self.get_node(1)
        self.targetNode = self.get_node(2)
    
    def get_node(self,node):
        for i in range(len(self.board)):
            for j in range(len(self.board[i])):
                if self.board[i][j] == node:
                    return (i,j)
        return None
    
    def display(self,win):
        win.fill(white)
        for i in range(len(self.board)):
            for j in range(len(self.board[i])):
                color = None
                if self.board[i][j] == 1:
                    color = green
                elif self.board[i][j] == 2:
                    color = red
                elif self.board[i][j] == 3:
                    color = pathC
                elif self.board[i][j] == -1:
                    color = black
                elif self.board[i][j] == 4:
                    color = op
                elif self.board[i][j] == 5:
                    color = cl
                if color:
                    pg.draw.rect(win,color,(self.length*j,self.length*i,self.length,self.length))
                pg.draw.line(win,black,(0,self.length*i),(W_WIDTH,self.length*i))
                if i == len(self.board)-1: # draw vertical lines #
                    pg.draw.line(win,black,(self.length*j,0),(self.length*j,W_HEIGHT))
    
    def set(self,nBoard):
        self.board = nBoard
    
    def clicked(self,x,y):
        result = (y//self.length,x//self.length)
        if  0 <= result[0] < len(self.board) and 0 <= result[1] < len(self.board[0]):
            return result
        return None
    
    def clear(self,walls=True):
        nums = [-1,3,4,5] if walls else [3,4,5]
        for i in range(len(self.board)):
            for j in range(len(self.board[0])):
                if self.board[i][j] in nums:
                    self.board[i][j] = 0
    
    def move_node(self,node,toPos):
        if 0 <= toPos[0] < len(self.board) and 0 <= toPos[1] < len(self.board[0]):
            if self.board[toPos[0]][toPos[1]] not in (1,2):
                y,x = self.get_node(node)
                self.board[y][x] = 0
                self.board[toPos[0]][toPos[1]] = node
                self.startNode = self.get_node(1)
                self.targetNode = self.get_node(2)

size = 0
count = 0
while not 20 <= size <= 100:
    print("Enter size of each cube (between 20 and 100), 20 is recommended")
    try:
        size = int(input())
    except:
        print("Not a valid number!")

grid = Grid(size)
startNode = grid.get_node(1)
targetNode = grid.get_node(2)


def solve(grid,showSteps=True):
    paused = False
    operations = 0
    av = (0,3,4,5)
    clock = pg.time.Clock()
    openList = NodeList()
    closedList = NodeList()
    board = grid.board
    startNode = Node(startPos=grid.startNode,targetPos=grid.targetNode)
    openList.items.append(startNode)
    abreak = False
    s = time.time()
    start = grid.startNode
    end = grid.targetNode
    while(True):
        if len(openList.items) == 0:
            print("no path")
            time.sleep(1)
            return board
        neighbors = NodeList()
        n = openList.getMin()

        curr = openList.items[n]
        openList.items.pop(n)
        closedList.items.append(curr)
        neighbors = curr.getNeighbors(board)
        if curr.pos == end:
            print("done")
            break
        for neighbor in neighbors:
            if neighbor.pos == end:
                abreak = True
                break
            index1 = openList.contains(neighbor)
            index2 = closedList.contains(neighbor)
            if index1 >= 0 and openList.items[index1].cost > neighbor.cost:
                openList.items.pop(index1)
                openList.items.append(neighbor)
            if index2 >= 0 and closedList.items[index2].cost > neighbor.cost:
                closedList.items.pop(index2)
                openList.items.append(neighbor)
            if index1 == -1 and index2 == -1:
                openList.items.append(neighbor)

        if showSteps:
            for node in closedList.items:
                y,x = node.pos
                if (y,x) != start:
                    grid.board[y][x] = 4
                    
            for node in openList.items:
                y,x = node.pos
                if (y,x) != start:
                    grid.board[y][x] = 5

            for event in pg.event.get():
                if event.type == pg.QUIT:
                    return board
                elif event.type == pg.KEYDOWN:
                    if event.key == pg.K_ESCAPE:
                        return board
                    if event.key == pg.K_SPACE:
                        paused = True
                        pg.event.clear()
                        break

            while paused:
                for event in pg.event.get():
                    if event.type == pg.QUIT:
                        return board
                    elif event.type == pg.KEYDOWN:
                        if event.key == pg.K_SPACE:
                            paused = False
                            break
                        elif event.key == pg.K_ESCAPE:
                            return board

                        

            grid.display(win)
            pg.display.flip()
            #clock.tick(60)

        if abreak:
            break
    
    print("time: ",time.time()-s)
    path = NodeList()
    curr = closedList.items[-1]
    while curr.pos != start:
        if board[y][x] in av and (y,x) != start:
            path.items.append(curr)
        curr = curr.parent
        
    path.items = reversed(path.items)
    for elem in path.items:
        clock.tick(60)
        y, x = elem.pos
        board[y][x] = 3
        grid.display(win)
        pg.display.flip()
    return board

def main(win):
    global startNode, targetNode
    solving = True
    editing = False
    moving = False
    while(solving):
        for event in pg.event.get():
            if event.type == pg.MOUSEBUTTONDOWN:
                if event.button == 1:
                    pos1 = pg.mouse.get_pos()
                    pos1 = grid.clicked(*pos1)
                    if pos1:
                        y,x = pos1
                        k = grid.board[y][x]
                        if k == 0 or k == -1 or k == 3 or k == 4 or k ==5:
                            editing = True
                            if k == -1:
                                grid.board[y][x] = 0
                            else:
                                grid.board[y][x] = -1
                        elif k == 1 or k == 2:
                            moving = True

            elif event.type == pg.MOUSEBUTTONUP:
                if event.button == 1:
                    editing = False
                    moving = False
            if moving or editing:
                pos = pg.mouse.get_pos()
                pos = grid.clicked(*pos)
                if pos:
                    if moving:
                            grid.move_node(k,pos)
                            startNode = grid.get_node(1)
                            targetNode = grid.get_node(2)

                    if pos != pos1:
                        y,x = pos
                        k = grid.board[y][x]
                        if editing:
                            if k == 0 or k == -1 or k == 3 or k == 4 or k ==5:
                                if k == -1:
                                    grid.board[y][x] = 0
                                else:
                                    grid.board[y][x] = -1
                    pos1 = pg.mouse.get_pos()
                    pos1 = grid.clicked(*pos1)

            if event.type == pg.KEYDOWN:
                if event.key == pg.K_p:
                    grid.clear(walls=False)
                elif event.key == pg.K_c:
                    grid.clear()
                elif event.key == pg.K_SPACE:
                    grid.clear(walls=False)
                    grid.set(solve(grid))
                    grid.display(win)
                    pg.event.clear()

                elif event.key == pg.K_ESCAPE:
                    pg.quit()
                    return
            elif event.type == pg.QUIT:
                pg.quit()
                return
        grid.display(win)
        pg.display.flip()
        #clock.tick(120)
        
        

if __name__ == "__main__":
    main(win)
