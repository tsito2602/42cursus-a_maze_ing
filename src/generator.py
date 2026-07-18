import random

WIDTH = 20
HEIGHT = 15
ENTRY = (0, 0)
EXIT = (19, 14)
SEED = 42

NORTH = 0b0001
EAST = 0b0010
SOUTH = 0b0100
WEST = 0b1000
ALL_WALLS = NORTH | EAST | SOUTH | WEST

DIRECTIONS: dict[str, tuple[int, int, int, int]] = {
    "N": (0, -1, NORTH, SOUTH),
    "E": (1, 0, EAST, WEST),
    "S": (0, 1, SOUTH, NORTH),
    "W": (-1, 0, WEST, EAST),
}

PATTERN_42: list[tuple[int, int]] = [
    # 4　のところ
    (0, 0), (2, 0),
    (0, 1), (2, 1),
    (0, 2), (1, 2), (2, 2),
    (2, 3),
    (2, 4),
    # ２のところ
    (4, 0), (5, 0), (6, 0),
    (6, 1),
    (4, 2), (5, 2), (6, 2),
    (4, 3),
    (4, 4), (5, 4), (6, 4),
]
PATTERN_WIDTH = 7
PATTERN_HEIGHT = 5


class MazeGenerator:
    def __init__(
        self,
        width: int = WIDTH,
        height: int = HEIGHT,
        entry: tuple[int, int] = ENTRY,
        exit_: tuple[int, int] = EXIT,
        seed: int = SEED,
    ) -> None:
        self.width = width
        self.height = height
        self.entry = entry
        self.exit = exit_
        self.rng = random.Random(seed)
        self.grid: list[list[int]] = [
            [ALL_WALLS] * width for _ in range(height)
        ]
        self.blocked: set[tuple[int, int]] = self._place_42_pattern()
        self.visited: set[tuple[int, int]] = set()

    def _place_42_pattern(self) -> set[tuple[int, int]]:
        if self.width < PATTERN_WIDTH + 2 or self.height < PATTERN_HEIGHT + 2:
            print("error :42 pattern is too big for the maze size  ")
            return set()
        off_x = (self.width - PATTERN_WIDTH) // 2
        off_y = (self.height - PATTERN_HEIGHT) // 2
        return {(off_x + x, off_y + y) for (x, y) in PATTERN_42}

    def _unvisited_neighbours(self, x: int, y: int) -> list[str]:
        result: list[str] = []
        for name, (dx, dy, _, _) in DIRECTIONS.items():
            nx, ny = x + dx, y + dy
            if not (0 <= nx < self.width and 0 <= ny < self.height):
                continue
            if (nx, ny) in self.visited:
                continue
            result.append(name)
        return result

    def generate(self) -> None:
        self.visited = set(self.blocked)
        self.visited.add(self.entry)
        passage: list[tuple[int, int]] = [self.entry]
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


if __name__ == "__main__":
    generator = MazeGenerator()
    generator.generate()
