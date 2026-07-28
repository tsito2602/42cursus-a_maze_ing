import sys
from amazeing import MazeConfig, run
from amazeing import parse_config

CONFIG = MazeConfig(
    width=20,
    height=15,
    entry=(0, 0),
    exit_=(19, 14),
    output_file="maze.txt",
    perfect=False,
    seed=42,
)


def main() -> None:
    """Parse the command-line configuration path and start the application."""
    if len(sys.argv) != 2:
        print("Usage: a_maze_ing.py <file>")
        return

    config_file = sys.argv[1]

    try:
        config = parse_config(config_file)
        run(config)
    except Exception as e:
        print(f"Error: {e}")


if __name__ == "__main__":
    main()
