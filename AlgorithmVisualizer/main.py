import pygame 
import math
from queue import PriorityQueue
from colours import *


# setting up display grid
WIDTH = 900
# not in term with the actual map simply sets the windows width
WIN = pygame.display.set_mode((WIDTH, WIDTH))
WINDOW = pygame.display.set_mode((WIDTH,WIDTH))
pygame.display.set_caption("A* pahtfinding algorithm")



class spotGUI:
    def __init__(self,row,col,width,total_rows):
        self.row = row
        self.col = col
        self.x = row * width
        self.y = row * width
        self.color = WHITE
        self.neighbours = []
        self.width = width
        self.total_rows = total_rows

    # note for positioning: black = borders, orange = start node, purple = path, dark purple = end  etc...
        
    def getPosition(self):
        return self.row, self.col
    
    def isClosed(self):
        # spot "closed" 
        return self.color == RED
    
    def isOpen(self):
        return self.color ==  GREEN
    
    def isBarrier(self):
        return self.color == BLACK
    
    def isStart(self):
        return self.color == ORANGE
    
    def isEnd(self):
        return self.color == DARK_PURPLE
    
    def reset(self):
        return self.color == WHITE
    

    # functions here will set certain nodes as its designated color

    def makeStart(self):
        self.color = ORANGE
        
    def makeClosed(self):
        self.color = RED
    
    def makeOpen(self):
        self.color = GREEN

    def makeBarrier(self):
        self.color = BLACK

    def makeEnd(self):
        self.color = TURQUOISE

    def makePath(self):
        self.color = PURPLE

    def drawGrid(self, WIN):
        # argument to draw in cube
        pygame.draw.rect(WIN, self.color, (self.x, self.y, self.width, self.width))


    # implement later
    def updateNeighborNode(self, grid):
        pass  

    def __lt__(self, other):
        return False


def heuristics(p1,p2):
    # Manhattan distance calculations
    x1, y1 = p1
    x2, y2 = p2
    return abs(x1 - x2) + abs(y1 - y2)


def reconstructPath(Origin_point, current, draw):
    while current in Origin_point:
        current = Origin_point[current]
        current.makepath()
        draw()


def pathfindingAlgorithm(draw, grid, start, end):
    count = 0
    clearSet = PriorityQueue()
    clearSet.put((0,count, start))
    # look at specifics of Priorityqueue implementation
    originPoint = {}

    # look at if this sections f score and g score need the spotGUI specification instead of spot

    g_score = {spot: float("inf") for row in grid for spot in row}
    g_score[start] = 0
    

    f_score = {spot: float("inf") for row in grid for spot in row}
    f_score[start] = heuristics(start.getPosition(), end.getPosition())

    clearSetHash = {start}

    while not clearSet.empty():
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()

        current = clearSet.get()[2]
        clearSetHash.remove(current)

        if current == end:
            reconstructPath(originPoint, end, draw)
            end.makeEnd()
            return True
        

        for neighbor in current.neighbors:
            temp_g_Score = g_score[current] + 1

            if temp_g_Score < g_score[neighbor]:
                originPoint[neighbor] = current
                g_score[neighbor] = temp_g_Score
                f_score[neighbor] = temp_g_Score + heuristics(neighbor.getPosition(), end.getPosition())
                if neighbor not in clearSetHash:
                    count += 1
                    clearSet.put((f_score[neighbor], count, neighbor))
                    clearSetHash.add(neighbor)
                    neighbor.makeOpen()
        draw()

        if current != start:
            current.makeClosed()

    return False


def gridAllocation(rows,width):
    # continue from here...
    grid = []
    gap = width // rows
    for i in range(rows):
        grid.append([])
        for j in range(rows):
            spot = spotGUI(i, j, gap, rows)
            grid[i].append(spot)

    return grid


def formGrid(win, rows, width):
    gap = width // rows
    for i in range(rows):
        pygame.draw.line(win, LIGHT_GRAY, (0,i * gap), (width, i * gap))
        for j in range(rows):
            pygame.draw.line(win,LIGHT_GRAY, (j * gap, 0), (j * gap , width))



def draw(win, grid, rows, width):
    win.fill(WHITE)

    for row in grid:
        for spot in row:
            spot.draw(win)

    formGrid(win, rows, width)
    pygame.display.update()


def clickedPosition(pos, rows, width):
    gap = width // rows 
    y, x = pos
    row = y // gap
    col = x // gap
    return row, col

def main(win, width):
    ROWS = 50
    grid = gridAllocation(ROWS, width)

    start = None
    end =  None
    run = True
    while run:
        draw(win, grid, ROWS, width)
        for x in pygame.event.get():
            if x.type == pygame.QUIT:
                run = False

            if pygame.mouse.get_pressed()[0]: # 0 for left click
                pos = pygame.mouse.get_pos()
                row, col = clickedPosition(pos, ROWS, width)
                spot = grid[row][col]
                if not start and spot != end:
                    start = spot
                    start.makeStart()

                elif not end and spot != start:
                    end = spot 
                    end.makeEnd()

                elif spot != end and spot != start:
                    spot.makeBarrier()

            elif pygame.mouse.get_pressed()[2]: # 2 for right click
                pos = pygame.mouse.get_pos()
                row, col = clickedPosition(pos, ROWS, width)
                spot = grid[row][col]
                spot.reset()
                if spot == start:
                    start = None
                elif spot == end:
                    end == None


            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_SPACE and start and end:
                    for row in grid:
                        for spot in row:
                            spot.updateNeighborNode(grid)


                    pathfindingAlgorithm(lambda: draw(win, grid, ROWS, width), grid, start, end)

                if event.key == pygame.K_c:
                    start = None
                    end = None
                    grid = gridAllocation(ROWS, width)


    pygame.quit()


main(WIN, WIDTH)
