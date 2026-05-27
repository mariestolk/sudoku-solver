"""Unit tests for Puzzle.is_valid_solution."""

from __future__ import annotations

import copy

from sudoku_solver.puzzle import Puzzle

# A known valid standard sudoku solution used as the base for all tests.
_VALID_GRID = [
    [5, 3, 4, 6, 7, 8, 9, 1, 2],
    [6, 7, 2, 1, 9, 5, 3, 4, 8],
    [1, 9, 8, 3, 4, 2, 5, 6, 7],
    [8, 5, 9, 7, 6, 1, 4, 2, 3],
    [4, 2, 6, 8, 5, 3, 7, 9, 1],
    [7, 1, 3, 9, 2, 4, 8, 5, 6],
    [9, 6, 1, 5, 3, 7, 2, 8, 4],
    [2, 8, 7, 4, 1, 9, 6, 3, 5],
    [3, 4, 5, 2, 8, 6, 1, 7, 9],
]


def _grid_with(row: int, col: int, value: int) -> list[list[int]]:
    grid = copy.deepcopy(_VALID_GRID)
    grid[row][col] = value
    return grid


def test_valid_solution_returns_true() -> None:
    """Test that a valid sudoku solution is recognized as valid."""
    assert Puzzle(_VALID_GRID).is_valid_solution is True


def test_row_violation_returns_false() -> None:
    """Test that a solution with row violation is recognized as invalid."""
    # Row 0: replace the 3 at col 1 with a second 5 → duplicate in row 0.
    assert Puzzle(_grid_with(0, 1, 5)).is_valid_solution is False


def test_column_violation_returns_false() -> None:
    """Test that a solution with column violation is recognized as invalid."""
    # Col 0: replace the 6 at row 1 with a second 5 → duplicate in col 0.
    assert Puzzle(_grid_with(1, 0, 5)).is_valid_solution is False


def test_group_violation_returns_false() -> None:
    """Test that a solution with group violation is recognized as invalid."""
    # Top-left group: replace the 7 at (1,1) with a second 5 → duplicate in group 0.
    assert Puzzle(_grid_with(1, 1, 5)).is_valid_solution is False


def test_unsolved_puzzle_returns_false() -> None:
    """Test that a n incomplete sudoku is recognized as invalid."""
    grid = copy.deepcopy(_VALID_GRID)
    grid[0][0] = 0  # leave one cell empty
    assert Puzzle(grid).is_valid_solution is False
