import pygame
import random
pygame.init()


"""Initialise screen and define Cell dimensions"""
width = 15
height = 15
screen = pygame.display.set_mode((735,735))
pygame.display.set_caption('Maze')


"""Cell class that defines each walkable Cell on the grid"""
class Cell():
    def __init__(self, x, y):
        self.x = x
        self.y = y
        self.visited = False
        self.walls = [True, True, True, True] # Left, Right, Up, Down


    """Check if the Cell has any surrounding unvisited Cells that are walkable"""
    def haschildren(self, grid):
        a = [(1, 0), (-1,0), (0, 1), (0, -1)] # Surrounding squares
        children = []

        for x, y in a:
            if self.x+x in [len(grid), -1] or self.y+y in [-1, len(grid)]: # Check if the neighbouring square is within range
                continue
        
            child = grid[self.y+y][self.x+x] # Get the child cell

            if child.visited: # Check if the child has already been visited
                continue

            children.append(child)
        return children


    """Draw a Cells existing walls"""
    def show(self, width, height, c, c2):
        x = self.x
        y = self.y

        if self.walls[0]:
            pygame.draw.rect(screen, (20,20,20), (width*x+c-width, height*y+c2, width, height))
        if self.walls[1]:
            pygame.draw.rect(screen, (20,20,20), (width*x+c+width, height*y+c2, width, height))
        if self.walls[2]:
            pygame.draw.rect(screen, (20,20,20), (width*x+c, height*y+c2-height, width, height))    
        if self.walls[3]:
            pygame.draw.rect(screen, (20,20,20), (width*x+c, height*y+c2+height, width, height))  
    

    """Mark the current cell"""
    def mark(self, width, height):
        x = self.x*width
        y = self.y*height
        pygame.draw.rect(screen, (134, 46, 222), (x*2+width,y*2+height, width, height))


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


"""Fill in the 'corners' of the grid (due to the walls being square)"""
def cornerFill():
    c = c2 = 0
    for x in range(len(grid)+1):
        for y in range(len(grid)+1):
            pygame.draw.rect(screen, (20,20,20), (x*width+c, y*height+c2, width, height))
            c2 += height
        c2 = 0
        c += width


"""Define the grid, set the current Cell and initialise the stack"""
grid = [[Cell(x, y) for x in range(24)] for y in range(24)]
current = grid[0][0]
stack = []


"""Main loop"""
exit = False
while not exit:
    c = 0
    c2 = 0
    for x in range(len(grid)):
        for y in range(len(grid)):
            grid[x][y].show(width, height, c2+width, c+height) # Draw walls
            c2 += height
        c2 = 0
        c += width
    
    cornerFill()

    current.visited = True
    current.mark(width, height) # Highlight the current Cell

    """If the current has neighours then choose a random one, mark it as visited, """
    """remove the walls between it and the current and set it as the new current"""
    children = current.haschildren(grid) 
    if children:
        choice = random.choice(children)
        choice.visited = True

        stack.append(current)

        removeWalls(current, choice)

        current = choice
    
    
    elif stack: # If the current has no neighbours go back to the last Cell on the stack
        current = stack.pop()

    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            exit = True
    
    pygame.display.update()
    screen.fill((210, 210 ,210))
pygame.quit()
quit()