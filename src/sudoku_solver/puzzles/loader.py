"""Loader for sudoku puzzles from CSV files."""

import csv
from collections.abc import Iterator
from pathlib import Path

from sudoku_solver.puzzles import PuzzleData

STANDARD_GROUP_MAP = [[(r // 3) * 3 + (c // 3) for c in range(9)] for r in range(9)]


def _parse_grid(s: str) -> list[list[int]]:
    """Convert an 81-character string into a 9x9 grid of ints."""
    return [[int(s[r * 9 + c]) for c in range(9)] for r in range(9)]


def load_from_csv(path: str | Path) -> Iterator[PuzzleData]:
    """Yield PuzzleData for each row in a Kaggle-format sudoku CSV.

    Expects columns 'puzzle' and 'solution' as 81-character digit strings.
    """
    with open(path, newline="") as f:
        for row in csv.DictReader(f):
            yield PuzzleData(
                values=_parse_grid(row["puzzle"]),
                groups=STANDARD_GROUP_MAP,
                solution=_parse_grid(row["solution"]),
            )
