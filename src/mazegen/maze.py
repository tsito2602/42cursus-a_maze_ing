from enum import IntFlag
from typing import Annotated
from pydantic import BaseModel, ConfigDict, Field, model_validator

Coordinate = tuple[int, int]
Cell = Annotated[int, Field(ge=0, le=0xF)]


class Wall(IntFlag):
    NORTH = 0b0001
    EAST = 0b0010
    SOUTH = 0b0100
    WEST = 0b1000
    ALL = NORTH | EAST | SOUTH | WEST


class Maze(BaseModel):
    model_config = ConfigDict(frozen=True)

    cells: tuple[tuple[Cell, ...], ...]
    entry: Coordinate
    exit: Coordinate
    solution: tuple[Coordinate, ...] = ()
    blocked_cells: tuple[Coordinate, ...]

    @property
    def width(self) -> int:
        return len(self.cells[0])

    @property
    def height(self) -> int:
        return len(self.cells)

    @model_validator(mode="after")
    def validate_maze(self) -> "Maze":
        if not self.cells or not self.cells[0]:
            raise ValueError("Maze must contain at least one cell")

        width = len(self.cells[0])

        if any(len(row) != width for row in self.cells):
            raise ValueError("All maze rows must have the same width")

        self._validate_coordinate("ENTRY", self.entry)
        self._validate_coordinate("EXIT", self.exit)

        for coordinate in self.solution:
            self._validate_coordinate("SOLUTION", coordinate)

        for coordinate in self.blocked_cells:
            self._validate_coordinate("BLOCKED_CELL", coordinate)

        return self

    def _validate_coordinate(
        self,
        name: str,
        coordinate: Coordinate,
    ) -> None:
        x, y = coordinate

        if not (0 <= x < self.width and 0 <= y < self.height):
            raise ValueError(f"{name} {coordinate} is outside the maze bounds")
