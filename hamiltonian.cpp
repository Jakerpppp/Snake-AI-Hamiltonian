#include <iostream>
#include <vector>
#include <fstream>
#include <string>

const int BLOCK_SIZE = 20;
const std::pair<int, int> directions[4] = {{1, 0}, {0, 1}, {-1, 0}, {0, -1}}; // Right, Down, 

class Hamiltonian {
public:
    Hamiltonian(int width, int height);
    std::vector<std::pair<int, int>> calculateHamiltonianCycle();

private:
    int w, h;
    std::vector<std::vector<int>> graph;
    std::vector<std::vector<bool>> visited;
    std::vector<std::pair<int, int>> path;

    int getTotal();
    std::vector<std::vector<int>> createGraph();
    bool isSafe(int x, int y);
    bool calculateHamiltonianCycleUtil(int x, int y, int steps);
    bool cycleExists();
    void writeCycleToFile();
};

Hamiltonian::Hamiltonian(int width, int height) {
    w = width / BLOCK_SIZE;
    h = height / BLOCK_SIZE;
    graph = createGraph();
    visited = std::vector<std::vector<bool>>(w, std::vector<bool>(h, false));
}

int Hamiltonian::getTotal() {
    return w * h;
}

std::vector<std::vector<int>> Hamiltonian::createGraph() {
    return std::vector<std::vector<int>>(w, std::vector<int>(h, 1));
}

bool Hamiltonian::isSafe(int x, int y) {
    return x >= 0 && x < w && y >= 0 && y < h && graph[x][y] == 1 && !visited[x][y];
}

bool Hamiltonian::calculateHamiltonianCycleUtil(int x, int y, int steps) {
    if (steps == getTotal()) {
        for (const auto& dir : directions) {
            int dx = dir.first, dy = dir.second;
            if (x + dx == 0 && y + dy == 0) return true;
        }
        return false;
    }

    for (const auto& dir : directions) {
        int next_x = x + dir.first, next_y = y + dir.second;
        if (isSafe(next_x, next_y)) {
            visited[next_x][next_y] = true;
            path.push_back({next_x, next_y});

            if (calculateHamiltonianCycleUtil(next_x, next_y, steps + 1)) {
                return true;
            }

            visited[next_x][next_y] = false;
            path.pop_back();
        }
    }
    return false;
}

std::vector<std::pair<int, int>> Hamiltonian::calculateHamiltonianCycle() {
    visited[0][0] = true;
    path.push_back({0, 0});

    if (calculateHamiltonianCycleUtil(0, 0, 1)) {
        writeCycleToFile();
        return path;
    } else {
        return {};
    }
}

bool Hamiltonian::cycleExists() {
    std::ifstream file("hamcycles.txt");
    std::string line, new_cycle_str = std::to_string(w) + "x" + std::to_string(h) + "\n";
    for (size_t i = 0; i < path.size(); ++i) {
        new_cycle_str += "(" + std::to_string(path[i].first) + ", " + std::to_string(path[i].second) + ")";
        if (i < path.size() - 1) {
            new_cycle_str += " -> ";
        }
    }
    new_cycle_str += "\n"; // Ensure the string ends with a newline to match the file format

    if (file.is_open()) {
        while (getline(file, line)) {
            // Add a newline to the read line for matching the exact cycle format
            line += '\n';
            if (line == new_cycle_str) {
                return true;
            }
        }
    }
    return false;
}


void Hamiltonian::writeCycleToFile() {
    if (!cycleExists()) {
        std::ofstream file("hamcycles.txt", std::ios::app);
        if (file.is_open()) {
            file << std::to_string(w) + "x" + std::to_string(h) + "\n";
            for (size_t i = 0; i < path.size(); ++i) {
                file << "(" << path[i].first << ", " << path[i].second << ")";
                // Only add " -> " if this is not the last element
                if (i < path.size() - 1) {
                    file << " -> ";
                }
            }
            file << "\n\n";
            file.close(); // Close the file explicitly (though it would be closed upon leaving scope)
        }
    }
}


int main() {
    int width = 120, height = 120; // Define width and height
    Hamiltonian hamiltonian(width, height); // Use the defined width and height
    auto cycle = hamiltonian.calculateHamiltonianCycle();

    int w = width / BLOCK_SIZE;
    int h = height / BLOCK_SIZE;

    if (!cycle.empty()) {
        std::cout << "Hamiltonian Cycle found for " << w << "x" << h << ":\n";
        for (size_t i = 0; i < cycle.size(); ++i) {
            std::cout << "(" << cycle[i].first * BLOCK_SIZE << ", " << cycle[i].second * BLOCK_SIZE << ")";
            // Only add " -> " if this is not the last element
            if (i < cycle.size() - 1) {
                std::cout << " -> ";
            }
        }
        std::cout << std::endl;
    } else {
        std::cout << "No Hamiltonian Cycle found for " << width << "x" << height << "." << std::endl;
    }

    return 0;
}


