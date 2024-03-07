def prims_mst_grid(grid):
    num_rows = len(grid)
    num_cols = len(grid[0]) if num_rows > 0 else 0
    
    # Each vertex is identified by its (row, col) position
    # Start from the top-left cell
    start_vertex = (0, 0)
    
    # Set of visited vertices
    visited = set([start_vertex])
    
    # List of edges in the MST
    mst_edges = []
    
    # Directions for up, down, left, right
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

# Example usage:
grid = [
    [1, 1, 1],
    [1, 1, 1],
    [1, 1, 1]
]

mst_edges = prims_mst_grid(grid)
print("Edges in the MST:", mst_edges)