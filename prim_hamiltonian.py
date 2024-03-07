import matplotlib.pyplot as plt
import numpy as np
import random


BLOCK_SIZE = 20
#ideal width=640 height=480

class Hamiltonian:

    def __init__(self, width=200, height=200):
        self.w = int(width / BLOCK_SIZE)
        self.h = int(height / BLOCK_SIZE)
        self.graph = self.createGraph(self.w, self.h)
        self.visited = [[False for _ in range(self.h)] for _ in range(self.w)]
        self.path = []

    def getTotal(self):
        return self.w * self.h
    
    def createGraph(self, width, height):
        start = []
        for i in range(self.w):
            current = [1 for _ in range(self.h)]
            start.append(current)
        return start
        
    def cycleExists(self, new_cycle):
        try:
            with open("hamcycles.txt", "r") as file:
                existing_cycles = file.read()
                # Format the new cycle the same way as it's stored in the file
                new_cycle_str = f"{self.w}x{self.h}\n" + ' -> '.join([f"({x}, {y})" for x, y in new_cycle])
                if new_cycle_str in existing_cycles:
                    return True
        except FileNotFoundError:
            return False
        return False

    def writeCycleToFile(self, cycle):
        if not self.cycleExists(cycle):
            with open("hamcycles.txt", "a") as file:
                cycle_str = ' -> '.join([f"({x}, {y})" for x, y in cycle])
                file.write(f"{self.w}x{self.h}\n{cycle_str}\n\n")
        
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

    #Hamiltonian Cycle using Prims Minimum Spanning Tree Algorithm
        
    def calculatePrimsTree(self):
        # Generate a Maze of Half Width and Half Height using Prims Algorithm
        half_w = int(self.w / 2)
        half_h = int(self.h / 2)
        treeGraph = self.createGraph(half_w, half_h)
        maze = [] #Order of Visiting the Nodes
        #Tree: Add them all if they create a cycle or are already in the tree then reject them
        for x in range(half_w):
            for y in range(half_h):
                if (x, y) not in maze:
                    maze.append((x,y))
        print(maze)


    def noCycles(self, maze):
        # Check if there are any cycles in the tree
        visited = set()

        def dfs(vertex, parent):
            visited.add(vertex)
            for neighbor in maze[vertex]:
                if neighbor not in visited:
                    parent[neighbor] = vertex
                    if dfs(neighbor, parent):
                        return True
                elif parent[vertex] != neighbor:
                    # A visited neighbor not equal to parent means a back edge is found, indicating a cycle
                    return True
            return False

        for vertex in maze:
            if vertex not in visited:
                if dfs(vertex, None):
                    return True
        return False

                
                




        # Generate a Tree of Half Width and Half Height using Prims Algorithm






# Example usage
ham = Hamiltonian()
cycle = ham.calculatePrimsTree()
if cycle:
    print("Hamiltonian Cycle found:")
    ham.visualiseCycle()
else:
    print("No Hamiltonian Cycle found.")