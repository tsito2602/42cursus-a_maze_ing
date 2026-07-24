"""Render and display mazes in an ANSI-capable terminal."""

from mazegen import Maze, Wall, Coordinate

WALL_COLORS = (
    "\x1b[48;5;252m",  # white
    "\x1b[48;5;39m",  # blue
    "\x1b[48;5;82m",  # green
    "\x1b[48;5;208m",  # orange
)

BACKGROUND_COLORS = {
    "wall": WALL_COLORS[0],
    "passage": "\x1b[48;5;232m",
    "pattern": "\x1b[48;5;245m",
    "entry": "\x1b[48;5;201m",
    "exit": "\x1b[48;5;196m",
    "path": "\x1b[48;5;141m",
    "player": "\x1b[48;5;226m",
}

PIXEL = "  "
RESET = "\x1b[0m"
CLEAR_SCREEN = "\x1b[2J\x1b[H"

Canvas = list[list[str]]


def display_maze(maze: Maze) -> None:
    """Print a rendered maze to the terminal."""
    print(_render_maze(maze))


def display_color_guide() -> None:
    """Display the meaning and rotation order of maze colors."""
    entry = f'{BACKGROUND_COLORS["entry"]}{PIXEL}{RESET}'
    exit_ = f'{BACKGROUND_COLORS["exit"]}{PIXEL}{RESET}'

    color_blocks = [color + PIXEL + RESET for color in WALL_COLORS]

    print()
    print(f"{entry}: entry     {exit_}: exit")
    print("Wall color rotation: " + " → ".join(color_blocks))
    print()


def display_menu() -> None:
    """Display the interactive menu options."""
    print("=== A-Maze-ing ===")
    print("1. Regenerate a new maze")
    print("2. Show / Hide the shortest path")
    print("3. Rotate the wall colors")
    print("4. Quit")


def rotate_wall_color() -> None:
    """Change the wall color to the next color in the rotation."""
    current_color = BACKGROUND_COLORS["wall"]
    current_index = WALL_COLORS.index(current_color)
    next_index = (current_index + 1) % len(WALL_COLORS)

    BACKGROUND_COLORS["wall"] = WALL_COLORS[next_index]


def _render_maze(maze: Maze) -> str:
    """Render a maze as an ANSI-colored string."""
    canvas = _create_canvas(maze)

    _mark_passages(canvas, maze)

    _paint_cell_center(canvas, maze.entry, "entry")
    _paint_cell_center(canvas, maze.exit, "exit")

    for coordinate in maze.pattern_cells:
        _paint_cell_center(canvas, coordinate, "pattern")

    return _canvas_to_ansi(canvas)


def _create_canvas(maze: Maze) -> Canvas:
    """Create a wall-filled canvas sized for the maze."""
    canvas_width = maze.width * 2 + 1
    canvas_height = maze.height * 2 + 1

    return [["wall"] * canvas_width for _ in range(canvas_height)]


def _mark_passages(canvas: Canvas, maze: Maze) -> None:
    """Mark cell centers and openings as passages on the canvas."""
    for y, row in enumerate(maze.cells):
        for x, cell in enumerate(row):
            center_x = x * 2 + 1
            center_y = y * 2 + 1

            canvas[center_y][center_x] = "passage"

            if cell & Wall.NORTH == 0:
                canvas[center_y - 1][center_x] = "passage"

            if cell & Wall.EAST == 0:
                canvas[center_y][center_x + 1] = "passage"

            if cell & Wall.SOUTH == 0:
                canvas[center_y + 1][center_x] = "passage"

            if cell & Wall.WEST == 0:
                canvas[center_y][center_x - 1] = "passage"


def _paint_cell_center(
    canvas: Canvas, coordinate: Coordinate, kind: str
) -> None:
    """Paint one maze cell center with the requested display kind."""
    x, y = coordinate
    center_x = x * 2 + 1
    center_y = y * 2 + 1

    canvas[center_y][center_x] = kind


def _canvas_to_ansi(canvas: Canvas) -> str:
    """Convert a canvas into an ANSI-colored string."""
    lines = []

    for row in canvas:
        line = "".join(BACKGROUND_COLORS[kind] + PIXEL for kind in row)
        lines.append(line + RESET)

    return "\n".join(lines)
