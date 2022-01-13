# Maze Game with Adventure World
# by G.G.Otto

import turtle
import random

class Player:
    '''Represents the player going through the maze'''

    def __init__(self, maze, color):
        '''Player(maze) -> Player
        creates the player for maze
        maze: Maze
        color: color string or tuple'''
        # get maze info
        self.blockSize = maze.get_block_size()
        self.width = maze.get_width()
        self.maze = maze
        self.barriars = maze.get_barriars()
        self.emptyBlocks = maze.get_empty_blocks() # get empty list
        
        # set up turtle
        self.color = color
        self.t = turtle.Turtle()
        self.t.pu()
        self.t.color(self.color)
        self.t.pensize(self.blockSize / 15)
        self.t.shapesize(self.blockSize / 50)
        self.t.seth(90)
        
        # put in start position
        start = self.maze.block_to_coord(
            self.maze.coord_to_block(-(self.width - 2) * self.blockSize / 2,-(self.width - 2) * self.blockSize / 2))
        self.t.goto(start)
        self.t.pd()

        # get screen info
        self.windowWidth = self.width * self.blockSize + 6200
        self.viewWidth = self.t.screen.window_width() - 40
        self.viewHeight = self.t.screen.window_height() - 90
        self.t.screen.screensize(self.windowWidth,self.windowWidth)
        self.canvas = self.t.screen.getcanvas()

        # get shape
        sh = turtle.Shape("compound")
        sh.addcomponent(((25.00,0.00), (23.10,9.57),
            (17.68,17.68), (9.57,23.10),(0.00,25.00),
            (-9.57,23.10), (-17.68,17.68), (-23.10,9.57),
            (-25.00,0.00), (-23.10,-9.57),(-17.68,-17.68),
            (-9.57,-23.10), (0.00,-25.00), (9.57,-23.10),
            (17.68,-17.68), (23.10,-9.57), (25.00,0.00)),color)
        screenWidth = self.t.screen.window_width()/2 + 25 # width of view screen
        sh.addcomponent(((self.windowWidth,self.windowWidth),
            (-self.windowWidth,self.windowWidth),(-self.windowWidth,-self.windowWidth),
            (self.windowWidth,-self.windowWidth),(self.windowWidth,self.windowWidth),
            (screenWidth,screenWidth),(screenWidth,-screenWidth),
            (-screenWidth,-screenWidth),(-screenWidth,screenWidth),
            (screenWidth,screenWidth)),self.maze.get_bg())
        turtle.register_shape("player",sh)
        self.t.shape("player")

        self.moving = False # tells if moving or not
        self.isWon = False  # tells if game is won

        # move screen
        self.t.screen.update()
        self.move_screen()
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
            # if passage out of board
            if passage == None:
                continue
            # if passage way in maze or not blocked area out of maze
            if passage in self.emptyBlocks or \
                 (maze.is_out(passage) and passage not in self.barriars):
                directions.append(index) 
        return directions

    def move_screen(self):
        '''Player.move_screen()
        moves the screen to the position of the player'''
        self.canvas.xview_moveto(
            (self.t.xcor() + self.windowWidth/2 - self.viewWidth/2)/self.windowWidth)
        self.canvas.yview_moveto(
            1 - (self.t.ycor() + self.windowWidth/2 + self.viewWidth/2)/self.windowWidth)
        
    def go_up(self):
        '''Player.go_up()
        moves the player up with screen'''
        if not self.moving and 0 in self.can_move():
            self.moving = True
            self.t.sety(self.t.ycor() + self.blockSize)
            self.move_screen()
            self.moving = False
            self.check_win()
            self.t.screen.update()

    def go_right(self):
        '''Player.got_right()
        moves the player to the right with screen'''
        if not self.moving and 1 in self.can_move():
            self.moving = True
            self.t.setx(self.t.xcor() + self.blockSize)
            self.move_screen()
            self.moving = False
            self.check_win()
            self.t.screen.update()

    def go_down(self):
        '''Player.go_down()
        moves the player down with screen'''
        if not self.moving and 2 in self.can_move():
            self.moving = True
            self.t.sety(self.t.ycor() - self.blockSize)
            self.move_screen()
            self.moving = False
            self.check_win()
            self.t.screen.update()

    def go_left(self):
        '''Player.go_left()
        moves the player to the left with screen'''
        if not self.moving and 3 in self.can_move():
            self.moving = True
            self.t.setx(self.t.xcor() - self.blockSize)
            self.move_screen()
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
            size = int(1.5 * self.blockSize)                              # font size
            self.t.color("yellow")
            
            self.moving = True
            self.t.goto(self.maze.block_to_coord(self.emptyBlocks[-1]))   # go to place for text
            self.t.sety(self.t.ycor() + 2 * self.blockSize)               # go up a little
            self.t.write("You win!",False,"center",("Arial",size,"bold")) # write message
            self.t.goto(x,y)
            self.moving = False
            
            self.t.color(self.color)
            self.isWon = True                                             # game is won

class Maze:
    '''Represents the maze the player is going through'''

    def __init__(self, width, blockSize, passageColor, bgColor):
        '''Maze(width,blockSize) -> Maze
        creates and randomly generates a maze with dimensions width x width
        and blocks blockSize in width
        width: int telling the num blocks in width. Must be an odd number
        blockSize: int telling the width of each block
        passageColor,bgColor: color string or tuple'''
        # initialize given info
        self.width = width
        self.blockSize = blockSize

        # initialize turtle for drawing
        self.t = turtle.Turtle()
        self.t.speed(0)
        self.t.ht()
        self.t.pu()
        self.t.shapesize(self.blockSize / 20)
        self.t.shape("square")
        self.t.color("white")          # color for text
        self.t.screen.bgcolor("black") # bgcolor is black for now
        # get colors
        self.passageColor = passageColor
        self.bgColor = bgColor
        
        # set up lists of blocks
        self.emptyBlocks = [self.coord_to_block(self.width * self.blockSize / 2 - 2 * self.blockSize,
                self.width * self.blockSize / 2 - self.blockSize),
            self.coord_to_block(self.width * self.blockSize / 2 - 2 * self.blockSize,
                self.width * self.blockSize / 2)] # blocks player can go through with end blocks
        self.blocksWithPassages = []                           # blocks to draw from                                   # blocks player can't go through

        # get adventure world
        self.adventureWorld = AdventureWorld(self)

        # write end message and create maze
        self.generate_maze()
        self.draw_board()
        self.t.goto(self.block_to_coord(self.emptyBlocks[-1]))
        self.t.sety(self.t.ycor() + self.blockSize)
        self.t.write(" End",False,"center",("Arial",self.blockSize + 4,"normal"))
        self.barriars = self.adventureWorld.get_barriars()
        self.t.screen.update()

    def block_to_coord(self,blockNum):
        '''Maze.block_to_coord(blockNum) -> tuple containing the x and y coordinates
        returns the corrisponding coordinate of a block
        if block not in maze, returns None
        blockNum: int'''
        width = self.width + 2 * (3000 // (2 * self.blockSize)) + 4

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
        width = self.width + 2 * (3000 // (2 * self.blockSize)) + 4
                        
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

    def get_end(self):
        '''Maze.get_end() -> x,y
        returns the x and y coordinates of the end block'''
        return self.block_to_coord(self.emptyBlocks[-1])

    def get_bg(self):
        '''Maze.get_bg()
        returns the bg color of the maze'''
        return self.bgColor

    def generate_maze(self):
        '''Maze.generate_maze()
        generates a maze using width'''
        # write message
        self.t.write("Generating Maze...",False,"center",("Arial",50,"italic"))
        self.t.screen.update()
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
        self.t.clear() # remove text
        self.t.screen.setup(450,450) # make screen smaller

    def draw_board(self):        
        # draw adventure world
        self.adventureWorld.draw_world()
    
        # draw background
        self.t.goto(self.width * self.blockSize / 2,self.width * self.blockSize / 2)
        self.t.fillcolor(self.bgColor) # get color for background
        self.t.seth(0)
        self.t.begin_fill()
        for i in range(4):
            self.t.right(90)
            self.t.fd(self.width * self.blockSize)
        self.t.end_fill()
        self.t.goto(0,0)
        self.t.color(self.passageColor)     # get color for passages
        self.t.fillcolor(self.passageColor) # make each block solid
        
        # draw maze
        self.t.st()
        self.t.undo()
        self.emptyBlocks.sort()
        for block in self.emptyBlocks:
            self.t.goto(self.block_to_coord(block))
            self.t.stamp()
        self.t.ht()
        
class AdventureWorld:
    '''Generates the outside adventure world'''

    def __init__(self,maze):
        '''AdventureWorld(maze) -> AdventureWorld
        constructs a adventure world for maze
        maze: Maze'''
        # get maze info
        self.blockSize = maze.get_block_size()
        self.width = maze.get_width()
        self.windowWidth = (self.width + 2 * (3000 // (2 * self.blockSize)) + 4) * self.blockSize
        self.maze = maze
        
        # set up turtle
        self.t = turtle.Turtle()
        self.t.ht()
        self.t.pu()
        self.t.shapesize(self.blockSize/20)
        self.t.shape("square")

        self.barriars = []

    def get_barriars(self):
        '''AdventureWorld.get_barriars() -> list
        returns a list of all barriars'''
        return self.barriars

    def get_block_in_direction(self,x,y,direction):
        '''AdventureWorld.get_block_in_direction(x,ydirection) -> x,y
        returns the coordinates of the block in the direction
        direction: int represeting direction (up: 0, right: 1, down: 2, left: 3)'''
        # create list of directions
        up = x,y + self.blockSize
        right = x + self.blockSize,y
        down = x,y - self.blockSize
        left = x - self.blockSize,y
        directionList = [up,right,down,left]

        return directionList[direction]

    def draw_rock(self,numBlocks,color,x,y):
        '''AdventureWorld.draw_rock(numBlocks,color,x,y)
        draws a rock at (x,y) and adds it to the barriars
        numBlocks: int representing the number of blocks in the rock
        color: string or color tuple for rock color'''
        if self.maze.coord_to_block(x,y) == None:
            return
        # first block
        blocksToDraw = [self.maze.block_to_coord(self.maze.coord_to_block(x,y))]

        # loop until rock is generated
        while len(blocksToDraw) != numBlocks:
            randomX,randomY = random.choice(blocksToDraw) # get random coords and unpack
            randomCoords = self.get_block_in_direction(randomX,randomY,
                    random.randint(0,3))
            if randomCoords not in blocksToDraw:          # if not in use
                blocksToDraw.append(randomCoords)         # add to rock
        
        # draw rock
        self.t.color(color)
        for blockPos in blocksToDraw:
            blockX,blockY = blockPos # unpack coords
            self.t.goto(blockX,blockY)
            self.t.stamp()
            # add to barriars
            if self.maze.coord_to_block(blockX,blockY) != None:
                self.barriars.append(self.maze.coord_to_block(blockX,blockY))

    def draw_tree(self,diameter,color,x,y):
        '''AdventureWorld.draw_tree(diameter,color,x,y)
        draws a tree at (x,y) with diameter (in blockNums)
        diameter: int
        color: string or color tuple'''
        # original position and color
        self.t.color(color)

        # get x,y coord
        if self.maze.coord_to_block(x,y) == None:
            return
        x,y = self.maze.block_to_coord(self.maze.coord_to_block(x,y))

        # loop through coords
        for i in range(-diameter//2,diameter//2+1):
            for j in range(-diameter//2,diameter//2+1):
                distance = (i**2 + j**2)**(1/2)
                if (diameter/2 - 0.5 <= distance <= diameter/2 - 0.1 and random.random() > 0.3) \
                   or distance < diameter/2 - 0.5:                                # if in radius
                    blockX,blockY = i * self.blockSize + x,j * self.blockSize + y
                    self.t.goto(blockX,blockY)                                    # get into position
                    self.t.stamp()
                    self.barriars.append(self.maze.coord_to_block(blockX,blockY)) # add to barriars

    def draw_ground_variance(self,diameter,color,x,y):
        '''AdventureWorld.draw_ground_variance(diamter,color,x,y)
        draws a type of circle on the ground at (x,y). Does not add to barriars
        diameter: int
        color: string or color tuple'''
        # original position and color
        self.t.color(color)

        if self.maze.coord_to_block(x,y) == None:
            return
        x,y = self.maze.block_to_coord(self.maze.coord_to_block(x,y))

        # loop through coords
        for i in range(-diameter//2,diameter//2+1):
            for j in range(-diameter//2,diameter//2+1):
                distance = (i**2 + j**2)**(1/2)
                if (diameter/2 - diameter//10 <= distance <= diameter/2 - diameter//25 and random.random() > 0.4) \
                   or distance < diameter/2 - diameter//10:                                # if in radius
                    blockX,blockY = i * self.blockSize + x,j * self.blockSize + y
                    self.t.goto(blockX,blockY)                                    # get into position
                    self.t.stamp()
        
    def draw_hill(self,diameter,height,x,y):
        '''AdventureWorld.draw_hill(diamter,height,color,x,y)
        draws a hill with height at (x,y)
        diameter: int
        height: int between -1 and 6'''
        if height < 0 or height > 5:
            raise ValueError("height must be between -1 and 6")
        color = 210
        levelDia = diameter # diameter for each level
        # loop through heights
        for i in range(height):
            self.draw_ground_variance(levelDia,(20,color,20),x,y)
            color += 10                    # lighter color
            levelDia -= diameter // height # bring level down

    def draw_flower(self,diamter,outColor,inColor,x,y):
        '''AdventureWorld.draw_flower(diamter,outColor,inColor,x,y)
        draws a flower with diamter at (x,y)
        diamter: int represeting the diamter of the flower
        outColor: string or color tuple for the petal color
        inColor: string or color tuple for the inside of the flower'''
        if self.maze.coord_to_block(x,y) == None:
            return
        # get into position
        self.t.goto(self.maze.block_to_coord(self.maze.coord_to_block(x,y)))
        # petals
        self.t.color(outColor)
        self.t.dot(self.blockSize * diamter)
        # inside
        self.t.color(inColor)
        self.t.dot(self.blockSize * diamter / 2.5)

    def draw_sand(self,diameter,x,y):
        '''AdventureWorld.draw_sand(diameter,color,x,y)
        draws a sand pit at (x,y)
        diameter: int'''
        # outer ring
        self.draw_ground_variance(diameter,(227,195,160),x,y)
        # middle ring
        if diameter > 3: 
            self.draw_ground_variance(diameter - 3,(231,185,150),x,y)
        # inner ring
        if diameter > 8:
            self.draw_ground_variance(diameter - 8,(233,178,148),x,y)
            
    def draw_pond(self,diameter,sandMargin,x,y):
        '''AdventureWorld.draw_pond(diameter,sandMargin,x,y)
        draws a pond at (x,y)
        diameter: int'''
        self.draw_sand(diameter + sandMargin,x,y) # bank
        self.draw_tree(diameter,"blue",x,y)                # water (using the tree method)

    def random_coord(self):
        '''AdventureWorld.random_coord() -> x,y
        returns random point (x,y)'''
        # get random coord
        x = random.randint(-self.windowWidth//2,self.windowWidth//2)
        y = random.randint(-self.windowWidth//2,self.windowWidth//2)
        blockNum = self.maze.coord_to_block(x,y)

        # get distance from the end
        endX,endY = self.maze.get_end()
        distanceFromEnd = ((x - endX) ** 2 + (y - endY) ** 2) ** (1/2)
        # loop until coord is correct
        while not self.maze.is_out(blockNum) or distanceFromEnd < (self.width // 10) * self.blockSize:
            x = random.randint(-self.windowWidth//2,self.windowWidth//2)
            y = random.randint(-self.windowWidth//2,self.windowWidth//2)
            blockNum = self.maze.coord_to_block(x,y)

            # get distance from the end
            endX,endY = self.maze.get_end()
            distanceFromEnd = ((x - endX) ** 2 + (y - endY) ** 2) ** (1/2)

        return x,y
    
    def draw_world(self):
        '''AdventureWorld.draw_world()
        draws the adventure world'''
        # background
        self.t.color(0,180,0)
        # hills and grass coloring
        for i in range(self.width // 7):
            x,y = self.random_coord()
            self.draw_hill(random.randint(15,35),random.randint(1,5),x,y)
        for i in range(self.width * 10):
            x,y = self.random_coord()
            self.t.goto(self.random_coord())
            self.t.stamp()
        # flowers
        for i in range(self.width * 7):
            outColor = random.choice(["red","blue","pink"])
            inColor = random.choice(["black","yellow"])
            x,y = self.random_coord()
            self.draw_flower(2/random.randint(3,6),outColor,inColor,x,y)
        # sand
        for i in range(self.width // 5):
            x,y = self.random_coord()
            self.draw_sand(random.randint(5,20),x,y)
        # trees
        for i in range(self.width * 3 // 2):
            x,y = self.random_coord()
            self.draw_tree(random.randrange(3,6,2),(0,random.randint(80,150),0),x,y)
        # rocks
        for i in range(self.width * 4 // 5):
            x,y = self.random_coord()
            color = random.randint(50,180)
            self.draw_rock(random.randint(1,50),(color,color,color),x,y)
        # pond
        for i in range(random.randint(0,self.width // 25)):
            x,y = self.random_coord()
            self.draw_pond(random.randint(8,20),random.randint(2,6),x,y)
        self.t.screen.bgcolor(0,200,0)
            
turtle.tracer(0)
turtle.colormode(255)
wn = turtle.Screen()
wn.title("Maze")

# get difficulty
userInput = int(wn.numinput("Difficulty","Hard (1), Medium (2), or Easy (3)?",2,1,3))
if userInput == 1:
    maze = Maze(101,50,(229,223,215),(75,57,34))
elif userInput == 2:
    maze = Maze(51,50,(229,223,215),(75,57,34))
else:
    maze = Maze(25,50,(229,223,215),(75,57,34))
player = Player(maze,'red')

wn.onkeypress(player.go_up,"Up")
wn.onkeypress(player.go_right,"Right")
wn.onkeypress(player.go_down,"Down")
wn.onkeypress(player.go_left,"Left")
wn.onkeypress(player.pen_control,"space")
wn.listen()

wn.mainloop()
