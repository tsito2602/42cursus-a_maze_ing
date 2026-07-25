from .maze import DIRECTIONS, Coordinate, Maze


class Solver:
    def __init__(self, maze: Maze) -> None:
        self.maze = maze
        self.width = maze.width
        self.height = maze.height

    def _walkable_neighbours(self, x: int, y: int) -> list[Coordinate]:
        """Return neighbouring cells reachable without crossing a wall."""
        neighbours: list[Coordinate] = []
        walls_here = self.maze.cells[y][x]

        for dx, dy, wall, _opposite in DIRECTIONS.values():
            if walls_here & wall:
                continue

            nx, ny = x + dx, y + dy
            if 0 <= nx < self.width and 0 <= ny < self.height:
                neighbours.append((nx, ny))

        return neighbours

    def solve(self) -> Maze:
        """Find a path from entry to exit and return a Maze with it set."""
        entry = self.maze.entry
        exit_ = self.maze.exit

        visited: set[Coordinate] = {entry}
        path: list[Coordinate] = [entry]

        while path[-1] != exit_:
            current_x, current_y = path[-1]
            next_cell = None
            for neighbour in self._walkable_neighbours(current_x, current_y):
                if neighbour not in visited:
                    next_cell = neighbour
                    break

            if next_cell is None:
                path.pop()
                if not path:
                    raise ValueError("not find route")
                continue
            visited.add(next_cell)
            path.append(next_cell)

        return Maze(
            cells=self.maze.cells,
            entry=self.maze.entry,
            exit=self.maze.exit,
            pattern_cells=self.maze.pattern_cells,
            solution=tuple(path),
        )