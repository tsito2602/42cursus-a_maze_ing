from pathlib import Path

import pytest
from pydantic import ValidationError

from amazeing import parse_config

VALID_CONFIG_LINES = (
    "# Comment",
    "WIDTH=20",
    "HEIGHT=15",
    "ENTRY=0,0",
    "EXIT=19,14",
    "OUTPUT_FILE=maze.txt",
    "PERFECT=True",
    "SEED=42",
)


def _write_config(
    tmp_path: Path,
    extra_lines: tuple[str, ...] = (),
    lines: tuple[str, ...] = VALID_CONFIG_LINES,
) -> Path:
    """Write selected configuration lines with optional additions."""
    config_file = tmp_path / "config.txt"
    config_file.write_text(
        "\n".join((*lines, *extra_lines)),
        encoding="utf-8",
    )

    return config_file


def _replace_value(key: str, value: str) -> tuple[str, ...]:
    """Replace one value in the valid configuration."""
    prefix = f"{key}="
    return tuple(
        f"{prefix}{value}" if line.startswith(prefix) else line
        for line in VALID_CONFIG_LINES
    )


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


def test_parse_rejects_line_without_separator(tmp_path: Path) -> None:
    """Reject a configuration line that is not KEY=VALUE."""
    config_file = _write_config(tmp_path, ("BROKEN LINE",))

    with pytest.raises(ValueError, match="expected KEY=VALUE"):
        parse_config(str(config_file))


def test_parse_rejects_duplicated_key(tmp_path: Path) -> None:
    """Reject a key that appears more than once."""
    config_file = _write_config(tmp_path, ("WIDTH=30",))

    with pytest.raises(ValueError, match="duplicated key WIDTH"):
        parse_config(str(config_file))


def test_parse_rejects_unknown_key(tmp_path: Path) -> None:
    """Reject a key not supported by the configuration format."""
    config_file = _write_config(tmp_path, ("ALGORITHM=dfs",))

    with pytest.raises(ValueError, match="unknown key 'ALGORITHM'"):
        parse_config(str(config_file))


@pytest.mark.parametrize(
    ("key", "value", "message"),
    (
        ("WIDTH", "abc", "Invalid integer for WIDTH"),
        ("ENTRY", "0", "Invalid coordinate '0': expected x,y"),
        ("EXIT", "x,1", "x and y must be integers"),
        ("PERFECT", "true", "expected True or False"),
    ),
)
def test_parse_rejects_invalid_value_syntax(
    tmp_path: Path,
    key: str,
    value: str,
    message: str,
) -> None:
    """Reject malformed values according to their configuration key."""
    config_file = _write_config(
        tmp_path,
        lines=_replace_value(key, value),
    )

    with pytest.raises(ValueError, match=message):
        parse_config(str(config_file))


@pytest.mark.parametrize(
    ("key", "field"),
    (
        ("WIDTH", "width"),
        ("HEIGHT", "height"),
        ("ENTRY", "entry"),
        ("EXIT", "exit_"),
        ("OUTPUT_FILE", "output_file"),
        ("PERFECT", "perfect"),
    ),
)
def test_parse_rejects_missing_required_key(
    tmp_path: Path,
    key: str,
    field: str,
) -> None:
    """Reject a configuration missing one mandatory key."""
    lines = tuple(
        line for line in VALID_CONFIG_LINES if not line.startswith(f"{key}=")
    )
    config_file = _write_config(tmp_path, lines=lines)

    with pytest.raises(ValidationError) as error:
        parse_config(str(config_file))

    assert error.value.errors()[0]["loc"] == (field,)


def test_parse_rejects_equal_entry_and_exit(tmp_path: Path) -> None:
    """Reject identical entry and exit coordinates."""
    config_file = _write_config(
        tmp_path,
        lines=_replace_value("EXIT", "0,0"),
    )

    with pytest.raises(
        ValidationError,
        match="ENTRY and EXIT must be different",
    ):
        parse_config(str(config_file))


@pytest.mark.parametrize(
    ("key", "value"),
    (
        ("ENTRY", "-1,0"),
        ("EXIT", "20,14"),
    ),
)
def test_parse_rejects_coordinate_outside_maze(
    tmp_path: Path,
    key: str,
    value: str,
) -> None:
    """Reject entry and exit coordinates outside the configured bounds."""
    config_file = _write_config(
        tmp_path,
        lines=_replace_value(key, value),
    )

    with pytest.raises(ValidationError, match=f"{key} .* outside"):
        parse_config(str(config_file))


@pytest.mark.parametrize(
    ("key", "value"),
    (
        ("WIDTH", "0"),
        ("HEIGHT", "-1"),
        ("OUTPUT_FILE", ""),
    ),
)
def test_parse_rejects_invalid_config_value(
    tmp_path: Path,
    key: str,
    value: str,
) -> None:
    """Reject parsed values that violate MazeConfig constraints."""
    config_file = _write_config(
        tmp_path,
        lines=_replace_value(key, value),
    )

    with pytest.raises(ValidationError):
        parse_config(str(config_file))
