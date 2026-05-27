"""Tests for built-in puzzle definitions and a sample of Kaggle CSV puzzles."""

from __future__ import annotations

from itertools import islice
from pathlib import Path

import pytest
from sudoku_solver.puzzle import Puzzle
from sudoku_solver.puzzles import PuzzleData
from sudoku_solver.puzzles.chaossudoku_3 import cs_3
from sudoku_solver.puzzles.chaossudoku_4 import cs_4
from sudoku_solver.puzzles.loader import load_from_csv

_CSV_PATH = Path(__file__).parent.parent / "src/sudoku_solver/puzzles/sudoku.csv"
_CSV_SAMPLE = 20


def _solve(pd: PuzzleData) -> tuple[bool, list[list[int | None]]]:
    puzzle = Puzzle(pd.values, pd.groups)
    while puzzle.solve_step() is not None:
        pass
    grid = [[cell.value for cell in row] for row in puzzle.rows]
    return puzzle.is_solved, grid


# --- Built-in chaos puzzles ---


@pytest.mark.parametrize("pd", [cs_3, cs_4], ids=["chaos-3", "chaos-4"])
def test_chaos_puzzle_solves(pd: PuzzleData) -> None:
    """Verify built-in chaos puzzles can be solved."""
    solved, _ = _solve(pd)
    assert solved


# --- Kaggle CSV puzzles ---

_csv_puzzles: list[PuzzleData] = (
    list(islice(load_from_csv(_CSV_PATH), _CSV_SAMPLE)) if _CSV_PATH.exists() else []
)
_csv_ids = [f"csv-{i + 1}" for i in range(len(_csv_puzzles))]
_requires_csv = pytest.mark.skipif(
    not _CSV_PATH.exists(), reason="sudoku.csv not available"
)


@_requires_csv
@pytest.mark.parametrize("pd", _csv_puzzles, ids=_csv_ids)
def test_csv_puzzle_solves(pd: PuzzleData) -> None:
    """Verify that sample CSV puzzles from the dataset can be solved."""
    solved, _ = _solve(pd)
    assert solved


@_requires_csv
@pytest.mark.parametrize("pd", _csv_puzzles, ids=_csv_ids)
def test_csv_puzzle_solution_correct(pd: PuzzleData) -> None:
    """Ensure the solver produces the expected solution for a CSV puzzle.

    If the puzzle cannot be solved this test will be skipped because
    that case is covered by test_csv_puzzle_solves.
    """
    solved, grid = _solve(pd)
    if not solved:
        pytest.skip("puzzle could not be solved — caught by test_csv_puzzle_solves")
    assert grid == pd.solution
