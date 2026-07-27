from pytest import CaptureFixture
from amazeing.display import (
    Display,
    WALL_COLORS,
    BACKGROUND_COLORS,
    PIXEL,
    RESET,
)
from mazegen import Maze, Wall

WALL = BACKGROUND_COLORS["wall"] + PIXEL
PASSAGE = BACKGROUND_COLORS["passage"] + PIXEL
ENTRY = BACKGROUND_COLORS["entry"] + PIXEL
EXIT = BACKGROUND_COLORS["exit"] + PIXEL
PATTERN = BACKGROUND_COLORS["pattern"] + PIXEL
PATH = BACKGROUND_COLORS["path"] + PIXEL


def test_display_maze_renders_connected_cells(
    capsys: CaptureFixture[str],
) -> None:
    """
    Render two horizontally connected cells with entry and exit markers.
    ■■■■■
    ■◯□☓■
    ■■■■■
    ■: wall, □: passage, ◯: entry, ☓: exit
    """
    maze = Maze(
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

    Display(maze).display_maze()

    expected = "\n".join(
        (
            WALL * 5 + RESET,
            WALL + ENTRY + PASSAGE + EXIT + WALL + RESET,
            WALL * 5 + RESET,
        )
    )

    assert capsys.readouterr().out == expected + "\n"


def test_display_maze_marks_pattern_cells(capsys: CaptureFixture[str]) -> None:
    """
    Render pattern cells with the 42-pattern color.
    ■■■■■■■
    ■◯■◆■☓■
    ■■■■■■■
    ■: wall, ◆: 42 pattern, ◯: entry, ☓: exit
    """
    maze = Maze(
        cells=(
            (
                int(Wall.ALL),
                int(Wall.ALL),
                int(Wall.ALL),
            ),
        ),
        entry=(0, 0),
        exit=(2, 0),
        pattern_cells=((1, 0),),
    )

    Display(maze).display_maze()

    expected = "\n".join(
        (
            WALL * 7 + RESET,
            (WALL + ENTRY + WALL + PATTERN + WALL + EXIT + WALL + RESET),
            WALL * 7 + RESET,
        )
    )

    assert capsys.readouterr().out == expected + "\n"


def test_display_maze_renders_solution_without_repainting_endpoints(
    capsys: CaptureFixture[str],
) -> None:
    """Render path centers and segments while preserving entry and exit."""
    maze = Maze(
        cells=(
            (
                int(Wall.NORTH | Wall.SOUTH | Wall.WEST),
                int(Wall.NORTH | Wall.SOUTH),
                int(Wall.NORTH | Wall.EAST | Wall.SOUTH),
            ),
        ),
        entry=(0, 0),
        exit=(2, 0),
        solution=((0, 0), (1, 0), (2, 0)),
        pattern_cells=(),
    )
    display = Display(maze)
    display.show_solution = True

    display.display_maze()

    expected = "\n".join(
        (
            WALL * 7 + RESET,
            WALL + ENTRY + PATH * 3 + EXIT + WALL + RESET,
            WALL * 7 + RESET,
        )
    )
    assert capsys.readouterr().out == expected + "\n"


def test_display_maze_renders_solution_between_adjacent_endpoints(
    capsys: CaptureFixture[str],
) -> None:
    """Render the path segment when the solution has no middle cell."""
    maze = Maze(
        cells=(
            (
                int(Wall.NORTH | Wall.SOUTH | Wall.WEST),
                int(Wall.NORTH | Wall.EAST | Wall.SOUTH),
            ),
        ),
        entry=(0, 0),
        exit=(1, 0),
        solution=((0, 0), (1, 0)),
        pattern_cells=(),
    )
    display = Display(maze)
    display.show_solution = True

    display.display_maze()

    expected = "\n".join(
        (
            WALL * 5 + RESET,
            WALL + ENTRY + PATH + EXIT + WALL + RESET,
            WALL * 5 + RESET,
        )
    )
    assert capsys.readouterr().out == expected + "\n"


def test_display_maze_renders_vertical_solution(
    capsys: CaptureFixture[str],
) -> None:
    """Render path centers and segments in the vertical direction."""
    maze = Maze(
        cells=(
            (int(Wall.NORTH | Wall.EAST | Wall.WEST),),
            (int(Wall.EAST | Wall.WEST),),
            (int(Wall.EAST | Wall.SOUTH | Wall.WEST),),
        ),
        entry=(0, 0),
        exit=(0, 2),
        solution=((0, 0), (0, 1), (0, 2)),
        pattern_cells=(),
    )
    display = Display(maze)
    display.show_solution = True

    display.display_maze()

    expected = "\n".join(
        (
            WALL * 3 + RESET,
            WALL + ENTRY + WALL + RESET,
            WALL + PATH + WALL + RESET,
            WALL + PATH + WALL + RESET,
            WALL + PATH + WALL + RESET,
            WALL + EXIT + WALL + RESET,
            WALL * 3 + RESET,
        )
    )
    assert capsys.readouterr().out == expected + "\n"


def test_rotate_wall_color_cycles() -> None:
    """Cycle through every wall color and return to the first."""
    maze = Maze(
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

    # The expected color sequence after each call to rotate_wall_color().
    expected_colors = WALL_COLORS[1:] + WALL_COLORS[:1]

    display = Display(maze)
    for expected_color in expected_colors:
        display.rotate_wall_color()

        assert display.bg_colors["wall"] == expected_color
