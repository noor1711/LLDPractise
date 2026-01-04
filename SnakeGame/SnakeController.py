from typing import List, Tuple, Optional
from dataclasses import dataclass
from abc import ABC, abstractmethod
import math
import time
import threading
from enum import Enum
from random import random

# Constants
class GameConfig:
    DEFAULT_GRID_SIZE = 10
    INITIAL_ROW = 5
    INITIAL_COL = 5
    MOVE_INTERVAL = 1.0
    FOOD_SPAWN_INTERVAL = 3.0
    MAX_FOOD_PLACEMENT_ATTEMPTS = 100

# Enums
class BlockEnum(Enum):
    EMPTY = 1
    SNAKE = 2
    FOOD = 3

class DirectionEnum(Enum):
    LEFT = 1
    RIGHT = 2
    UP = 3
    DOWN = 4

class GameState(Enum):
    PLAYING = 1
    PAUSED = 2
    GAME_OVER = 3

# Block class
class Block:
    def __init__(self, row: int, col: int):
        self._type = BlockEnum.EMPTY
        self.row = row
        self.col = col
    
    def makeEmpty(self):
        self._type = BlockEnum.EMPTY
    
    def addFood(self):
        self._type = BlockEnum.FOOD
    
    def addSnake(self):
        self._type = BlockEnum.SNAKE
    
    def hasFood(self) -> bool:
        return self._type == BlockEnum.FOOD
    
    def hasSnake(self) -> bool:
        return self._type == BlockEnum.SNAKE
    
    def isEmpty(self) -> bool:
        return self._type == BlockEnum.EMPTY
    
    def eatFood(self):
        if self._type == BlockEnum.FOOD:
            self._type = BlockEnum.SNAKE

# Immutable state for Snake
@dataclass(frozen=True)
class SnakeState:
    """Immutable snapshot of snake state for collision detection"""
    head_position: Tuple[int, int]
    direction: DirectionEnum
    body_positions: Tuple[Tuple[int, int], ...]
    length: int

# Grid - Only responsible for data storage
class Grid:
    def __init__(self, n: int):
        if n <= 0:
            raise ValueError("Grid size must be positive")
        self._size = n
        self._grid = [[Block(row, col) for col in range(n)] for row in range(n)]
    
    def getBlock(self, row: int, col: int) -> Block:
        if not (0 <= row < self._size and 0 <= col < self._size):
            raise IndexError(f"Position ({row}, {col}) out of bounds")
        return self._grid[row][col]
    
    def getSize(self) -> int:
        return self._size
    
    def getAllBlocks(self) -> List[List[Block]]:
        """Returns grid for iteration (read-only access)"""
        return self._grid

# GridNavigator - Only responsible for navigation logic
class GridNavigator:
    def __init__(self, grid: Grid):
        self._grid = grid
    
    def getLeft(self, row: int, col: int) -> Block:
        if col - 1 >= 0:
            return self._grid.getBlock(row, col - 1)
        return self._grid.getBlock(row, self._grid.getSize() - 1)  # Wrap around
    
    def getRight(self, row: int, col: int) -> Block:
        if col + 1 < self._grid.getSize():
            return self._grid.getBlock(row, col + 1)
        return self._grid.getBlock(row, 0)
    
    def getUp(self, row: int, col: int) -> Block:
        if row - 1 >= 0:
            return self._grid.getBlock(row - 1, col)
        return self._grid.getBlock(self._grid.getSize() - 1, col)
    
    def getDown(self, row: int, col: int) -> Block:
        if row + 1 < self._grid.getSize():
            return self._grid.getBlock(row + 1, col)
        return self._grid.getBlock(0, col)
    
    def getNextBlock(self, row: int, col: int, direction: DirectionEnum) -> Block:
        if direction == DirectionEnum.UP:
            return self.getUp(row, col)
        elif direction == DirectionEnum.DOWN:
            return self.getDown(row, col)
        elif direction == DirectionEnum.LEFT:
            return self.getLeft(row, col)
        else:  # RIGHT
            return self.getRight(row, col)

# GridRenderer - Only responsible for rendering
class GridRenderer:
    def __init__(self, grid: Grid):
        self._grid = grid
    
    def render(self):
        for row in self._grid.getAllBlocks():
            for block in row:
                toPrint = "*" if block.isEmpty() else "S" if block.hasSnake() else "F"
                print(toPrint, end=" ")
            print()
        print("------------------------")

# FoodPlacer - Only responsible for food placement logic
class FoodPlacer:
    def __init__(self, grid: Grid):
        self._grid = grid
    
    def placeFood(self) -> bool:
        """Places food on an empty block. Returns True if successful."""
        for _ in range(GameConfig.MAX_FOOD_PLACEMENT_ATTEMPTS):
            row = math.floor(random() * self._grid.getSize())
            col = math.floor(random() * self._grid.getSize())
            block = self._grid.getBlock(row, col)
            if block.isEmpty():
                block.addFood()
                return True
        return False  # Grid is full

# Snake - Properly encapsulated with public interface
class Snake:
    def __init__(self, block: Block):
        self._head = block
        self._tail = block
        block.addSnake()
        self._length = 1
        self._blocks: List[Block] = []
        self._direction = DirectionEnum.LEFT
    
    def getState(self) -> SnakeState:
        """Returns immutable state snapshot for collision detection"""
        return SnakeState(
            head_position=(self._head.row, self._head.col),
            direction=self._direction,
            body_positions=tuple((b.row, b.col) for b in self._blocks),
            length=self._length
        )
    
    def turn(self, direction: DirectionEnum):
        """Changes direction with validation to prevent opposite direction"""
        opposite_directions = {
            DirectionEnum.LEFT: DirectionEnum.RIGHT,
            DirectionEnum.RIGHT: DirectionEnum.LEFT,
            DirectionEnum.UP: DirectionEnum.DOWN,
            DirectionEnum.DOWN: DirectionEnum.UP
        }
        if direction != opposite_directions.get(self._direction):
            self._direction = direction
    
    def getLength(self) -> int:
        return self._length
    
    # Internal methods for SnakeMover (friend class pattern)
    def _getNextHeadPosition(self, navigator: GridNavigator) -> Block:
        """Internal method for getting next head position"""
        return navigator.getNextBlock(
            self._head.row,
            self._head.col,
            self._direction
        )
    
    def _moveTo(self, newHeadBlock: Block, isEatingFood: bool):
        """Internal method to update snake position"""
        if isEatingFood:
            newHeadBlock.eatFood()
            self._length += 1
            self._blocks.insert(0, self._head)
        else:
            if self._blocks:
                tailBlock = self._blocks.pop()
                tailBlock.makeEmpty()
                self._blocks.insert(0, self._head)
            else:
                self._head.makeEmpty()
        
        newHeadBlock.addSnake()
        self._head = newHeadBlock
        
        if self._blocks:
            self._tail = self._blocks[-1]
        else:
            self._tail = self._head

# CollisionDetector - Only responsible for collision detection
class CollisionDetector:
    def __init__(self, navigator: GridNavigator):
        self._navigator = navigator
    
    def willCollide(self, snake_state: SnakeState, grid: Grid) -> bool:
        """Checks if snake will collide with itself at next position"""
        nextBlock = self._navigator.getNextBlock(
            snake_state.head_position[0],
            snake_state.head_position[1],
            snake_state.direction
        )
        return nextBlock.hasSnake()

# SnakeMover - Only responsible for movement logic
class SnakeMover:
    def __init__(self, navigator: GridNavigator):
        self._navigator = navigator
    
    def move(self, snake: Snake, grid: Grid):
        """Moves snake forward, handling food consumption"""
        newHeadBlock = snake._getNextHeadPosition(self._navigator)
        isEatingFood = newHeadBlock.hasFood()
        snake._moveTo(newHeadBlock, isEatingFood)

# InputHandler - Only responsible for input processing
class InputHandler:
    def __init__(self):
        self._key_mapping = {
            "w": DirectionEnum.UP,
            "a": DirectionEnum.LEFT,
            "s": DirectionEnum.DOWN,
            "d": DirectionEnum.RIGHT
        }
    
    def parseInput(self, input_str: str) -> Optional[DirectionEnum]:
        """Parses input string to direction. Returns None if invalid."""
        return self._key_mapping.get(input_str.strip().lower())

# GameEngine - Only responsible for game rules and state transitions
class GameEngine:
    def __init__(self, snake: Snake, grid: Grid, navigator: GridNavigator):
        self._snake = snake
        self._grid = grid
        self._navigator = navigator
        self._collision_detector = CollisionDetector(navigator)
        self._snake_mover = SnakeMover(navigator)
        self._score = 0
        self._state = GameState.PLAYING
    
    def canMove(self) -> bool:
        """Checks if snake can move without collision"""
        if self._state != GameState.PLAYING:
            return False
        snake_state = self._snake.getState()
        return not self._collision_detector.willCollide(snake_state, self._grid)
    
    def update(self) -> bool:
        """Updates game state. Returns False if game over."""
        if not self.canMove():
            self._state = GameState.GAME_OVER
            return False
        
        snake_state = self._snake.getState()
        nextBlock = self._navigator.getNextBlock(
            snake_state.head_position[0],
            snake_state.head_position[1],
            snake_state.direction
        )
        
        if nextBlock.hasFood():
            self._score += 1
        
        self._snake_mover.move(self._snake, self._grid)
        return True
    
    def getScore(self) -> int:
        return self._score
    
    def getState(self) -> GameState:
        return self._state
    
    def getSnake(self) -> Snake:
        return self._snake

# Thread classes
class KeyboardThread(threading.Thread):
    def __init__(self, callback, name: str):
        self._callback = callback
        self._running = True
        super(KeyboardThread, self).__init__(name=name, daemon=True)
        self.start()
    
    def run(self):
        try:
            while self._running:
                try:
                    user_input = input()
                    if user_input:
                        self._callback(user_input)
                except EOFError:
                    break
        except Exception as e:
            print(f"Input error: {e}")

class GameThread(threading.Thread):
    def __init__(self, callback, name: str, interval: float):
        self._callback = callback
        self._interval = interval
        self._running = True
        super(GameThread, self).__init__(name=name, daemon=True)
        self.start()
    
    def run(self):
        while self._running:
            time.sleep(self._interval)
            self._callback()

# GameController - Only responsible for orchestrating components
class GameController:
    def __init__(self, grid_size: int = GameConfig.DEFAULT_GRID_SIZE):
        # Initialize core components
        self._grid = Grid(grid_size)
        self._navigator = GridNavigator(self._grid)
        self._renderer = GridRenderer(self._grid)
        self._food_placer = FoodPlacer(self._grid)
        self._input_handler = InputHandler()
        
        # Initialize game entities
        initial_block = self._grid.getBlock(
            GameConfig.INITIAL_ROW,
            GameConfig.INITIAL_COL
        )
        self._snake = Snake(initial_block)
        
        # Initialize game engine
        self._game_engine = GameEngine(
            self._snake,
            self._grid,
            self._navigator
        )
        
        # Thread synchronization
        self._lock = threading.Lock()
        
        # Initialize threads
        self._keyboard_thread = KeyboardThread(
            self._handleInput,
            "keyboard-thread"
        )
        self._food_thread = GameThread(
            self._addFood,
            "food-thread",
            GameConfig.FOOD_SPAWN_INTERVAL
        )
    
    def _handleInput(self, input_str: str):
        """Handles input from keyboard thread"""
        direction = self._input_handler.parseInput(input_str)
        if direction:
            with self._lock:
                self._snake.turn(direction)
    
    def _addFood(self):
        """Adds food to grid (called by food thread)"""
        with self._lock:
            self._food_placer.placeFood()
    
    def _getNextState(self) -> bool:
        """Updates game state. Returns False if game over."""
        with self._lock:
            return self._game_engine.update()
    
    def _printState(self):
        """Renders current game state"""
        with self._lock:
            self._renderer.render()
    
    def runGameLoop(self):
        """Main game loop"""
        while True:
            if not self._getNextState():
                print(f"Game Over! Score: {self._game_engine.getScore()}")
                break
            self._printState()
            time.sleep(GameConfig.MOVE_INTERVAL)

if __name__ == "__main__":
    controller = GameController(10)
    controller.runGameLoop()
