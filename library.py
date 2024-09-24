import pathlib
import argparse
import doctest


def parse_file(input_file: str) -> list[tuple[str, int, int]]:
    """Parse the file and return a list of tuples containing the line, line number, and line length"""
    with open(input_file, "r", encoding="utf-8") as file:
        return [
            (  # line, line_number, line_length
                line.split("|")[0].strip(),
                int(line.split("|")[1]),
                len(line.split("|")[0].strip()),
            )
            for line in file
        ]


def find_average_line_length(lines: list[tuple[str, int, int]]) -> int:
    """
    >>> find_average_line_length([("hello", 1, 5), ("world", 2, 5), ("hella", 3, 5)])
    5
    >>> find_average_line_length([("hello", 1, 10), ("world", 2, 30), ("hella", 3, 20)])
    20
    """
    return int(sum(line[2] for line in lines) / len(lines))


def find_longest_line(lines: list[tuple[str, int, int]]) -> tuple[str, int, int]:
    """
    >>> find_longest_line([("hello", 1, 5), ("world", 2, 5), ("hella", 3, 5)])
    ('hella', 3, 5)
    """
    max_length = max(line[2] for line in lines)
    longest_lines = [line for line in lines if line[2] == max_length]
    return max(longest_lines, key=lambda x: x[1])


def write_to_file(
    input_file: str,
    longest_line: tuple[str, int, int],
    average_line_length: int,
    sorted_lines: list[tuple[str, int, int]],
):
    """Write the sorted lines to a file"""
    output_file = input_file.stem[:3].upper().ljust(3, "X")[:3] + "_book.txt"
    with open(output_file, "w", encoding="utf-8") as f:
        f.write(f"{input_file.stem[:3].upper()}\n")
        f.write(f"Longest line ({longest_line[1]}): {longest_line[0]}\n")
        f.write(f"Average length: {average_line_length}\n")
        for line in sorted_lines:
            f.write(f"{line[0]}\n")

    print(f"Lines written to {output_file}")


def sort_file(input_file: str):
    """Sort the file"""
    lines = parse_file(input_file)
    sorted_lines = sorted(lines, key=lambda x: x[1])

    average_line_length = find_average_line_length(lines)
    longest_line = find_longest_line(lines)

    write_to_file(input_file, longest_line, average_line_length, sorted_lines)


def main():
    parser = argparse.ArgumentParser(
        description="Process library files and generate summary output files"
    )
    parser.add_argument(
        "input_files",
        type=str,
        nargs="+",
        help="paths to the library files: 'python library.py TTL.txt WOO.txt'",
    )
    args = parser.parse_args()

    for file_path in args.input_files:
        path = pathlib.Path(file_path)
        if not path.exists():
            print(f"File {file_path} does not exist")
        else:
            sort_file(path)


if __name__ == "__main__":
    main()
    doctest.testmod()
