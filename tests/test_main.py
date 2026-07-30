import sys
from pathlib import Path
from pydantic import ValidationError
from pytest import CaptureFixture, MonkeyPatch, raises
import a_maze_ing
from amazeing import MazeConfig

BOUNDS_ERROR = (
    "EXIT (19, 17) is outside the maze bounds (WIDTH=4, HEIGHT=5).\n"
    "Expected 0 <= x < 4 and 0 <= y < 5."
)


def _invalid_config() -> MazeConfig:
    """Create a validation error for an out-of-bounds exit."""
    return MazeConfig(
        width=4,
        height=5,
        entry=(0, 0),
        exit_=(19, 17),
        output_file="maze.txt",
        perfect=True,
    )


def _valid_config() -> MazeConfig:
    """Create the smallest valid configuration used by main tests."""
    return MazeConfig(
        width=2,
        height=1,
        entry=(0, 0),
        exit_=(1, 0),
        output_file="maze.txt",
        perfect=True,
    )


def test_format_validation_error_omits_pydantic_details() -> None:
    """Keep only actionable configuration validation information."""
    with raises(ValidationError) as error:
        _invalid_config()

    message = a_maze_ing.format_validation_error(error.value)

    assert message == BOUNDS_ERROR


def test_main_reports_validation_error(
    monkeypatch: MonkeyPatch,
    capsys: CaptureFixture[str],
) -> None:
    """Report concise validation details to standard error."""
    monkeypatch.setattr(sys, "argv", ["a_maze_ing.py", "config.txt"])
    monkeypatch.setattr(
        a_maze_ing,
        "parse_config",
        lambda _: _invalid_config(),
    )

    with raises(SystemExit) as exit_info:
        a_maze_ing.main()

    captured = capsys.readouterr()
    assert exit_info.value.code == 1
    assert captured.out == ""
    assert captured.err == f"Error: {BOUNDS_ERROR}\n"


def test_main_reports_missing_config_file(
    tmp_path: Path,
    monkeypatch: MonkeyPatch,
    capsys: CaptureFixture[str],
) -> None:
    """Report a missing configuration file as a normal CLI error."""
    missing_file = tmp_path / "missing.txt"
    monkeypatch.setattr(sys, "argv", ["a_maze_ing.py", str(missing_file)])

    with raises(SystemExit) as exit_info:
        a_maze_ing.main()

    captured = capsys.readouterr()
    assert exit_info.value.code == 1
    assert captured.out == ""
    assert captured.err.startswith("Error: ")
    assert str(missing_file) in captured.err


def test_main_reports_keyboard_interrupt(
    monkeypatch: MonkeyPatch,
    capsys: CaptureFixture[str],
) -> None:
    """Exit cleanly when the user presses Ctrl+C."""
    monkeypatch.setattr(sys, "argv", ["a_maze_ing.py", "config.txt"])
    monkeypatch.setattr(a_maze_ing, "parse_config", lambda _: _valid_config())

    def interrupt(_: MazeConfig) -> None:
        raise KeyboardInterrupt

    monkeypatch.setattr(a_maze_ing, "run", interrupt)

    with raises(SystemExit) as exit_info:
        a_maze_ing.main()

    captured = capsys.readouterr()
    assert exit_info.value.code == 130
    assert captured.out == ""
    assert captured.err == "\nInterrupted.\n"


def test_main_rejects_missing_argument(
    monkeypatch: MonkeyPatch,
    capsys: CaptureFixture[str],
) -> None:
    """Report command-line usage as an error."""
    monkeypatch.setattr(sys, "argv", ["a_maze_ing.py"])

    with raises(SystemExit) as exit_info:
        a_maze_ing.main()

    captured = capsys.readouterr()
    assert exit_info.value.code == 2
    assert captured.out == ""
    assert captured.err == "Usage: a_maze_ing.py <file>\n"
