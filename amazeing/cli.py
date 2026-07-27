from amazeing.output import output_maze
from mazegen import Maze, MazeGenerator

from .config import MazeConfig
from .display import CLEAR_SCREEN, Display


def run(config: MazeConfig) -> None:
    maze = _generate_maze(config, config.seed)
    output_maze(maze, config.output_file)
    display = Display(maze)

    while True:
        print(CLEAR_SCREEN, end="")
        display.display_maze()
        display.display_color_guide()
        display.display_menu()

        choice = _read_menu_choice()

        match choice:
            case "1":
                new_maze = _generate_maze(
                    config,
                    seed=None,
                )
                display.update_maze(new_maze)

            case "2":
                display.toggle_show_solution()

            case "3":
                display.rotate_wall_color()

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
        perfect=config.perfect,
        seed=seed,
    )

    return generator.generate()


def _read_menu_choice() -> str:
    while True:
        choice = input("Choice? (1-4): ").strip()

        if choice in {"1", "2", "3", "4"}:
            return choice

        print("Please enter 1, 2, 3, or 4.")
