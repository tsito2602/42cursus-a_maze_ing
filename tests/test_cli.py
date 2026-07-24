from pytest import CaptureFixture, MonkeyPatch
import amazeing.cli as cli
from amazeing import MazeConfig
from mazegen import Maze, Wall


def test_read_menu_choice_retries_invalid_input(
    monkeypatch: MonkeyPatch,
    capsys: CaptureFixture[str],
) -> None:
    """Retry until a valid menu choice is entered."""
    choices = iter(("x", "5", "3"))

    monkeypatch.setattr(
        "builtins.input",
        lambda _: next(choices),
    )

    result = cli.read_menu_choice()

    error_message = "Please enter 1, 2, 3, or 4.\n"

    assert result == "3"
    assert capsys.readouterr().out == error_message * 2


def test_run_handles_menu_actions(
    monkeypatch: MonkeyPatch,
) -> None:
    """Handle regenerate, rotate, and quit menu actions."""
    config = MazeConfig(
        width=2,
        height=1,
        entry=(0, 0),
        exit_=(1, 0),
        output_file="maze.txt",
        perfect=True,
        seed=42,
    )
    maze = Maze(
        cells=((int(Wall.ALL), int(Wall.ALL)),),
        entry=(0, 0),
        exit=(1, 0),
        pattern_cells=(),
    )

    choices = iter(("1", "3", "4"))
    generated_seeds: list[int | None] = []
    rotation_count = 0

    def fake_generate_maze(
        _: MazeConfig,
        seed: int | None,
    ) -> Maze:
        """Record the seed and return the test maze."""
        generated_seeds.append(seed)
        return maze

    def fake_read_menu_choice() -> str:
        """Return the next predefined menu choice."""
        return next(choices)

    def fake_rotate_wall_color() -> None:
        """Record one wall-color rotation."""
        nonlocal rotation_count
        rotation_count += 1

    def do_nothing(*_: object) -> None:
        """Ignore display calls during the CLI test."""
        pass

    monkeypatch.setattr(cli, "generate_maze", fake_generate_maze)
    monkeypatch.setattr(cli, "read_menu_choice", fake_read_menu_choice)
    monkeypatch.setattr(cli, "rotate_wall_color", fake_rotate_wall_color)
    monkeypatch.setattr(cli, "display_maze", do_nothing)
    monkeypatch.setattr(cli, "display_color_guide", do_nothing)
    monkeypatch.setattr(cli, "display_menu", do_nothing)
    monkeypatch.setattr(cli, "CLEAR_SCREEN", "")

    cli.run(config)

    assert generated_seeds == [42, None]
    assert rotation_count == 1
