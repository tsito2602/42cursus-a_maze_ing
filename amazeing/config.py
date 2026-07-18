from pydantic import BaseModel, ConfigDict, Field, model_validator


class MazeConfig(BaseModel):
    model_config = ConfigDict(extra="forbid", strict=True)

    width: int = Field(ge=1)
    height: int = Field(ge=1)
    entry: tuple[int, int]
    exit: tuple[int, int]
    output_file: str = Field(min_length=1)
    perfect: bool
    seed: int | None = Field(default=None)

    @model_validator(mode="after")
    def validate_coordinates(self) -> "MazeConfig":
        """Validate that entry and exit are inside the maze."""
        self._validate_coordinate("ENTRY", self.entry)
        self._validate_coordinate("EXIT", self.exit)

        if self.entry == self.exit:
            raise ValueError(
                f"ENTRY and EXIT must be different. Both are {self.entry}"
            )

        return self

    def _validate_coordinate(
        self, key: str, coordinate: tuple[int, int]
    ) -> None:
        """Validate one coordinate against the maze bounds."""
        x, y = coordinate
        if 0 <= x < self.width and 0 <= y < self.height:
            return

        raise ValueError(
            f"{key} {coordinate} is outside the maze bounds "
            f"(WIDTH={self.width}, HEIGHT={self.height}).\n"
            f"Expected 0 <= x < {self.width} and 0 <= y < {self.height}."
        )
