import random


class Cell:
    """Cell class that defines each walkable Cell on the grid"""
    def __init__(self, x: int, y: int):
        self.x = x
        self.y = y
        self.visited = False
        self.walls = [True, True, True, True] # Left, Right, Up, Down


    def getChildren(self, grid: list) -> list:
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
    for yindex, y in enumerate(grid):
        for xindex, x in enumerate(y):
            for i, w in enumerate(x.walls):
                if i == 0 and w:
                    binGrid[yindex*2+1][xindex*2] = '⬛'
                if i == 1 and w:
                    binGrid[yindex*2+1][xindex*2+2] = '⬛'
                if i == 2 and w:
                    binGrid[yindex*2][xindex*2+1] = '⬛'
                if i == 3 and w:
                    binGrid[yindex*2+2][xindex*2+1] = '⬛'
    return binGrid


def drawBorder(grid: list) -> list:
    """Draw a border around the maze"""
    length = len(grid)
    for row in grid:
        row[0] = row[length-1] = '⬛'
        
    grid[0] = grid[length-1] = ['⬛'] * length
    return grid


def displayMaze(grid: list):
    """Draw the maze using ASCII characters and display the maze"""
    binGrid = []
    length = len(grid)*2+1
    for x in range(length):
        if x % 2 == 0:
            binGrid.append(['⬜' if x % 2 != 0 else '⬛' for x in range(length)])
        else:
            binGrid.append(['⬜'] * length)
    
    binGrid = drawWalls(grid, binGrid)
            
    binGrid = drawBorder(binGrid)

    print('\n'.join([''.join(x) for x in binGrid]))


# Request the user to input a maze size and initialise the maze, stack and initial Cell
size = int(input('Enter a maze size: '))
grid = [[Cell(x, y) for x in range(size)] for y in range(size)]
current = grid[0][0]
stack = []


# Main loop to generate the maze
while True:
    current.visited = True
    children = current.getChildren(grid)

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


# Display the maze
grid = displayMaze(grid)
