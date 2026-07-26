from collections import deque
from .maze import DIRECTIONS, Coordinate, Maze


def solve(
    cells: list[list[int]], entry: Coordinate, exit_: Coordinate
) -> tuple[Coordinate, ...]:
    """Find the shortest path from entry to exit."""
    queue: deque[Coordinate] = deque([entry])
    came_from: dict[Coordinate, Coordinate | None] = {entry: None}

    while queue:
        current = queue.popleft()
        if current == exit_:
            break

        for neighbour in _walkable_neighbours(cells, current):
            if neighbour in came_from:
                continue
            came_from[neighbour] = current
            queue.append(neighbour)
    else:
        raise ValueError("Route not found.")

    path: list[Coordinate] = [exit_]
    while True:
        previous = came_from[path[-1]]
        if previous is None:
            break
        path.append(previous)

    path.reverse()
    return tuple(path)


def _walkable_neighbours(
    cells: list[list[int]], coordinate: Coordinate
) -> list[Coordinate]:
    """Return neighbouring cells reachable without crossing a wall."""
    x, y = coordinate
    width = len(cells[0])
    height = len(cells)

    neighbours: list[Coordinate] = []
    walls_here = cells[y][x]

    for dx, dy, wall, _ in DIRECTIONS.values():
        if walls_here & wall:
            continue

        nx, ny = x + dx, y + dy
        if 0 <= nx < width and 0 <= ny < height:
            neighbours.append((nx, ny))

    return neighbours
