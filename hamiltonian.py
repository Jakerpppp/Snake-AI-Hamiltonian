



#Constants
BLOCK_SIZE = 20

class Hamiltonian:

    def __init__(self, width=640, height=480):
        self.w = int(width / BLOCK_SIZE)
        self.h = int(height / BLOCK_SIZE)
        self.graph = self.createGraph()

    def getTotal(self):
        return self.w * self.h
    
    def createGraph(self):
        start = []
        for i in range (self.w):
            current = []
            for j in range (self.h):
                current.append(1)
            start.append(current)
        print(start)
    
    
    #Depth First Search through a Graph of Squares determining the Ham Cycle
    def calculateHamiltonianCycle(self):
        row = len(self.graph)
        column = len(self.graph[0])
        list = []
        for i in range (row):
            for j in range (column):
                if self.graph[i][j] == 1:
                    self.graph[i][j] = 0
                    list.append[(i,j)]
                    self.calculateHamiltonianCycle()


ham = Hamiltonian()
ham.createGraph()

