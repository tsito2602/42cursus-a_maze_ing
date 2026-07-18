from pathlib import Path
from amazeing import parse_config


def test_parse_valid_config(tmp_path: Path) -> None:
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
            ]
        ),
        encoding="utf-8",
    )

    config = parse_config(str(config_file))

    assert config.width == 20
    assert config.height == 15
    assert config.entry == (0, 0)
    assert config.exit == (19, 14)
    assert config.output_file == "maze.txt"
    assert config.perfect is True
    assert config.seed == 42
