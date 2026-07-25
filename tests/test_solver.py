import pytest
from mazegen import Maze, Wall
from mazegen.solver import Solver

ENTRY = (0, 0)
EXIT = (1, 0)


def _maze(cells: list[list[int]], entry: tuple[int, int], exit_: tuple[int, int]) -> Maze:
    return Maze(
        cells=tuple(tuple(row) for row in cells),
        entry=entry,
        exit=exit_,
        pattern_cells=(),
    )


def test_solve_finds_path_between_entry_and_exit() -> None:
    # Two cells side by side, connected (no wall between them).
    cells = [
        [Wall.ALL & ~Wall.EAST, Wall.ALL & ~Wall.WEST],
    ]
    maze = Solver(_maze(cells, ENTRY, EXIT)).solve()

    assert maze.solution[0] == ENTRY
    assert maze.solution[-1] == EXIT


def test_solve_path_is_a_valid_connected_walk() -> None:
    cells = [
        [Wall.ALL & ~Wall.EAST, Wall.ALL & ~Wall.WEST],
    ]
    maze = Solver(_maze(cells, ENTRY, EXIT)).solve()

    for (x1, y1), (x2, y2) in zip(maze.solution, maze.solution[1:]):
        assert abs(x1 - x2) + abs(y1 - y2) == 1


def test_solve_raises_when_exit_is_unreachable() -> None:
    # Two cells side by side, but the wall between them blocks the only path.
    cells = [
        [Wall.ALL, Wall.ALL],
    ]
    solver = Solver(_maze(cells, ENTRY, EXIT))

    with pytest.raises(ValueError):
        solver.solve()


def test_solve_trivial_maze_where_entry_equals_exit() -> None:
    cells = [[Wall.ALL]]
    maze = Solver(_maze(cells, (0, 0), (0, 0))).solve()

    assert maze.solution == ((0, 0),)