from pytest import CaptureFixture, MonkeyPatch
import amazeing.display as display
from mazegen import Maze, Wall

WALL = display.BACKGROUND_COLORS["wall"] + display.PIXEL
PASSAGE = display.BACKGROUND_COLORS["passage"] + display.PIXEL
ENTRY = display.BACKGROUND_COLORS["entry"] + display.PIXEL
EXIT = display.BACKGROUND_COLORS["exit"] + display.PIXEL
PATTERN = display.BACKGROUND_COLORS["pattern"] + display.PIXEL


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

    display.display_maze(maze)

    expected = "\n".join(
        (
            WALL * 5 + display.RESET,
            WALL + ENTRY + PASSAGE + EXIT + WALL + display.RESET,
            WALL * 5 + display.RESET,
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

    display.display_maze(maze)

    expected = "\n".join(
        (
            WALL * 7 + display.RESET,
            (
                WALL
                + ENTRY
                + WALL
                + PATTERN
                + WALL
                + EXIT
                + WALL
                + display.RESET
            ),
            WALL * 7 + display.RESET,
        )
    )

    assert capsys.readouterr().out == expected + "\n"


def test_rotate_wall_color_cycles(
    monkeypatch: MonkeyPatch,
) -> None:
    """Cycle through every wall color and return to the first."""
    monkeypatch.setitem(
        display.BACKGROUND_COLORS,
        "wall",
        display.WALL_COLORS[0],
    )

    # The expected color sequence after each call to rotate_wall_color().
    expected_colors = display.WALL_COLORS[1:] + display.WALL_COLORS[:1]

    for expected_color in expected_colors:
        display.rotate_wall_color()

        assert display.BACKGROUND_COLORS["wall"] == expected_color
