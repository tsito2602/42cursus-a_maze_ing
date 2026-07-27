from typing import TypeAlias
import pytest
from mazegen import Wall
from mazegen.solve import solve

ENTRY = (0, 0)
EXIT = (1, 0)

Cells: TypeAlias = list[list[int]]


def test_solve_finds_path_between_entry_and_exit() -> None:
    cells: Cells = [
        [Wall.ALL & ~Wall.EAST, Wall.ALL & ~Wall.WEST],
    ]
    path = solve(cells, ENTRY, EXIT)

    assert path[0] == ENTRY
    assert path[-1] == EXIT


def test_solve_path_is_a_valid_connected_walk() -> None:
    cells: Cells = [
        [Wall.ALL & ~Wall.EAST, Wall.ALL & ~Wall.WEST],
    ]
    path = solve(cells, ENTRY, EXIT)

    for (x1, y1), (x2, y2) in zip(path, path[1:]):
        assert abs(x1 - x2) + abs(y1 - y2) == 1


def test_solve_raises_when_exit_is_unreachable() -> None:
    cells: Cells = [
        [Wall.ALL, Wall.ALL],
    ]

    with pytest.raises(ValueError):
        solve(cells, ENTRY, EXIT)


def test_solve_trivial_maze_where_entry_equals_exit() -> None:
    cells: Cells = [[Wall.ALL]]
    path = solve(cells, (0, 0), (0, 0))

    assert path == ((0, 0),)


def test_solve_returns_the_shortest_route_around_a_loop() -> None:
    cells: Cells = [[Wall.ALL] * 3 for _ in range(3)]

    def link(
        x1: int, y1: int, wall: Wall,
        x2: int, y2: int, opposite: Wall,
    ) -> None:
        cells[y1][x1] &= ~wall
        cells[y2][x2] &= ~opposite

    link(0, 0, Wall.EAST, 1, 0, Wall.WEST)
    link(1, 0, Wall.EAST, 2, 0, Wall.WEST)
    link(2, 0, Wall.SOUTH, 2, 1, Wall.NORTH)
    link(2, 1, Wall.SOUTH, 2, 2, Wall.NORTH)
    link(2, 2, Wall.WEST, 1, 2, Wall.EAST)
    link(1, 2, Wall.WEST, 0, 2, Wall.EAST)
    link(0, 2, Wall.NORTH, 0, 1, Wall.SOUTH)
    link(0, 1, Wall.NORTH, 0, 0, Wall.SOUTH)

    path = solve(cells, (0, 0), (2, 0))

    assert path == ((0, 0), (1, 0), (2, 0))
