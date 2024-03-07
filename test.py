def prims_mst_grid(grid):
    num_rows = len(grid)
    num_cols = len(grid[0]) if num_rows > 0 else 0
    
    start_vertex = (0, 0)
    visited = set([start_vertex])
    mst_edges = []
    
    directions = [(-1, 0), (1, 0), (0, -1), (0, 1)]
    
    while len(visited) < num_rows * num_cols:
        edge_found = False
        for row, col in visited:
            for drow, dcol in directions:
                new_row, new_col = row + drow, col + dcol
                if 0 <= new_row < num_rows and 0 <= new_col < num_cols and (new_row, new_col) not in visited:
                    visited.add((new_row, new_col))
                    mst_edges.append(((row, col), (new_row, new_col)))
                    edge_found = True
                    break
            if edge_found:
                break
    
    return mst_edges

def print_mst_edges(mst_edges):
    print("MST Edges:")
    for edge in mst_edges:
        print(f"{edge[0]} -> {edge[1]}")

grid = [
    [1, 1, 1],
    [1, 1, 1],
    [1, 1, 1]
]

mst_edges = prims_mst_grid(grid)
print_mst_edges(mst_edges)

position_within_maze = dict()
        for x in range(self.w):
            for y in range(self.h):
                position_within_maze[(x, y)] = [(x // 2, y // 2), (x % 2, y % 2)]

        while len(self.path) < self.w * self.h:
            current_position = self.path[-1]
            neighbours = self.get_neighbours(current_position[0], current_position[1], self.w - 1, self.h - 1)
            print(current_position)

            current_cell, cell_pos = position_within_maze[current_position]
            maze_wall = tree_map[current_cell]

            for neighbour in neighbours:
                if neighbour not in self.path:
                    neighbourhood = neighbours[neighbour]

                    if current_cell != position_within_maze[neighbour][0]:
                        if neighbourhood in maze_wall:
                            cycle.append(neighbour)
                            break
