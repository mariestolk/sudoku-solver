"""Module for Sudoku cell representation and creation.

This module provides the Cell class and create_cell function for managing
individual cells in a Sudoku puzzle.
"""


class Cell:
    """A cell class that represents a cell in a sudoku."""

    def __init__(self, row: int, column: int, group: int) -> None:
        """Initialize a cell with its grid position and group."""
        self.row: int = row
        self.column: int = column
        self.group: int = group
        self.value: int | None = None
        self.candidates: set[int] = set()
        self.deciding_rule: str | None = None

    def __repr__(self) -> str:
        """Return a string representation of the cell."""
        return f"Cell({self.row}, {self.column}, {self.group}, value={self.value})"

    def set_value(self, value: int) -> None:
        """Set the value of the cell and clear candidates."""
        self.value = value
        self.candidates.clear()
        self.deciding_rule = None

    def set_candidates(self, candidates: list[int]) -> None:
        """Set the candidates for the cell."""
        self.candidates = set(candidates)


def create_cell(row: int, column: int, group: int, value: int | None = None) -> Cell:
    """Create a new cell for the Sudoku puzzle."""
    cell = Cell(row, column, group)
    cell.value = value
    if value is not None:
        cell.candidates = set()
    else:
        cell.candidates = set(range(1, 10))
    return cell
