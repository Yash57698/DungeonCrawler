import random

def recursivebacktrack(maze,start):
    """
        Implements an iterative version of Recursive Backtracking for maze generation
        Args: 
            maze: the 2d array to complete as maze
            start:The start node from where to start the maze generatoin from
    """
    stk = []
    maze[start[0]][start[1]] = 2
    stk.append(start)

    while len(stk) > 0:
        p = stk.pop(len(stk)-1)
        x,y = p
        choices = []
        if x>=2 and maze[y][x-2] == 0:
            choices.append((y,x-2))
        if y>=2 and maze[y-2][x] == 0:
            choices.append((y-2,x))
        if x<(len(maze[0])-2) and maze[y][x+2]==0:
            choices.append((y,x+2))
        if y<(len(maze)-2) and maze[y+2][x]==0:
            choices.append((y+2,x))      
        if(len(choices) > 0):
            random.shuffle(choices)
            maze[choices[0][0]][choices[0][1]] = 2
            maze[int((choices[0][0]+y)/2)][int((choices[0][1]+x)/2)] = 0
            stk.append((x,y))
            stk.append((choices[0][1],choices[0][0]))
        
def generateMaze(width,height):
    """
    creates an empty maze and populates it using recursivebacktracking
    Args:
        width: the width of the maze to generate
        height: the height of the maze to generate
    """
    maze = []
    width = width -1
    for i in range(height):
        row = []
        for j in range(width):
            if i%2 ==0 and j%2 == 0:
                row.append(0)
            else:
                row.append(1)
        maze.append(row)

    maze[0][0] = 0
    recursivebacktrack(maze,(0,0))
    for i in range(height):
        for j in range(width):
            if maze[i][j] == 2:
                maze[i][j] = 0
    for i in range(height):
        maze[i] = maze[i] + [1]
    maze[-2][-1] = 0
    return maze

