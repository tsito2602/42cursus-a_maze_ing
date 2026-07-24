from amazeing.config import MazeConfig
from mazegen import Coordinate

CONFIG_FIELDS = {
    "WIDTH": "width",
    "HEIGHT": "height",
    "ENTRY": "entry",
    "EXIT": "exit_",
    "OUTPUT_FILE": "output_file",
    "PERFECT": "perfect",
    "SEED": "seed",
}


def parse_int(key: str, value: str) -> int:
    try:
        return int(value)
    except ValueError as e:
        raise ValueError(f"Invalid integer for {key}: {value!r}") from e


def parse_coordinate(key: str, value: str) -> Coordinate:
    parts = value.split(",")

    if len(parts) != 2:
        raise ValueError(f"Invalid coordinate {value!r}: expected x,y")

    try:
        x = int(parts[0])
        y = int(parts[1])
    except ValueError as e:
        raise ValueError(
            f"Invalid coordinate {key}: {value!r}; x and y must be integers"
        ) from e

    return x, y


def parse_bool(key: str, value: str) -> bool:
    if value == "True":
        return True

    if value == "False":
        return False

    raise ValueError(
        f"Invalid boolean for {key}: {value!r}; expected True or False"
    )


def parse_value(key: str, value: str) -> object:
    match key:
        case "WIDTH" | "HEIGHT" | "SEED":
            return parse_int(key, value)

        case "ENTRY" | "EXIT":
            return parse_coordinate(key, value)

        case "PERFECT":
            return parse_bool(key, value)

        case _:
            return value


def parse_config(path: str) -> MazeConfig:
    values: dict[str, str] = {}

    with open(path, encoding="utf-8") as file:
        for line_number, raw_line in enumerate(file, start=1):
            line = raw_line.strip()

            if not line or line.startswith("#"):
                continue

            if "=" not in line:
                raise ValueError(f"Line {line_number}: expected KEY=VALUE")

            key, value = line.split("=", 1)
            key = key.strip()
            value = value.strip()

            if key in values:
                raise ValueError(f"Line {line_number}: duplicated key {key}")

            if key not in CONFIG_FIELDS:
                raise ValueError(f"Line {line_number}: unknown key {key!r}")

            values[key] = value

    config_data: dict[str, object] = {
        CONFIG_FIELDS[key]: parse_value(key, value)
        for key, value in values.items()
    }

    return MazeConfig.model_validate(config_data)
