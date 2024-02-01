

BLOCK_SIZE = 20

class Hamiltonian:

    def __init__(self, width=640, height=480):
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
        print(start)
        return start
    
    
    def isSafe(self, x, y):
        return 0 <= x < self.w and 0 <= y < self.h and self.graph[x][y] == 1 and not self.visited[x][y]
    
    def calculateHamiltonianCycleUtil(self, x, y, steps):
        #Base Case - If we have visited every single square a
        if steps == self.getTotal():
            # Optionally, check here if (x, y) can return to the start point to form a complete cycle
            return True
        
        #Recursive Case Depth First Search
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
            return self.path
        else:
            return None

# Example usage
ham = Hamiltonian()
cycle = ham.calculateHamiltonianCycle()
if cycle:
    print("Hamiltonian Cycle found:")
    print(cycle)
else:
    print("No Hamiltonian Cycle found.")
