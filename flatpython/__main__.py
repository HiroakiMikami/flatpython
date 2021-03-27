import argparse
from flatpython._lint import lint
import logging

logging.basicConfig(level=logging.INFO)


def main():
    parser = argparse.ArgumentParser()
    parser.add_argument(
        "files", metavar="<file>", type=str, nargs="+",
        help="target files",
    )
    args = parser.parse_args()
    for file in args.files:
        with open(file) as f:
            if not lint(f.read()):
                exit(1)


if __name__ == "__main__":
    main()
