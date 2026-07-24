from amazeing import MazeConfig, run

CONFIG = MazeConfig(
    width=20,
    height=15,
    entry=(0, 0),
    exit_=(19, 14),
    output_file="maze.txt",
    perfect=True,
    seed=42,
)


def main() -> None:
    run(CONFIG)


if __name__ == "__main__":
    main()
