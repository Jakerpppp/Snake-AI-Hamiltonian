from ai_game import SnakeGameAI
from hamiltonian import Hamiltonian

#Constants
BLOCK_SIZE = 20
WIDTH = 160
HEIGHT = 160

pairs_dict = {}

def parse_cycle(cycle_str):
    pairs = cycle_str.split(" -> ")
    tuple_list = [tuple(map(int, pair.strip("()").split(", "))) for pair in pairs]
    return tuple_list

# Open and read the file
with open('hamcycles.txt', 'r') as file:
    lines = file.readlines()
    count = 0
    for i in range(len(lines)):
        if lines[i] != "\n":
            if count == 0:
                key = lines[i].strip()
                count = 1
            else:
                value = lines[i].strip()
                pairs_dict[key] = value
                count = 0


ham = Hamiltonian(WIDTH, HEIGHT)
w = int(WIDTH / BLOCK_SIZE)
h = int(HEIGHT / BLOCK_SIZE)

cycle_str = pairs_dict.get(f'{w}x{h}')

if cycle_str:
    print("Reading from File")
    cycle = parse_cycle(cycle_str)
else:
    print("Not in File: Calculating")
    cycle = ham.calculateHamiltonianCycle()


if cycle:
    ai = SnakeGameAI(cycle, WIDTH, HEIGHT)
    while True:
        ai.play_step()
else:
    print("No Cycle Found")