from mazegen import Maze, Wall, MazeGenerator

WIDTH = 20
HEIGHT = 15
ENTRY = (0, 0)
EXIT = (19, 14)
SEED = 42


def test_seed() -> None:
    first = MazeGenerator(WIDTH, HEIGHT, ENTRY, EXIT, SEED)
    first.generate()
    second = MazeGenerator(WIDTH, HEIGHT, ENTRY, EXIT, SEED)
    second.generate()

    assert first.grid == second.grid


def test_outer_walls() -> None:
    maze = MazeGenerator(WIDTH, HEIGHT, ENTRY, EXIT, SEED)
    maze.generate()

    for x in range(WIDTH):
        assert maze.grid[0][x] & Wall.NORTH
        assert maze.grid[HEIGHT - 1][x] & Wall.SOUTH
    for y in range(HEIGHT):
        assert maze.grid[y][0] & Wall.WEST
        assert maze.grid[y][WIDTH - 1] & Wall.EAST


def test_generate_returns_maze() -> None:
    result = MazeGenerator(WIDTH, HEIGHT, ENTRY, EXIT, SEED).generate()

    assert isinstance(result, Maze)
    assert result.entry == ENTRY
    assert result.exit == EXIT


def test_generate_dimensions_match_grid() -> None:
    generator = MazeGenerator(WIDTH, HEIGHT, ENTRY, EXIT, SEED)
    result = generator.generate()

    assert result.width == WIDTH
    assert result.height == HEIGHT
    assert result.cells == tuple(tuple(row) for row in generator.grid)
