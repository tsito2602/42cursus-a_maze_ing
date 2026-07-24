from mazegen import Maze

BACKGROUND_COLOR = {
    "wall": "\x1b[48;5;252m",
    "passage": "\x1b[48;5;232m",
    "entry": "\x1b[48;5;201m",
    "exit": "\x1b[48;5;196m",
    "path": "\x1b[48;5;141m",
    "player": "\x1b[48;5;226m",
}

PIXEL = "  "
RESET = "\x1b[0m"

NORTH = 0b0001
EAST = 0b0010
SOUTH = 0b0100
WEST = 0b1000


SAMPLE_MAZE_ROWS = (
    "9139551111555515515395153",
    "ac2a9102829113855692c3a92",
    "814402aac42ac2a9138452a86",
    "a8116aa8552812c0028138683",
    "868696845142a8386846c6942",
    "81294143943a8284529553812",
    "8446943a852c2c4512a95286a",
    "a951292c2f816fffaac296852",
    "8416c2852fc4157f829285452",
    "81453ac56fffafff86aa8153a",
    "84112813913fafd503c2ac102",
    "812a82ac6c2fafffac54692aa",
    "aaaaa8453943c111413956aaa",
    "8682c453c43c3c6c3a82916c2",
    "83ac111451692915286a86956",
    "82c386815416c4292a9685693",
    "829429681141138444294552a",
    "ac69443aa83aa841392c39382",
    "839453a82c46845682812aa82",
    "c44556c6c555455546c446c46",
)

SAMPLE_MAZE_ENTRY = (1, 1)
SAMPLE_MAZE_EXIT = (19, 14)
SAMPLE_MAZE_SOLUTION = (
    (1, 1),
    (2, 1),
    (2, 2),
    (3, 2),
    (4, 2),
    (4, 1),
    (5, 1),
    (6, 1),
    (7, 1),
    (7, 2),
    (7, 3),
    (7, 4),
    (8, 4),
    (9, 4),
    (9, 5),
    (10, 5),
    (10, 6),
    (10, 7),
    (11, 7),
    (11, 8),
    (12, 8),
    (12, 9),
    (12, 10),
    (12, 11),
    (12, 12),
    (13, 12),
    (14, 12),
    (15, 12),
    (16, 12),
    (17, 12),
    (18, 12),
    (18, 13),
    (19, 13),
    (19, 14),
)

SAMPLE_MAZE = Maze(
    cells=tuple(
        tuple(int(cell, 16) for cell in row) for row in SAMPLE_MAZE_ROWS
    ),
    entry=SAMPLE_MAZE_ENTRY,
    exit=SAMPLE_MAZE_EXIT,
    solution=SAMPLE_MAZE_SOLUTION,
)


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


def render_maze(maze: Maze) -> str:
    canvas_width = maze.width * 2 + 1
    canvas_height = maze.height * 2 + 1

    canvas = [["wall"] * canvas_width for _ in range(canvas_height)]

    dig_passages(canvas, maze)

    paint_cell(canvas, maze.entry, "entry")
    paint_cell(canvas, maze.exit, "exit")

    return render_canvas(canvas)


def display_maze(maze: Maze) -> None:
    print(render_maze(maze))


if __name__ == "__main__":
    display_maze(SAMPLE_MAZE)
