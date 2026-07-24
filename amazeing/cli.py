from mazegen import Maze, MazeGenerator

from .config import MazeConfig
from .display import (
    CLEAR_SCREEN,
    display_color_guide,
    display_maze,
    display_menu,
    rotate_wall_color,
)


def run(config: MazeConfig) -> None:
    maze = _generate_maze(config, config.seed)

    while True:
        print(CLEAR_SCREEN, end="")
        display_maze(maze)
        display_color_guide()
        display_menu()

        choice = _read_menu_choice()

        match choice:
            case "1":
                maze = _generate_maze(
                    config,
                    seed=None,
                )

            case "2":
                pass

            case "3":
                rotate_wall_color()

            case "4":
                return


def _generate_maze(
    config: MazeConfig,
    seed: int | None,
) -> Maze:
    generator = MazeGenerator(
        width=config.width,
        height=config.height,
        entry=config.entry,
        exit_=config.exit_,
        seed=seed,
    )

    return generator.generate()


def _read_menu_choice() -> str:
    while True:
        choice = input("Choice? (1-4): ").strip()

        if choice in {"1", "2", "3", "4"}:
            return choice

        print("Please enter 1, 2, 3, or 4.")
