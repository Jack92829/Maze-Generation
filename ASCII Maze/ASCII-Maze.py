import random


class Cell():
    """Cell class that defines each walkable Cell on the grid"""
    def __init__(self, x: int, y: int):
        self.x = x
        self.y = y
        self.visited = False
        self.walls = [True, True, True, True] # Left, Right, Up, Down


    def haschildren(self, grid: list) -> list:
        """Check if the Cell has any surrounding unvisited Cells that are walkable"""
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


def removeWalls(current: Cell, choice: Cell):
    """Removeing the wall between two Cells"""
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


def drawWalls(grid: list, binGrid: list) -> list:
    """Draw existing walls around Cells"""
    for yi, y in enumerate(grid):
        for xi, x in enumerate(y):
            for i, w in enumerate(x.walls):
                if i == 0 and w:
                    binGrid[yi*2+1][xi*2] = '⬛'
                if i == 1 and w:
                    binGrid[yi*2+1][xi*2+2] = '⬛'
                if i == 2 and w:
                    binGrid[yi*2][xi*2+1] = '⬛'
                if i == 3 and w:
                    binGrid[yi*2+2][xi*2+1] = '⬛'
    return binGrid


def drawBorder(grid: list) -> list:
    """Draw a border around the maze"""
    for i, x in enumerate(grid):
        x[0] = x[len(grid)-1] = '⬛'
        grid[i] = x
        
    grid[0] = grid[len(grid)-1] = ['⬛' for x in range(len(grid))] 
    return grid


def displayMaze(grid: list):
    """Draw the maze using ASCII characters and display the maze"""
    binGrid = []
    for x in range(len(grid)+len(grid)+1):
        if x % 2 == 0:
            binGrid.append(['⬜' if x % 2 != 0 else '⬛' for x in range(len(grid)+len(grid)+1)])
        else:
            binGrid.append(['⬜' for x in range(len(grid)+len(grid)+1)])
    
    binGrid = drawWalls(grid, binGrid)
            
    binGrid = drawBorder(binGrid)

    print('\n'.join([''.join(x) for x in binGrid]))


"""Request the user to input a maze size and initialise the maze, stack and initial Cell"""
size = int(input('Enter a maze size: '))
grid = [[Cell(x, y) for x in range(size)] for y in range(size)]
current = grid[0][0]
stack = []


"""Main loop to generate the maze"""
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
        break


"""Display the maze"""
grid = displayMaze(grid)