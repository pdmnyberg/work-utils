import json
import sys
from contextlib import contextmanager
import difflib
from typing import Callable


@contextmanager
def read_from_path(path: str, *args, **kwargs):
    if path == "-":
        yield sys.stdin
    else:
        with open(path, *args, **kwargs) as f:
            yield f


def map_entries(
    entries: list[dict],
    targets: list[dict],
    source_value: str,
    target_value: str,
    transform: Callable[[str], str],
    cutoff: float = 0.6
):
    mapped_targets = {
        transform(target[target_value]): target
        for target in targets
    }
    target_values = set(mapped_targets.keys())

    output_map = {}
    for entry in entries:
        value = transform(entry[source_value])
        if value:
            if value in mapped_targets:
                output_map[value] = mapped_targets[value]
            else:
                try:
                    closest_match = difflib.get_close_matches(
                        value,
                        target_values,
                        cutoff=cutoff
                    )[0]
                    output_map[value] = mapped_targets[closest_match]
                except IndexError:
                    raise ValueError(f"No match for '{value}'")
    return json.dumps(output_map)


def load_entries(path: str):
    with read_from_path(path) as f:
        return json.load(f)


def parse_transform(transform_id: str) -> Callable[[str], str]:
    try:
        transforms = {
            "lower": lambda v: v.lower(),
            "upper": lambda v: v.upper(),
            "none": lambda v: v,
            "prefix": lambda v: v[:20]
        }
        return transforms[transform_id.lower()]
    except KeyError:
        raise ValueError(f"Not matching transform '{transform_id}'")


def main(argv: list[str]):
    try:
        source = argv[0]
        target = argv[1]
        source_value = argv[2]
        target_value = argv[3]
        transform = parse_transform(argv[4])
        cutoff = float(argv[5]) if len(argv) > 5 else 0.6

        entries = load_entries(source)
        targets = load_entries(target)
        print(
            map_entries(
                entries,
                targets,
                source_value,
                target_value,
                transform,
                cutoff
            )
        )
    except (IndexError, ValueError) as e:
        print(
            "This scripts maps values of the source json list the value of "
            "the target json list: \n"
            "Usage: python map_entries.py <source-path.json> "
            "<target-path.json> <source_value> <target_value> "
            "<transform> [cutoff|0.6]\n"
            "  - source-path: If file-path equals '-' the script reads "
            "from stdin otherwise it is used as a file path\n"
            "  - target-path: If file-path equals '-' the script reads "
            "from stdin otherwise it is used as a file path\n"
            "  - source_value: The property to be mapped from source data \n"
            "  - target_value: The property to be mapped from target data \n"
            "  - transform: Tranform applied to source and target data \n"
            "  - cutoff(optional): Cut-off [0, 1] value for closes match \n"
            "\n"
            f"Error: {e}"
        )


if __name__ == "__main__":
    main(sys.argv[1:])
