// Cell class defining every walkable cell in the grid
class Cell {
    constructor(x, y) {
        this.x = x;
        this.y = y;
        this.visited = false;
        this.walls = [true, true, true, true];
    }

    // A method of the Cell class to check if a Cell has surrounding walkable Cells
    getChildren(grid) {
        const a = [[1, 0], [-1,0], [0, 1], [0, -1]];
        const children = [];
        
        for ([x, y] of a){
            if ([grid.length, -1].includes(this.x+x) || [grid.length, -1].includes(this.y+y)) {
                continue;
            }

            let child = grid[this.y+y][this.x+x];

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
}


// Draw the border around the Grid
function drawBorder(grid) {
    for ([i, x] in grid.entries()) {
        x[0] = x[grid.length-1] = '⬛';
        grid[i] = x;
    }

    const hm = [];
    for (m=0; m<grid.length; m++) { 
        hm.push('⬛');
    }
    
    grid[0] = grid[grid.length-1] = hm;
}


// Convert the maze to ASCII characters to be displayed
function displayMaze(grid) {
    let binGrid = [];
    for (x=0; x < grid.length*2+1; x++) {
        const lst = [];
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

    drawWalls(grid, binGrid);

    drawBorder(binGrid);

    const toPrint = [];
    for (x=0; x<binGrid.length; x++) {
        toPrint.push(binGrid[x].join(''));
    }
    console.log(toPrint.join('\n'));
}


// For randomly picking a neighbouring Cell
function random(mn, mx) {  
    return Math.floor(Math.random() * (mx - mn) + mn);
}


// Defining the dimensions of the grid
const grid = [];
const size = 20
for (y=0; y<size; ++y) {
    let inner = []
    for (x=0; x<size; x++) {
        inner.push(new Cell(x, y));
    }
    grid.push(inner);
}


// Set the start cell and initialise the stack
let current = grid[0][0];
const stack = [];


// Main loop that generates the maze
while (true) {
    current.visited = true;
    let children = current.getChildren(grid);

    if (children.length > 0) {
        let choice = children[random(0, children.length)];

        choice.visited = true;

        stack.push(current);

        removeWalls(current, choice);

        current = choice;
    }
    else if (stack.length > 0) {
        current = stack.pop();
    }
    else {break}
}


// Converting the maze to a viewable format to then be displayed
displayMaze(grid);
