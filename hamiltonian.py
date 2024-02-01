import matplotlib.pyplot as plt
import numpy as np


BLOCK_SIZE = 20

class Hamiltonian:

    def __init__(self, width=120, height=140):
        self.w = int(width / BLOCK_SIZE)
        self.h = int(height / BLOCK_SIZE)
        self.graph = self.createGraph()
        self.visited = [[False for _ in range(self.h)] for _ in range(self.w)]
        self.path = []

    def getTotal(self):
        return self.w * self.h
    
    def createGraph(self):
        start = []
        for i in range(self.w):
            current = [1 for _ in range(self.h)]
            start.append(current)
        return start
    
    #Checks if valid move
    def isSafe(self, x, y):
        return 0 <= x < self.w and 0 <= y < self.h and self.graph[x][y] == 1 and not self.visited[x][y]
    
    #The Backtracking Algorithm
    def calculateHamiltonianCycleUtil(self, x, y, steps):
        # Base Case - If we have visited every single square and check if we can return to the start
        if steps == self.getTotal():
            # Check if the last cell is adjacent to the start cell (0, 0) to form a cycle
            for dx, dy in [(0, -1), (-1, 0), (0, 1), (1, 0)]:  # Directions to check
                if (x + dx, y + dy) == (0, 0):
                    return True
            return False  # Return to start is not possible, not a cycle

        # Recursive Case Depth First Search
        for dx, dy in [(0, -1), (-1, 0), (0, 1), (1, 0)]:  # Left, Up, Right, Down
            next_x, next_y = x + dx, y + dy
            if self.isSafe(next_x, next_y):
                self.visited[next_x][next_y] = True
                self.path.append((next_x, next_y))

                if self.calculateHamiltonianCycleUtil(next_x, next_y, steps + 1):
                    return True

                # Backtrack
                self.visited[next_x][next_y] = False
                self.path.pop()

        return False
    
    def calculateHamiltonianCycle(self):
        # Initialize the starting point and visited matrix
        self.visited[0][0] = True
        self.path.append((0, 0))
        
        if self.calculateHamiltonianCycleUtil(0, 0, 1):
            self.writeCycleToFile(self.path)
            return self.path
        else:
            return None
        
    def cycleExists(self, new_cycle):
        try:
            with open("hamcycles.txt", "r") as file:
                existing_cycles = file.read()
                # Format the new cycle the same way as it's stored in the file
                new_cycle_str = f"{self.w}x{self.h} Cycle: " + ' -> '.join([f"({x}, {y})" for x, y in new_cycle])
                if new_cycle_str in existing_cycles:
                    return True
        except FileNotFoundError:
            return False
        return False

    def writeCycleToFile(self, cycle):
        if not self.cycleExists(cycle):
            with open("hamcycles.txt", "a") as file:
                cycle_str = ' -> '.join([f"({x}, {y})" for x, y in cycle])
                file.write(f"{self.w}x{self.h} Cycle: {cycle_str}\n\n")
        
    def visualiseCycle(self):
        grid = np.zeros((self.h, self.w))
        for order, (x, y) in enumerate(self.path, start=1):
            grid[y, x] = order

        # Adjusting the figure size based on grid size to prevent overlap
        fig, ax = plt.subplots(figsize=(8, 6))  # Adjust figure size dynamically
        ax.matshow(grid, cmap='tab20c')

        # Adjusting text size for clarity
        text_size = min(4, 6) * 1.5  # Dynamically adjust text size

        for (i, j), val in np.ndenumerate(grid):
            ax.text(j, i, f'{int(val)}', ha='center', va='center', color='black', fontsize=text_size)

        plt.xticks([])
        plt.yticks([])
        plt.title('Hamiltonian Path Visiting Order', fontsize=16)

        plt.show()


# # Example usage
# ham = Hamiltonian()
# cycle = ham.calculateHamiltonianCycle()
# if cycle:
#     print("Hamiltonian Cycle found:")
#     ham.visualiseCycle()
# else:
#     print("No Hamiltonian Cycle found.")
