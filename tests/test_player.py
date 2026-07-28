"""Test player movement on the maze's expanded walkable grid."""

import pytest

from amazeing.player import Player
from mazegen import Coordinate, Maze, Wall


HORIZONTAL_MAZE = Maze(
    cells=(
        (
            int(Wall.NORTH | Wall.SOUTH | Wall.WEST),
            int(Wall.NORTH | Wall.EAST | Wall.SOUTH),
        ),
    ),
    entry=(0, 0),
    exit=(1, 0),
    pattern_cells=(),
)

VERTICAL_MAZE = Maze(
    cells=(
        (int(Wall.NORTH | Wall.EAST | Wall.WEST),),
        (int(Wall.EAST | Wall.SOUTH | Wall.WEST),),
    ),
    entry=(0, 0),
    exit=(0, 1),
    pattern_cells=(),
)


def test_player_starts_at_entry() -> None:
    """Place a new player at the entry cell center."""
    player = Player(HORIZONTAL_MAZE)

    assert player.position == (1, 1)
    assert player.reached_exit is False


@pytest.mark.parametrize(
    ("maze", "key", "segment", "destination"),
    (
        (HORIZONTAL_MAZE, "d", (2, 1), (3, 1)),
        (
            HORIZONTAL_MAZE.model_copy(
                update={"entry": (1, 0), "exit": (0, 0)}
            ),
            "a",
            (2, 1),
            (1, 1),
        ),
        (VERTICAL_MAZE, "s", (1, 2), (1, 3)),
        (
            VERTICAL_MAZE.model_copy(
                update={"entry": (0, 1), "exit": (0, 0)}
            ),
            "w",
            (1, 2),
            (1, 1),
        ),
    ),
)
def test_player_moves_through_segment_to_adjacent_cell(
    maze: Maze,
    key: str,
    segment: Coordinate,
    destination: Coordinate,
) -> None:
    """Move through a passage segment before reaching the adjacent cell."""
    player = Player(maze)

    assert player.move(key) is True
    assert player.position == segment
    assert player.reached_exit is False

    assert player.move(key) is True
    assert player.position == destination
    assert player.reached_exit is True


def test_player_does_not_move_through_wall() -> None:
    """Keep the player in place when a wall blocks the requested move."""
    maze = Maze(
        cells=((int(Wall.ALL), int(Wall.ALL)),),
        entry=(0, 0),
        exit=(1, 0),
        pattern_cells=(),
    )
    player = Player(maze)

    assert player.move("d") is False
    assert player.position == (1, 1)


def test_player_accepts_uppercase_key() -> None:
    """Treat an uppercase movement key as its lowercase equivalent."""
    player = Player(HORIZONTAL_MAZE)

    assert player.move("D") is True
    assert player.position == (2, 1)


def test_player_ignores_invalid_key() -> None:
    """Reject an unsupported key without changing the player position."""
    player = Player(HORIZONTAL_MAZE)

    assert player.move("x") is False
    assert player.position == (1, 1)


def test_player_does_not_move_outside_grid() -> None:
    """Prevent movement beyond the expanded grid boundary."""
    maze = Maze(
        cells=((int(Wall.NORTH | Wall.EAST | Wall.SOUTH),),),
        entry=(0, 0),
        exit=(0, 0),
        pattern_cells=(),
    )
    player = Player(maze)

    assert player.move("a") is True
    assert player.position == (0, 1)

    assert player.move("a") is False
    assert player.position == (0, 1)
