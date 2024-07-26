import csv
import json
import sys
from contextlib import contextmanager


@contextmanager
def read_from_path(path: str, *args, **kwargs):
    if path == "-":
        yield sys.stdin
    else:
        with open(path, *args, **kwargs) as f:
            yield f


def csv_to_json(path: str, delimiter: str = ","):
    with read_from_path(path) as f:
        items = list(csv.DictReader(f, delimiter=delimiter))
        return json.dumps(items)


def main(argv: list[str]):
    try:
        path = argv[0]
        delimiter = argv[1] if len(argv) > 1 else ","
        print(csv_to_json(path, delimiter=delimiter))
    except IndexError:
        print(
            "This scripts converts a csv to a list of "
            "objects in a JSON format: \n"
            "Usage: python csv-to-json.py <file-path> \n"
            "  file-path: If file-path equals '-' the script reads "
            "from stdin otherwise it is used as a file path\n"
            "Example: printf \"a,b,c\\n1,2,3\" | "
            "python3 utility-scripts/csv-to-json.py -"
        )


if __name__ == "__main__":
    main(sys.argv[1:])
