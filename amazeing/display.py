from mazegen import Maze

WALL_COLORS = (
    "\x1b[48;5;252m",  # white
    "\x1b[48;5;39m",  # blue
    "\x1b[48;5;82m",  # green
    "\x1b[48;5;208m",  # orange
)

BACKGROUND_COLOR = {
    "wall": WALL_COLORS[0],
    "passage": "\x1b[48;5;232m",
    "pattern_42": "\x1b[48;5;245m",
    "entry": "\x1b[48;5;201m",
    "exit": "\x1b[48;5;196m",
    "path": "\x1b[48;5;141m",
    "player": "\x1b[48;5;226m",
}

PIXEL = "  "
RESET = "\x1b[0m"
CLEAR_SCREEN = "\x1b[2J\x1b[H"

NORTH = 0b0001
EAST = 0b0010
SOUTH = 0b0100
WEST = 0b1000


def dig_passages(canvas: list[list[str]], maze: Maze) -> None:
    for y, row in enumerate(maze.cells):
        for x, cell in enumerate(row):
            center_x = x * 2 + 1
            center_y = y * 2 + 1

            canvas[center_y][center_x] = "passage"

            if cell & NORTH == 0:
                canvas[center_y - 1][center_x] = "passage"

            if cell & EAST == 0:
                canvas[center_y][center_x + 1] = "passage"

            if cell & SOUTH == 0:
                canvas[center_y + 1][center_x] = "passage"

            if cell & WEST == 0:
                canvas[center_y][center_x - 1] = "passage"


def paint_cell(
    canvas: list[list[str]], coordinate: tuple[int, int], kind: str
) -> None:
    x, y = coordinate
    center_x = x * 2 + 1
    center_y = y * 2 + 1

    canvas[center_y][center_x] = kind


def render_canvas(canvas: list[list[str]]) -> str:
    lines = []

    for row in canvas:
        line = "".join(BACKGROUND_COLOR[kind] + PIXEL for kind in row)
        lines.append(line + RESET)

    return "\n".join(lines)


def display_maze(maze: Maze) -> None:
    canvas_width = maze.width * 2 + 1
    canvas_height = maze.height * 2 + 1

    canvas = [["wall"] * canvas_width for _ in range(canvas_height)]

    dig_passages(canvas, maze)

    paint_cell(canvas, maze.entry, "entry")
    paint_cell(canvas, maze.exit, "exit")

    for coordinate in maze.blocked_cells:
        paint_cell(canvas, coordinate, "pattern_42")

    return print(render_canvas(canvas))


def display_color_guide() -> None:
    entry = f'{BACKGROUND_COLOR["entry"]}{PIXEL}{RESET}'
    exit_ = f'{BACKGROUND_COLOR["exit"]}{PIXEL}{RESET}'

    color_blocks = [color + PIXEL + RESET for color in WALL_COLORS]

    print()
    print(f"{entry}: entry     {exit_}: exit")
    print("Wall color rotation: " + " → ".join(color_blocks))
    print()


def display_menu() -> None:
    print("=== A-Maze-ing ===")
    print("1. Regenerate a new maze")
    print("2. Show / Hide the shortest path")
    print("3. Rotate the wall colors")
    print("4. Quit")


def rotate_wall_color() -> None:
    current_color = BACKGROUND_COLOR["wall"]
    current_index = WALL_COLORS.index(current_color)
    next_index = (current_index + 1) % len(WALL_COLORS)

    BACKGROUND_COLOR["wall"] = WALL_COLORS[next_index]
