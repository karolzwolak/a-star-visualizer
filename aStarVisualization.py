# from # https://github.com/DeathEyeXD/PythonProjects/blob/master/aStarVisualization.py
import pygame as pg
import time
W_WIDTH, W_HEIGHT = 1200, 900

black = (0, 0, 0)
white = (255, 255, 255)
green = (0, 255, 0)
pathC = (255, 255, 0)
cl = (0, 255, 255)
op = (30, 144, 255)
red = (255, 0, 0)


class Node:
    def __init__(self, pos=None, parent_node=None, start_pos=None, target_pos=None):
        if start_pos != None and target_pos != None:
            self.pos = start_pos
            self.g_cost = 0
            self.h_cost = 0
            self.cost = 0

        elif pos != None and parent_node != None:
            self.parent = parent_node
            self.pos = pos
            self.g_cost = parent_node.g_cost + self.distance(self.parent.pos)
            self.h_cost = self.get_h_val()
            self.cost = self.g_cost+self.h_cost

    def get_h_val(self):
        a = abs(self.pos[0] - target_node[0])
        b = abs(self.pos[1] - target_node[1])
        return a+b

    def distance(self, from_pos):
        dis = ((self.pos[0]-from_pos[0])**2+(self.pos[1]-from_pos[1])**2)**0.5
        return dis

    def get_neighbors(self, board):
        n = (0, 1, 2, 3, 4, 5)
        y, x = self.pos

        down = False
        up = False
        left_up = False
        left_down = False
        right_up = False
        right_down = False

        h_len = len(board[0])  # x, pos[1] #
        v_len = len(board)  # y, pos[0] #
        neighbors = []

        if y < v_len-1:
            y1 = y+1
            x1 = x
            down = True
            if board[y1][x1] in n:
                neighbors.append(Node(pos=(y1, x1), parent_node=self))
                left_down = True
                right_down = True

        if y > 0:
            y1 = y-1
            x1 = x
            up = True
            if board[y1][x1] in n:
                neighbors.append(Node(pos=(y1, x1), parent_node=self))
                left_up = True
                right_up = True

        if x < h_len-1:
            y1 = y
            x1 = x+1
            if board[y1][x1] in n:
                neighbors.append(Node(pos=(y1, x1), parent_node=self))
                right_up = True
                right_down = True
            # else:
                # right_up = False
                # right_down = False

            if right_up and up:
                y1 = y-1
                if board[y1][x1] in n:
                    neighbors.append(Node(pos=(y1, x1), parent_node=self))
            if right_down and down:
                y1 = y+1
                if board[y1][x1] in n:
                    neighbors.append(Node(pos=(y1, x1), parent_node=self))
        if x > 0:
            y1 = y
            x1 = x-1
            if board[y1][x1] in n:

                neighbors.append(Node(pos=(y1, x1), parent_node=self))
                left_up = True
                left_down = True

            if left_up and up:
                y1 = y-1
                if board[y1][x1] in n:
                    neighbors.append(Node(pos=(y1, x1), parent_node=self))
            if left_down and down:
                y1 = y+1
                if board[y1][x1] in n:
                    neighbors.append(Node(pos=(y1, x1), parent_node=self))

        return neighbors


class NodeList:
    def __init__(self):
        self.items = []

    def contains(self, obj):
        if len(self.items) > 0:

            for i, node in enumerate(self.items):
                if obj.pos == node.pos:
                    return i

        return -1

    def get_min(self):
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
            print(node.pos, end=",")

        print()


class Grid:

    def __init__(self, length):
        self.length = length
        self.board = [[0 for _ in range(W_WIDTH//length)]
                      for _ in range(W_HEIGHT//length)]

        self.board[0][0] = 1
        self.board[-1][-1] = 2

        self.start_node = self.get_node(1)
        self.target_node = self.get_node(2)

    def switch(self):
        self.board[self.start_node[0]][self.start_node[1]] = 2
        self.board[self.target_node[0]][self.target_node[1]] = 1

        self.start_node = self.get_node(1)
        self.target_node = self.get_node(2)

        return (self.start_node, self.target_node)

    def get_node(self, node):
        for i in range(len(self.board)):
            for j in range(len(self.board[i])):

                if self.board[i][j] == node:
                    return (i, j)

        return None

    def display(self, win):
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

                    pg.draw.rect(win, color, (self.length*j,
                                 self.length*i, self.length, self.length))

                pg.draw.line(win, black, (0, self.length*i),
                             (W_WIDTH, self.length*i))

                if i == len(self.board)-1:  # draw vertical lines #
                    pg.draw.line(win, black, (self.length*j, 0),
                                 (self.length*j, W_HEIGHT))

    def set(self, n_board):
        self.board = n_board

    def clicked(self, x, y):
        result = (y//self.length, x//self.length)
        if 0 <= result[0] < len(self.board) and 0 <= result[1] < len(self.board[0]):
            return result
        return None

    def clear(self, walls=True):
        nums = [-1, 3, 4, 5] if walls else [3, 4, 5]
        for i in range(len(self.board)):
            for j in range(len(self.board[0])):
                if self.board[i][j] in nums:
                    self.board[i][j] = 0

    def move_node(self, node, to_pos):
        if 0 <= to_pos[0] < len(self.board) and 0 <= to_pos[1] < len(self.board[0]):
            if self.board[to_pos[0]][to_pos[1]] not in (1, 2):
                y, x = self.get_node(node)
                self.board[y][x] = 0
                self.board[to_pos[0]][to_pos[1]] = node
                self.start_node = self.get_node(1)
                self.target_node = self.get_node(2)


def solve(win, grid, show_steps=True):
    paused = False

    av = (0, 3, 4, 5)
    clock = pg.time.Clock()
    open_list = NodeList()
    closed_list = NodeList()

    board = grid.board
    start_node = Node(start_pos=grid.start_node, target_pos=grid.target_node)
    open_list.items.append(start_node)

    a_break = False
    start = grid.start_node
    end = grid.target_node

    no_count = 0.
    s = time.time()

    while True:

        # Actual algorithm ----------- #
        if not open_list.items:
            print("NoPathException")
            return board

        neighbors = NodeList()
        n = open_list.get_min()

        curr = open_list.items[n]
        open_list.items.pop(n)
        closed_list.items.append(curr)
        neighbors = curr.get_neighbors(board)

        if curr.pos == end:
            break
        for neighbor in neighbors:
            if neighbor.pos == end:
                a_break = True
                break

            index1 = open_list.contains(neighbor)
            index2 = closed_list.contains(neighbor)

            if index1 >= 0 and open_list.items[index1].cost > neighbor.cost:
                open_list.items.pop(index1)
                open_list.items.append(neighbor)

            if index2 >= 0 and closed_list.items[index2].cost > neighbor.cost:
                closed_list.items.pop(index2)
                # adding this neighbor to openlist isnt necessary, but it might turn out to be shortest path #
                open_list.items.append(neighbor)

            if index1 == -1 and index2 == -1:
                open_list.items.append(neighbor)

        # End of actual algorithm ----------- #
        if show_steps:

            start_no_count = time.time()

            for node in closed_list.items:
                y, x = node.pos
                if (y, x) != start:
                    grid.board[y][x] = 4

            for node in open_list.items:
                y, x = node.pos
                if (y, x) != start:
                    grid.board[y][x] = 5

            for event in pg.event.get():
                if event.type == pg.QUIT:
                    return board

                elif event.type == pg.KEYDOWN:

                    if event.key == pg.K_ESCAPE:
                        return board
                    if event.key == pg.K_SPACE:
                        paused = True
                        grid.clear(walls=False)
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
            # clock.tick(200)

            no_count += time.time() - start_no_count

        if a_break:
            break

    actual_time = time.time() - s - no_count

    # Extracting path ------------ #
    # path is reversed #
    path = NodeList()
    length = 0
    curr = closed_list.items[-1]

    while curr.pos != start:
        y, x = curr.pos

        if board[y][x] in av and (y, x) != start:
            path.items.append(curr)
            length += curr.g_cost

        curr = curr.parent

    length = round(length, 3)

    # elapsedTime = time.time()-s

    if show_steps:
        print("found path of length", length, "time: ", actual_time, "s")

    path.items = reversed(path.items)

    for elem in path.items:
        clock.tick(60)
        y, x = elem.pos

        board[y][x] = 3
        grid.display(win)
        pg.display.flip()

    return board


def get_size_from_user():
    size = 0
    while not 10 <= size <= 50:
        print("Enter size of each cube (between 10 and 50), 20 is default")
        try:
            inp = input()
            size = int(inp)
        except:
            if inp == "":
                size = 20
                break
            print("Not a valid number!")

    return size


def init():

    win = pg.display.set_mode((W_WIDTH, W_HEIGHT))

    pg.display.set_caption(
        "A* visualization. mouse-click to draw, c to clear board, space to start/pause, p to clear path, s to switch start and end nodes ")

    size = get_size_from_user()
    grid = Grid(size)

    start_node = grid.get_node(1)
    target_node = grid.get_node(2)

    return win, grid, start_node, target_node


def main():
    global start_node, target_node

    win, grid, start_node, target_node = init()

    solving = True
    editing = False
    moving = False

    while solving:

        for event in pg.event.get():
            if event.type == pg.MOUSEBUTTONDOWN:

                if event.button == 1:
                    pos1 = pg.mouse.get_pos()
                    pos1 = grid.clicked(*pos1)

                    if pos1:
                        y, x = pos1
                        k = grid.board[y][x]
                        if k == 0 or k == -1 or k == 3 or k == 4 or k == 5:

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
                        grid.move_node(k, pos)
                        start_node = grid.get_node(1)
                        target_node = grid.get_node(2)

                    if pos != pos1:
                        y, x = pos
                        k = grid.board[y][x]

                        if editing:
                            if k == 0 or k == -1 or k == 3 or k == 4 or k == 5:
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
                    grid.set(solve(win, grid))
                    grid.display(win)
                    pg.event.clear()

                elif event.key == pg.K_s:
                    start_node, target_node = grid.switch()

                elif event.key == pg.K_ESCAPE:
                    pg.quit()
                    return

            elif event.type == pg.QUIT:
                pg.quit()
                return

        grid.display(win)
        pg.display.flip()


if __name__ == "__main__":
    main()
