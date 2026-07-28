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


class Display:
    def __init__(self, maze: Maze) -> None:
        self.maze = maze
        self.bg_colors = BACKGROUND_COLORS.copy()
        self.show_solution = False

    def _create_canvas(self) -> Canvas:
        """Create a wall-filled canvas sized for the maze."""
        canvas_width = self.maze.width * 2 + 1
        canvas_height = self.maze.height * 2 + 1

        return [["wall"] * canvas_width for _ in range(canvas_height)]

    def _mark_passages(self, canvas: Canvas) -> None:
        """Mark cell centers and openings as passages on the canvas."""
        for y, row in enumerate(self.maze.cells):
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
        self, canvas: Canvas, coordinate: Coordinate, kind: str
    ) -> None:
        """Paint one maze cell center with the requested display kind."""
        x, y = coordinate
        center_x = x * 2 + 1
        center_y = y * 2 + 1

        canvas[center_y][center_x] = kind

    def _canvas_to_ansi(self, canvas: Canvas) -> str:
        """Convert a canvas into an ANSI-colored string."""
        lines = []

        for row in canvas:
            line = "".join(self.bg_colors[kind] + PIXEL for kind in row)
            lines.append(line + RESET)

        return "\n".join(lines)

    def _render_solution(self, canvas: Canvas) -> None:
        for coordinate in self.maze.solution[1:-1]:
            self._paint_cell_center(canvas, coordinate, "path")

        for previous, current in zip(
            self.maze.solution,
            self.maze.solution[1:],
        ):
            previous_x = previous[0] * 2 + 1
            previous_y = previous[1] * 2 + 1
            current_x = current[0] * 2 + 1
            current_y = current[1] * 2 + 1
            segment_x = (previous_x + current_x) // 2
            segment_y = (previous_y + current_y) // 2
            canvas[segment_y][segment_x] = "path"

    def _render_player(self, canvas: Canvas, position: Coordinate) -> None:
        x, y = position
        canvas[y][x] = "player"

    def _render_maze(self, player_pos: Coordinate | None = None) -> str:
        """Render a maze as an ANSI-colored string."""
        canvas = self._create_canvas()

        self._mark_passages(canvas)

        for coordinate in self.maze.pattern_cells:
            self._paint_cell_center(canvas, coordinate, "pattern")

        if self.show_solution:
            self._render_solution(canvas)

        self._paint_cell_center(canvas, self.maze.entry, "entry")
        self._paint_cell_center(canvas, self.maze.exit, "exit")

        if player_pos is not None:
            self._render_player(canvas, player_pos)

        return self._canvas_to_ansi(canvas)

    def display_maze(self, player_pos: Coordinate | None = None) -> None:
        """Print a rendered maze to the terminal."""
        print(self._render_maze(player_pos))

    def display_color_guide(self) -> None:
        """Display the meaning and rotation order of maze colors."""
        entry = f'{self.bg_colors["entry"]}{PIXEL}{RESET}'
        exit_ = f'{self.bg_colors["exit"]}{PIXEL}{RESET}'
        player = f'{self.bg_colors["player"]}{PIXEL}{RESET}'

        color_blocks = [color + PIXEL + RESET for color in WALL_COLORS]

        print()
        print(f"{entry}: Entry     {exit_}: Exit     {player}: Player")
        print("Wall color rotation: " + " → ".join(color_blocks))
        print()

    def display_menu(self) -> None:
        """Display the interactive menu options."""
        print("=== A-Maze-ing ===")
        print("W/A/S/D: Player moves")
        print("1. Regenerate a new maze")
        print("2. Show / Hide the shortest path")
        print("3. Rotate the wall colors")
        print("4. Quit")

    def update_maze(self, new_maze: Maze) -> None:
        self.maze = new_maze
        self.show_solution = False

    def toggle_show_solution(self) -> None:
        if self.show_solution:
            self.show_solution = False
        else:
            self.show_solution = True

    def rotate_wall_color(self) -> None:
        """Change the wall color to the next color in the rotation."""
        current_color = self.bg_colors["wall"]
        current_index = WALL_COLORS.index(current_color)
        next_index = (current_index + 1) % len(WALL_COLORS)

        self.bg_colors["wall"] = WALL_COLORS[next_index]
