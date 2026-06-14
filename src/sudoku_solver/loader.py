"""Loader for sudoku puzzles from CSV files."""

import csv
import json
from collections.abc import Iterator
from pathlib import Path

from sudoku_solver.puzzle import STANDARD_GROUP_MAP, PuzzleData


def _parse_grid(s: str) -> list[list[int]]:
    """Convert an 81-character string into a 9x9 grid of ints."""
    return [[int(s[r * 9 + c]) for c in range(9)] for r in range(9)]


def load_from_json(path: str | Path) -> PuzzleData:
    """Load a PuzzleData from a JSON file saved by the evaluator's --save-first-stuck flag."""
    data = json.loads(Path(path).read_text())
    solution = _parse_grid(data["solution"]) if "solution" in data else None
    return PuzzleData(
        values=_parse_grid(data["puzzle"]),
        groups=STANDARD_GROUP_MAP,
        solution=solution,
    )


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
