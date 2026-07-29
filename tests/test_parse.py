from pathlib import Path

import pytest

from amazeing import parse_config


def _write_config(
    tmp_path: Path,
    extra_lines: tuple[str, ...] = (),
) -> Path:
    """Write a valid config with optional extra lines."""
    config_file = tmp_path / "config.txt"
    config_file.write_text(
        "\n".join(
            [
                "# Comment",
                "WIDTH=20",
                "HEIGHT=15",
                "ENTRY=0,0",
                "EXIT=19,14",
                "OUTPUT_FILE=maze.txt",
                "PERFECT=True",
                "SEED=42",
                *extra_lines,
            ]
        ),
        encoding="utf-8",
    )

    return config_file


def test_parse_valid_config(tmp_path: Path) -> None:
    config_file = _write_config(
        tmp_path,
        ("WALL_BREAK_RATIO=0.5",),
    )

    config = parse_config(str(config_file))

    assert config.width == 20
    assert config.height == 15
    assert config.entry == (0, 0)
    assert config.exit_ == (19, 14)
    assert config.output_file == "maze.txt"
    assert config.perfect is True
    assert config.seed == 42
    assert config.wall_break_ratio == 0.5


def test_parse_uses_default_wall_break_ratio(tmp_path: Path) -> None:
    config_file = _write_config(tmp_path)

    config = parse_config(str(config_file))

    assert config.wall_break_ratio == 0.3


@pytest.mark.parametrize("ratio", ("0", "1.1"))
def test_parse_rejects_invalid_wall_break_ratio(
    tmp_path: Path,
    ratio: str,
) -> None:
    config_file = _write_config(
        tmp_path,
        (f"WALL_BREAK_RATIO={ratio}",),
    )

    with pytest.raises(ValueError, match="wall_break_ratio"):
        parse_config(str(config_file))


def test_parse_rejects_non_numeric_wall_break_ratio(
    tmp_path: Path,
) -> None:
    config_file = _write_config(
        tmp_path,
        ("WALL_BREAK_RATIO=abc",),
    )

    with pytest.raises(
        ValueError,
        match="Invalid float for WALL_BREAK_RATIO",
    ):
        parse_config(str(config_file))
