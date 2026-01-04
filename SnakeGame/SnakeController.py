from typing import List
import math
import time
import threading
from enum import Enum
from random import random

N = 10

class BlockEnum(Enum):
    EMPTY=1
    SNAKE=2
    FOOD=3

# Block clss
class Block:
    def __init__(self, row, col):
        self.type = BlockEnum.EMPTY
        self.row = row
        self.col = col
    
    def makeEmpty(self):
        self.type = BlockEnum.EMPTY

    def addFood(self):
        self.type = BlockEnum.FOOD
    
    def addSnake(self):
        self.type = BlockEnum.SNAKE
    
    def hasFood(self):
        return self.type == BlockEnum.FOOD
    
    def hasSnake(self):
        return self.type == BlockEnum.SNAKE

    def isEmpty(self):
        return self.type == BlockEnum.EMPTY

    def eatFood(self):
        if self.type == BlockEnum.FOOD:
            self.type = BlockEnum.SNAKE


class Grid:

    def __init__(self, n):
        self.n = n
        self.grid = [[Block(row, col) for col in range(n)] for row in range(n)]
    
    def printGrid(self):
        for row in self.grid:
            for block in row:
                toPrint = "*" if block.isEmpty() else "S" if block.hasSnake() else "F"
                print(toPrint, end=" ")
            print()
        print("------------------------")

    def getBlock(self, row, col):
        return self.grid[row][col]
    
    def getLeft(self, row, col):
        if col - 1 >= 0:
            return self.grid[row][col - 1]
        return self.grid[row][-1]

    def getRight(self, row, col):
        if col + 1 < self.n:
            return self.grid[row][col + 1]
        return self.grid[row][0]
    
    def getUp(self, row, col):
        if row - 1 >= 0:
            return self.grid[row - 1][col]
        return self.grid[-1][col]

    def getDown(self, row, col):
        if row + 1 < self.n:
            return self.grid[row + 1][col]
        return self.grid[0][col]

    def getNextBlock(self, row, col, direction):
        if direction == DirectionEnum.UP:
            return self.getUp(row, col)
        elif direction == DirectionEnum.DOWN:
            return self.getDown(row, col)
        elif direction == DirectionEnum.LEFT:
            return self.getLeft(row, col)
        else:
            return self.getRight(row, col)

    def getRandomBlock(self):
        row = math.floor(random() * self.n)
        col = math.floor(random() * self.n)
        return self.getBlock(row, col)

class DirectionEnum(Enum):
    LEFT=1
    RIGHT=2
    UP=3
    DOWN=4

class Snake:

    def __init__(self, block: Block) -> None:
        self.head = block
        self.tail = block
        block.addSnake()
        self.length = 1
        self.blocks: List[Block] = []
        self.direction = DirectionEnum.LEFT
    
    def findTailBlocks(self, GRID):
        newTailBlock = None
        if self.direction == DirectionEnum.LEFT:
            newTailBlock = GRID.getRight(self.tail.row, self.tail.col)
        elif self.direction == DirectionEnum.RIGHT:
            newTailBlock = GRID.getLeft(self.tail.row, self.tail.col)
        elif self.direction == DirectionEnum.UP:
            newTailBlock = GRID.getDown(self.tail.row, self.tail.col)
        else:
            newTailBlock = GRID.getUp(self.tail.row, self.tail.col)

        return newTailBlock

    def turn(self, direction):
        self.direction = direction
    
    def eatFood(self, grid: Grid):
        if not self.head.hasFood():
            return 
        
        self.length += 1
        # we need to add num blocks to the tail
        self.tail = self.findTailBlocks(grid)
        self.tail.addSnake()
        self.blocks.append(self.tail)
    
    def checkIsSnakeValid(self, grid: Grid):
        # lets find if new head collides with any part of the snake
        newBlock: Block = grid.getNextBlock(self.head.row, self.head.col, self.direction)

        return not newBlock.hasSnake()
    
    def moveForward(self, grid: Grid):
        # Get the next block for the head
        newHeadBlock: Block = grid.getNextBlock(self.head.row, self.head.col, self.direction)
        
        # Check if we're eating food at the new head position
        isEatingFood = newHeadBlock.hasFood()
        
        if isEatingFood:
            # Eating food - snake grows
            newHeadBlock.eatFood()  # Convert food to snake
            self.length += 1
            # Add the old head to the body (snake grows by one segment)
            self.blocks.insert(0, self.head)
        else:
            # Not eating food - move normally
            if self.blocks:
                # Remove the tail (last block in body)
                tailBlock = self.blocks.pop()
                tailBlock.makeEmpty()
                # Add old head to body
                self.blocks.insert(0, self.head)
            else:
                # No body yet, just clear the old head position
                self.head.makeEmpty()
        
        # Move head to new position
        newHeadBlock.addSnake()
        self.head = newHeadBlock
        
        # Update tail reference
        if self.blocks:
            self.tail = self.blocks[-1]
        else:
            self.tail = self.head

class KeyboardThread(threading.Thread):
    def __init__(self, callback, name):
        self.callback = callback
        super(KeyboardThread, self).__init__(name=name, daemon=True)
        self.start()
    
    def run(self):
        while True:
            self.callback(input())

class GameThread(threading.Thread):
    def __init__(self, callback, name):
        self.callback = callback
        super(GameThread, self).__init__(name=name, daemon=True)
        self.start()
    
    def run(self):
        while True:
            time.sleep(3)
            self.callback()

class Controller:
    def __init__(self, n):
        self.grid = Grid(n)
        self.snake = Snake(self.grid.getBlock(5, 5))
        self.keyboardThread = KeyboardThread(self.getInput, "keyboard-thread")
        self.foodThread = GameThread(self.addFood, "food-thread")
        
    def getInput(self, input):
        # w - up
        # a - left
        # s - right
        # z - down
        print("INPUT IS", input)
        if input == "w":
            self.snake.turn(DirectionEnum.UP)
        elif input == "a":
            self.snake.turn(DirectionEnum.LEFT)
        elif input == "d":
            self.snake.turn(DirectionEnum.RIGHT)
        elif input == "s":
            self.snake.turn(DirectionEnum.DOWN)       

    def getNextState(self):
        if not self.snake.checkIsSnakeValid(self.grid):
            return False
        self.snake.moveForward(self.grid)
        return True

    def addFood(self):
        # set it on a random row, col
        block = self.grid.getRandomBlock()
        block.addFood()

    def printState(self):
        self.grid.printGrid()

if __name__ == "__main__":
    controller = Controller(10)
    
    while True:
        if not controller.getNextState():
            break
        controller.printState()
        time.sleep(1)
    