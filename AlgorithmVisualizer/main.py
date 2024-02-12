import pygame 
import math
from queue import PriorityQueue
from colours import *


# setting up display constants
WIDTH = 900
WINDOW = pygame.display.set_mode((WIDTH,WIDTH))
pygame.display.set_caption("A* pahtfinding algorithm")



class spotGUI:
    def __init__(self, row,col,width,total_rows):
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

    def updateNeighbour(self, grid):
        pass  

    def __lt__(self, other):
        return False


def heuristics(p1,p2):
    # Manhattan distance calculations
    x1, y1 = p1
    x2, y2 = p2
    return abs(x1 - x2) + abs(y1 - y2)
    