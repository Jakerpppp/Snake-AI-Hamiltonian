from ai_game import SnakeGameAI
from hamiltonian import Hamiltonian

#Constants
WIDTH = 120
HEIGHT = 140




ham = Hamiltonian(WIDTH, HEIGHT)
cycle = ham.calculateHamiltonianCycle()
if cycle:
    ai = SnakeGameAI(cycle, WIDTH, HEIGHT)
    while True:
        ai.play_step()
else:
    print("No Cycle Found")