from cv2 import cv2
import random
import numpy as np
import os, sys


"""Cell class that defines each walkable Cell on the grid"""
class Cell():
    def __init__(self, x, y):
        self.x = x
        self.y = y
        self.visited = False
        self.walls = [True, True, True, True] # Left, Right, Up, Down


    """Check if the Cell has any surrounding unvisited Cells that are walkable"""
    def haschildren(self, grid):
        a = [(1, 0), (-1,0), (0, 1), (0, -1)]
        children = []
        for x, y in a:
            if self.x+x in [len(grid), -1] or self.y+y in [-1, len(grid)]:
                continue
            
            child = grid[self.y+y][self.x+x]
            if child.visited:
                continue
            children.append(child)
        return children


"""Removeing the wall between two Cells"""
def removeWalls(current, choice):
    if choice.x > current.x:     
        current.walls[1] = False
        choice.walls[0] = False
    elif choice.x < current.x:
        current.walls[0] = False
        choice.walls[1] = False
    elif choice.y > current.y:
        current.walls[3] = False
        choice.walls[2] = False
    elif choice.y < current.y:
        current.walls[2] = False
        choice.walls[3] = False


"""Draw existing walls around Cells"""
def drawWalls(grid, binGrid):
    for yi, y in enumerate(grid):
        for xi, x in enumerate(y):
            for i, w in enumerate(x.walls):
                if i == 0 and w:
                    binGrid[yi*2+1][xi*2] = (20,20,20)
                if i == 1 and w:
                    binGrid[yi*2+1][xi*2+2] = (20,20,20)
                if i == 2 and w:
                    binGrid[yi*2][xi*2+1] = (20,20,20)
                if i == 3 and w:
                    binGrid[yi*2+2][xi*2+1] = (20,20,20)
    return binGrid


"""Draw a border around the maze"""
def drawBorder(grid):
    for i, x in enumerate(grid): # Left and Right border
        x[0] = x[len(grid)-1] = (20,20,20)
        grid[i] = x
        
    grid[0] = grid[len(grid)-1] = [(20,20,20) for x in range(len(grid))] # Top and Bottom border
    return grid


"""Turn the grid into RGB values to then be turned into an image"""
def prepareGrid(grid):
    binGrid = []
    for x in range(len(grid)+len(grid)+1):
        if x % 2 == 0:
            binGrid.append([(210, 210 ,210) if x % 2 != 0 else (20,20,20) for x in range(len(grid)+len(grid)+1)])
        else:
            binGrid.append([(210, 210 ,210) for x in range(len(grid)+len(grid)+1)])
    
    binGrid = drawWalls(grid, binGrid)
            
    binGrid = drawBorder(binGrid)

    return binGrid


"""Turn the grid into a numpy array to then be resized"""
def prepareImage(grid):
    grid = np.uint8(np.array([np.array(xi) for xi in grid]))

    scale_percent = 1000
    width = int(grid.shape[1] * scale_percent / 100)
    height = int(grid.shape[0] * scale_percent / 100)

    return cv2.resize(grid, (width, height), interpolation=cv2.INTER_AREA)


"""Generate a maze of Cell classes to then be turned into an image later"""
def generateMaze():
    size = int(input('Enter a maze size: '))
    grid = [[Cell(x, y) for x in range(size)] for y in range(size)]
    current = grid[0][0]
    stack = []

    while True:
        current.visited = True
        children = current.haschildren(grid)

        if children:
            choice = random.choice(children)
            choice.visited = True

            stack.append(current)

            removeWalls(current, choice)

            current = choice
        
        elif stack:
            current = stack.pop()
        else:
            return grid


"""Save the image in the same directory as the python script under a given name"""
def createImage(grid):
    image = prepareImage(grid)

    name = input('\nEnter a name to save the image under\nIt will be stored in the same directory as this python script\n>>> ')
    result = cv2.imwrite(f'{os.path.dirname(sys.argv[0])}/{name}.png', image)
    
    print(f'Status: {"Success" if result else "Failed"}')


grid = generateMaze()

gridRGB = prepareGrid(grid)

createImage(gridRGB)
