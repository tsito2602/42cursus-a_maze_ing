from typing import TypeAlias
from mazegen import Maze, Wall, Coordinate

MOVES = {
    "w": (0, -1),
    "a": (-1, 0),
    "s": (0, 1),
    "d": (1, 0),
}

WalkableGrid: TypeAlias = list[list[bool]]


def _create_walkable_path(maze: Maze) -> WalkableGrid:
    width = maze.width * 2 + 1
    height = maze.height * 2 + 1
    grid = [[False] * width for _ in range(height)]

    for y, row in enumerate(maze.cells):
        for x, cell in enumerate(row):
            center_x = x * 2 + 1
            center_y = y * 2 + 1

            grid[center_y][center_x] = True

            if not cell & Wall.NORTH:
                grid[center_y - 1][center_x] = True
            if not cell & Wall.EAST:
                grid[center_y][center_x + 1] = True
            if not cell & Wall.SOUTH:
                grid[center_y + 1][center_x] = True
            if not cell & Wall.WEST:
                grid[center_y][center_x - 1] = True

    return grid


def _cell_to_canvas_coordinate(position: Coordinate) -> Coordinate:
    x, y = position
    return (x * 2 + 1, y * 2 + 1)


class Player:
    def __init__(self, maze: Maze) -> None:
        self.maze = maze
        self.position = _cell_to_canvas_coordinate(maze.entry)
        self.walkable = _create_walkable_path(maze)

    def move(self, key: str) -> bool:
        movement = MOVES.get(key.lower())

        if movement is None:
            return False

        dx, dy = movement
        x, y = self.position
        dest = (x + dx, y + dy)

        if not self.walkable[dest[1]][dest[0]]:
            return False

        self.position = dest
        return True

    @property
    def reached_exit(self) -> bool:
        return self.position == _cell_to_canvas_coordinate(self.maze.exit)
