from mazegen import Coordinate, Maze

DIRECTION_LETTERS: dict[tuple[int, int], str] = {
    (0, -1): "N",
    (1, 0): "E",
    (0, 1): "S",
    (-1, 0): "W",
}


def _path_to_letters(path: tuple[Coordinate, ...]) -> str:
    """Turn a list of coordinates into a string of N/E/S/W moves."""
    letters = []

    for (x1, y1), (x2, y2) in zip(path, path[1:]):
        letters.append(DIRECTION_LETTERS[(x2 - x1, y2 - y1)])

    return "".join(letters)


def output_maze(maze: Maze, output_file: str) -> None:
    """Write the maze to output_file using the format from the subject."""
    with open(output_file, "w", encoding="utf-8") as file:
        for row in maze.cells:
            file.write("".join(format(cell, "x") for cell in row) + "\n")

        file.write("\n")
        file.write(f"{maze.entry[0]},{maze.entry[1]}     # entry (x, y)\n")
        file.write(f"{maze.exit[0]},{maze.exit[1]}     # exit (x, y)\n")
        file.write(_path_to_letters(maze.solution) + "\n")
