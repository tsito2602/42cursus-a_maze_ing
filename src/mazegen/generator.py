import random
from typing import TypeAlias
from .maze import DIRECTIONS, Maze, Wall, Coordinate
from .solve import solve

WIDTH = 20
HEIGHT = 15
ENTRY = (0, 0)
EXIT = (19, 14)
PERFECT = True
SEED = 42

PATTERN_42: list[Coordinate] = [
    # coordinates of 4
    (0, 0),
    (0, 1),
    (0, 2),
    (1, 2),
    (2, 2),
    (2, 3),
    (2, 4),
    # coordinates of 2
    (4, 0),
    (5, 0),
    (6, 0),
    (6, 1),
    (4, 2),
    (5, 2),
    (6, 2),
    (4, 3),
    (4, 4),
    (5, 4),
    (6, 4),
]
PATTERN_WIDTH = 7
PATTERN_HEIGHT = 5

EXTRA_WALLS_RATIO = 0.3

WallCandidate: TypeAlias = tuple[int, int, str]


class MazeGenerator:
    """Generate reproducible mazes from dimensions and endpoint settings."""

    def __init__(
        self,
        width: int,
        height: int,
        entry: Coordinate,
        exit_: Coordinate,
        perfect: bool = True,
        seed: int | None = None,
    ) -> None:
        """Set up a cells with entry/exit and the 42 pattern placed."""
        self.width = width
        self.height = height
        self.entry = entry
        self.exit = exit_
        self.perfect = perfect
        self.rng = random.Random(seed)
        self.cells: list[list[int]] = [
            [Wall.ALL] * width for _ in range(height)
        ]

        if not self._in_frame(*self.entry):
            raise ValueError("ENTRY is outside the maze")

        if not self._in_frame(*self.exit):
            raise ValueError("EXIT is outside the maze")

        self.pattern_cells: set[Coordinate] = self._place_42_pattern()

        if self.entry in self.pattern_cells:
            raise ValueError("ENTRY overlaps the 42 pattern")

        if self.exit in self.pattern_cells:
            raise ValueError("EXIT overlaps the 42 pattern")

        self.visited: set[Coordinate] = set()

    def _in_frame(self, x: int, y: int) -> bool:
        """Check whether (x, y) lies within the maze bounds."""
        if 0 <= x < self.width and 0 <= y < self.height:
            return True
        else:
            return False

    def _place_42_pattern(self) -> set[Coordinate]:
        """Return the cell coordinates that make up the centered 42 pattern."""
        if self.width < PATTERN_WIDTH + 2 or self.height < PATTERN_HEIGHT + 2:
            print("error :42 pattern is too big for the maze size  ")
            return set()

        off_x = (self.width - PATTERN_WIDTH) // 2
        off_y = (self.height - PATTERN_HEIGHT) // 2

        return {(off_x + x, off_y + y) for (x, y) in PATTERN_42}

    def _unvisited_neighbours(self, x: int, y: int) -> list[str]:
        """Return the directions from (x, y) leading to an unvisited cell."""
        result: list[str] = []

        for name, (dx, dy, _, _) in DIRECTIONS.items():
            nx, ny = x + dx, y + dy
            if not (0 <= nx < self.width and 0 <= ny < self.height):
                continue
            if (nx, ny) in self.visited:
                continue
            result.append(name)

        return result

    def generate(self) -> Maze:
        """Generate a perfect or imperfect maze from the current settings."""
        self._generate_perfect_maze()

        if not self.perfect:
            self._open_extra_walls()

        return Maze(
            cells=tuple(tuple(row) for row in self.cells),
            entry=self.entry,
            exit=self.exit,
            pattern_cells=tuple(self.pattern_cells),
            solution=solve(self.cells, self.entry, self.exit),
        )

    def _generate_perfect_maze(self) -> None:
        """Generate a perfect maze using randomized depth-first search."""
        self.visited = set(self.pattern_cells)
        self.visited.add(self.entry)

        passage: list[Coordinate] = [self.entry]

        while passage:
            x, y = passage[-1]
            choices = self._unvisited_neighbours(x, y)

            if not choices:
                passage.pop()
                continue

            name = self.rng.choice(choices)
            dx, dy, wall, opposite = DIRECTIONS[name]
            nx, ny = x + dx, y + dy

            self.cells[y][x] &= ~wall
            self.cells[ny][nx] &= ~opposite
            self.visited.add((nx, ny))
            passage.append((nx, ny))

    def _openable_walls(self) -> list[WallCandidate]:
        """Return closed walls that can be opened outside the 42 pattern."""
        candidates: list[WallCandidate] = []

        for y in range(self.height):
            for x in range(self.width):
                if (x, y) in self.pattern_cells:
                    continue

                if (
                    x + 1 < self.width
                    and (x + 1, y) not in self.pattern_cells
                    and self.cells[y][x] & Wall.EAST
                ):
                    candidates.append((x, y, "E"))

                if (
                    y + 1 < self.height
                    and (x, y + 1) not in self.pattern_cells
                    and self.cells[y][x] & Wall.SOUTH
                ):
                    candidates.append((x, y, "S"))

        return candidates

    def _open_wall(self, candidate: WallCandidate) -> None:
        """Open a shared wall on both adjacent cells."""
        x, y, direction = candidate
        dx, dy, wall, opposite = DIRECTIONS[direction]
        nx, ny = x + dx, y + dy

        self.cells[y][x] &= ~wall
        self.cells[ny][nx] &= ~opposite

    def _close_wall(self, candidate: WallCandidate) -> None:
        """Close a shared wall on both adjacent cells."""
        x, y, direction = candidate
        dx, dy, wall, opposite = DIRECTIONS[direction]
        nx, ny = x + dx, y + dy

        self.cells[y][x] |= wall
        self.cells[ny][nx] |= opposite

    def _is_open_3x3(self, start_x: int, start_y: int) -> bool:
        """Check whether one 3-by-3 area has no internal walls."""
        for y in range(start_y, start_y + 3):
            for x in range(start_x, start_x + 2):
                if self.cells[y][x] & Wall.EAST:
                    return False

        for y in range(start_y, start_y + 2):
            for x in range(start_x, start_x + 3):
                if self.cells[y][x] & Wall.SOUTH:
                    return False

        return True

    def _has_open_3x3(self) -> bool:
        """Check whether the maze contains a fully open 3-by-3 area."""
        if self.width < 3 or self.height < 3:
            return False

        for y in range(self.height - 2):
            for x in range(self.width - 2):
                if self._is_open_3x3(x, y):
                    return True

        return False

    def _get_openable_cnt(self) -> int:
        """Calculate the target number of extra walls to open."""
        usable_cells = self.width * self.height - len(self.pattern_cells)
        return max(1, int(usable_cells * EXTRA_WALLS_RATIO))

    def _open_extra_walls(self) -> None:
        """Open extra walls without creating a fully open 3-by-3 area."""
        candidates = self._openable_walls()
        self.rng.shuffle(candidates)

        openable = self._get_openable_cnt()
        opened = 0

        for candidate in candidates:
            self._open_wall(candidate)

            if self._has_open_3x3():
                self._close_wall(candidate)
                continue

            opened += 1

            if opened >= openable:
                break

        if opened == 0:
            raise ValueError("Cannot generate imperfect maze.")


if __name__ == "__main__":
    generator = MazeGenerator(WIDTH, HEIGHT, ENTRY, EXIT, PERFECT, SEED)
    maze = generator.generate()
    print(maze)
