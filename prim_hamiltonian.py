import matplotlib.pyplot as plt
import numpy as np
import random

#References: https://github.com/illayyy/snake_ai?tab=readme-ov-file
#https://johnflux.com/2015/05/02/nokia-6110-part-3-algorithms/


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
        
    def get_neighbours(self, x , y, width, height):
        frontier = []
        if x > 0:
            frontier.append((x-1, y))
        if x < width - 1:
            frontier.append((x+1, y))
        if y > 0:
            frontier.append((x, y-1))
        if y < height - 1:
            frontier.append((x, y+1))
        return frontier
    
    # def get_directions(self, x, y, width, height):
    #     directions = dict()
    #     if x > 0:
    #         directions[x, y] = "U"
    #     if x < width - 1:
    #         directions[x, y] = "D"
    #     if y > 0:
    #         directions[x, y] = "L"
    #     if y < height - 1:
    #         directions[x, y] = "R"
    #     return directions
        
    def prims_mst_tree(self):
        tree_map = dict()
        neighbours = dict()
        half_w = self.w // 2
        half_h = self.h // 2

        for x in range(self.w // 2):
            for y in range(self.h // 2):
                neighbours[(x, y)] = self.get_neighbours(x, y, half_w, half_h)
                tree_map[(x, y)] = [] #Array as it may have multiple edges
        
        #Start at 0,0 for Now - Make Random Later
        visited = [(0,0)]
        frontier = neighbours[0,0]
        while len(visited) < (self.w // 2) * (self.h // 2):
            available = []
            new_frontier = []
            random_neighbour = random.choice(frontier)
            for adj in neighbours[random_neighbour]:
                if adj in visited:
                    available.append(adj)

                elif adj not in frontier:
                    new_frontier.append(adj)

            previously_checked_node = random.choice(available)

            visited.append(random_neighbour)
            tree_map[random_neighbour].append(previously_checked_node)
            tree_map[previously_checked_node].append(random_neighbour)

            
            frontier.remove(random_neighbour)
            frontier += new_frontier
        return tree_map
    
    def hamiltonian_cycle(self):
        #Follow the Trees path like a wall in a maze
        tree_map = self.prims_mst_tree()
        start = (0, 0)  # Starting at the top-left corner, for example
        cycle = [start]
        visited = set(start)
        current = start

        directions = [(0, -1), (1, 0), (0, 1), (-1, 0)]  # Up, Right, Down, Left
        dir_index = 1  # Start by trying to go right

        while len(cycle) < self.w * self.h:
            next_dir = directions[dir_index]
            next_cell = (current[0] + next_dir[0], current[1] + next_dir[1])

            # Check if next cell is valid and not part of the MST or if it's not visited
            if (0 <= next_cell[0] < self.w and 0 <= next_cell[1] < self.h and
                    next_cell not in visited and 
                    (current, next_cell) not in tree_map and 
                    (next_cell, current) not in tree_map):
                visited.add(next_cell)
                cycle.append(next_cell)
                current = next_cell
                # Reset direction to try right first next time
                dir_index = 1
            else:
                # Try the next direction clockwise (right-hand rule)
                dir_index = (dir_index + 1) % 4

        print(cycle)
        self.path = cycle

        return cycle





            

        



        


            


    
        


# Example usage

ham = Hamiltonian()
cycle = ham.hamiltonian_cycle()
if cycle:
    print("Hamiltonian Cycle found:")
    ham.visualiseCycle()
else:
    print("No Hamiltonian Cycle found.")