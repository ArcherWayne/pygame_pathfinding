from pathfinding.core.grid import Grid
from pathfinding.finder.a_star import AStarFinder
from pathfinding.core.diagonal_movement import DiagonalMovement

matrix = [
    [1, 1, 1, 1, 1, 1],
    [1, 0, 1, 1, 1, 1],
    [1, 1, 1, 1, 1, 1], 
]

# 1. create a grid
grid = Grid(matrix=matrix)

# 2. create a start and end cell
start = grid.node(0, 0)
end = grid.node(5, 2)

# 3. create a finder with a movement style
# 此处是创建了一个实例
finder = AStarFinder(diagonal_movement=DiagonalMovement.always)

# 4. use the finder to find the path
(path, runs) = finder.find_path(start, end, grid)

# 5. print the results
print(path)
print(runs)