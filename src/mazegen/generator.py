import random
from .maze import DIRECTIONS, Maze, Wall, Coordinate
from .solver import Solver

WIDTH = 20
HEIGHT = 15
ENTRY = (0, 0)
EXIT = (19, 14)
SEED = 42

PATTERN_42: list[Coordinate] = [
    # 4のところ
    (0, 0),
    (2, 0),
    (0, 1),
    (2, 1),
    (0, 2),
    (1, 2),
    (2, 2),
    (2, 3),
    (2, 4),
    # 2のところ
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


class MazeGenerator:
    def __init__(
        self,
        width: int,
        height: int,
        entry: Coordinate,
        exit_: Coordinate,
        seed: int | None = None,
    ) -> None:
        """Set up an empty walled grid with entry/exit and the 42 pattern placed."""
        self.width = width
        self.height = height
        self.entry = entry
        self.exit = exit_
        self.rng = random.Random(seed)
        self.grid: list[list[int]] = [
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
        """Carve a maze via randomized backtracking and return it, solved."""
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

            self.grid[y][x] &= ~wall
            self.grid[ny][nx] &= ~opposite
            self.visited.add((nx, ny))
            passage.append((nx, ny))

        maze = Maze(
            cells=tuple(tuple(row) for row in self.grid),
            entry=self.entry,
            exit=self.exit,
            pattern_cells=tuple(self.pattern_cells),
        )

        return Solver(maze).solve()


if __name__ == "__main__":
    generator = MazeGenerator(WIDTH, HEIGHT, ENTRY, EXIT, SEED)
    maze = generator.generate()
    print(maze)
