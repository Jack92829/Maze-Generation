// Cell class defining every walkable cell in the grid
class Cell {
    constructor(x, y) {
        this.x = x;
        this.y = y;
        this.visited = false;
        this.walls = [true, true, true, true];
    }

    // A method of the Cell class to check if a Cell has surrounding walkable Cells
    hasChildren(grid) {
        var a = [[1, 0], [-1,0], [0, 1], [0, -1]];
        var children = [];
        
        var i;
        for (i of a){
            var x = i[0];
            var y = i[1];
            if ([grid.length, -1].includes(this.x+x) || [grid.length, -1].includes(this.y+y)) {
                continue;
            }

            var child = grid[this.y+y][this.x+x];

            if (child.visited) {
                continue;
            }
            children.push(child);
        }
        return children;
    }
}


// Remove the wall between two Cells
function removeWalls(current, choice) {
    if (choice.x > current.x) {   
        current.walls[1] = false;
        choice.walls[0] = false;
    }
    else if (choice.x < current.x) {
        current.walls[0] = false;
        choice.walls[1] = false;
    }
    else if (choice.y > current.y) {
        current.walls[3] = false;
        choice.walls[2] = false;
    }
    else if (choice.y < current.y) {
        current.walls[2] = false;
        choice.walls[3] = false;
    }
    return current, choice;
}


// Draw the existing walls of a Cell
function drawWalls(grid, binGrid) {
    for ([yi, y] of grid.entries()) {
        for ([xi, x] of y.entries()) {
            for ([i, w] of x.walls.entries()) {
                if (i == 0 && w) {
                    binGrid[yi*2+1][xi*2] = '⬛';
                }
                if (i == 1 && w) {
                    binGrid[yi*2+1][xi*2+2] = '⬛';
                }
                if (i == 2 && w) {
                    binGrid[yi*2][xi*2+1] = '⬛';
                }
                if (i == 3 && w) {
                    binGrid[yi*2+2][xi*2+1] = '⬛';
                }
            }
        } 
    }
    return binGrid;
}


// Draw the border around the Grid
function drawBorder(grid) {
    for ([i, x] in grid.entries()) {
        x[0] = x[grid.length-1] = '⬛';
        grid[i] = x;
    }

    var hm = [];
    for (m=0; m<grid.length; m++) { 
        hm.push('⬛');
    }

    grid[0] = grid[grid.length-1] = hm;
    return grid;
}


// Convert the maze to ASCII characters to be displayed
function displayMaze(grid) {
    var binGrid = [];
    for (x=0; x < grid.length*2+1; x++) {
        var lst = [];
        if (x % 2 == 0) {
            for (n=0; n < grid.length*2+1; n++) {
                if (n % 2 != 0) {
                    lst.push('⬜');
                }
                else {
                    lst.push('⬛');
                }
            }
            binGrid.push(lst);
        }
        else {
            for (m=0; m < grid.length*2+1; m++) {
                lst.push('⬜');
            }
            binGrid.push(lst);
        }
    }
    
    var binGrid = drawWalls(grid, binGrid);

    var binGrid = drawBorder(binGrid);

    var toPrint = [];
    for (x=0; x<binGrid.length; x++) {
        toPrint.push(binGrid[x].join(''));
    }
    console.log(toPrint.join('\n'))
}


// For randomly picking a neighbouring Cell
function random(mn, mx) {  
    return Math.floor(Math.random() * (mx - mn) + mn);
}


// Defining the dimensions of the grid
var grid = [];
var size = 20
for (y=0; y<size; ++y) {
    var inner = []
    for (x=0; x<size; x++) {
        inner.push(new Cell(x, y));
    }
    grid.push(inner);
}


// Set the start cell and initialise the stack
var current = grid[0][0];
var stack = [];


// Main loop that generates the maze
while (true) {
    current.visited = true;
    var children = current.hasChildren(grid);

    if (children.length > 0) {
        var choice = children[random(0, children.length)];

        choice.visited = true;

        stack.push(current);

        current, choice = removeWalls(current, choice);

        var current = choice;
    }
    else if (stack.length > 0) {
        var current = stack.pop();
    }
    else {break}
}


// Converting the maze to a viewable format to then be displayed
displayMaze(grid);
