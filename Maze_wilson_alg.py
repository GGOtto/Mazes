import turtle
import random
import time

class Player:
    '''Represents the player going through the maze'''

    def __init__(self, maze, penColor):
        '''Player(maze) -> Player
        creates the player for maze
        maze: Maze'''
        # get maze info
        self.blockSize = maze.get_block_size()
        self.width = maze.get_width()
        self.maze = maze
        self.barriars = maze.get_barriars()
        self.emptyBlocks = maze.get_empty_blocks() # get empty list
        
        # set up turtle
        self.color = penColor
        self.t = turtle.Turtle()
        self.t.pu()
        self.t.shape("circle")
        self.t.color(self.color)
        self.t.pensize(self.blockSize / 2)
        self.t.shapesize(self.blockSize / 20)
        self.t.seth(90)

        # put in start position
        start = self.maze.block_to_coord(
            self.maze.coord_to_block(-(self.width) * self.blockSize / 2,-(self.width + 2) * self.blockSize / 2))
        self.t.goto(start)
        self.t.pd()
        
        self.moving = False # tells if moving or not
        self.isWon = False # tells if game is won
        self.t.screen.update()

    def can_move(self):
        '''Player.can_move() -> list
        returns a list containing all the directions play can move'''
        directions = [] # initialize output list
        blockX,blockY = self.t.pos() # get position

        # get passages
        up = self.maze.coord_to_block(blockX,blockY + self.blockSize)
        right = self.maze.coord_to_block(blockX + self.blockSize,blockY)
        down = self.maze.coord_to_block(blockX,blockY - self.blockSize)
        left = self.maze.coord_to_block(blockX - self.blockSize,blockY)
        passageList = [up,right,down,left]

        for index in range(4): # look through passage indexes
            passage = passageList[index]

            # if passage way in maze or not blocked area out of maze
            if passage in self.emptyBlocks or \
                 (maze.is_out(passage) and passage not in self.barriars):
                directions.append(index)
            
        return directions        
        
    def go_up(self):
        '''Player.go_up()
        moves the player up'''
        if not self.moving and 0 in self.can_move():
            self.moving = True
            self.t.sety(self.t.ycor() + self.blockSize)
            self.moving = False
            self.check_win()
            self.t.screen.update()

    def go_right(self):
        '''Player.got_right()
        moves the player to the right'''
        if not self.moving and 1 in self.can_move():
            self.moving = True
            self.t.setx(self.t.xcor() + self.blockSize)
            self.moving = False
            self.check_win()
            self.t.screen.update()

    def go_down(self):
        '''Player.go_down()
        moves the player down'''
        if not self.moving and 2 in self.can_move():
            self.moving = True
            self.t.sety(self.t.ycor() - self.blockSize)
            self.moving = False
            self.check_win()
            self.t.screen.update()

    def go_left(self):
        '''Player.go_left()
        moves the player to the left'''
        if not self.moving and 3 in self.can_move():
            self.moving = True
            self.t.setx(self.t.xcor() - self.blockSize)
            self.moving = False
            self.check_win()
            self.t.screen.update()

    def pen_control(self):
        '''Player.pen_control()
        pen up or pen down according to what is current'''
        if self.t.isdown():
            self.t.pu()
        else:
            self.t.pd()

    def check_win(self):
        '''Player.check_win()
        checks if player has won and displays message'''
        x,y = self.t.pos()                                                # record current position
        if self.maze.is_out(self.maze.coord_to_block(x,y)) and not self.isWon:
            self.t.pu()                                                   # lift pen
            size = 2 * self.blockSize                                     # font size
            self.t.color("yellow")
            
            self.moving = True
            self.t.goto(self.maze.block_to_coord(self.emptyBlocks[-1]))   # go to place for text
            self.t.sety(self.t.ycor() + 4 * self.blockSize)               # go up a little
            self.t.write("You win!",False,"center",("Arial",size,"bold")) # write message
            self.t.goto(x,y)
            self.moving = False
            
            self.t.color(self.color)
            self.isWon = True                                             # game is won

## Begin Section Added by CaptainFlint ##
            
class WilsonMazeGenerator:
    """Maze Generator using Wilson's Loop Erased Random Walk Algorithm"""

    def __init__(self,width,height):
        """WilsonMazeGenerator(int,int) -> WilsonMazeGenerator
        Creates a maze generator with specified width and height.
        width: width of generated mazes
        height: height of generated mazes"""        
        self.width = 2*(width//2) + 1   # Make width odd
        self.height = 2*(height//2) + 1 # Make height odd

        # grid of cells
        self.grid = [[0 for i in range(self.width)] for j in range(self.height)]

        # declare instance variable
        self.visited = []    # visited cells
        self.unvisited = []  # unvisited cells
        self.path = dict()   # random walk path

        # valid directions in random walk
        self.directions = [(0,1),(1,0),(0,-1),(-1,0)]

    def __str__(self):
        """WilsonMazeGenerator.__str__() -> str
        outputs a string version of the grid"""
        out = ""
        for i in range(self.height):
            for j in range(self.width):
                out += str(self.grid[i][j])
                out += " "
            out += "\n"
        return out

    def get_grid(self):
        """WilsonMazeGenerator.get_grid() -> list
        returns the maze grid"""
        return self.grid

    def get_next_cell(self,cell,dirNum,fact):
        """WilsonMazeGenerator.get_next_cell(tuple,int,int) -> tuple
        Outputs the next cell when moved a distance fact in the the
        direction specified by dirNum from the initial cell.
        cell: tuple (y,x) representing position of initial cell
        dirNum: int with values 0,1,2,3
        fact: int distance to next cell"""
        dirTup = self.directions[dirNum]
        return (cell[0]+fact*dirTup[0],cell[1]+fact*dirTup[1])

    def is_valid_direction(self,cell,dirNum):
        """WilsonMazeGenerator(tuple,int) -> boolean
        Checks if the adjacent cell in the direction specified by
        dirNum is within the grid
        cell: tuple (y,x) representing position of initial cell
        dirNum: int with values 0,1,2,3"""
        newCell = self.get_next_cell(cell,dirNum,2)
        tooSmall = newCell[0] < 0 or newCell[1] < 0
        tooBig = newCell[0] >= self.height or newCell[1] >= self.width
        return not (tooSmall or tooBig)

    def initialize_grid(self):
        """WilsonMazeGenerator.initialize_grid() -> None
        Resets the maze grid to blank before generating a maze."""
        for i in range(self.height):
            for j in range(self.width):
                self.grid[i][j] = 0
                
        # fill up unvisited cells
        for r in range(self.height):
            for c in range(self.width):
                if r % 2 == 0 and c % 2 == 0:
                    self.unvisited.append((r,c))

        self.visited = []
        self.path = dict()

    def cut(self,cell):
        """WilsonMazeGenerator.cut(tuple) -> None
        Sets the value of the grid at the location specified by cell
        to 1
        cell: tuple (y,x) location of where to cut"""
        self.grid[cell[0]][cell[1]] = 1

    def generate_maze(self):
        """WilsonMazeGenerator.generate_maze() -> None
        Generates the maze according to the Wilson Loop Erased Random
        Walk Algorithm"""
        # reset the grid before generation
        self.initialize_grid()

        # choose the first cell to put in the visited list
        # see Step 1 of the algorithm.
        current = self.unvisited.pop(random.randint(0,len(self.unvisited)-1))
        self.visited.append(current)
        self.cut(current)

        # loop until all cells have been visited
        while len(self.unvisited) > 0:
            # choose a random cell to start the walk (Step 2)
            first = self.unvisited[random.randint(0,len(self.unvisited)-1)]
            current = first
            # loop until the random walk reaches a visited cell
            while True:
                # choose direction to walk (Step 3)
                dirNum = random.randint(0,3)
                # check if direction is valid. If not, choose new direction
                while not self.is_valid_direction(current,dirNum):
                    dirNum = random.randint(0,3)
                # save the cell and direction in the path
                self.path[current] = dirNum
                # get the next cell in that direction
                current = self.get_next_cell(current,dirNum,2)
                if (current in self.visited): # visited cell is reached (Step 5)
                    break

            current = first # go to start of path
            # loop until the end of path is reached
            while True:
                # add cell to visited and cut into the maze
                self.visited.append(current)
                self.unvisited.remove(current) # (Step 6.b)
                self.cut(current)

                # follow the direction to next cell (Step 6.a)
                dirNum = self.path[current]
                crossed = self.get_next_cell(current,dirNum,1)
                self.cut(crossed) # cut crossed edge

                current = self.get_next_cell(current,dirNum,2)
                if (current in self.visited): # end of path is reached
                    self.path = dict() # clear the path
                    break

## End Section Added by CaptainFlint ##
                
class Maze:
    '''Represents the maze the player is going through'''

    def __init__(self, width, blockSize, color):
        '''Maze(width,blockSize) -> Maze
        creates and randomly generates a maze with dimensions width x width
        and blocks blockSize in width
        width: int telling the num blocks in width. Must be an odd number
        blockSize: int telling the width of each block
        color: the color of the passage ways'''
        # initialize given info
        self.width = width
        self.blockSize = blockSize

        # coordinate grid
        self.coordGrid = [[0 for i in range(self.width)] for j in range(self.width)]

        for i in range(self.width):
            for j in range(self.width):
                self.coordGrid[i][j] = (self.blockSize*(self.width//2 - i),self.blockSize*(-self.width//2 + j))

        # initialize turtle for drawing
        self.t = turtle.Turtle()
        self.t.speed(0)
        self.t.ht()
        self.t.pu()
        self.t.color(color)
        self.t.shapesize(self.blockSize / 20)
        self.t.shape("square")

        # set up lists of blocks
        self.emptyBlocks = [self.coord_to_block(self.width * self.blockSize / 2 - self.blockSize,
            self.width * self.blockSize / 2 - self.blockSize),
            self.coord_to_block(self.width * self.blockSize / 2 - self.blockSize,
                self.width * self.blockSize / 2),
            self.coord_to_block(self.width * self.blockSize / 2 - self.blockSize,
                self.width * self.blockSize / 2 + self.blockSize)] # blocks player can go through with end blocks
        self.barriars = []                                     # blocks player can't go through

        # write end message and create maze
        self.generate_maze()
        self.t.goto(self.block_to_coord(self.emptyBlocks[-1]))
        self.t.sety(self.t.ycor() + self.blockSize)
        self.t.write(" End",False,"center",("Arial",self.blockSize + 4,"normal"))

    def block_to_coord(self,blockNum):
        '''Maze.block_to_coord(blockNum) -> tuple containing the x and y coordinates
        returns the corrisponding coordinate of a block
        if block not in maze, returns None
        blockNum: int'''
        width = self.width + 2 * (600 // (2 * self.blockSize)) + 4

        # if out of maze
        if blockNum == None:
            return None
        elif blockNum < -width ** 2 // 2 or blockNum > width ** 2 // 2:
            return

        blockNum += width ** 2 // 2 # bring up for computation
        x = (blockNum % width + 0.5 - width / 2) * self.blockSize
        y = (blockNum // width + 0.5 - width / 2) * self.blockSize
        return x,y  
            
    def coord_to_block(self,x,y):
        '''maze.coord_to_block(x,y) -> int that is the block number
        returns the block number that point (x,y) is in
        if point not in maze, returns None
        x,y: int'''
        width = self.width + 2 * (600 // (2 * self.blockSize)) + 4
                        
        # translate the coords into the first quadrant
        newX = x + width * self.blockSize / 2
        newY = y + width * self.blockSize / 2

        # not in maze
        if newX >= width * self.blockSize or newX < 0 or newY >= width * self.blockSize or newY < 0:
           return

        # output for in maze
        output = newX // self.blockSize + (newY // self.blockSize) * width - width ** 2 // 2
        return output

    def is_out(self,blockNum):
        '''Maze.is_out(blockNum,margin) -> boolean
        returns True if blockNum is out of the maze. Else returns False
        blockNum: int'''
        if blockNum == None: # out of board
            return True
        x,y = self.block_to_coord(blockNum)
        if x > (self.width + 2) * self.blockSize / 2 or x < -(self.width + 2) * self.blockSize / 2 or \
              y > (self.width + 3) * self.blockSize / 2 or y < -(self.width + 3) * self.blockSize / 2: # out of maze
            return True
        return False # in maze

    def get_empty_blocks(self):
        '''Maze.get_empty_blocks() -> list
        returns a list containing all empty blocks'''
        return self.emptyBlocks

    def get_block_size(self):
        '''Maze.get_block_size() -> int
        returns an int representing the size of the blocks'''
        return self.blockSize

    def get_width(self):
        '''Maze.get_width() -> int
        returns an int rperesenting the width of the board'''
        return self.width

    def get_barriars(self):
        '''Maze.get_width() -> int
        returns a list containing all the barriar numbers'''
        return self.barriars

    def generate_maze(self):
        '''Maze.generate_maze()
        generates a maze using width'''
        # write message
        self.t.write("Generating Maze",False,"center",("Arial",50,"italic"))

        mazeGen = WilsonMazeGenerator(self.width,self.width)
        mazeGen.generate_maze()
        grid = mazeGen.get_grid()

        for i in range(self.width):
            for j in range(self.width):
                if grid[i][j] == 1:
                    x,y = self.coordGrid[i][j]
                    self.emptyBlocks.append(self.coord_to_block(x,y))
                    
        # draw maze
        self.t.clear()
        self.emptyBlocks.sort()
        for block in self.emptyBlocks:
            self.t.goto(self.block_to_coord(block))
            self.t.stamp()


## COLORS ##
BKGRD = "black"
GRID  = "white"
TRACK = "red"

## SETUP ##
turtle.tracer(0)
wn = turtle.Screen()
wn.bgcolor(BKGRD)
wn.title("Maze")

# change this to change the size of the maze
# the width of the maze must be odd
maze = Maze(75,6,GRID)
player = Player(maze,TRACK)

wn.onkeypress(player.go_up,"Up")
wn.onkeypress(player.go_right,"Right")
wn.onkeypress(player.go_down,"Down")
wn.onkeypress(player.go_left,"Left")
wn.onkeypress(player.pen_control,"space")
wn.listen()
wn.mainloop()
