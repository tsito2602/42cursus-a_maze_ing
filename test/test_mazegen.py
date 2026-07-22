from pathlib import Path
from src.mazegen import MazeGenerator


WIDTH = 20
HEIGHT = 15
ENTRY = (0, 0)
EXIT = (19, 14)
SEED = 42

NORTH = 0b0001
EAST = 0b0010
SOUTH = 0b0100
WEST = 0b1000

def test_seed():
    first = MazeGenerator(WIDTH, HEIGHT, ENTRY, EXIT, SEED)
    first.generate()
    second = MazeGenerator(WIDTH, HEIGHT, ENTRY, EXIT, SEED)
    second.generate()

    assert first.grid == second.grid


def test_outer_walls():
    maze = MazeGenerator(WIDTH, HEIGHT, ENTRY, EXIT, SEED)
    maze.generate()

    for x in range(WIDTH):
        assert maze.grid[0][x] & NORTH
        assert maze.grid[HEIGHT - 1][x] & SOUTH
    for y in range(HEIGHT):
        assert maze.grid[y][0] & WEST
        assert maze.grid[y][WIDTH - 1] & EAST