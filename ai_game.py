import pygame
import random
from enum import Enum
from collections import namedtuple
import time

# Constants
WHITE = (255, 255, 255)
RED = (200, 0, 0)
GREEN1 = (0, 255, 0)
GREEN2 = (0, 155, 0)
BLACK = (0, 0, 0)
BLOCK_SIZE = 20
SPEED = 200

Point = namedtuple('Point', 'x, y')

class Direction(Enum):
    RIGHT = 1
    LEFT = 2
    UP = 3
    DOWN = 4

class SnakeGameAI:

    def __init__(self, cycle, w=120, h=140):
        pygame.init()
        self.w = w #* BLOCK_SIZE  # Convert grid blocks to pixels
        self.h = h #* BLOCK_SIZE  # Convert grid blocks to pixels
        self.cycle = cycle
        self.cycle_index = 0
        self.display = pygame.display.set_mode((self.w, self.h))
        pygame.display.set_caption('Snake')
        self.clock = pygame.time.Clock()
        self.reset()

    def reset(self):
        # Adjust to start at the first position of the cycle
        start_pos = self.cycle[self.cycle_index]
        self.head = Point(start_pos[0] * BLOCK_SIZE, start_pos[1] * BLOCK_SIZE)
        self.snake = [self.head]
        self.score = 0
        self.food = None
        self._place_food()

        self.cycle_index = 1 # Start moving to the second point in the cycle next



    def _place_food(self):
        x = random.randint(0, (self.w-BLOCK_SIZE )//BLOCK_SIZE )*BLOCK_SIZE
        y = random.randint(0, (self.h-BLOCK_SIZE )//BLOCK_SIZE )*BLOCK_SIZE
        self.food = Point(x, y)
        if self.food in self.snake:
            if len(self.snake) == len(self.cycle):
                print("Snake Complete!")
                time.sleep(10)
                pygame.quit()
                quit()
            self._place_food()


    def play_step(self):
        if len(self.snake) == len(self.cycle):
            print("Snake Complete!")

        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                quit()
        
        # 2. move
        self._move() # update the head
        self.snake.insert(0, self.head)
        
        # 3. check if game over
        game_over = False
        if self.is_collision():
            game_over = True
            return game_over

        # 4. place new food or just move
        if self.head == self.food:
            self.score += 1
            self._place_food()
        else:
            self.snake.pop()
        
        # 5. update ui and clock
        self._update_ui()
        self.clock.tick(SPEED)


    def is_collision(self, pt=None):
        if pt is None:
            pt = self.head
        # hits boundary
        if pt.x > self.w - BLOCK_SIZE or pt.x < 0 or pt.y > self.h - BLOCK_SIZE or pt.y < 0:
            return True
        # hits itself
        if pt in self.snake[1:]:
            return True
        return False


    def _update_ui(self):
        self.display.fill(BLACK)

        for pt in self.snake:
            pygame.draw.rect(self.display, GREEN1, pygame.Rect(pt.x , pt.y, BLOCK_SIZE, BLOCK_SIZE))
            pygame.draw.rect(self.display, GREEN2, pygame.Rect(pt.x+4, pt.y+4, 12, 12))

        pygame.draw.rect(self.display, RED, pygame.Rect(self.food.x, self.food.y, BLOCK_SIZE, BLOCK_SIZE))

        # font = pygame.font.SysFont('times new roman', 50)
        # text = font.render("Score: " + str(self.score), True, WHITE)
        
        # self.display.blit(text, [0, 0])
        pygame.display.flip()


    def _move(self):
        legal_moves = self.allLegalMoves()

        if self.cycle_index >= len(self.cycle):
            self.cycle_index = 0  # Loop back to the start of the cycle.
        next_cycle_point = self.cycle[self.cycle_index]
        self.head = Point(next_cycle_point[0] * BLOCK_SIZE, next_cycle_point[1] * BLOCK_SIZE)
        self.cycle_index += 1

        if self.is_collision(self.head):
            print("Collision would be found here: Checking legal moves")
            self.head = random.choice(legal_moves)
            if self.head:
                print("Move Successful")
            else:
                time.sleep(100)
        
        # if len(self.snake) < len(self.cycle) * 0.3 : #If the snake is less than 75% of the grid, use Shortcuts
        #     #Check if Legal and Safe Moves are able to be made
        #     if legal_moves:
        #         best_move = self.rankLegalMoves(legal_moves)
        #         if best_move:
        #             best_move_index = self.cycle.index((best_move.x // BLOCK_SIZE, best_move.y // BLOCK_SIZE))
        #             head_index = self.cycle.index((self.head.x // BLOCK_SIZE, self.head.y // BLOCK_SIZE))
        #             food_index = self.cycle.index((self.food.x // BLOCK_SIZE, self.food.y // BLOCK_SIZE))
        #             skip_dist1 = self.calculateSkipDistance(head_index, food_index)
        #             skip_dist2 = self.calculateSkipDistance(best_move_index, food_index)
        #             if skip_dist2 < skip_dist1:
        #                 self.head = best_move
        #                 self.cycle_index = self.cycle.index((best_move.x // BLOCK_SIZE, best_move.y // BLOCK_SIZE))
        #                 if self.is_collision(self.head):
        #                     print("Collision Found via best move")
            

    
    def _move_with_only_cycle(self):
        #Move the snake's head to the next point in the cycle
        if self.cycle_index >= len(self.cycle):
            self.cycle_index = 0  # Loop back to the start of the cycle
        next_point = self.cycle[self.cycle_index]
        self.head = Point(next_point[0] * BLOCK_SIZE, next_point[1] * BLOCK_SIZE)
        self.cycle_index += 1

    def calculateSkipDistance(self, move_index, food_index):
        skip_dist = food_index - move_index
        if skip_dist < 0:
            skip_dist = len(self.cycle) - abs(skip_dist)
        return skip_dist

    def allLegalMoves(self):
        moves = []
        # Directions based on grid coordinates, not pixels
        for direction in [Direction.RIGHT, Direction.LEFT, Direction.UP, Direction.DOWN]:
            if direction == Direction.RIGHT:
                new_point = Point(self.head.x + BLOCK_SIZE, self.head.y)
            elif direction == Direction.LEFT:
                new_point = Point(self.head.x - BLOCK_SIZE, self.head.y)
            elif direction == Direction.UP:
                new_point = Point(self.head.x, self.head.y - BLOCK_SIZE)
            elif direction == Direction.DOWN:
                new_point = Point(self.head.x, self.head.y + BLOCK_SIZE)
            
            if not self.is_collision(new_point):
                moves.append(new_point)
        return moves
    
    def rankLegalMoves(self, moves):
        #Use Manhattan Distance to rank the moves
        current_best = [float('inf'), None]
        for move in moves:
            if self.isOrderedAfterMove(move) and move not in self.snake:
                move_index = self.cycle.index((move.x // BLOCK_SIZE, move.y // BLOCK_SIZE))
                food_index = self.cycle.index((self.food.x // BLOCK_SIZE, self.food.y // BLOCK_SIZE))
                skip_dist = self.calculateSkipDistance(move_index, food_index)
                if skip_dist < current_best[0]:
                    current_best = [skip_dist, move]
        return current_best[1]
    
    def isOrderedAfterMove(self, potential_move):
        # Simulate the move
        simulated_snake = self.snake[:-1] # Create a copy of the snake
        simulated_snake.insert(0, potential_move) # Simulate adding the new head
        head_index = self.cycle.index((potential_move.x // BLOCK_SIZE, potential_move.y // BLOCK_SIZE))
        tail_index = self.cycle.index((simulated_snake[-1].x // BLOCK_SIZE, simulated_snake[-1].y // BLOCK_SIZE))



        if head_index > tail_index:
            for i in range(0, tail_index):
                if self.cycle[i] in self.snake:

                    return False
            for i in range(head_index + 1, len(self.cycle)):
                if self.cycle[i] in self.snake:
                
                    return False
        # If the tail has overtaken the head, check that no snake segments appear between the head and the tail.
        else:
            for i in range(head_index + 1, tail_index):
                if self.cycle[i] in self.snake:

                    return False
        return True


