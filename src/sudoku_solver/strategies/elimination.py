"""Basic elimination strategies: row, column, and group."""

from collections.abc import Sequence

from sudoku_solver.cell import Cell


def _reduce_unit(unit: Sequence[Cell]) -> None:
    """Remove placed values from candidates of all unsolved cells in a unit."""
    placed: set[int] = {cell.value for cell in unit if cell.value is not None}
    if not placed:
        return
    for cell in unit:
        if cell.value is None:
            cell.candidates -= placed


def reduce_rows(rows: list[list[Cell]]) -> None:
    """Reduce candidates in each row based on current values."""
    for row in rows:
        _reduce_unit(row)


def reduce_columns(columns: list[list[Cell]]) -> None:
    """Reduce candidates in each column based on current values."""
    for column in columns:
        _reduce_unit(column)


def reduce_groups(groups: list[list[Cell]]) -> None:
    """Reduce candidates in each group based on current values."""
    for group in groups:
        _reduce_unit(group)
