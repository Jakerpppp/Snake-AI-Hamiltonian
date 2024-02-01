



#Constants
BLOCK_SIZE = 20

class Hamiltonian:

    def __init__(self, width, height):
        self.w = width
        self.h = height

    def calculateSquares(self):
        return ((self.w / BLOCK_SIZE ) * (self.h / BLOCK_SIZE))


    
    
    
    
    
    
    #Depth First Search through a Graph 
    def calculateHamiltonianCycle(self):
        pass


class Graph:
    
    def __init__(self) -> None:
        self.number = -1

