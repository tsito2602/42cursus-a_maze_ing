from typing import TypeAlias
from mazegen import Maze, Wall, Coordinate

MOVES = {
    "w": (0, -1),
    "a": (-1, 0),
    "s": (0, 1),
    "d": (1, 0),
}

WalkableGrid: TypeAlias = list[list[bool]]


def _cell_to_grid_coordinate(position: Coordinate) -> Coordinate:
    """Convert a maze cell coordinate to its expanded-grid center."""
    x, y = position
    return (x * 2 + 1, y * 2 + 1)


class Player:
    """Store and update a player's position within a maze."""

    def __init__(self, maze: Maze) -> None:
        """Place the player at the maze entry and build its movement grid."""
        self.maze = maze
        self.position = _cell_to_grid_coordinate(maze.entry)
        self.walkable = self._create_walkable_grid(maze)

    @staticmethod
    def _create_walkable_grid(maze: Maze) -> WalkableGrid:
        """Build an expanded grid marking cell centers and open passages."""
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

    def move(self, key: str) -> bool:
        """Move one grid position for a valid, unobstructed movement key."""
        movement = MOVES.get(key.lower())

        if movement is None:
            return False

        dx, dy = movement
        x, y = self.position
        dest_x, dest_y = x + dx, y + dy

        if not (
            0 <= dest_x < len(self.walkable[0])
            and 0 <= dest_y < len(self.walkable)
        ):
            return False

        if not self.walkable[dest_y][dest_x]:
            return False

        self.position = (dest_x, dest_y)
        return True

    @property
    def reached_exit(self) -> bool:
        """Return whether the player has reached the exit cell center."""
        return self.position == _cell_to_grid_coordinate(self.maze.exit)
