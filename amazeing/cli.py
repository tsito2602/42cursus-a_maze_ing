import sys
import termios
import tty
from .output import output_maze
from .player import Player
from .config import MazeConfig
from .display import CLEAR_SCREEN, Display
from mazegen import Maze, MazeGenerator

VALID_COMMANDS = {"w", "a", "s", "d", "1", "2", "3", "4"}
GREEN = "\x1b[38;5;82m"
BOLD = "\x1b[1m"
RESET = "\x1b[0m"


def run(config: MazeConfig) -> None:
    maze = _generate_maze(config, config.seed)
    output_maze(maze, config.output_file)
    display = Display(maze)
    player = Player(maze)

    while True:
        print(CLEAR_SCREEN, end="")
        display.display_maze(player.position)
        display.display_color_guide()
        display.display_menu()

        choice = _read_menu_choice()

        match choice:
            case "w" | "a" | "s" | "d":
                player.move(choice)

            case "1":
                player = _regenerate(config, display)

            case "2":
                display.toggle_show_solution()

            case "3":
                display.rotate_wall_color()

            case "4":
                return

        if player.reached_exit:
            clear_choice = _show_clear_screen(display, player)

            if clear_choice == "4":
                return

            player = _regenerate(config, display)


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


def _regenerate(config: MazeConfig, display: Display) -> Player:
    new_maze = _generate_maze(config, seed=None)
    output_maze(new_maze, config.output_file)
    display.update_maze(new_maze)

    return Player(new_maze)


def _read_key() -> str:
    if not sys.stdin.isatty():
        return input().strip().lower()

    fd = sys.stdin.fileno()
    old_settings = termios.tcgetattr(fd)

    try:
        tty.setcbreak(fd)
        return sys.stdin.read(1).lower()
    finally:
        termios.tcsetattr(
            fd,
            termios.TCSADRAIN,
            old_settings,
        )


def _read_menu_choice() -> str:
    while True:
        choice = _read_key()

        if choice in VALID_COMMANDS:
            return choice

        print("Please enter W, A, S, D or 1-4.")


def _show_clear_screen(display: Display, player: Player) -> str:
    print(CLEAR_SCREEN, end="")
    display.display_maze(player.position)

    print()
    print(f"{GREEN}{BOLD}=== MAZE CLEARED!!! ==={RESET}")
    print()
    print("1. Generate a new maze")
    print("4. Quit")

    while True:
        choice = _read_key()

        if choice in {"1", "4"}:
            return choice

        print("Please enter 1 or 4.")
