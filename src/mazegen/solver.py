from collections import deque
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
        for dx, dy, wall, _ in DIRECTIONS.values():
            if walls_here & wall:
                continue
            nx, ny = x + dx, y + dy
            if 0 <= nx < self.width and 0 <= ny < self.height:
                neighbours.append((nx, ny))
        return neighbours

    def solve(self) -> tuple[Coordinate, ...]:
        """Find the shortest path from entry to exit."""
        entry = self.maze.entry
        exit_ = self.maze.exit
        queue: deque[Coordinate] = deque([entry])
        came_from: dict[Coordinate, Coordinate | None] = {
                entry: None
        }
        while queue:
            current = queue.popleft()
            if current == exit_:
                break
            x, y = current
            for neighbour in self._walkable_neighbours(x, y):
                if neighbour in came_from:
                    continue
                came_from[neighbour] = current
                queue.append(neighbour)
        else:
            raise ValueError("not find route")
        path: list[Coordinate] = [exit_]
        while True:
            previous = came_from[path[-1]]
            if previous is None:
                break
            path.append(previous)
        path.reverse()
        return tuple(path)
