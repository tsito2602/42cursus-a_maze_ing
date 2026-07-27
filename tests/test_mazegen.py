from mazegen import Maze, Wall, MazeGenerator

WIDTH = 20
HEIGHT = 15
ENTRY = (0, 0)
EXIT = (19, 14)
PERFECT = True
SEED = 42


def test_seed() -> None:
    first = MazeGenerator(WIDTH, HEIGHT, ENTRY, EXIT, True, SEED)
    first.generate()
    second = MazeGenerator(WIDTH, HEIGHT, ENTRY, EXIT, True, SEED)
    second.generate()

    assert first.cells == second.cells


def test_outer_walls() -> None:
    maze = MazeGenerator(WIDTH, HEIGHT, ENTRY, EXIT, True, SEED)
    maze.generate()

    for x in range(WIDTH):
        assert maze.cells[0][x] & Wall.NORTH
        assert maze.cells[HEIGHT - 1][x] & Wall.SOUTH
    for y in range(HEIGHT):
        assert maze.cells[y][0] & Wall.WEST
        assert maze.cells[y][WIDTH - 1] & Wall.EAST


def test_generate_returns_maze() -> None:
    result = MazeGenerator(
        WIDTH, HEIGHT, ENTRY, EXIT, True, SEED
    ).generate()

    assert isinstance(result, Maze)
    assert result.entry == ENTRY
    assert result.exit == EXIT


def test_generate_dimensions_match_grid() -> None:
    generator = MazeGenerator(WIDTH, HEIGHT, ENTRY, EXIT, True, SEED)
    result = generator.generate()

    assert result.width == WIDTH
    assert result.height == HEIGHT
    assert result.cells == tuple(tuple(row) for row in generator.cells)


def test_imperfect_maze_opens_extra_walls() -> None:
    """Verify that an imperfect maze has more passages than a perfect maze."""
    perfect = MazeGenerator(
        WIDTH,
        HEIGHT,
        ENTRY,
        EXIT,
        perfect=True,
        seed=SEED,
    )
    perfect.generate()

    imperfect = MazeGenerator(
        WIDTH,
        HEIGHT,
        ENTRY,
        EXIT,
        perfect=False,
        seed=SEED,
    )
    imperfect.generate()

    assert _count_open_passages(imperfect) > _count_open_passages(perfect)


def _count_open_passages(generator: MazeGenerator) -> int:
    """Count open passages between non-pattern cells."""
    count = 0

    for y in range(generator.height):
        for x in range(generator.width):
            if (x, y) in generator.pattern_cells:
                continue

            if (
                x + 1 < generator.width
                and (x + 1, y) not in generator.pattern_cells
                and not generator.cells[y][x] & Wall.EAST
            ):
                count += 1

            if (
                y + 1 < generator.height
                and (x, y + 1) not in generator.pattern_cells
                and not generator.cells[y][x] & Wall.SOUTH
            ):
                count += 1

    return count


def test_imperfect_maze_keeps_42_cells_closed() -> None:
    """Verify that every cell forming the 42 pattern remains fully closed."""
    generator = MazeGenerator(
        WIDTH,
        HEIGHT,
        ENTRY,
        EXIT,
        perfect=False,
        seed=SEED,
    )
    generator.generate()

    for x, y in generator.pattern_cells:
        assert generator.cells[y][x] == Wall.ALL


def test_imperfect_maze_is_reproducible() -> None:
    """Verify that the same seed produces the same imperfect maze."""
    first = MazeGenerator(
        WIDTH,
        HEIGHT,
        ENTRY,
        EXIT,
        perfect=False,
        seed=SEED,
    )
    first.generate()

    second = MazeGenerator(
        WIDTH,
        HEIGHT,
        ENTRY,
        EXIT,
        perfect=False,
        seed=SEED,
    )
    second.generate()

    assert first.cells == second.cells


def test_imperfect_maze_walls_are_symmetric() -> None:
    """Verify that shared walls match on both adjacent cells."""
    generator = MazeGenerator(
        WIDTH,
        HEIGHT,
        ENTRY,
        EXIT,
        perfect=False,
        seed=SEED,
    )
    generator.generate()

    for y in range(HEIGHT):
        for x in range(WIDTH):
            if x + 1 < WIDTH:
                east = bool(generator.cells[y][x] & Wall.EAST)
                west = bool(generator.cells[y][x + 1] & Wall.WEST)
                assert east == west

            if y + 1 < HEIGHT:
                south = bool(generator.cells[y][x] & Wall.SOUTH)
                north = bool(generator.cells[y + 1][x] & Wall.NORTH)
                assert south == north


def test_imperfect_maze_has_no_fully_open_3x3_area() -> None:
    """Verify that the maze contains no completely open 3-by-3 area."""
    generator = MazeGenerator(
        WIDTH,
        HEIGHT,
        ENTRY,
        EXIT,
        perfect=False,
        seed=SEED,
    )
    generator.generate()

    assert generator._has_open_3x3() is False
