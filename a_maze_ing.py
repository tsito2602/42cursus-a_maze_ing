import sys
from pydantic import ValidationError
from amazeing import run
from amazeing import parse_config


def format_validation_error(error: ValidationError) -> str:
    """Return concise, user-facing messages for invalid configuration."""
    messages: list[str] = []

    for detail in error.errors(include_url=False, include_input=False):
        message = str(detail["msg"])
        if message.startswith("Value error, "):
            message = message.removeprefix("Value error, ")

        location = ".".join(
            str(loc).rstrip("_").upper() for loc in detail["loc"]
        )
        if location:
            message = f"{location}: {message}"

        messages.append(message)

    if len(messages) == 1:
        return messages[0]

    return "Invalid configuration:\n  " + "\n  ".join(messages)


def main() -> None:
    """Parse the command-line configuration path and start the application."""
    if len(sys.argv) != 2:
        print("Usage: a_maze_ing.py <file>", file=sys.stderr)
        raise SystemExit(2)

    config_file = sys.argv[1]

    try:
        config = parse_config(config_file)
        run(config)
    except KeyboardInterrupt:
        print("\nInterrupted.", file=sys.stderr)
        raise SystemExit(130)
    except ValidationError as e:
        print(f"Error: {format_validation_error(e)}", file=sys.stderr)
        raise SystemExit(1)
    except Exception as e:
        print(f"Error: {e}", file=sys.stderr)
        raise SystemExit(1)


if __name__ == "__main__":
    main()
