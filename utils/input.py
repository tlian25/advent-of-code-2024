from typing import List


def read_input_file_lines(filename: str) -> List[str]:
    with open(f"./inputs/{filename}") as f:
        return [l.replace("\n", "") for l in f.readlines()]
