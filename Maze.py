import turtle
import random
import time

class Player:
    '''Represents the player going through the maze'''

    def __init__(self, maze):
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
        self.t = turtle.Turtle()
        self.t.pu()
        self.t.shape("circle")
        self.t.color("red")
        self.t.pensize(self.blockSize / 15)
        self.t.shapesize(self.blockSize / 20)
        self.t.seth(90)

        # put in start position
        start = self.maze.block_to_coord(
            self.maze.coord_to_block(-(self.width - 2) * self.blockSize / 2,-(self.width - 2) * self.blockSize / 2))
        self.t.goto(start)
        self.t.pd()

        # get screen info
        self.t.screen.screensize(self.width * self.blockSize + 600,
            self.width * self.blockSize + 600)
        self.windowWidth, self.windowHeight = self.t.screen.screensize()
        self.canvas = self.t.screen.getcanvas()
        
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
            # move with screen
            for i in range(self.blockSize):
                self.t.sety(self.t.ycor() + 1)
                self.canvas.xview_moveto((self.t.xcor() + self.windowWidth/2 - 300) / self.windowWidth)
                self.canvas.yview_moveto(1 - (self.t.ycor() + self.windowHeight/2 + 300) / self.windowHeight)
                self.t.screen.update()
            self.moving = False
            self.check_win()
            self.t.screen.update()

    def go_right(self):
        '''Player.got_right()
        moves the player to the right'''
        if not self.moving and 1 in self.can_move():
            self.moving = True
            # move with screen
            for i in range(self.blockSize):
                self.t.setx(self.t.xcor() + 1)
                self.canvas.xview_moveto((self.t.xcor() + self.windowWidth/2 - 300) / self.windowWidth)
                self.canvas.yview_moveto(1 - (self.t.ycor() + self.windowHeight/2 + 300) / self.windowHeight)
                self.t.screen.update()
            self.moving = False
            self.check_win()
            self.t.screen.update()

    def go_down(self):
        '''Player.go_down()
        moves the player down'''
        if not self.moving and 2 in self.can_move():
            self.moving = True
            # move with screen
            for i in range(self.blockSize):
                self.t.sety(self.t.ycor() - 1)
                self.canvas.xview_moveto((self.t.xcor() + self.windowWidth/2 - 300) / self.windowWidth)
                self.canvas.yview_moveto(1 - (self.t.ycor() + self.windowHeight/2 + 300) / self.windowHeight)
                self.t.screen.update()
            self.moving = False
            self.check_win()
            self.t.screen.update()

    def go_left(self):
        '''Player.go_left()
        moves the player to the left'''
        if not self.moving and 3 in self.can_move():
            self.moving = True
            # move with screen
            for i in range(self.blockSize):
                self.t.setx(self.t.xcor() - 1)
                self.canvas.xview_moveto((self.t.xcor() + self.windowWidth/2 - 300) / self.windowWidth)
                self.canvas.yview_moveto(1 - (self.t.ycor() + self.windowHeight/2 + 300) / self.windowHeight)
                self.t.screen.update()
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
            
            self.t.color("red")
            self.isWon = True                                             # game is won

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

        # initialize turtle for drawing
        self.t = turtle.Turtle()
        self.t.speed(0)
        self.t.ht()
        self.t.pu()
        self.t.color(color)
        self.t.shapesize(self.blockSize / 20)
        self.t.shape("square")

        # set up lists of blocks
        self.emptyBlocks = [self.coord_to_block(self.width * self.blockSize / 2 - 2 * self.blockSize,
            self.width * self.blockSize / 2 - self.blockSize)] # blocks player can go through with end blocks
        self.blocksWithPassages = []                           # blocks to draw from
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
        '''Maze.is_out(blockNum) -> boolean
        returns True if blockNum is out of the maze. Else returns False
        blockNum: int'''
        if blockNum == None: # out of board
            return True
        x,y = self.block_to_coord(blockNum)
        if x > (self.width) * self.blockSize / 2 or x < -(self.width) * self.blockSize / 2 or \
              y > (self.width) * self.blockSize / 2 or y < -(self.width) * self.blockSize / 2: # out of maze
            return True
        return False # in maze

    def check_passage(self,blockNumList):
        '''Maze.check_passage(blockNumList) -> boolean
        returns True if the block numbers in blockNumList make a valid passage. Else returns False
        blockNumList: list'''
        for blockNum in blockNumList:
            if self.is_out(blockNum) or blockNum in self.emptyBlocks:
                return False
        return True
    
    def check_passages(self,blockNum):
        '''Maze.check_passages(blockNum) -> list all passages from blockNum
        blockNum: int'''
        blockX,blockY = self.block_to_coord(blockNum) # get the coords of blockNum
        availablePassages = [] # initialize availablePassages

        # get passages
        up = [self.coord_to_block(blockX,blockY + self.blockSize),
           self.coord_to_block(blockX,blockY + 2 * self.blockSize)]
        right = [self.coord_to_block(blockX + self.blockSize,blockY),
           self.coord_to_block(blockX + 2 * self.blockSize,blockY)]
        left = [self.coord_to_block(blockX,blockY - self.blockSize),
           self.coord_to_block(blockX,blockY - 2 * self.blockSize)]
        down = [self.coord_to_block(blockX - self.blockSize,blockY),
           self.coord_to_block(blockX - 2 * self.blockSize,blockY)]
        
        # loop through passages
        for passage in [up,right,left,down]:
            if self.check_passage(passage):
                availablePassages.append(passage)
        return availablePassages

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
        # find first block
        randomX = random.randrange(0,self.width - 2,2) * self.blockSize # get random x-cor
        randomY = random.randrange(0,self.width - 2,2) * self.blockSize # get random y-cor
        startBlock = self.coord_to_block(-self.width * self.blockSize / 2 + self.blockSize + randomX,
             -self.width * self.blockSize / 2 + self.blockSize + randomY)
        self.emptyBlocks.append(startBlock)
        self.blocksWithPassages.append(startBlock)

        # loop until maze is done
        while len(self.blocksWithPassages) != 0:
            # generate maze
            randomBlock = random.choice(self.blocksWithPassages)
            randomPassage = random.choice(self.check_passages(randomBlock))
            for blockToDraw in randomPassage:
                self.emptyBlocks.append(blockToDraw)

            # add new position to list
            self.blocksWithPassages.append(blockToDraw)

            # get block coords
            blockX,blockY = self.block_to_coord(blockToDraw) 
            # remove used blocks from list
            for x in (blockX - 2 * self.blockSize,
                      blockX, blockX + 2 * self.blockSize):
                for y in (blockY - 2 * self.blockSize,
                      blockY, blockY + 2 * self.blockSize):
                    block = self.coord_to_block(x,y)
                    if len(self.check_passages(block)) == 0 and block in self.blocksWithPassages:
                        self.blocksWithPassages.remove(block)
                    
        # draw maze
        self.t.clear()
        self.emptyBlocks.sort()
        for block in self.emptyBlocks:
            self.t.goto(self.block_to_coord(block))
            self.t.stamp()
            
turtle.tracer(0)
wn = turtle.Screen()
wn.bgcolor('black')
wn.title("Maze")

# change this to change the size of the maze
# the width of the maze must be odd
maze = Maze(101,40,'white')
player = Player(maze)

wn.onkeypress(player.go_up,"Up")
wn.onkeypress(player.go_right,"Right")
wn.onkeypress(player.go_down,"Down")
wn.onkeypress(player.go_left,"Left")
wn.onkeypress(player.pen_control,"space")
wn.listen()


    

